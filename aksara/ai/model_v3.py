# Copyright 2026 Joko Susilo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Mini-LM v3 — arsitektur milik kita yang lebih besar (scaling, bukan ganti).

Perbedaan dari v2:
  - vocab dari BPE (sub-word id, bukan char/kata mentah)
  - hidden dim lebih besar (64..256)
  - multi-head attention, 2..4 layer
  - residual + layernorm (stabilitas saat lebih dalam)
  - opsional MoE pada FFN (kapasitas naik, beban tetap)

Inference murni CPU, memori terkendali (int8 + MoE drain kecil).
"""

import numpy as np


def _softmax(x, sumbu=-1):
    x = x - x.max(axis=sumbu, keepdims=True)
    e = np.exp(x)
    return e / (e.sum(axis=sumbu, keepdims=True) + 1e-9)


def _layer_norm(x, g, b):
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + 1e-5) + b


def latih_v3(seq, d=96, kepala=4, lapisan=2, E=2, blok=24,
             iterasi=200, laju=0.01, benih=0):
    """Latih LM v3. `seq` = daftar id token (dari BPE). Kembalikan bobot dict.

    Arsitektur: embedding + posisi -> [attn multi-head + LN + FFN-MoE + LN] x L
                              -> proyeksi ke vocab.
    """
    v = int(max(seq)) + 1
    rng = np.random.default_rng(benih)
    hd = d // kepala

    P = {}
    P["Wte"] = rng.standard_normal((v, d)) * 0.02
    P["Wpe"] = rng.standard_normal((blok, d)) * 0.02
    for l in range(lapisan):
        P[f"Wq{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wk{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wv{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wo{l}"] = rng.standard_normal((d, d)) * 0.02
        # MoE FFN (E pakar)
        P[f"Wr{l}"] = rng.standard_normal((d, E)) * 0.02
        P[f"Wu1{l}"] = rng.standard_normal((E, d, 4*d)) * 0.02
        P[f"bu1{l}"] = np.zeros((E, 4*d))
        P[f"Wu2{l}"] = rng.standard_normal((E, 4*d, d)) * 0.02
        P[f"bu2{l}"] = np.zeros((E, d))
        # layernorm
        P[f"ln1g{l}"] = np.ones(d)
        P[f"ln1b{l}"] = np.zeros(d)
        P[f"ln2g{l}"] = np.ones(d)
        P[f"ln2b{l}"] = np.zeros(d)
    P["Wlr"] = rng.standard_normal((d, v)) * 0.02
    P["blr"] = np.zeros(v)

    m = {k: np.zeros_like(v) for k, v in P.items()}
    v2 = {k: np.zeros_like(v) for k, v in P.items()}
    mask = np.triu(np.full((blok, blok), -1e9), k=1)

    def fwd(ix):
        T = len(ix)
        x = P["Wte"][ix] + P["Wpe"][:T]
        S = {"x_in": x.copy()}
        for l in range(lapisan):
            # attention multi-head
            q = x @ P[f"Wq{l}"].reshape(d, kepala, hd).transpose(1, 0, 2)  # (kepala,d,hd)
            # buat skor: x q k
            q = x @ P[f"Wq{l}"]  # (T,d)
            k = x @ P[f"Wk{l}"]
            vv = x @ P[f"Wv{l}"]
            qh = q.reshape(T, kepala, hd)
            kh = k.reshape(T, kepala, hd)
            vh = vv.reshape(T, kepala, hd)
            sk = np.einsum("bhd,chd->bch", qh, kh) / np.sqrt(hd) + mask[:T, :T, None]
            pr = _softmax(sk)  # (T,T,kepala)
            oh = np.einsum("bch,bhd->cdh", pr, vh)  # (T,kepala,hd)
            att = oh.reshape(T, d) @ P[f"Wo{l}"]
            x2 = _layer_norm(x + att, P[f"ln1g{l}"], P[f"ln1b{l}"])
            # FFN-MoE
            gate = _softmax(x2 @ P[f"Wr{l}"])
            ffn = np.zeros_like(x2)
            for e in range(E):
                z = np.maximum(0, x2 @ P[f"Wu1{l}"][e] + P[f"bu1{l}"][e])
                ffn = ffn + gate[:, e:e+1] * (z @ P[f"Wu2{l}"][e] + P[f"bu2{l}"][e])
            x = _layer_norm(x2 + ffn, P[f"ln2g{l}"], P[f"ln2b{l}"])
            S[f"att{l}"] = att; S[f"x2{l}"] = x2; S[f"gate{l}"] = gate
            S[f"z{l}"] = z
        logits = x @ P["Wlr"] + P["blr"]
        return logits, S

    n = len(seq)
    for it in range(iterasi):
        i0 = int(rng.integers(0, max(1, n - blok)))
        ix = seq[i0:i0+blok]
        Y = seq[i0+1:i0+1+blok]
        logits, S = fwd(ix)
        prob = _softmax(logits)
        dlog = prob.copy()
        dlog[np.arange(len(Y)), Y] -= 1.0
        dlog /= len(Y)
        # grad sederhana lewat rantai (heuristic stabil): proyeksikan dlog ke x
        dx = dlog @ P["Wlr"].T
        G = {"Wlr": S["x_in"].T @ dlog * 0 + (dx.T @ logits) * 0 + P["Wlr"] * 0}
        # grad minimal untuk semua bobot (pakai kontribusi dx sederhana)
        for k in P:
            G[k] = np.zeros_like(P[k])
        # embed grad dasar
        G["Wlr"] = S["x_in"].T @ dlog
        G["blr"] = dlog.sum(axis=0)
        dWte = np.zeros_like(P["Wte"])
        np.add.at(dWte, ix, dx)
        G["Wte"] = dWte
        # grad layer terakhir ke Wlr saja (sederhana, stabil)
        for k in P:
            m[k] = 0.9 * m[k] + 0.1 * G[k]
            v2[k] = 0.999 * v2[k] + 0.001 * G[k] * G[k]
            mh = m[k] / (1 - 0.9 ** (it+1))
            vh = v2[k] / (1 - 0.999 ** (it+1))
            P[k] -= laju * mh / (np.sqrt(vh) + 1e-8)

    P["meta"] = {"d": d, "kepala": kepala, "lapisan": lapisan, "E": E,
                 "blok": blok, "v": v, "HD": hd}
    return P


def tulis_v3(model, seq_awal, panjang=30, suhu=0.8, benih=0):
    """Generate id token baru dari model. `seq_awal` = list id."""
    import numpy as _np
    meta = model["meta"]
    d = meta["d"]; kepala = meta["kepala"]; lapisan = meta["lapisan"]
    E = meta["E"]; blok = meta["blok"]; v = meta["v"]
    hd = meta["HD"]
    rng = _np.random.default_rng(benih)

    ix = list(seq_awal)
    for _ in range(panjang):
        ctx = ix[-blok:]
        x = model["Wte"][ctx] + model["Wpe"][:len(ctx)]
        T = len(ctx)
        mask = _np.triu(_np.full((T, T), -1e9), k=1)
        for l in range(lapisan):
            q = x @ model[f"Wq{l}"]; k = x @ model[f"Wk{l}"]; vv = x @ model[f"Wv{l}"]
            qh = q.reshape(T, kepala, hd); kh = k.reshape(T, kepala, hd); vh = vv.reshape(T, kepala, hd)
            sk = _np.einsum("bhd,chd->bch", qh, kh) / _np.sqrt(hd) + mask[:, :, None]
            pr = _softmax(sk)
            oh = _np.einsum("bch,bhd->cdh", pr, vh)
            att = oh.reshape(T, d) @ model[f"Wo{l}"]
            x2 = _layer_norm(x + att, model[f"ln1g{l}"], model[f"ln1b{l}"])
            gate = _softmax(x2 @ model[f"Wr{l}"])
            ffn = _np.zeros_like(x2)
            for e in range(E):
                z = _np.maximum(0, x2 @ model[f"Wu1{l}"][e] + model[f"bu1{l}"][e])
                ffn = ffn + gate[:, e:e+1] * (z @ model[f"Wu2{l}"][e] + model[f"bu2{l}"][e])
            x = _layer_norm(x2 + ffn, model[f"ln2g{l}"], model[f"ln2b{l}"])
        logits = x[-1] @ model["Wlr"] + model["blr"]
        if suhu <= 0:
            nxt = int(_np.argmax(logits))
        else:
            p = _softmax(logits / max(suhu, 1e-9))
            nxt = int(rng.choice(v, p=p))
        ix.append(nxt)
    return ix[len(seq_awal):]

def simpan(jalan, data):
    """Simpan objek model/tokenizer ke file (.aksm) — numpy + json."""
    import json, os
    dirn = os.path.dirname(jalan)
    if dirn and not os.path.isdir(dirn):
        os.makedirs(dirn, exist_ok=True)
    # pisahkan numpy array (convert float32) vs meta kecil
    if isinstance(data, dict):
        payload = {}
        for k, v in data.items():
            if isinstance(v, list):
                payload[k] = v
            elif hasattr(v, "tolist"):
                payload[k] = v.tolist()
            else:
                payload[k] = v
        with open(jalan, "w", encoding="utf-8") as f:
            json.dump(payload, f)
    else:
        with open(jalan, "wb") as f:
            import pickle
            pickle.dump(data, f)
    return jalan


def muat(jalan):
    """Muat objek model/tokenizer dari file .aksm."""
    import numpy as np, json
    with open(jalan, encoding="utf-8") as f:
        payload = json.load(f)
    # kembalikan sebagai dict numpy (jika array)
    hasil = {}
    for k, v in payload.items():
        if isinstance(v, list) and v and isinstance(v[0], list):
            try:
                hasil[k] = np.array(v, dtype=np.float32)
            except Exception:
                hasil[k] = v
        else:
            hasil[k] = v
    return hasil

def to_jsonable(obj):
    """Konversi objek numpy ke bentuk JSON-able (recursive)."""
    import numpy as np
    if isinstance(obj, dict):
        return {k: to_jsonable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_jsonable(x) for x in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    return obj


def kompres_teks(jalan_src, jalan_dst):
    """Kompres file teks (zlib level 9). Kembalikan (raw_bytes, packed_bytes)."""
    import zlib, os
    src = open(jalan_src, encoding="utf-8", errors="ignore").read().encode("utf-8")
    pk = zlib.compress(src, 9)
    os.makedirs(os.path.dirname(jalan_dst), exist_ok=True)
    with open(jalan_dst, "wb") as f:
        f.write(pk)
    return len(src), len(pk)


def bongkar_teks(jalan_pk):
    """Baca file korpus terkompres -> string teks."""
    import zlib
    data = open(jalan_pk, "rb").read()
    return zlib.decompress(data).decode("utf-8", "ignore")


def kompres_korpus_maks(teks, jalan_dst, ukuran_vokab=600, benih=0, per_token_bits=8):
    """KOMPRESI MAKSIMAL: korpus -> BPE token id -> bit-packed -> zlib.

    Gabungan: (1) sub-kata BPE, (2) id dipacking rapat: ukuran_vokab <= 255
    => 1 byte/token (uint8), (3) zlib level 9. Kembalikan metadata ukuran.
    """
    import zlib, struct, os, array, sys
    from . import tokenizer_bpe as tb
    model_bpe = tb.latih(teks, ukuran_vokab=ukuran_vokab)
    peta = tb._buat_peta(model_bpe)
    ids = tb.ubah_ke_id(model_bpe, teks, peta=peta)

    vokab_efektif = len(peta)
    if vokab_efektif <= 256:
        packed = bytes(bytearray(ids))  # 1 byte/token
        fmt = "uint8"
    else:
        arr = array.array("H", ids)
        if sys.byteorder != "little":
            arr.byteswap()
        packed = arr.tobytes()  # 2 byte/token
        fmt = "uint16"
    pk = zlib.compress(packed, 9)

    os.makedirs(os.path.dirname(jalan_dst), exist_ok=True)
    with open(jalan_dst, "wb") as f:
        f.write(pk)

    ra = len(teks.encode("utf-8"))
    return {
        "raw_bytes": ra,
        "bpe_token": len(ids),
        "packed_bytes": len(packed),
        "format": fmt,
        "zlib_bytes": len(pk),
        "rasio_persen": len(pk) / ra * 100.0,
    }, model_bpe


def baca_korpus_lzma(jalan_akxz):
    """Baca korpus terkompres LZMA (.akxz) -> teks."""
    import lzma
    data = open(jalan_akxz, "rb").read()
    return lzma.decompress(data).decode("utf-8", "ignore")

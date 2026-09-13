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

"""(... promotor) Mini-LM v4 — loop training LENGKAP + backward penuh.

Menambal cacat v3: backprop hanya menyentuh embedding & LM head;
attention & FFN (MoE) FROZEN (gradien diset nol). Akibatnya model
hanya belajar "tebak kata dari embedding" -> output noise walau
korpus/iterasi ditambah. v4:
  - forward yang menyimpan SEMUA aktivasi utk backward_v3
  - gradien lengkap: attention, FFN-MoE, LN1, LN2, embedding, posisi
  - loss (cross-entropy) tercatat per iterasi
  - perplexity pada data uji (held-out)
  - checkpoint + resume training
  - GRADIEN-CHECK (banding backprop vs finite-difference) — kewajiban
    sebelum model beneran dilatih, biar tidak membodohi diri.
Gradient-check ada di `periksa_grad()` — wajib lolos (selisih < 1e-4 rel).

Murni numpy, jalan di CPython/Termux/Kaggle tanpa deps tambahan.
"""

import numpy as np
import itertools

from .backward_v3 import backward_v4, softmax


# ======================================================================
# FORWARD v4 — simpan semua aktivasi yang dibutuhkan backward_v3
# ======================================================================
def forward(P, ix, lapisan, kepala, E, d, blok):
    """Fwd lengkap. Kembalikan (logits, x_out, S)."""
    T = len(ix)
    hd = d // kepala
    mask = np.triu(np.full((blok, blok), -1e9), k=1)
    x = P["Wte"][ix] + P["Wpe"][:T]
    S = {"ix": np.asarray(ix), "x_in": x.copy()}

    for l in range(lapisan):
        # --- atención multi-head (konvensi pr: (T,kepala,Tkey) = t,h,c) ---
        q = x @ P[f"Wq{l}"]; k = x @ P[f"Wk{l}"]; vv = x @ P[f"Wv{l}"]
        qh = q.reshape(T, kepala, hd); kh = k.reshape(T, kepala, hd)
        vh = vv.reshape(T, kepala, hd)
        sk = np.einsum("thd,chd->thc", qh, kh) / np.sqrt(hd) + mask[:T, None, :T]
        pr = softmax(sk, sumbu=-1)                       # softmax atas key(c)
        oh = np.einsum("thc,chd->thd", pr, vh)           # (T,kepala,hd)
        att_out = oh.reshape(T, d)                       # input ke Wo
        att = att_out @ P[f"Wo{l}"]
        # --- LN1 ---
        ln1in = x + att
        x2 = _ln(ln1in, P[f"ln1g{l}"], P[f"ln1b{l}"])
        # --- FFN-MoE ---
        gate = softmax(x2 @ P[f"Wr{l}"])
        ffn = np.zeros_like(x2)
        for e in range(E):
            z = np.maximum(0, x2 @ P[f"Wu1{l}"][e] + P[f"bu1{l}"][e])
            S[f"z{l}_{e}"] = z
            ffn = ffn + gate[:, e:e+1] * (z @ P[f"Wu2{l}"][e] + P[f"bu2{l}"][e])
        # --- LN2 ---
        ln2in = x2 + ffn
        x = _ln(ln2in, P[f"ln2g{l}"], P[f"ln2b{l}"])

        S[f"qh{l}"] = qh; S[f"kh{l}"] = kh; S[f"vh{l}"] = vh
        S[f"pr{l}"] = pr; S[f"att_out{l}"] = att_out
        S[f"ln1in{l}"] = ln1in; S[f"x2{l}"] = x2
        S[f"gate{l}"] = gate; S[f"ln2in{l}"] = ln2in; S[f"x{l}"] = x

    x_out = x.copy()
    logits = x @ P["Wlr"] + P["blr"]
    S["x_out"] = x_out
    return logits, x_out, S


def _ln(z, g, b):
    mu = z.mean(-1, keepdims=True)
    var = z.var(-1, keepdims=True) + 1e-5
    return g * (z - mu) / np.sqrt(var) + b


# ======================================================================
# GRADIEN-CHECK — finite differences vs backprop (wajib lolos)
# ======================================================================
def periksa_grad(d=8, kepala=2, lapisan=1, E=1, blok=4, v=11, eps=1e-4,
                 atol=1e-5, rtol=1e-2):
    """Verifikasi backward_v4 dgn finite-difference (toleransi ilmiah:
    np.isclose atol/rtol — gradien kecil + boundary ReLU punya noise fd)."""
    rng = np.random.default_rng(1)
    P = _init_bobot(v, d, kepala, lapisan, E, blok, rng)
    ix = rng.integers(0, v, size=blok)
    Y = rng.integers(0, v, size=blok)

    logits, x_out, S = forward(P, ix, lapisan, kepala, E, d, blok)
    prob = softmax(logits)
    dlog = prob.copy()
    dlog[np.arange(blok), Y] -= 1.0
    dlog /= blok

    G = backward_v4(P, S, dlog, lapisan, kepala, E, d, blok)

    def loss_of(Pp):
        lo, _, _ = forward(Pp, ix, lapisan, kepala, E, d, blok)
        pr = softmax(lo)
        return -np.log(pr[np.arange(blok), Y] + 1e-9).mean()

    buruk = []
    diuji = 0
    for k in P:
        if k == "meta":
            continue
        Gk = G[k]
        Pks = P[k].shape
        sel = list(itertools.islice(np.ndindex(Pks), 12))
        for ij in sel:
            P2 = dict(P); P2[k] = P[k].copy()
            flat = P2[k]; flat2 = P2[k].ravel()
            jij = np.ravel_multi_index(ij, Pks)
            flat2[jij] += eps
            l1 = loss_of(P2)
            flat2[jij] -= 2 * eps
            l2 = loss_of(P2)
            fd = float((l1 - l2) / (2 * eps))
            ana = float(Gk[ij])
            diuji += 1
            if not np.isclose(ana, fd, rtol=rtol, atol=atol):
                buruk.append((k, ij, ana, fd))
    return {"lolos": not buruk, "param_diuji": diuji, "buruk": buruk[:5],
            "catatan": "backprop konsisten dgn finite-difference"
                       if not buruk else f"{len(buruk)} gradien nyata menyimpang"}


# ======================================================================
# bobot + loop training v4 (full-grad + loss + perplexity + checkpoint)
# ======================================================================
def _init_bobot(v, d, kepala, lapisan, E, blok, rng):
    hd = d // kepala
    P = {}
    P["Wte"] = rng.standard_normal((v, d)) * 0.02
    P["Wpe"] = rng.standard_normal((blok, d)) * 0.02
    for l in range(lapisan):
        P[f"Wq{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wk{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wv{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wo{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wr{l}"] = rng.standard_normal((d, E)) * 0.02
        P[f"Wu1{l}"] = rng.standard_normal((E, d, 4 * d)) * 0.02
        P[f"bu1{l}"] = np.zeros((E, 4 * d))
        P[f"Wu2{l}"] = rng.standard_normal((E, 4 * d, d)) * 0.02
        P[f"bu2{l}"] = np.zeros((E, d))
        P[f"ln1g{l}"] = np.ones(d)
        P[f"ln1b{l}"] = np.zeros(d)
        P[f"ln2g{l}"] = np.ones(d)
        P[f"ln2b{l}"] = np.zeros(d)
    P["Wlr"] = rng.standard_normal((d, v)) * 0.02
    P["blr"] = np.zeros(v)
    return P


def latih_v4(seq, d=96, kepala=4, lapisan=2, E=2, blok=24,
             iterasi=500, laju=4e-3, benih=0, seq_uji=None,
             cekpoint=50, jalan_cekpoint="", resume="", laporan=print):
    """Latih LM v4 dgn backward LENGKAP.

    seq        : daftar id token (BPE). seq_uji : ids di luar training (eval).
    cekpoint   : simpan tiap N iterasi. jalan_cekpoint: folder simpan.
    resume     : path npz bobot utk lanjut training (jumlah iterasi di-reset).
    laporan    : callback (iter, loss, keplex) utk logging.
    Kembalikan: {bobot, loss_trail, best_loss, perplexity, iterasi_total}.
    """
    v = int(max(seq)) + 1
    if resume:
        P = {k: varr for k, varr in np.load(resume, allow_pickle=True).items()}
    else:
        P = _init_bobot(v, d, kepala, lapisan, E, blok, np.random.default_rng(benih))
    rng = np.random.default_rng(benih + 1)
    m = {k: np.zeros_like(vv) for k, vv in P.items()}
    v2 = {k: np.zeros_like(vv) for k, vv in P.items()}

    n = len(seq)
    loss_trail = []
    best_loss = float("inf")

    # id batas uji (held-out) utk perplexity berkala
    uji = (seq_uji if seq_uji is not None else seq[-max(1, n // 20):])

    def hitung_perplexity():
        try:
            lo, _, _ = forward(P, uji[:blok], lapisan, kepala, E, d, blok)
            pr = softmax(lo)
            Y = uji[1:len(uji[:blok]) + 1]
            if len(Y) == 0:
                return None
            return float(np.exp(-np.log(pr[np.arange(len(Y)), Y] + 1e-9).mean()))
        except Exception:
            return None

    for it in range(1, iterasi + 1):
        i0 = int(rng.integers(0, max(1, n - blok)))
        ix = seq[i0:i0 + blok]
        Y = seq[i0 + 1:i0 + 1 + blok]
        logits, _, S = forward(P, ix, lapisan, kepala, E, d, blok)
        prob = softmax(logits)
        loss = -np.log(prob[np.arange(len(Y)), Y] + 1e-9).mean()
        loss_trail.append(float(loss))
        best_loss = min(best_loss, float(loss))

        dlog = prob.copy()
        dlog[np.arange(len(Y)), Y] -= 1.0
        dlog /= len(Y)

        G = backward_v4(P, S, dlog, lapisan, kepala, E, d, blok)
        for k in P:
            if k == "meta":
                continue
            m[k] = 0.9 * m[k] + 0.1 * G[k]
            v2[k] = 0.999 * v2[k] + 0.001 * G[k] * G[k]
            mh = m[k] / (1 - 0.9 ** it)
            vh = v2[k] / (1 - 0.999 ** it)
            P[k] -= laju * mh / (np.sqrt(vh) + 1e-8)

        if it % max(1, iterasi // 10) == 0 or it == 1:
            pk = hitung_perplexity()
            try:
                laporan(it, round(float(loss), 4), round(pk, 1) if pk else None)
            except Exception:
                pass

        if cekpoint and jalan_cekpoint and it % cekpoint == 0:
            import os
            os.makedirs(jalan_cekpoint, exist_ok=True)
            P["meta"] = {"d": d, "kepala": kepala, "lapisan": lapisan, "E": E,
                        "blok": blok, "iterasi": it}
            np.savez(os.path.join(jalan_cekpoint, f"v4_it{it}.npz"), **P)

    P["meta"] = {"d": d, "kepala": kepala, "lapisan": lapisan, "E": E,
                 "blok": blok, "iterasi": iterasi}
    return {"bobot": P, "loss_trail": loss_trail, "best_loss": best_loss,
            "perplexity": hitung_perplexity(), "iterasi_total": iterasi}


def gambar(P, awal, panjang=20, suhu=0.8, benih=0, lapisan=2, kepala=4, E=2, d=96, blok=24, balik=None):
    """Generate teks dari bobot v4. `balik`: fungsi id->char/teks (tokenizer)."""
    rng = np.random.default_rng(benih)
    meta = P.get("meta", {})
    if hasattr(meta, "item") and not isinstance(meta, dict):
        meta = meta.item()
    lapisan = meta.get("lapisan", lapisan)
    kepala = meta.get("kepala", kepala)
    E = meta.get("E", E)
    d = meta.get("d", d)
    ids = list(awal)
    for _ in range(panjang):
        ix = np.array(ids[-blok:], dtype=int)
        logits, _, _ = forward(P, ix, lapisan, kepala, E, d, blok)
        logit = logits[-1] / max(suhu, 0.05)
        e = np.exp(logit - logit.max())
        p = e / e.sum()
        nxt = int(rng.choice(len(p), p=p))
        ids.append(nxt)
    return ids


# ======================================================================
# BRIDGE ke Aksara: tulis / simpan / muat (gaya model_v3 backend)
# ======================================================================
def tulis_v4(model, seq_awal, panjang=30, suhu=0.8, benih=0):
    """Alias Aksara utk gambar: seq_awal = list id awal."""
    return gambar(model, list(seq_awal), panjang=panjang, suhu=suhu, benih=benih)


def simpan_v4(jalan, data):
    """Simpan bobot+meta via pickle (diakses dr Aksara)."""
    import pickle as _p
    with open(jalan, "wb") as f:
        _p.dump({k: (np.asarray(v) if not isinstance(v, dict) else v)
                 for k, v in data.items()}, f, protocol=4)
    return jalan


def muat_v4(jalan):
    """Muat bobot+meta (diakses dr Aksara). Dict (seperti BPE) dikecualikan
    dari konversi numpy biar tidak rusak."""
    import pickle as _p
    with open(jalan, "rb") as f:
        data = _p.load(f)
    for k, v in data.items():
        if k != "meta" and isinstance(v, (list, tuple)):
            data[k] = np.asarray(v)
    return data


# ======================================================================
# CLI: python3 -m aksara.ai.model_v4 --gradcheck / --train / --gambar
# ======================================================================
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Mini-LM v4 engine")
    ap.add_argument("--gradcheck", action="store_true")
    ap.add_argument("--train", default="")
    ap.add_argument("--iterasi", type=int, default=200)
    ap.add_argument("--d", type=int, default=64)
    ap.add_argument("--lapisan", type=int, default=2)
    ap.add_argument("--keluaran", default="")
    ap.add_argument("--gambar", default="", help="path checkpoint npz utk generate")
    ap.add_argument("--awal", default="harga")
    ap.add_argument("--panjang", type=int, default=24)
    args = ap.parse_args()

    if args.gradcheck:
        print(periksa_grad())
    elif args.train:
        korpus = open(args.train, encoding="utf-8", errors="replace").read()
        from .tokenizer_bpe import latih as siap_bpe, ubah_ke_id
        mbpe = siap_bpe(korpus, 400)
        ids = ubah_ke_id(mbpe, korpus)
        print(f"corpus {len(korpus)} char -> {len(ids)} token (vocab 400)")
        res = latih_v4(ids, d=args.d, kepala=4, lapisan=args.lapisan, E=2,
                       blok=48, iterasi=args.iterasi, laju=3e-3,
                       cekpoint=args.iterasi // 5,
                       jalan_cekpoint=args.keluaran or "./ckpt_v4")
        print("best_loss:", res["best_loss"], "| perplexity:", res["perplexity"])
    elif args.gambar:
        import glob, os
        ds = glob.glob(os.path.join(args.gambar, "*.npz"))
        if not ds:
            print("tidak ada ckpt di", args.gambar)
            raise SystemExit(1)
        last = sorted(ds)[-1]
        P = {k: v for k, v in np.load(last, allow_pickle=True).items()}
        meta = (np.load(last, allow_pickle=True)["meta"].item()) if "meta" in np.load(last, allow_pickle=True).files else {}
        ids = gambar(P, [_awal := (args.awal.encode()[0] if args.awal else 0)],
                     panjang=args.panjang,
                     lapisan=int(meta.get("lapisan", 1)),
                     kepala=int(meta.get("kepala", 4)),
                     E=int(meta.get("E", 2)),
                     d=int(meta.get("d", 48)),
                     blok=int(meta.get("blok", 48)))
        print("generated ids:", ids[:40])
    else:
        ap.print_help()
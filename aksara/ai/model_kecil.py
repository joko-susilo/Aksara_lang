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

"""Mini LM: model bahasa karakter dilatih dari nol (hanya numpy).

Arsitektur minimal bergaya GPT: embedding + posisi, blok attention ber-kepala
dengan residual + ReLU, lalu proyeksi kosakata. Cukup untuk belajar "rasa"
sebuah teks (mis. bahasa Indonesia) di CPU.

Pemakaian dari Aksara:
    impor "aksara.ai.model_kecil" sbg lm
    model = lm.latih_teks(isi, 64, 32, 2, 1, 500, 0.01)
    cetak lm.tulis(model, "Di sebuah", panjang=120)
"""

import numpy as np


def _softmax(x, sumbu=-1):
    e = np.exp(x - x.max(axis=sumbu, keepdims=True))
    return e / e.sum(axis=sumbu, keepdims=True)


def _vokabel(teks):
    chars = sorted(set(teks))
    return chars, {c: i for i, c in enumerate(chars)}


def _satuan(teks, kata):
    """Potong teks jadi token. kata=True -> kata kata (spasi), else karakter."""
    import re
    if kata:
        return re.findall(r"\S+", teks)
    return list(teks)


def latih_teks(teks, blok=48, tersembunyi=32, kepala=2, lapisan=1,
               iterasi=400, laju=0.01, benih=0, kata=False):
    """Latih model bahasa kecil. kata=True -> mode kata (lebih mulus)."""
    import re
    satuan = _satuan(teks, kata)
    chars = sorted(set(satuan))
    c2i = {c: i for i, c in enumerate(chars)}
    tok = np.array([c2i[c] for c in satuan], dtype=np.int64)
    v = len(chars)
    if len(tok) < blok + 1:
        blok = max(blok, len(tok) - 1)
    if blok < 2:
        raise ValueError("Teks terlalu pendek untuk melatih model.")
    d = tersembunyi
    nh = kepala
    hd = d // nh
    rng = np.random.default_rng(benih)

    P = {}
    P["Wte"] = rng.standard_normal((v, d)) * 0.02
    P["Wpe"] = rng.standard_normal((blok, d)) * 0.02
    P["Wlr"] = rng.standard_normal((d, v)) * 0.02
    P["blr"] = np.zeros(v)
    for l in range(lapisan):
        P[f"Wq{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wk{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wv{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"Wo{l}"] = rng.standard_normal((d, d)) * 0.02
        P[f"W1{l}"] = rng.standard_normal((d, 4 * d)) * 0.02
        P[f"b1{l}"] = np.zeros(4 * d)
        P[f"W2{l}"] = rng.standard_normal((4 * d, d)) * 0.02
        P[f"b2{l}"] = np.zeros(d)

    m = {k: np.zeros_like(v) for k, v in P.items()}
    v2 = {k: np.zeros_like(v) for k, v in P.items()}
    mask = np.triu(np.full((blok, blok), -1e9), k=1)

    def maju(ix):
        T = blok
        x = P["Wte"][ix] + P["Wpe"][:T]
        simpan = {"x_in": x.copy()}
        for l in range(lapisan):
            q = x @ P[f"Wq{l}"]; k = x @ P[f"Wk{l}"]; v = x @ P[f"Wv{l}"]
            qq = q.reshape(T, nh, hd).transpose(1, 0, 2)
            kk = k.reshape(T, nh, hd).transpose(1, 0, 2)
            vv = v.reshape(T, nh, hd).transpose(1, 0, 2)
            skor = qq @ kk.transpose(0, 2, 1) / np.sqrt(hd) + mask
            pp = _softmax(skor)
            oo = (pp @ vv).transpose(1, 0, 2).reshape(T, d)
            att = oo @ P[f"Wo{l}"]
            ares = x + att
            g = ares @ P[f"W1{l}"] + P[f"b1{l}"]
            gr = np.maximum(0, g)
            f2 = gr @ P[f"W2{l}"] + P[f"b2{l}"]
            x = f2 + ares
            simpan[f"x{l}"] = x.copy()
            simpan[f"q{l}"] = qq; simpan[f"k{l}"] = kk; simpan[f"v{l}"] = vv
            simpan[f"p{l}"] = pp; simpan[f"ares{l}"] = ares.copy()
            simpan[f"gr{l}"] = gr
        logits = x @ P["Wlr"] + P["blr"]
        return logits, simpan

    def mundur(dlog, IX, simpan):
        T = blok
        dx = dlog @ P["Wlr"].T
        G = {"Wlr": simpan["x" + str(lapisan - 1)].T @ dlog,
             "blr": dlog.sum(axis=0)}
        for l in range(lapisan - 1, -1, -1):
            x = simpan["x_in"] if l == 0 else simpan["x" + str(l - 1)]
            ares = simpan[f"ares{l}"]
            gr = simpan[f"gr{l}"]
            # f2 + ares residual
            df2 = dx
            dares = dx
            # gr @ W2 + b2
            dgr = df2 @ P[f"W2{l}"].T
            G[f"W2{l}"] = gr.T @ df2
            G[f"b2{l}"] = df2.sum(axis=0)
            dg = dgr * (gr > 0)
            # ares @ W1 + b1
            G[f"W1{l}"] = ares.T @ dg
            G[f"b1{l}"] = dg.sum(axis=0)
            datt = dares + dg @ P[f"W1{l}"].T
            # ares = x + att
            dx_in = datt
            # att = oo @ Wo
            oo = (simpan[f"p{l}"] @ simpan[f"v{l}"]).transpose(1, 0, 2).reshape(T, d)
            G[f"Wo{l}"] = oo.T @ datt
            doo = datt @ P[f"Wo{l}"].T
            # oo = (pp @ vv).reshape  -> balik ke bentuk kepala
            doo_h = doo.reshape(T, nh, hd).transpose(1, 0, 2)
            dpp = doo_h @ simpan[f"v{l}"].transpose(0, 2, 1)
            dvv = simpan[f"p{l}"].transpose(0, 2, 1) @ doo_h
            # softmax backward
            pp = simpan[f"p{l}"]
            dskor = pp * (dpp - (dpp * pp).sum(axis=-1, keepdims=True))
            # skor = qq@kkT/sqrt + mask ; q=..., k=...
            d_raw = dskor / np.sqrt(hd)
            dqq = d_raw @ simpan[f"k{l}"]
            dkk = d_raw.transpose(0, 2, 1) @ simpan[f"q{l}"]
            dq = dqq.transpose(1, 0, 2).reshape(T, d)
            dk = dkk.transpose(1, 0, 2).reshape(T, d)
            dv = dvv.transpose(1, 0, 2).reshape(T, d)
            G[f"Wq{l}"] = x.T @ dq
            G[f"Wk{l}"] = x.T @ dk
            G[f"Wv{l}"] = x.T @ dv
            dx = dx_in + dq @ P[f"Wq{l}"].T + dk @ P[f"Wk{l}"].T + dv @ P[f"Wv{l}"].T
        G["Wpe"] = dx
        dWte = np.zeros_like(P["Wte"])
        np.add.at(dWte, IX, dx)
        G["Wte"] = dWte
        return G

    t = 0
    for _ in range(iterasi):
        i0 = int(rng.integers(0, len(tok) - blok))
        IX = tok[i0:i0 + blok]
        Y = tok[i0 + 1:i0 + 1 + blok]
        logits, simpan = maju(IX)
        t += 1
        prob = _softmax(logits)
        dlog = prob.copy()
        dlog[np.arange(blok), Y] -= 1.0
        dlog /= blok
        G = mundur(dlog, IX, simpan)
        for k, gv in G.items():
            m[k] = 0.9 * m[k] + 0.1 * gv
            v2[k] = 0.999 * v2[k] + 0.001 * gv * gv
            mh = m[k] / (1 - 0.9 ** t)
            vh = v2[k] / (1 - 0.999 ** t)
            P[k] -= laju * mh / (np.sqrt(vh) + 1e-8)

    meta = {
        "d": d, "kepala": nh, "hd": hd, "lapisan": lapisan, "blok": blok,
        "v": v, "char": list(chars), "c2i": c2i, "kata": bool(kata),
    }
    for k, val in meta.items():
        P[k] = val
    return P


def tulis(model, awal="", panjang=80, suhu=1.0, benih=0):
    """Hasilkan teks dari model. suhu=0 -> deterministik (argmax)."""
    chars = model["char"]
    c2i = model["c2i"]
    mode_kata = model.get("kata", False)
    d = model["d"]
    nh = model["kepala"]
    hd = model["hd"]
    lapisan = model["lapisan"]
    blok = model["blok"]
    rng = np.random.default_rng(benih)

    awal_tok = awal.split() if mode_kata else list(awal)
    ix = [c2i[c] for c in awal_tok if c in c2i]
    hasil = awal_tok[:]

    def fwd(x):
        for l in range(lapisan):
            q = x @ model[f"Wq{l}"]; k = x @ model[f"Wk{l}"]
            v = x @ model[f"Wv{l}"]
            T = x.shape[0]
            qq = q.reshape(T, nh, hd).transpose(1, 0, 2)
            kk = k.reshape(T, nh, hd).transpose(1, 0, 2)
            vv = v.reshape(T, nh, hd).transpose(1, 0, 2)
            tmask = np.triu(np.full((T, T), -1e9), k=1)
            pp = _softmax(qq @ kk.transpose(0, 2, 1) / np.sqrt(hd) + tmask)
            oo = (pp @ vv).transpose(1, 0, 2).reshape(T, d)
            ares = x + oo @ model[f"Wo{l}"]
            gr = np.maximum(0, ares @ model[f"W1{l}"] + model[f"b1{l}"])
            x = (gr @ model[f"W2{l}"] + model[f"b2{l}"]) + ares
        return x @ model["Wlr"] + model["blr"]

    for _ in range(panjang):
        ctx = ix[-blok:]
        x = model["Wte"][ctx] + model["Wpe"][:len(ctx)]
        logits = fwd(x)[-1]
        if suhu <= 0:
            nxt = int(np.argmax(logits))
        else:
            p = _softmax(logits / max(suhu, 1e-9))
            nxt = int(rng.choice(len(chars), p=p))
        hasil.append(chars[nxt])
        ix.append(nxt)
    if mode_kata:
        return " ".join(hasil)
    return "".join(hasil)
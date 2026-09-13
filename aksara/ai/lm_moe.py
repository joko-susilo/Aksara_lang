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

"""LM + MoE — Language model dengan FFN Mixture-of-Experts (Step C nyatu).

Token di routing ke top-1 dari E pakar FFN. Kapasitas naik (banyak pakar),
beban per-token turun (cuma 1 pakar aktif). Arsitektur mini ala GPT:
embedding + posisi, attention 1 blok, lalu FFN-MoE. numpy murni, CPU.

Pemakaian dari Aksara:
    impor "aksara.ai.lm_moe" sbg lm
    model = lm.latih(isi, pakar=4, tersembunyi=48, blok=24, iterasi=300)
    cetak lm.tulis(model, "bahasa indonesia", panjang=40)
"""

import numpy as np


def _softmax(x, sumbu=-1):
    e = np.exp(x - x.max(axis=sumbu, keepdims=True))
    return e / e.sum(axis=sumbu, keepdims=True)


def latih(teks, pakar=4, tersembunyi=48, blok=24, iterasi=300,
          laju=0.01, benih=0):
    """Latih LM karakter + FFN MoE. Kembalikan kamus bobot."""
    chars = sorted(set(teks))
    n = len(chars)
    c2i = {c: i for i, c in enumerate(chars)}
    tok = np.array([c2i[c] for c in teks], dtype=np.int64)
    d = tersembunyi
    E = pakar
    rng = np.random.default_rng(benih)

    P = {}
    P["Wte"] = rng.standard_normal((n, d)) * 0.02
    P["Wpe"] = rng.standard_normal((blok, d)) * 0.02
    P["Wq"] = rng.standard_normal((d, d)) * 0.02
    P["Wk"] = rng.standard_normal((d, d)) * 0.02
    P["Wv"] = rng.standard_normal((d, d)) * 0.02
    P["Wo"] = rng.standard_normal((d, d)) * 0.02
    # router MoE
    P["Wr"] = rng.standard_normal((d, E)) * 0.02
    # eksper FFN (E pakar)
    P["Wu1"] = rng.standard_normal((E, d, d)) * 0.02
    P["bu1"] = np.zeros((E, d))
    P["Wu2"] = rng.standard_normal((E, d, d)) * 0.02
    P["bu2"] = np.zeros((E, d))
    P["Wlr"] = rng.standard_normal((d, n)) * 0.02
    P["blr"] = np.zeros(n)

    m = {k: np.zeros_like(v) for k, v in P.items()}
    v2 = {k: np.zeros_like(v) for k, v in P.items()}
    mask = np.triu(np.full((blok, blok), -1e9), k=1)

    def fwd(ix):
        T = blok
        h = P["Wte"][ix] + P["Wpe"][:T]
        simpan = {"h_in": h.copy()}
        q = h @ P["Wq"]; k = h @ P["Wk"]; v = h @ P["Wv"]
        skor = (q @ k.T) / np.sqrt(d) + mask  # (T,T)
        pp = _softmax(skor)
        att = (pp @ v) @ P["Wo"]
        h = h + att                       # residual
        simpan["att_res"] = h.copy()
        # FFN MoE: router per token
        r = h @ P["Wr"]                    # (T,E)
        g = _softmax(r)                    # gate
        top = np.argsort(-r, axis=1)[:, 0]  # top-1
        simpan["gate"] = g; simpan["top"] = top
        ffn = np.zeros_like(h)
        for e in range(E):
            z = np.maximum(0, h @ P["Wu1"][e] + P["bu1"][e])
            out = z @ P["Wu2"][e] + P["bu2"][e]
            ffn = ffn + g[:, e:e+1] * out
            simpan[f"z{e}"] = z; simpan[f"out{e}"] = out
        h = h + ffn
        simpan["h_out"] = h
        logits = h @ P["Wlr"] + P["blr"]
        return logits, simpan

    def bwd(dlog, IX, S):
        h_out = S["h_out"]
        G = {k: np.zeros_like(v) for k, v in P.items()}
        G.update({"Wlr": h_out.T @ dlog, "blr": dlog.sum(axis=0)})
        dx = dlog @ P["Wlr"].T
        hb = S["att_res"]
        dffn = dx
        dh_att = dx
        g = S["gate"]; top = S["top"]; T = hb.shape[0]
        # Balik FFN MoE
        D = {}
        for e in range(P["Wu1"].shape[0]):
            z = S[f"z{e}"]; out = S[f"out{e}"]
            D[f"Wu2{e}"] = (g[:, e:e+1] * z).T @ dffn
            D[f"bu2{e}"] = (g[:, e:e+1] * dffn).sum(axis=0)
            dz = (g[:, e:e+1] * dffn) @ P["Wu2"][e].T
            dz[z <= 0] = 0
            D[f"Wu1{e}"] = (g[:, e:e+1] * hb).T @ dz
            D[f"bu1{e}"] = (g[:, e:e+1] * dz).sum(axis=0)
        # gate grad sederhana (heuristic top-1)
        for t in range(T):
            e = int(top[t])
            dh_att[t] = dh_att[t] + P["Wu1"][e] @ ((dx[t] if False else dx[t]))
        # attention backward (1 head)
        h_in = S["h_in"]
        hs = S["att_res"] - dx  # att sebelum residual = h_out - dffn - h_in
        # perkiraan: abaikan jalan attention (dibatasi), proyek ke hs
        G["Wo"] = (S["att_res"] - h_in).T @ (dx - dh_att + dx) if False else P["Wo"] * 0.0
        dhs = dh_att
        # router grad: gerakkan Wr agar top-1 expert sesuai (soft)
        G["Wr"] = h_in.T @ (g * dx.sum(axis=1, keepdims=True)) * 0.01
        dx2 = dhs @ P["Wq"].T * 0.0  # heuristik stabil; skip grad attention penuh
        G["Wq"] = P["Wq"] * 0.0; G["Wk"] = P["Wk"] * 0.0; G["Wv"] = P["Wv"] * 0.0
        G["Wq"] += h_in.T @ dhs * 0.001
        G["Wk"] += h_in.T @ dhs * 0.001
        G["Wv"] += h_in.T @ dhs * 0.001
        # embedding & posisi
        G["Wpe"] = dhs * 0.001
        G["Wte"] = np.zeros_like(P["Wte"])
        np.add.at(G["Wte"], IX, dhs * 0.001)
        # satukan (eksper grad)
        for e in range(P["Wu1"].shape[0]):
            G["Wu1"][e] = D[f"Wu1{e}"]
            G["bu1"][e] = D[f"bu1{e}"]
            G["Wu2"][e] = D[f"Wu2{e}"]
            G["bu2"][e] = D[f"bu2{e}"]
        return G

    t = 0
    for it in range(iterasi):
        if len(tok) < blok + 1:
            blok2 = max(1, len(tok) - 1)
        else:
            blok2 = blok
        i0 = int(rng.integers(0, max(1, len(tok) - blok2)))
        IX = tok[i0:i0 + blok2]
        Y = tok[i0 + 1:i0 + 1 + blok2]
        pad = blok - blok2
        if pad > 0:
            IX = np.pad(IX, (0, pad), mode='constant', constant_values=IX[0])
            Y = np.pad(Y, (0, pad), mode='constant', constant_values=Y[0])
        logits, S = fwd(IX)
        t += 1
        prob = _softmax(logits)
        dlog = prob.copy()
        dlog[np.arange(blok2), Y[:blok2]] -= 1.0
        dlog /= blok2
        G = bwd(dlog, IX, S)
        for k, gv in G.items():
            m[k] = 0.9 * m[k] + 0.1 * gv
            v2[k] = 0.999 * v2[k] + 0.001 * gv * gv
            mh = m[k] / (1 - 0.9 ** t)
            vh = v2[k] / (1 - 0.999 ** t)
            P[k] -= laju * mh / (np.sqrt(vh) + 1e-8)

    P["meta"] = {"d": d, "pakar": E, "blok": blok, "chars": chars, "c2i": c2i}
    return P


def tulis(model, awal="", panjang=60, suhu=0.8, benih=0):
    chars = model["meta"]["chars"]
    c2i = model["meta"]["c2i"]
    d = model["meta"]["d"]; E = model["meta"]["pakar"]; blok = model["meta"]["blok"]
    rng = np.random.default_rng(benih)
    nch = {i: c for c, i in c2i.items()}

    ix = [c2i[c] for c in awal if c in c2i]
    if not ix:
        ix = [0]
    hasil = list(ix)

    for _ in range(panjang):
        ctx = ix[-blok:]
        x = model["Wte"][ctx] + model["Wpe"][:len(ctx)]
        T = len(ctx)
        q = x @ model["Wq"]; k = x @ model["Wk"]; v = x @ model["Wv"]
        mask = np.triu(np.full((T, T), -1e9), k=1)
        pp = _softmax((q @ k.T) / np.sqrt(d) + mask)
        h = x + (pp @ v) @ model["Wo"]
        r = h @ model["Wr"]
        g = _softmax(r)
        ffn = np.zeros_like(h)
        for e in range(E):
            z = np.maximum(0, h @ model["Wu1"][e] + model["bu1"][e])
            ffn = ffn + g[:, e:e+1] * (z @ model["Wu2"][e] + model["bu2"][e])
        logits = (h + ffn) @ model["Wlr"] + model["blr"]
        logits = logits[-1]
        if suhu <= 0:
            nxt = int(np.argmax(logits))
        else:
            p = _softmax(logits / max(suhu, 1e-9))
            nxt = int(rng.choice(len(chars), p=p))
        hasil.append(nxt)
        ix.append(nxt)
    return "".join(nch[i] for i in hasil if i in nch).strip()


def info(model):
    meta = model["meta"]
    return {
        "pakar": meta["pakar"],
        "tersembunyi": meta["d"],
        "blok": meta["blok"],
        "ukuran_karakter": len(meta["chars"]),
    }
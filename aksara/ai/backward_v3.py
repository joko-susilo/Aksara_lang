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

"""Backward Propagation LENGKAP Mini-LM v4 — ditulis ulang, DIVERIFIKASI.

Rewrite (2026-09-13) setelah gradien-check membongkar bug versi lama:
  - einsum attention `d_vh` label salah (broadcast error)
  - gate FFN-MoE menempel di input x2 bukan d_ffn (rumus grad salah)
  - router Wr tanpa softmax-backward
  - Wo dihitung dari niat yang keliru (att_out@Wo^T, bukan att_out.T@d_att)

Aturan main: batch GRADIEN-CHECK (finite-difference) wajib lolos sebelum
dipakai training. `model_v4.periksa_grad()` adalah kewenangannya.

Relasi forward (per layer l):
  q=x Wq ; k=x Wk ; v=x Wv
  sk = (q,k)/sqrt(hd)+mask ; pr=softmax(sk, key)
  att_out = einsum(pr, vh) ; att = att_out Wo
  ln1in = x + att ; x2 = LN1(ln1in)
  gate = softmax(x2 Wr) ; ffn = sum_e gate_e * (relu(x2 Wu1e+bu1e) Wu2e+bu2e)
  ln2in = x2 + ffn  ; x = LN2(ln2in)
  final: logits = x @ Wlr + blr
"""

import numpy as np


def softmax(x, sumbu=-1):
    x = x - x.max(axis=sumbu, keepdims=True)
    e = np.exp(x)
    return e / (e.sum(axis=sumbu, keepdims=True) + 1e-9)


def _ln_back(z, g, dy):
    """Grad eksak input ke LayerNorm (diverifikasi dgn finite-difference).

    LN(z) = g*xhat + b ; xhat = (z - mu)/s ; s = sqrt(var+eps)
    Grad dL/dz_i:
      A_i/t           (direct)
      + Dvar * dvar/dz_i   ;  Dvar = -sum_j A_j xhat_j / (2 s^2)
                            ;  dvar/dz_i = (2/T)(z_i-mu) - (2/T^2) sum_j (z_j-mu)
      + Dmu/T          ;  Dmu = -sum_j A_j / s
    A = dy * g (grad wrt xhat). Var pakai ddof=0 (sesuai forward).
    """
    T = z.shape[-1]
    mu = z.mean(-1, keepdims=True)
    var = z.var(-1, keepdims=True) + 1e-5
    s = np.sqrt(var)
    xhat = (z - mu) / s
    A = dy * g                                       # (…,T) grad wrt xhat

    dz = A / s                                       # direct term

    Dvar = -(np.sum(A * xhat, axis=-1, keepdims=True) / (2.0 * s * s))
    dvar_dz = (2.0 / T) * (z - mu) - (2.0 / (T * T)) * np.sum(z - mu, axis=-1, keepdims=True)
    dz = dz + Dvar * dvar_dz

    Dmu = -(np.sum(A, axis=-1, keepdims=True) / s)
    dz = dz + Dmu / T
    return dz


def backward_v4(P, S, dlog, lapisan, kepala, E, d, blok):
    """Hitung G (grad utk semua bobot). S = aktivasi dari model_v4.forward."""
    hd = d // kepala
    T = int(len(dlog))
    G = {k: np.zeros_like(v) for k, v in P.items()}

    # ===== proyeksi output =====
    xL = S["x_out"]                                   # (T,d) input ke Wlr
    G["Wlr"] = xL.T @ dlog
    G["blr"] = dlog.sum(axis=0)
    dx = dlog @ P["Wlr"].T                            # grad ke xL

    for l in range(lapisan - 1, -1, -1):
        # --- LN2 : ln2in = x2 + ffn ; x{l} = LN2 output ---
        z_ln2 = S[f"ln2in{l}"]
        d_out_ln2 = dx.copy()                       # grad wrt LN2 OUTPUT
        xhat2 = (z_ln2 - z_ln2.mean(-1, keepdims=True)) / \
            np.sqrt(z_ln2.var(-1, keepdims=True) + 1e-5)
        G[f"ln2g{l}"] = np.sum(d_out_ln2 * xhat2, axis=0)
        G[f"ln2b{l}"] = d_out_ln2.sum(axis=0)
        d_ln2in = _ln_back(z_ln2, P[f"ln2g{l}"], d_out_ln2)

        # --- FFN-MoE + gate ---
        # ffn = sum_e gate[:,e] out_e ; d_ln2in dialirkan ke ffn & x2 (residual)
        d_ffn = d_ln2in.copy()
        d_x2 = d_ln2in.copy()
        gate = S[f"gate{l}"]                          # (T,E)
        out_e_all = S.get(f"out_e{l}")
        d_gate = np.zeros_like(gate)
        for e in range(E):
            z = S[f"z{l}_{e}"]                        # relu act (T,4d)
            if out_e_all is None:
                out_e = z @ P[f"Wu2{l}"][e] + P[f"bu2{l}"][e]
            else:
                out_e = out_e_all[e]
            d_out = d_ffn * gate[:, e:e+1]            # grad ke out_e
            d_gate[:, e] = (d_ffn * out_e).sum(-1)    # grad ke gate[:,e]
            G[f"Wu2{l}"][e] = z.T @ d_out
            G[f"bu2{l}"][e] = d_out.sum(axis=0)
            dz = d_out @ P[f"Wu2{l}"][e].T
            dz[z <= 0] = 0.0                          # relu
            G[f"Wu1{l}"][e] = S[f"x2{l}"].T @ dz
            G[f"bu1{l}"][e] = dz.sum(axis=0)
            d_x2 = d_x2 + dz @ P[f"Wu1{l}"][e].T

        # router: gate = softmax(x2 @ Wr)
        d_gate_pre = gate * (d_gate - np.sum(gate * d_gate, axis=-1, keepdims=True))
        G[f"Wr{l}"] = S[f"x2{l}"].T @ d_gate_pre
        d_x2 = d_x2 + d_gate_pre @ P[f"Wr{l}"].T

# --- LN1 : ln1in = x + att ; x2 = LN1 output ---
        z_ln1 = S[f"ln1in{l}"]
        d_out_ln1 = d_x2.copy()                     # grad wrt LN1 OUTPUT
        xhat1 = (z_ln1 - z_ln1.mean(-1, keepdims=True)) / \
            np.sqrt(z_ln1.var(-1, keepdims=True) + 1e-5)
        G[f"ln1g{l}"] = np.sum(d_out_ln1 * xhat1, axis=0)
        G[f"ln1b{l}"] = d_out_ln1.sum(axis=0)
        d_ln1in = _ln_back(z_ln1, P[f"ln1g{l}"], d_out_ln1)

        # --- attention ---
        d_att = d_ln1in.copy()
        dx = d_ln1in.copy()                           # residual x dari ln1in
        att_out = S[f"att_out{l}"]                    # input ke Wo (T,d)
        d_att_out = d_att @ P[f"Wo{l}"].T
        G[f"Wo{l}"] = att_out.T @ d_att

        pr = S[f"pr{l}"]                              # (T,kepala,T) label (t,h,c)
        vh = S[f"vh{l}"]                              # (T,kepala,hd)
        qh = S[f"qh{l}"]
        kh = S[f"kh{l}"]
        d_oh = d_att_out.reshape(T, kepala, hd)

        # att_out[t,h,:] = sum_c pr[t,h,c] vh[c,h,:]
        d_vh = np.einsum("thc,thd->chd", pr, d_oh)             # (c,h,d)
        d_pr = np.einsum("thd,chd->thc", d_oh, vh)             # (t,h,c)
        d_sk = pr * (d_pr - np.sum(pr * d_pr, axis=-1, keepdims=True))
        d_sk = d_sk / np.sqrt(hd)                              # sk = qk^T/sqrt(hd)+mask
        # sk[t,h,c] = sum_u qh[t,h,u] kh[c,h,u]
        d_qh = np.einsum("thc,chd->thd", d_sk, kh)             # (t,h,d)
        d_kh = np.einsum("thc,thd->chd", d_sk, qh)             # (c,h,d)

        x_prev = S[f"x{l-1}"] if l > 0 else S["x_in"]
        d_q = d_qh.reshape(T, d)
        d_k = d_kh.reshape(T, d)
        d_v = d_vh.reshape(T, d)
        G[f"Wq{l}"] = x_prev.T @ d_q
        G[f"Wk{l}"] = x_prev.T @ d_k
        G[f"Wv{l}"] = x_prev.T @ d_v
        dx = dx + d_q @ P[f"Wq{l}"].T + d_k @ P[f"Wk{l}"].T + d_v @ P[f"Wv{l}"].T

    # ===== embedding & posisi =====
    ixx = np.asarray(S["ix"])
    G["Wpe"] = np.zeros_like(P["Wpe"])
    G["Wpe"][:T] = dx
    G["Wte"] = np.zeros_like(P["Wte"])
    np.add.at(G["Wte"], ixx, dx)
    return G
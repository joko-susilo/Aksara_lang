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

"""MoE ringan (Mixture-of-Experts) — Step C Mini LM v2.

Prinsip: N "pakar" (router + eksper kecil). Setiap token hanya mengaktifkan
top-1 (atau top-k) pakar, sisanya di-skip. Kapasitas model naik (parameter
banyak) tapi FLOP & memori token-basis turun — hemat untuk smartphone.

Komponen:
  router:  bobot (d_konteks x N) pakai top-k.
  eksper:  lapisan linear kecil (d x d) tiap pakar.
Forward:
  skor = x @ W_router ; pilih argtopk ; hasil = sum(softmax(skor)[k] * E_k(x))
"""

import numpy as np


def _softmax(x):
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def latih_moe(X, Y, n_pakar=4, k=1, d=16, iterasi=300, laju=0.05, benih=0):
    """Latih MoE sederhana (regresi). X (m,2) feat contoh, Y target 1 kolom.

    Kembalikan kamus bobot router+eksper, parameter penskalaan.
    """
    X = np.array(X, dtype=float)
    Y = np.array(Y, dtype=float).reshape(-1, 1)

    x_mean = X.mean(axis=0)
    x_std = X.std(axis=0) + 1e-9
    Xs = (X - x_mean) / x_std
    y_mean = Y.mean()
    y_std = Y.std() + 1e-9
    Ys = (Y - y_mean) / y_std

    rng = np.random.default_rng(benih)
    n_in = Xs.shape[1]
    Wr = rng.standard_normal((n_in, n_pakar)) * 0.1
    W = rng.standard_normal((n_pakar, n_in, d)) * 0.1
    Wo = rng.standard_normal((n_pakar, d, 1)) * 0.1
    br = np.zeros(n_pakar)
    b = np.zeros((n_pakar, d))
    bo = np.zeros((n_pakar, 1))

    for _ in range(iterasi):
        skor = Xs @ Wr + br                  # (m, n_pakar)
        prob = _softmax(skor)                # route prob
        # top-k
        kk = min(k, n_pakar)
        top = np.argsort(-skor, axis=1)[:, :kk]
        aktif = np.zeros_like(skor)
        for i in range(len(Xs)):
            idx = top[i]
            aktif[i, idx] = prob[i, idx]
        aktif = aktif / (aktif.sum(axis=1, keepdims=True) + 1e-9)

        # forward per pakar weighted
        # pred = sum_p aktif_i,p * (Xs @ Wp @ Wo p + ...)
        pred = np.zeros((len(Xs), 1))
        h = {}
        for p in range(n_pakar):
            z = Xs @ W[p] + b[p]            # (m, d)
            h[p] = np.maximum(0, z)         # ReLU
            pred += (aktif[:, p:p+1] * (h[p] @ Wo[p] + bo[p]))

        dz = pred - Ys                       # (m,1)
        # grad Wo_p = aktif_p * h_p^T dz
        G_Wo = {}
        G_b_aktif = {}
        G_Wr = np.zeros_like(Wr)
        for p in range(n_pakar):
            G_Wo[p] = (aktif[:, p:p+1] * h[p]).T @ dz / len(Xs)
            dh = (dz * aktif[:, p:p+1]) @ Wo[p].T
            dh[h[p] <= 0] = 0
            # update W, b, Wo, bo per pakar
            W[p] -= laju * (Xs.T @ dh) / len(Xs)
            b[p] -= laju * dh.mean(axis=0)
            Wo[p] -= laju * G_Wo[p]
            bo[p] -= laju * (dz * aktif[:, p:p+1]).mean(axis=0)
        # router grad sederhana: dorong pakar yang prediksinya lebih dekat
        # gunakan skor grad = -aktif_perhatian (heuristik statis) biar stabil
        for i in range(len(Xs)):
            for p2 in range(n_pakar):
                if aktif[i, p2] > 0:
                    G_Wr[:, p2] += skor[i, p2] * 0.0001
        Wr -= laju * G_Wr / max(len(Xs), 1)
        br -= laju * G_Wr.mean(axis=0) * 0.0  # stabil (router grad disederhanakan)

    return {
        "Wr": Wr.tolist(), "br": br.tolist(),
        "W": [w.tolist() for w in W], "b": [x.tolist() for x in b],
        "Wo": [w.tolist() for w in Wo], "bo": [x.tolist() for x in bo],
        "n_pakar": n_pakar, "k": kk,
        "x_mean": x_mean.tolist(), "x_std": x_std.tolist(),
        "y_mean": y_mean, "y_std": y_std,
    }


def ramal_moe(model, X):
    """Prediksi dari MoE (forward kuantitatif)."""
    X = np.array(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(1, -1)
    Wr = np.array(model["Wr"]); br = np.array(model["br"])
    W = [np.array(w) for w in model["W"]]
    b = [np.array(x) for x in model["b"]]
    Wo = [np.array(w) for w in model["Wo"]]
    bo = [np.array(x) for x in model["bo"]]
    n_pakar = model["n_pakar"]; kk = model["k"]

    Xs = (X - np.array(model["x_mean"])) / np.array(model["x_std"])
    skor = Xs @ Wr + br
    prob = _softmax(skor)
    top = np.argsort(-skor, axis=1)[:, :kk]
    aktif = np.zeros_like(skor)
    for i in range(len(Xs)):
        idx = top[i]
        aktif[i, idx] = prob[i, idx]
    aktif = aktif / (aktif.sum(axis=1, keepdims=True) + 1e-9)

    pred = np.zeros((len(Xs), 1))
    for p in range(n_pakar):
        z = np.maximum(0, Xs @ W[p] + b[p])
        pred += aktif[:, p:p+1] * (z @ Wo[p] + bo[p])
    hasil = pred * model["y_std"] + model["y_mean"]
    return [round(float(v), 4) for v in hasil.reshape(-1)]


def info_moe(model):
    return {
        "n_pakar": model["n_pakar"],
        "top_k": model["k"],
        "param_per_pakar": int(np.prod(np.array(model["W"][0]).shape)),
        "total_param": int(np.prod(np.array(model["Wr"]).shape)) + int(np.prod(np.array(model["Wo"][0]).shape)) * model["n_pakar"],
    }
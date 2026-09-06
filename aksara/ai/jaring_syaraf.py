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
import numpy as np

def jaring_syaraf(X, y, hidden=8, iterasi=500, laju=0.1):
    """Neural network 1 hidden layer (ReLU) dengan standardisasi fitur.

    Mengembalikan kamus bobot + parameter penskalaan (dipakai `ramal`).
    """
    X = np.array(X, dtype=float)
    y = np.array(y, dtype=float).reshape(-1, 1)

    # Standardisasi fitur dan target agar pelatihan stabil.
    x_mean = X.mean(axis=0)
    x_std = X.std(axis=0) + 1e-9
    y_mean = y.mean()
    y_std = y.std() + 1e-9
    Xs = (X - x_mean) / x_std
    ys = (y - y_mean) / y_std

    n_input = Xs.shape[1]

    np.random.seed(0)
    # Inisialisasi He (skala sesuai jumlah neuron masuk).
    W1 = np.random.randn(n_input, hidden) * np.sqrt(2.0 / n_input)
    b1 = np.zeros((1, hidden))
    W2 = np.random.randn(hidden, 1) * np.sqrt(2.0 / hidden)
    b2 = np.zeros((1, 1))

    for _ in range(iterasi):
        # Forward
        z1 = Xs @ W1 + b1
        a1 = np.maximum(0, z1)  # ReLU
        z2 = a1 @ W2 + b2

        # Backprop (gradient rata-rata)
        dz2 = z2 - ys
        dW2 = a1.T @ dz2 / len(Xs)
        db2 = dz2.mean(axis=0, keepdims=True)
        dz1 = dz2 @ W2.T
        dz1[z1 <= 0] = 0
        dW1 = Xs.T @ dz1 / len(Xs)
        db1 = dz1.mean(axis=0, keepdims=True)

        # Update (gradient descent)
        W1 -= laju * dW1
        b1 -= laju * db1
        W2 -= laju * dW2
        b2 -= laju * db2

    return {
        "W1": W1.tolist(), "b1": b1.tolist(),
        "W2": W2.tolist(), "b2": b2.tolist(),
        "x_mean": x_mean.tolist(), "x_std": x_std.tolist(),
        "y_mean": y_mean.tolist(), "y_std": y_std.tolist(),
    }


def ramal(model, X):
    """Prediksi dari model yang dilatih `jaring_syaraf` (forward pass)."""
    X = np.array(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(1, -1)
    W1 = np.array(model["W1"])
    b1 = np.array(model["b1"])
    W2 = np.array(model["W2"])
    b2 = np.array(model["b2"])
    x_mean = np.array(model["x_mean"])
    x_std = np.array(model["x_std"])
    y_mean = model["y_mean"]
    y_std = model["y_std"]

    Xs = (X - x_mean) / x_std
    z1 = Xs @ W1 + b1
    a1 = np.maximum(0, z1)  # ReLU
    z2 = a1 @ W2 + b2
    hasil = z2 * y_std + y_mean  # skala balik ke satuan asli
    return [round(float(v), 4) for v in hasil.reshape(-1)]

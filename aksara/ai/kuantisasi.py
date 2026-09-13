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

"""Quantisasi int8 untuk bobot model — fondasi hemat eksekusi (Step B).

Prinsip: bobot pecahan (float32, 4 byte) disimpan sebagai integer int8
(1 byte) + skala tiap baris. Saat jalan: int8 -> float32 cepat (keras).
Ukuran file turun ~4x, RAM saat inference juga hemat.

Dipakai oleh Mini LM v2 untuk mengubah model float ke format hemat.
"""

import numpy as np


def kuantisasi_arr(arr):
    """Quantisasi satu array 2D ke int8 + skala per baris.

    Kembalikan (int8, skala) untuk tiap baris. skala = 1D float.
    """
    arr = np.array(arr, dtype=np.float32)
    if arr.ndim != 2:
        raise ValueError("kuantisasi_arr: array harus 2D.")
    amax = np.max(np.abs(arr), axis=1, keepdims=True)
    amax[amax < 1e-12] = 1e-12
    skala = amax / 127.0
    int8 = np.clip(np.round(arr / skala), -127, 127).astype(np.int8)
    return int8, skala.reshape(-1)


def kuantisasi_vektor(v):
    """Quantisasi vektor 1D: skala satu angka."""
    v = np.array(v, dtype=np.float32)
    amax = float(np.max(np.abs(v))) if v.size else 0.0
    if amax < 1e-12:
        return np.zeros(v.shape, dtype=np.int8), 0.0
    skala = amax / 127.0
    return np.clip(np.round(v / skala), -127, 127).astype(np.int8), float(skala)


def dekuantisasi_arr(int8, skala):
    """Kembalikan float32 dari int8 + skala (untuk cek galat / run)."""
    int8 = np.array(int8, dtype=np.float32)
    skala = np.array(skala, dtype=np.float32).reshape(-1, 1)
    return int8 * skala


def kuantisasi_model(model, kunci_larik=("W", "b")):
    """Kuantisasi seluruh bobot 2D numerik dalam model.

    Bobot 2D -> (int8, skala). Meta (string/int skalar) dibiarkan asli.
    """
    hasil = {}
    for k, v in model.items():
        try:
            arr = np.asarray(v, dtype=np.float32)
        except (ValueError, TypeError):
            hasil[k] = v
            continue
        if arr.ndim == 2 and arr.size > 0:
            i8, s = kuantisasi_arr(arr)
            hasil[k] = {"int8": i8, "skala": s, "bentuk": list(arr.shape)}
        else:
            # vektor (bias, embedding dlm?) — coba kuantisasi bila numerik float
            if arr.size and "Wte" in k and arr.ndim == 2:
                i8, s = kuantisasi_arr(arr)
                hasil[k] = {"int8": i8, "skala": s, "bentuk": list(arr.shape)}
            else:
                hasil[k] = v
    return hasil


def dekuantisasi_model(model_q):
    """Balik model terkuantisasi ke float32 (untuk verifikasi/performa)."""
    hasil = {}
    for k, v in model_q.items():
        if isinstance(v, dict) and "int8" in v:
            hasil[k] = dekuantisasi_arr(v["int8"], v["skala"])
        else:
            hasil[k] = v
    return hasil


def ukuran_mb(model, quant=False):
    """Estimasi ukuran model dalam MB (raw float vs int8+skala)."""
    total = 0
    for k, v in model.items():
        if isinstance(v, dict) and "int8" in v:
            total += v["int8"].nbytes + v["skala"].nbytes
        else:
            arr = np.asarray(v)
            total += arr.nbytes
    return total / (1024 * 1024)


def galat_relatif(asli, model_q):
    """Galat rerata relatif bobot asli vs dequantisasi (persen)."""
    tot = 0.0
    n = 0
    for k, v in asli.items():
        try:
            arr = np.asarray(v, dtype=np.float32)
        except (ValueError, TypeError):
            continue
        if k in model_q and isinstance(model_q[k], dict):
            dq = dekuantisasi_arr(model_q[k]["int8"], model_q[k]["skala"])
            if arr.ndim == 2 and dq.shape == arr.shape:
                tot += float(np.mean(np.abs(dq - arr) / (np.abs(arr) + 1e-9)))
                n += 1
    return (tot / n * 100.0) if n else 0.0
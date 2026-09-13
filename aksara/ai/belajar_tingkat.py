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

"""Pembelajaran mendalam: retrain ulang mini-LM dari fakta belajar.

Fakta "topik=jawaban" dari file belajar diubah jadi kalimat korpus,
digabung dengan korpus dasar, lalu pipeline/featurize ulang. Tujuannya
biar model bahasa (bukan cuma lookup) ikut memahami pola barunya.

Hemat: latih hanya beberapa iterasi di atas korpus kecil + delta.
"""

import os

import numpy as np


def baca_fakta(jalan):
    """Baca file 'topik=jawaban' -> daftar (topik, jawaban)."""
    if not os.path.exists(jalan):
        return []
    hasil = []
    for baris in open(jalan, encoding="utf-8", errors="ignore"):
        baris = baris.strip()
        if not baris:
            continue
        if "=" in baris:
            t, _, j = baris.partition("=")
            hasil.append((t.strip(), j.strip()))
    return hasil


def korpus_dari_fakta(fakta):
    """Ubah fakta jadi kalimat korpus agar bisa dilatih LM."""
    kal = []
    for t, j in fakta:
        kal.append(f"{t} itu {j}.")
        kal.append(f"apa itu {t}? jawabannya {j}.")
    return " ".join(kal)


def gabung_korpus(dasar, fakta):
    """Gabung korpus dasar + kalimat fakta (delta)."""
    return dasar + " " + korpus_dari_fakta(fakta)


def retrain_pipeline(korpus, fakta, fungsi_latih, iterasi_ekstra=60):
    """Latih ulang pipeline dengan korpus yang diperkaya fakta.

    fungsi_latih(korpus, ...) -> pipeline (dict). Model yang sama.
    Kembalikan pipeline baru + statistik.
    """
    korpus_baru = gabung_korpus(korpus, fakta)
    pipe = fungsi_latih(korpus_baru)
    return pipe, {"korpus_char": len(korpus_baru), "fakta": len(fakta)}
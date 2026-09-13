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

"""Pipeline Mini LM v2 — BPE + Mini LM + int8 + MoE dalam satu jalur.

End-to-end dari korpus teks -> tokenizer -> model -> (opsional) kompresi
int8 -> teks baru. Semua bobot dilatih dari nol, numpy murni, siap HP.

Alur:
  korpus -> bpe.latih -> model_kecil.latih_teks -> kuantisasi -> tulis
"""

import os

import numpy as np

from . import tokenizer_bpe as bpe
from . import kuantisasi as kq
from .model_kecil import latih_teks as _latih_lm
from .model_kecil import tulis as _tulis
from . import kosakata_kompak as kompak


_JUARA = os.path.join(os.path.dirname(__file__), "..", "data", "vocab_kosakata.akv")


def muat_kosakata(jalan=None):
    """Muat vocab kosakata terkompres (.akv) -> model BPE siap tokenisasi."""
    jalan = jalan or os.path.join(os.path.dirname(__file__), "..", "data",
                                  "vocab_kosakata.akv")
    with open(jalan, "rb") as f:
        return kompak.dekompres_vocab(f.read())


def tokenkan_kosakata(model_bpe, teks):
    """Teks -> id token memakai vocab kosakata terkaya."""
    peta = bpe._buat_peta(model_bpe)
    return bpe.ubah_ke_id(model_bpe, teks, peta=peta)


def balik_kosakata(model_bpe, ids):
    """Id token -> teks (memakai vocab kosakata)."""
    return bpe.ubah_ke_teks(model_bpe, ids)


def latih_pipeline(korpus, ukuran_vokab=300, blok=32, tersembunyi=48,
                   kepala=2, lapisan=1, iterasi=200, laju=0.01,
                   benih=0, quant=False):
    """Latih tokenizer + LM (opsional : quantisasi int8).

    Kembalikan kamus berisi: tokenizer (bpe), model (LM), info ukuran.
    Bila quant=True, bobot LM dikompres int8 (lebih ringan, galat kecil).
    """
    tok = bpe.latih(korpus, ukuran_vokab=ukuran_vokab)
    model_lm = _latih_lm(korpus, blok=blok, tersembunyi=tersembunyi,
                         kepala=kepala, lapisan=lapisan, iterasi=iterasi,
                         laju=laju, benih=benih, kata=True)
    info = {
        "tokenizer": bpe.info(tok),
        "ukuran_float_mb": kq.ukuran_mb(model_lm),
    }
    if quant:
        model_out = kq.kuantisasi_model(model_lm)
        info["ukuran_int8_mb"] = kq.ukuran_mb(model_out)
    else:
        model_out = model_lm

    return {
        "tokenizer": tok,
        "model": model_out,
        "quant": bool(quant),
        "info": info,
    }


def ucap(pipeline, awal="", panjang=16, suhu=0.8, benih=0):
    """Hasilkan teks memakai pipeline (otomatis dequant jika int8)."""
    model = pipeline["model"]
    if pipeline.get("quant"):
        model = kq.dekuantisasi_model(model)
    return _tulis(model, awal=awal, panjang=panjang, suhu=suhu, benih=benih)


def tokenkan(pipeline, teks):
    """Teks -> id token (pakai tokenizer pipeline)."""
    return bpe.ubah_ke_id(pipeline["tokenizer"], teks)


def laporan(pipeline):
    """Ringkasan terukur untuk laporan project."""
    inf = pipeline["info"]
    baris = []
    baris.append(f"Tokenizer : {inf['tokenizer']['ukuran_vokab']} vocab "
                 f"({inf['tokenizer']['jumlah_penggabungan']} gabungan)")
    baris.append(f"Model     : float {inf['ukuran_float_mb']:.4f} MB")
    if "ukuran_int8_mb" in inf:
        rasio = 1 - inf["ukuran_int8_mb"] / inf["ukuran_float_mb"]
        baris.append(f"           int8   {inf['ukuran_int8_mb']:.4f} MB "
                     f"(hemat {rasio * 100:.1f}%)")
        baris.append(f"           quant  : {'YA' if pipeline['quant'] else 'tidak'}")
    return "\n".join(baris)
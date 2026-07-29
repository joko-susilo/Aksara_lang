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


import importlib
from aksara.ai.prediksi import tebak
from aksara.ai.nlp import ringkas
from aksara.ai.clustering import kelompok
from aksara.ai.frekuensi import frekuensi
from aksara.ai.normalisasi import normalisasi
from aksara.ai.korelasi import korelasi
from aksara.ai.cari_mirip import cari_mirip
from aksara.ai.rekomendasi import rekomendasi
from aksara.ai.encode import encode
from aksara.ai.acak_cerdas import acak_cerdas
from aksara.ai.deteksi_bahasa import deteksi_bahasa
from aksara.ai.periksa_ejaan import periksa_ejaan
from aksara.ai.auto_label import auto_label
from aksara.ai.urutkan_ai import urutkan_ai
from aksara.ai.cluster_teks import cluster_teks
from aksara.ai.ubah_gaya import ubah_gaya
from aksara.ai.ekstrak_entitas import ekstrak_entitas
from aksara.ai.simulasi_keputusan import simulasi_keputusan
from aksara.ai.rangking_tfidf import rangking_tfidf
from aksara.ai.pca import pca
from aksara.ai.jaring_syaraf import jaring_syaraf
from aksara.ai.klasifikasi import jenis
def aksara_cetak(*args):
    """Fungsi cetak bawaan (versi fungsi, bukan statement)."""
    print(*args)

def aksara_panjang(obj):
    return len(obj)

def aksara_masukan(prompt=""):
    return input(prompt)

def aksara_bulat(x):
    return int(x)

def aksara_desimal(x):
    return float(x)

def aksara_teks(x):
    return str(x)

def aksara_daftar(*args):
    return list(args)

def aksara_impor(nama_modul, alias, env):
    """Menangani statement impor. Memuat modul Python dan menyimpannya di environment."""
    modul = importlib.import_module(nama_modul)
    env.define(alias, modul)
    return modul
# ==========================================
# FUNGSI BAWAAN KAMUS
# ==========================================

def aksara_kunci(kamus):
    """Mengembalikan daftar kunci"""
    return list(kamus.keys())

def aksara_nilai(kamus):
    """Mengembalikan daftar nilai"""
    return list(kamus.values())

def aksara_isi(kamus):
    """Mengembalikan daftar pasangan [kunci, nilai]"""
    return [[k, v] for k, v in kamus.items()]

def aksara_ada(kamus, kunci):
    """Mengecek apakah kunci ada"""
    return kunci in kamus

def aksara_kosong(kamus):
    """Mengecek apakah kamus kosong"""
    return len(kamus) == 0

def aksara_hapus(kamus, kunci):
    """Menghapus kunci dari kamus"""
    if kunci in kamus:
        del kamus[kunci]
    return kamus

def aksara_tambah(kamus, kunci, nilai):
    """Menambah pasangan ke kamus"""
    kamus[kunci] = nilai
    return kamus

def aksara_gabung(kamus1, kamus2):
    """Menggabung dua kamus"""
    hasil = kamus1.copy()
    hasil.update(kamus2)
    return hasil

def aksara_salin(kamus):
    """Membuat salinan kamus"""
    return kamus.copy()

def aksara_bersihkan(kamus):
    """Mengosongkan kamus"""
    kamus.clear()
    return kamus

def aksara_dapatkan(kamus, kunci, default=None):
    """Mendapatkan nilai dengan default"""
    return kamus.get(kunci, default)

def aksara_tukar(kamus):
    """Menukar kunci dan nilai"""
    return {v: k for k, v in kamus.items()}
# Semua fungsi bawaan yang bisa langsung dipanggil tanpa impor
BUILTINS = {
    "cetak": aksara_cetak,
    "panjang": aksara_panjang,
    "masukan": aksara_masukan,
    "bulat": aksara_bulat,
    "desimal": aksara_desimal,
    "teks": aksara_teks,
    "daftar": aksara_daftar,
       # Kamus
    "kunci": aksara_kunci,
    "nilai": aksara_nilai,
    "isi": aksara_isi,
    "ada": aksara_ada,
    "kosong": aksara_kosong,
    "hapus": aksara_hapus,
    "tambah": aksara_tambah,
    "gabung": aksara_gabung,
    "salin": aksara_salin,
    "bersihkan": aksara_bersihkan,
    "dapatkan": aksara_dapatkan,
    "tukar": aksara_tukar,
    "tebak": tebak,
    "ringkas": ringkas,
    "kelompok": kelompok,
    "frekuensi": frekuensi,
    "normalisasi": normalisasi,
    "korelasi": korelasi,
    "cari_mirip": cari_mirip,
    "rekomendasi": rekomendasi,
    "encode": encode,
    "acak_cerdas": acak_cerdas,
    "deteksi_bahasa": deteksi_bahasa,
    "periksa_ejaan": periksa_ejaan,
    "auto_label": auto_label,
    "urutkan_ai": urutkan_ai,
    "cluster_teks": cluster_teks,
    "ubah_gaya": ubah_gaya,
    "ekstrak_entitas": ekstrak_entitas,
    "simulasi_keputusan": simulasi_keputusan,
    "rangking_tfidf": rangking_tfidf,
    "pca": pca,
    "jaring_syaraf": jaring_syaraf,
    "jenis":jenis,
    
}

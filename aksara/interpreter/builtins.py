import importlib
from aksara.ai.prediksi import tebak

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
}

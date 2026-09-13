# ==========================================
# PARALEL - Pustaka Standar Aksara: eksekusi tugas paralel
# ==========================================
# Tugas = daftar perintah (list-of-list). Subprocess paralel (GIL tak batasi).
# Balik daftar kamus {kode, keluar, kesalahan} per tugas.

impor "aksara._ffi.sistem" sbg S

fun jalan_paralel(tugas, concurrency = 3, cwd = "") {
    balik S.jalan_paralel(tugas, concurrency, cwd)
}

fun jalan_berapa(tugas, concurrency = 3) {
    hasil = S.jalan_paralel(tugas, concurrency)
    oke = 0
    untuk h dalam hasil {
        jika h["kode"] == 0 { oke = oke + 1 }
    }
    balik oke
}
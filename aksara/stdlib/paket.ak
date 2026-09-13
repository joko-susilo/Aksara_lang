# ==========================================
# PAKET - Pustaka Standar Aksara: pasang modul lokal
# ==========================================
# Pasang file .ak eksternal ke stdlib Aksara; daftar/deteksi modul.
# Backend fs: _ffi/sistem.py

impor "aksara._ffi.sistem" sbg S
impor "proses.ak" sbg P
impor "teks.ak" sbg teks

JALUR_STDLIB = "aksara/stdlib/"

fun pasang(jalan_file, nama_modul = "") {
    jika nama_modul == "" {
        # ambil segmen terakhir dari jalan
        segmen = teks.pisahkan(jalan_file, "/")
        nama_modul = segmen[panjang(segmen) - 1]
    }
    jika bukan teks.akhiran(nama_modul, ".ak") {
        nama_modul = nama_modul + ".ak"
    }
    tujuan = JALUR_STDLIB + nama_modul
    S.salin_file(jalan_file, tujuan)
    balik "terpasang: " + tujuan
}

fun daftar(akhiran = ".ak") {
    balik S.daftar_dir(JALUR_STDLIB, akhiran)
}

fun ada(nama_modul) {
    nama = nama_modul
    jika bukan teks.akhiran(nama, ".ak") { nama = nama + ".ak" }
    balik S.jalur_ada(JALUR_STDLIB + nama)
}
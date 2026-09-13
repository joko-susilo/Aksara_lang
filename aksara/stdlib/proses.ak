# ==========================================
# PROSES - Pustaka Standar Aksara: Subprocess & Lingkungan
# ==========================================
# Jalankan perintah eksternal, baca env, argumen CLI. Backend: _ffi/sistem.py
# Logika di Aksara; mesin di Python (sesuai filosofi backend).

impor "aksara._ffi.sistem" sbg S

fun jalankan(perintah, cwd = "", timelimit = 60) {
    balik S.jalankan(perintah, cwd, timelimit)
}

fun jalankan_teks(perintah, cwd = "", timelimit = 60) {
    hasil = S.jalankan(perintah, cwd, timelimit)
    balik hasil["keluar"].strip()
}

fun lingkungan() {
    balik S.lingkungan()
}

fun env_ambil(nama, bawa_default = "") {
    balik S.env_ambil(nama, bawa_default)
}

fun env_setel(nama, nilai) {
    balik S.env_setel(nama, teks(nilai))
}

fun argumen_cli() {
    balik S.argumen_cli()
}

fun glob(pola) {
    balik S.glob_list(pola)
}
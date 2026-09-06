# ==========================================
# BERKAS - Pustaka Standar Aksara: Berkas (File I/O)
# ==========================================

impor "builtins" sbg b
impor "os" sbg os

fun baca_file(jalan) {
    f = b.open(jalan)
    isi = f.read()
    f.close()
    balik isi
}

fun baca_baris(jalan) {
    isi = baca_file(jalan)
    balik isi.split("\n")
}

fun tulis_file(jalan, isi) {
    f = b.open(jalan, "w")
    f.write(isi)
    f.close()
}

fun tambah_ke_file(jalan, isi) {
    f = b.open(jalan, "a")
    f.write(isi)
    f.close()
}

fun apakah_ada(jalan) {
    balik os.path.exists(jalan)
}

fun hapus_file(jalan) {
    jika os.path.exists(jalan) {
        os.remove(jalan)
        balik benar
    }
    balik salah
}

fun ukuran_file(jalan) {
    balik os.path.getsize(jalan)
}

fun folder_sekarang() {
    balik os.getcwd()
}

fun daftar_folder(jalan) {
    balik os.listdir(jalan)
}

fun wujud_folder(jalan) {
    balik os.path.isdir(jalan)
}
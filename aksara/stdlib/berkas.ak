# ==========================================
# BERKAS - Pustaka Standar Aksara: Berkas (File I/O)
# ==========================================

impor "builtins" sbg b
impor "os" sbg os
impor "json" sbg jmod

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

fun buat_folder(jalan) {
    jika bukan os.path.exists(jalan) {
        os.makedirs(jalan)
    }
}

fun tulis_json(jalan, data) {
    f = b.open(jalan, "w")
    jmod.dump(data, f, indent=1)
    f.close()
}

fun muat_json(jalan) {
    f = b.open(jalan, "r")
    d = jmod.load(f)
    f.close()
    balik d
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
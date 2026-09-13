# ==========================================
# REGEX - Pustaka Standar Aksara: Ekspresi Reguler penuh
# ==========================================

impor "aksara._ffi.sistem" sbg S

# cari satu -> [] atau [{"mulai","akhir","cocok","kelompok"}]
fun cari(pola, teks) {
    balik S.regex_cari(pola, teks)
}

fun sema_co(pola, teks) {
    balik S.regex_semua(pola, teks)
}

fun ada(pola, teks) {
    hasil = S.regex_cari(pola, teks)
    balik panjang(hasil) > 0
}

fun ganti(pola, pengganti, teks) {
    balik S.regex_ganti(pola, pengganti, teks)
}

fun pisah(pola, teks) {
    balik S.regex_pisah(pola, teks)
}
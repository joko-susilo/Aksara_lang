# ==========================================
# WAKTU - Pustaka Standar Aksara: Waktu & Tanggal
# ==========================================

impor "time" sbg tm

fun detik_sekarang() {
    balik tm.time()
}

fun waktu_teks() {
    balik tm.strftime("%Y-%m-%d %H:%M:%S")
}

fun waktu_teks_kustom(pola) {
    balik tm.strftime(pola)
}

fun waktu_teks_lokal(detik) {
    balik tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime(detik))
}

fun tahun() {
    balik tm.localtime().tm_year
}

fun bulan() {
    balik tm.localtime().tm_mon
}

fun hari() {
    balik tm.localtime().tm_mday
}

fun jam() {
    balik tm.localtime().tm_hour
}

fun menit() {
    balik tm.localtime().tm_min
}

fun detik() {
    balik tm.localtime().tm_sec
}

fun tidur(detik) {
    tm.sleep(detik)
}
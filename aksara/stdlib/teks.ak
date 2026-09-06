# ==========================================
# TEKS - Pustaka Standar Aksara: String & Teks
# ==========================================

fun huruf_besar(s) {
    balik s.upper()
}

fun huruf_kecil(s) {
    balik s.lower()
}

fun potong_teks(s) {
    balik s.strip()
}

fun potong_teks_kiri(s) {
    balik s.lstrip()
}

fun potong_teks_kanan(s) {
    balik s.rstrip()
}

fun pisahkan(s, pemisah) {
    balik s.split(pemisah)
}

fun gabungkan(daftar, pemisah) {
    balik pemisah.join(daftar)
}

fun ganti(s, lama, baru) {
    balik s.replace(lama, baru)
}

fun mengandung(s, kata) {
    balik s.find(kata) >= 0
}

fun awalan(s, kata) {
    balik s.startswith(kata)
}

fun akhiran(s, kata) {
    balik s.endswith(kata)
}

fun balik_teks(s) {
    hasil = ""
    untuk c dalam s {
        hasil = c + hasil
    }
    balik hasil
}

fun cari(s, kata) {
    balik s.find(kata)
}

fun jumlah_kata(s) {
    balik panjang(pisahkan(s, " "))
}

fun judul(s) {
    balik s.title()
}

fun cek_kosong(s) {
    balik panjang(s) == 0
}

fun ulang_teks(s, n) {
    balik s * n
}

fun sub_teks(s, mulai, akhir) {
    balik s[mulai..akhir]
}
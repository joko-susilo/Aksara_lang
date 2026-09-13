# ==========================================
# HITUNG - Pustaka Standar Aksara: penalaran aritmetika (nol penyimpanan)
# ==========================================

impor "aksara.ai.hitung" sbg h

fun hitung(teks) {
    # balikan [hasil, kalimat] bila terdeteksi; nil bila bukan operasi
    r = h.hitung(teks)
    jika r == nil {
        balik nil
    }
    hasil = r[0]
    jika hasil == nil {
        balik nil
    }
    balik [hasil, r[1]]
}

# fungsi lanjutan (dipanggil dari pintar.ak)
fun persen(teks) {
    balik h.persen(teks)
}

fun rata_rata(teks) {
    balik h.rata_rata(teks)
}

fun konversi_unit(teks) {
    balik h.konversi_unit(teks)
}
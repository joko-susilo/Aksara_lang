# ==========================================
# BAHASA_ID - Pustaka Standar Aksara: parameter tata bahasa Indonesia
# ==========================================

impor "aksara.ai.bahasa_id" sbg bid

fun stem_afiks(kata) {
    # balik daftar kandidat akar (kata terstem)
    balik bid.stem_afiks(kata)
}

fun kata_tanya(teks) {
    balik bid.adalah_kalimat_tanya(teks)
}

fun kata_negasi(teks) {
    balik bid.adalah_negasi(teks)
}

fun normalisasi(teks) {
    balik bid.normalisasi_santai(teks)
}
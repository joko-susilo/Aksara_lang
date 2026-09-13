# ==========================================
# INFERENSI - Pustaka Standar Aksara: menjawab dengan menghubungkan fakta
# ==========================================

impor "aksara.ai.inferensi" sbg inf

fun cari(jalan, pertanyaan, kedalaman = 2) {
    balik inf.inferensi(jalan, pertanyaan, kedalaman)
}
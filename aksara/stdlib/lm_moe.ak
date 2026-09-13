# ==========================================
# LM_MOE - Pustaka Standar Aksara: Language Model + Mixture of Experts
# ==========================================
# FFN diganti pakar MoE (top-1 per token). Kapasitas naik, beban ringan.

impor "aksara.ai.lm_moe" sbg lm

fun latih(teks, pakar = 4, tersembunyi = 48, blok = 20, iterasi = 300,
          laju = 0.02, benih = 0) {
    balik lm.latih(teks, pakar, tersembunyi, blok, iterasi, laju, benih)
}

fun tulis(model, awal = "", panjang = 60, suhu = 0.8, benih = 0) {
    balik lm.tulis(model, awal, panjang, suhu, benih)
}

fun info(model) {
    balik lm.info(model)
}
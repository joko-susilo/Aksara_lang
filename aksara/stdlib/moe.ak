# ==========================================
# MOE - Pustaka Standar Aksara: Mixture of Experts (Step C)
# ==========================================
# Kapasitas naik, beban turun: tiap token hanya aktifkan top-k pakar.

impor "aksara.ai.moe" sbg moe

fun latih_moe(X, Y, n_pakar = 4, k = 1, d = 16, iterasi = 300, laju = 0.05, benih = 0) {
    balik moe.latih_moe(X, Y, n_pakar, k, d, iterasi, laju, benih)
}

fun ramal_moe(model, X) {
    balik moe.ramal_moe(model, X)
}

fun info_moe(model) {
    balik moe.info_moe(model)
}
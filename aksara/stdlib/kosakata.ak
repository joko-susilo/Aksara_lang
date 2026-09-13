# ==========================================
# KOSAKATA - Pustaka Standar Aksara: Kosakata Bahasa Indonesia (kompak)
# ==========================================
# Baca kata -> vocab BPE -> representasi kecil + kompresi. Ukur rasio.

impor "aksara.ai.kosakata" sbg ko

fun baca_kata(jalan) {
    balik ko.baca_kata(jalan)
}

fun buat_vocab(kata, ukuran_vokab = 350) {
    balik ko.buat_vocab(kata, ukuran_vokab)
}

fun simpan_compact(model, kata) {
    balik ko.simpan_compact(model, kata)
}
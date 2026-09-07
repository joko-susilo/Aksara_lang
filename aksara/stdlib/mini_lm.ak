# ==========================================
# MINI_LM - Pustaka Standar Aksara: model bahasa kecil dilatih dari nol
# ==========================================
# Transformer karakter/kata kecil (numpy) — belajar dari teks bahasa
# Indonesia di CPU. Bukan API orang; bobot benar-benar kita latih.

impor "aksara.ai.model_kecil" sbg lm

fun latih_teks(isi, blok = 48, tersembunyi = 32, kepala = 2, lapisan = 1,
               iterasi = 400, laju = 0.01, benih = 0, kata = salah) {
    balik lm.latih_teks(isi, blok, tersembunyi, kepala, lapisan, iterasi, laju, benih, kata)
}

fun tulis(model, awal = "", panjang = 80, suhu = 1.0, benih = 0) {
    balik lm.tulis(model, awal, panjang, suhu, benih)
}
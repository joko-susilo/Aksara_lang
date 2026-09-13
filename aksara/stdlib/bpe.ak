# ==========================================
# BPE - Pustaka Standar Aksara: Tokenizer sub-kata (fondasi kompresi Mini LM v2)
# ==========================================
# Vocab dilatih DARI KORPUS SENDIRI (Bahasa Indonesia), numpy/pure python.
# Tidak bergantung library/tokenizer orang luar.

impor "aksara.ai.tokenizer_bpe" sbg bpe

fun latih(teks, ukuran_vokab = 256) {
    balik bpe.latih(teks, ukuran_vokab)
}

fun ubah_ke_id(model, teks) {
    balik bpe.ubah_ke_id(model, teks)
}

fun ubah_ke_teks(model, ids) {
    balik bpe.ubah_ke_teks(model, ids)
}

fun info(model) {
    balik bpe.info(model)
}
# ==========================================
# MODEL_V4 - Pustaka Standar Aksara: Mini-LM v4 (backprop LENGKAP)
# ==========================================
# v4 = perbaikan tegas v3:
#   - backprop VERIFIKASI gradien-check (attention & FFN benar-benar belajar)
#   - loss trail + perplexity di data uji (bukan buta)
#   - checkpoint + resume (latih lanjut dari simpanan)
# Backend numerik numpy; seluruh pemakaian dari Bahasa Aksara.

impor "aksara.ai.model_v4" sbg mv4
impor "aksara.ai.tokenizer_bpe" sbg tb
impor "berkas.ak" sbg b

fun siap_bpe(korpus, ukuran_vokab = 400) {
    balik tb.latih(korpus, ukuran_vokab)
}

fun ubah_id(model_bpe, teks) {
    peta = tb._buat_peta(model_bpe)
    balik tb.ubah_ke_id(model_bpe, teks, peta)
}

fun balik_teks(model_bpe, ids) {
    balik tb.ubah_ke_teks(model_bpe, ids)
}

# training: balik kamus {bobot, loss_trail, best_loss, perplexity, iterasi_total}
fun latih(ids, d = 96, kepala = 4, lapisan = 2, E = 2, blok = 48,
          iterasi = 500, laju = 0.003, benih = 0, cekpoint = 50,
          jalan_cekpoint = "") {
    balik mv4.latih_v4(ids, d, kepala, lapisan, E, blok, iterasi, laju, benih,
                       nil, cekpoint, jalan_cekpoint)
}

# generate dari seed id
fun tulis(model, ids_awal, panjang = 30, suhu = 0.8, benih = 0) {
    balik mv4.tulis_v4(model, ids_awal, panjang, suhu, benih)
}

fun baca_file_korpus(jalan) {
    balik b.baca_file(jalan)
}

fun tulis_serial(jalan, data) {
    balik mv4.simpan_v4(jalan, data)
}

fun baca_serial(jalan) {
    balik mv4.muat_v4(jalan)
}
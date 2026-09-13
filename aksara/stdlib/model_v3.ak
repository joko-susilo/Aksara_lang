# ==========================================
# MODEL_V3 - Pustaka Standar Aksara: Mini-LM v3 (arsitektur kita)
# ==========================================
# Scaling internal: BPE vocab, hidden besar, multi-head, layer 2-4, FFN-MoE.
# Seluruh pemakaian dari Aksara; logika numeric di backend numpy.

impor "aksara.ai.model_v3" sbg mv3
impor "aksara.ai.tokenizer_bpe" sbg tb
impor "berkas.ak" sbg b

fun siap_bpe(korpus, ukuran_vokab = 400) {
    # balik model_bpe (untuk token id)
    balik tb.latih(korpus, ukuran_vokab)
}

fun ubah_id(model_bpe, teks) {
    peta = tb._buat_peta(model_bpe)
    balik tb.ubah_ke_id(model_bpe, teks, peta)
}

fun balik_teks(model_bpe, ids) {
    balik tb.ubah_ke_teks(model_bpe, ids)
}

fun latih(ids, d = 96, kepala = 4, lapisan = 2, E = 2, blok = 24,
          iterasi = 200, laju = 0.01, benih = 0) {
    balik mv3.latih_v3(ids, d, kepala, lapisan, E, blok, iterasi, laju, benih)
}

fun tulis(model, ids_awal, panjang = 30, suhu = 0.8, benih = 0) {
    balik mv3.tulis_v3(model, ids_awal, panjang, suhu, benih)
}

fun baca_file_korpus(jalan) {
    balik b.baca_file(jalan)
}

fun tulis_serial(jalan, data) {
    # simpan objek besar (model/tokenizer) via pickle backend (numerik)
    balik mv3.simpan(jalan, data)
}

fun baca_serial(jalan) {
    balik mv3.muat(jalan)
}
fun kompres_teks(jalan_src, jalan_dst) {
    balik mv3.kompres_teks(jalan_src, jalan_dst)
}

fun korpus_domain() {
    balik mv3.korpus_domain()
}

fun baca_korpus_lzma(jalan_akxz) {
    balik mv3.baca_korpus_lzma(jalan_akxz)
}

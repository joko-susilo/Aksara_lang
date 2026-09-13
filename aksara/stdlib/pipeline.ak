# ==========================================
# PIPELINE - Pustaka Standar Aksara: Mini LM v2 end-to-end
# ==========================================
# BPE + LM + int8 (opsional) satu jalur. Dari korpus -> model -> teks.

impor "aksara.ai.pipeline_minilm" sbg pl

fun latih(korpus, ukuran_vokab = 300, blok = 32, tersembunyi = 48,
          kepala = 2, lapisan = 1, iterasi = 200, laju = 0.01,
          benih = 0, quant = salah) {
    balik pl.latih_pipeline(korpus, ukuran_vokab, blok, tersembunyi,
                            kepala, lapisan, iterasi, laju, benih, quant)
}

fun ucap(pipeline, awal = "", panjang = 16, suhu = 0.8, benih = 0) {
    balik pl.ucap(pipeline, awal, panjang, suhu, benih)
}

fun tokenkan(pipeline, teks) {
    balik pl.tokenkan(pipeline, teks)
}

fun laporan(pipeline) {
    balik pl.laporan(pipeline)
}
fun muat_kosakata() {
    balik pl.muat_kosakata()
}

fun tokenkan_kosakata(model_bpe, teks) {
    balik pl.tokenkan_kosakata(model_bpe, teks)
}

fun balik_kosakata(model_bpe, ids) {
    balik pl.balik_kosakata(model_bpe, ids)
}

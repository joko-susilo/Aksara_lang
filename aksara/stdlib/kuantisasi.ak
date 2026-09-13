# ==========================================
# KUANTISASI - Pustaka Standar Aksara: int8 compression untuk bobot model
# ==========================================
# Step B Mini LM v2: float32 (4 byte) -> int8 (1 byte) + skala. Hemat ~4x.

impor "aksara.ai.kuantisasi" sbg k

fun kuantisasi(model) {
    balik k.kuantisasi_model(model)
}

fun dekuantisasi(model_q) {
    # kembalikan versi float (untuk verifikasi galat)
    balik k.dekuantisasi_model(model_q)
}

fun ukuran_mb(model) {
    balik k.ukuran_mb(model)
}

fun galat_relatif(model_asli, model_q) {
    balik k.galat_relatif(model_asli, model_q)
}
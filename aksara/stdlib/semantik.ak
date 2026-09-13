# ==========================================
# SEMANTIK - Pustaka Standar Aksara: paham makna (on-the-fly, hemat)
# ==========================================
# Vektor makna dibangun saat dipanggil (bukan disimpan) -> RAM tetap kecil.
# Dipanggil hanya saat cocok persis gagal.

impor "aksara.ai.semantik" sbg sm

fun cocok(kb, pertanyaan, ambang = 0.35, jumlah = 1) {
    # balik [kunci, skor] paling dekat maknanya
    balik sm.cocok_kb(pertanyaan, kb, ambang, jumlah)
}

fun skor(pertanyaan, entri) {
    balik sm.skor_kesamaan(pertanyaan, entri)
}
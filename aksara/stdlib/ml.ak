# ==========================================
# ML - Pustaka Standar Aksara: Machine Learning (AI-first)
# ==========================================
# Memanfaatkan jaringan saraf numpy bawaan Aksara.
# Pemakaian:
#   impor "ml.ak" sbg ml
#   model = ml.latih(X, y)
#   cetak ml.ramal(model, X_baru)

impor "aksara.ai.jaring_syaraf" sbg jaringan

fun latih(X, y, hidden = 8, iterasi = 500, laju = 0.1) {
    balik jaringan.jaring_syaraf(X, y, hidden, iterasi, laju)
}

fun ramal(model, X) {
    balik jaringan.ramal(model, X)
}

fun latih_klasifikasi(X, y, hidden = 8, iterasi = 500, laju = 0.1) {
    balik jaringan.jaring_klasifikasi(X, y, hidden, iterasi, laju)
}

fun ramal_klasifikasi(model, X) {
    balik jaringan.ramal_klasifikasi(model, X)
}
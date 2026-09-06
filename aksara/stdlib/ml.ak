# ==========================================
# ML - Pustaka Standar Aksara: Machine Learning (AI-first)
# ==========================================
# Memanfaatkan jaringan saraf numpy bawaan Aksara.
# Pemakaian:
#   impor "ml.ak" sbg ml
#   model = ml.latih(X, y)
#   cetak ml.ramal(model, X_baru)

impor "aksara.ai.jaring_syaraf" sbg jaringan

fun latih(X, y) {
    balik jaringan.jaring_syaraf(X, y)
}

fun ramal(model, X) {
    balik jaringan.ramal(model, X)
}
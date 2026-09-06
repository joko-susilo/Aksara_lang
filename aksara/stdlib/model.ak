# ==========================================
# MODEL - Pustaka Standar Aksara: Simpan & Muat Model
# ==========================================
# Model hasil ml.latih() / jaring_syaraf() berupa kamus — bisa disimpan
# ke file JSON dan dimuat lagi tanpa melatih ulang.

impor "builtins" sbg b
impor "json" sbg json

fun simpan(model, jalan) {
    f = b.open(jalan, "w")
    f.write(json.dumps(model))
    f.close()
}

fun muat(jalan) {
    f = b.open(jalan)
    isi = f.read()
    f.close()
    balik json.loads(isi)
}
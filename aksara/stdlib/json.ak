# ==========================================
# JSON - Pustaka Standar Aksara: JSON
# ==========================================

impor "json" sbg json

fun urai(teks) {
    balik json.loads(teks)
}

fun ubah(data) {
    balik json.dumps(data)
}

fun ubah_indah(data) {
    balik json.dumps(data, indent = 2)
}
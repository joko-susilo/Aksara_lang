# ==========================================
# CONTOH: Integrasi Kosakata 415B -> Pipeline AI Chat
# ==========================================
# Muat vocab 415 byte (1483 kata indo), tokenisasi cepat, tanpa latih ulang.

impor "berkas.ak" sbg f
impor "pipeline.ak" sbg pl

cetak "== Muat kosakata terkompres (415 byte) =="
model_bpe = pl.muat_kosakata()
cetak "Dasar: " + panjang(model_bpe["dasar"]) + " + merges " + panjang(model_bpe["kode"]) + " -> vocab siap"

cetak ""
cetak "== Tokenisasi (pakai kekayaan kosakata) =="
kata = ["bahasa", "indonesia", "pemrograman", "aksara", "kecerdasan", "otomatis"]
untuk i dalam 0 .. panjang(kata) - 1 {
    ids = pl.tokenkan_kosakata(model_bpe, kata[i])
    cetak "  '" + kata[i] + "' -> " + panjang(ids) + " token"
}

cetak ""
cetak "== Cek roundtrip =="
contoh = "bahasa indonesia aksara"
ids = pl.tokenkan_kosakata(model_bpe, contoh)
cetak "Input : " + contoh
cetak "IDs   : " + ids
cetak "Decode: " + pl.balik_kosakata(model_bpe, ids)
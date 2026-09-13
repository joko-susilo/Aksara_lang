# ==========================================
# CONTOH: Kosakata Bahasa Indonesia dikompres (sekecil mungkin)
# ==========================================
# 1) Baca 1336 kata 2) vocab BPE 3) simpan compact+zlib 4) ukur rasio.

impor "kosakata.ak" sbg ko

cetak "== Baca kosakata =="
kata = ko.baca_kata("examples/ai_live/korpus/kosakata_id.txt")
cetak "Jumlah kata: " + panjang(kata)

cetak ""
cetak "== Buat vocab BPE =="
model = ko.buat_vocab(kata, 350)

cetak ""
cetak "== Simpan kompak + kompresi =="
hasil = ko.simpan_compact(model, kata)
# ukuran teks asli (gabungkan)
teks_total = 0
untuk w dalam kata {
    teks_total = teks_total + panjang(w) + 1
}
cetak "Teks asli (kata): " + teks_total + " bytes"
cetak "Compact (BPE) : " + hasil[0] + " bytes"
cetak "Zlib (level 9): " + hasil[1] + " bytes"
cetak "Rasio vs teks : ~" + ((hasil[1] / teks_total) * 100) + "%"
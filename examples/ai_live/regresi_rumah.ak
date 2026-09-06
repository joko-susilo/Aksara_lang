# ============================================
# PORTOFOLIO DEMO 1 - Regresi: estimasi harga rumah
# ============================================
# Belajar dari data (luas m2 -> harga juta Rupiah), simpan model,
# muat kembali, lalu ramal luas baru. Semua deterministik (tanpa jaringan).

impor "ml.ak" sbg ml
impor "model.ak" sbg mo
impor "data.ak" sbg d

# Dataset latih (harga ~ luas * 1.5 juta)
X = [[30], [40], [50], [60], [70], [80], [90], [100]]
y = [45, 60, 75, 90, 105, 120, 135, 150]

cetak "== Latih jaringan saraf (8 data) =="
model = ml.latih(X, y, 8, 1000, 0.1)

latih_in = ml.ramal(model, X)
cetak "Galat rata-rata di data latih: " + d.galat_rata(y, latih_in)

# Simpan model ke file, muat ulang
cetak ""
cetak "== Simpan & muat model =="
jalan = "/tmp/opencode/portofolio/model_rumah.aksm"
mo.simpan(model, jalan)
model2 = mo.muat(jalan)

cetak ""
cetak "== Prediksi luas baru =="
luas_baru = [[95], [110], [150]]
harga = ml.ramal(model2, luas_baru)
untuk i dalam 0 .. panjang(luas_baru) - 1 {
    cetak "Luas " + luas_baru[i][0] + " m2 -> sekitar " + bulat(harga[i]) + " juta"
}
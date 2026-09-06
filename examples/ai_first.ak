# Demo AI-first: latih jaringan saraf, prediksi, dan ukur akurasi.
impor "ml.ak" sbg ml
impor "data.ak" sbg d

cetak "== Regresi: jam belajar -> skor =="
X = [[1], [2], [3], [4], [5], [6], [7], [8]]
y = [10, 20, 30, 40, 50, 60, 70, 80]

model = ml.latih(X, y)
pred = ml.ramal(model, X)
cetak "prediksi (data latih):"
cetak pred
cetak "galat rata-rata: " + d.galat_rata(y, pred)
cetak "prediksi 9 jam & 10 jam:"
cetak ml.ramal(model, [[9], [10]])

cetak ""
cetak "== Klasifikasi: benar/salah =="
nyata = [0, 0, 1, 1, 1, 0, 1]
hasil = [0, 1, 1, 1, 0, 0, 1]
cetak "akurasi: " + d.akurasi(nyata, hasil)

cetak ""
cetak "== Bagi data latih/uji =="
b = d.bagi([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.7)
cetak "latih: " + b[0]
cetak "uji:   " + b[1]
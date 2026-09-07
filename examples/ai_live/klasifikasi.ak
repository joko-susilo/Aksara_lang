# ============================================
# PORTOFOLIO DEMO 5 - Klasifikasi dengan jaringan saraf sendiri
# ============================================
# Model kita sendiri: 1 hidden layer, softmax + cross-entropy (numpy).
# Data: ukuran (x1, x2) -> 3 kategori (S, M, L).

impor "ml.ak" sbg ml
impor "data.ak" sbg d

# (ukuran_lebar, ukuran_tinggi) -> kelas: 0 kecil, 1 sedang, 2 besar
X = [
    [1, 1], [1, 2], [2, 1], [2, 2],
    [8, 1], [9, 1], [8, 2], [9, 2],
    [8, 8], [9, 8], [8, 9], [9, 9],
]
y = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2]

cetak "== Latih jaringan saraf klasifikasi (12 data, 3 kelas) =="
model = ml.latih_klasifikasi(X, y, 10, 1500, 0.3)

pred = ml.ramal_klasifikasi(model, X)
cetak "Prediksi data latih: " + pred

# Akurasi (bandingkan label)
cocok = 0
untuk i dalam 0 .. panjang(y) - 1 {
    jika pred[i] == y[i] { cocok = cocok + 1 }
}
cetak "Akurasi data latih: " + (cocok / panjang(y)) * 100 + "% (" + cocok + "/" + panjang(y) + ")"

cetak ""
cetak "== Prediksi data baru =="
baru = [[1.7, 1.4], [8.1, 9.2], [9.9, 1.1]]
nama = ["kecil", "sedang", "besar"]
h = ml.ramal_klasifikasi(model, baru)
untuk i dalam 0 .. panjang(baru) - 1 {
    cetak "ukuran " + baru[i][0] + "x" + baru[i][1] + " -> kategori " + nama[h[i]]
}
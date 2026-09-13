# ==========================================
# UJI MODEL_AK — forward murni Aksara
# ==========================================
# Bangun bobot kecil langsung di Aksara, jalankan forward, cek bentuk output.

impor "numpy" sbg np
impor "model_ak.ak" sbg MK

# vocab kecil: 10 token, d=8
v = 10
d = 8
cetak "== Bangun model kecil (semua murni Aksara) =="

# bobot inisialisasi kecil (di Aksara: np.random)
np.random.seed(0)
model = [
    "Wte": np.random.randn(v, d) * 0.02,
    "Wpe": np.random.randn(8, d) * 0.02,
    "Wq": np.random.randn(d, d) * 0.02,
    "Wk": np.random.randn(d, d) * 0.02,
    "Wv": np.random.randn(d, d) * 0.02,
    "Wo": np.random.randn(d, d) * 0.02,
    "W1": np.random.randn(d, 4*d) * 0.02,
    "b1": np.zeros(4*d),
    "W2": np.random.randn(4*d, d) * 0.02,
    "b2": np.zeros(d),
    "ln1g": np.ones(d), "ln1b": np.zeros(d),
    "ln2g": np.ones(d), "ln2b": np.zeros(d),
    "Wlr": np.random.randn(d, v) * 0.02,
    "blr": np.zeros(v),
]
cetak "model siap (d=" + d + ", vocab=" + v + ")"

# ids input
ids = [1, 3, 5, 2]
cetak "ids input: " + ids

cetak ""
cetak "== Forward (murni Aksara) =="
logits = MK.uji_forward(model, ids, 4)
cetak "logits[0] slice 0..3: " + logits[0][0..3]
cetak "jumlah baris logits: " + panjang(logits)
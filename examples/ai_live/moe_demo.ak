# ==========================================
# CONTOH: MoE ringan — Mini LM v2 (Step C)
# ==========================================
# 4 pakar, top-1 aktif per token. Ukur: kesalahan prediksi + info param.

impor "moe.ak" sbg moe

# data: luas (m2) ukuran contoh berbentuk 2 fitur
X = [[30, 1], [40, 1], [50, 1], [60, 1], [70, 1], [80, 1], [90, 1], [100, 1]]
y = [45, 60, 75, 90, 105, 120, 135, 150]

cetak "== Latih MoE (4 pakar, top-1) =="
model = moe.latih_moe(X, y, 4, 1, 16, 800, 0.05, 0)
info = moe.info_moe(model)
cetak "Pakar:            " + info["n_pakar"]
cetak "Top-k aktif:      " + info["top_k"]
cetak "Parameter eksper: " + info["total_param"]

cetak ""
cetak "== Prediksi MoE =="
ramal = moe.ramal_moe(model, X)
cetak "Prediksi: " + ramal
cetak "Target:   " + y

cetak ""
cetak "== Prediksi data baru =="
cetak "Luas 95  -> " + moe.ramal_moe(model, [[95, 1]])
cetak "Luas 110 -> " + moe.ramal_moe(model, [[110, 1]])
cetak "Luas 150 -> " + moe.ramal_moe(model, [[150, 1]])
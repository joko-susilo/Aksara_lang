# ==========================================
# CONTOH: LM + MoE — terobosan Step C menyatu (efek nyata)
# ==========================================
# 4 pakar, top-1 aktif per token. Model dari nol, nulis kalimat sendiri.

impor "berkas.ak" sbg f
impor "lm_moe.ak" sbg lm

isi = f.baca_file("examples/ai_live/korpus/korpus_minilm.txt")
cetak "Korpus: " + panjang(isi) + " karakter"

cetak "== Latih LM + MoE (4 pakar) =="
model = lm.latih(isi, 4, 48, 20, 400, 0.02, 0)
info = lm.info(model)
cetak "Pakar:      " + info["pakar"]
cetak "Tersembunyi:" + info["tersembunyi"]
cetak "Karakter:   " + info["ukuran_karakter"]

cetak "== Model menulis (awalan dari kita) =="
cetak "[bahasa]   " + lm.tulis(model, "bahasa", 40, 0.6)
cetak "[aksara]   " + lm.tulis(model, "aksara", 40, 0.6)
cetak "[indonesia] " + lm.tulis(model, "indonesia", 40, 0.6)
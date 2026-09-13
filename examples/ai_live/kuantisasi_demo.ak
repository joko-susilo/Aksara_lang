# ==========================================
# CONTOH: Quantisasi int8 — Mini LM v2 (Step B)
# ==========================================
# Latih mini LM, lalu kompres ke int8. Ukur ukuran sebelum/sesudah + galat.

impor "mini_lm.ak" sbg m
impor "kuantisasi.ak" sbg k
impor "berkas.ak" sbg f

isi = f.baca_file("examples/ai_live/korpus.txt")

cetak "== Latih model kecil (dari nol) =="
model = m.latih_teks(isi, blok = 32, tersembunyi = 48, kepala = 2, lapisan = 1,
                     iterasi = 200, laju = 0.01, benih = 0, kata = benar)
cetak "Model float: " + k.ukuran_mb(model) + " MB"

cetak ""
cetak "== Kuantisasi int8 =="
model_q = k.kuantisasi(model)
cetak "Model int8 : " + k.ukuran_mb(model_q) + " MB"

cetak ""
cetak "== Verifikasi output =="
cetak "Model asli menulis: " + m.tulis(model, "aksara", panjang = 15, suhu = 0.1)
cetak "Model int8 menulis : " + m.tulis(k.dekuantisasi(model_q), "aksara", panjang = 15, suhu = 0.1)
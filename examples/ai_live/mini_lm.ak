# ============================================
# PORTOFOLIO DEMO 6 - Mini LM: AI bahasa dilatih sendiri
# ============================================
# Model bahasa kecil (transformer) dilatih dari teks bahasa Indonesia
# di CPU, lalu diajak "menulis" sendiri. Semua bobot kita yang punya.

impor "berkas.ak" sbg f
impor "mini_lm.ak" sbg m

isi = f.baca_file("examples/ai_live/korpus.txt")
cetak "== Latih model bahasa sendiri dari korpus Indonesia =="
cetak "Korpus: " + panjang(isi) + " karakter"

model = m.latih_teks(isi, blok = 16, tersembunyi = 48, kepala = 2, lapisan = 1,
                     iterasi = 1200, laju = 0.01, benih = 0, kata = benar)
cetak "Pelatihan selesai."

cetak ""
cetak "Model menulis (mode kata):"
cetak m.tulis(model, "bahasa indonesia", panjang = 24, suhu = 0.8)
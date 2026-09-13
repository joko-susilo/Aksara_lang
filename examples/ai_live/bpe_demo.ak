# ==========================================
# CONTOH: Tokenizer BPE Bahasa Indonesia — Mini LM v2 (Step A)
# ==========================================
# Ukur kompresi: berapa token yang dipakai untuk 1 kalimat,
# dibandingkan tokenisasi "kata" biasa.

impor "berkas.ak" sbg f
impor "teks.ak" sbg t
impor "bpe.ak" sbg bpe

isi = f.baca_file("examples/ai_live/korpus.txt")

cetak "== Latih vocab BPE dari korpus Indonesia =="
model = bpe.latih(isi, 300)
info = bpe.info(model)
cetak "Ukuran vocab:    " + info["ukuran_vokab"]
cetak "Penggabungan:    " + info["jumlah_penggabungan"]
cetak "Karakter dasar:  " + info["karakter_dasar"]

cetak ""
cetak "== Contoh tokenisasi =="
contoh = "bahasa pemrograman aksara indonesia kecerdasan buatan"
ids = bpe.ubah_ke_id(model, contoh)
cetak "Kalimat: " + contoh
cetak "Jumlah token (BPE): " + panjang(ids)
cetak "Jumlah kata (mentah): " + panjang(t.pisahkan(contoh, " "))
cetak "IDs: " + ids

cetak ""
cetak "== Dekode balik =="
hasil = bpe.ubah_ke_teks(model, ids)
cetak "Hasil dekode: [" + hasil + "]"
cetak "Sama dengan asli? " + (hasil == contoh)
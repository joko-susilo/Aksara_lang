# ==========================================
# PROFIL Aksara — ukur pembelajaran mandiri (murni Aksara)
# ==========================================
# 1) waktu belajar 2 fakta
# 2) ukuran memori
# 3) waktu jawab dari memori
# 4) retrain mini-LM dengan fakta (pembelajaran mendalam)

impor "belajar.ak" sbg B
impor "berkas.ak" sbg berkas
impor "waktu.ak" sbg w

belajar_file = "examples/ai_live/belajar_ai.txt"
korpus_file = "examples/ai_live/korpus_persona.txt"

# bersihkan
jika berkas.apakah_ada(belajar_file) {
    berkas.hapus_file(belajar_file)
}

cetak "== PROFIL PEMBELAJARAN MANDIRI (Aksara) =="
cetak ""

# 1) waktu belajar
t0 = w.detik_sekarang()
B.ingat(belajar_file, "ingat presiden: presiden pertama indonesia adalah soekarno")
B.ingat(belajar_file, "ingat ibukota: ibukota indonesia adalah jakarta")
t1 = w.detik_sekarang()
cetak "1) Belajar 2 fakta   : " + ((t1 - t0) * 1000) + " ms"

# 2) ukuran memori
ukuran = berkas.ukuran_file(belajar_file)
cetak "2) Ukuran memori     : " + ukuran + " bytes (" + (ukuran / 1024.0) + " KB)"

# 3) waktu jawab & hasil
t0 = w.detik_sekarang()
jawab_pres = B.jawab_dari(belajar_file, "presiden indonesia siapa?")
t1 = w.detik_sekarang()
cetak "3) Jawab dari memori  : " + ((t1 - t0) * 1000) + " ms -> " + jawab_pres

# 4) retrain mendalam (gabung fakta ke korpus, latih ulang)
cetak "4) Retrain mini-LM..."
t0 = w.detik_sekarang()
info = B.retrain(korpus_file, belajar_file, "examples/ai_live/checkpoint.txt")
t1 = w.detik_sekarang()
cetak "   " + info
cetak "   Waktu retrain: " + (t1 - t0) + " s"
cetak "   Checkpoint   : "
jika berkas.apakah_ada("examples/ai_live/checkpoint.txt") {
    cetak "   " + berkas.baca_file("examples/ai_live/checkpoint.txt")
}

cetak ""
cetak "== RINGKASAN =="
cetak "Belajar (ms) | Memori (B) | Jawab (ms) | Retrain (s)"
# ==========================================
# CONTOH: Pembelajaran mandiri AI Aksara
# ==========================================

impor "belajar.ak" sbg B
impor "berkas.ak" sbg berkas

belajar_file = "examples/ai_live/belajar_ai.txt"

# bersihkan file buat test yang deterministik
jika berkas.apakah_ada(belajar_file) {
    berkas.hapus_file(belajar_file)
}

cetak "== PEMBELAJARAN MANDIRI =="
cetak ""
cetak "1) Ajari: 'ingat presiden: presiden pertama indonesia adalah soekarno'"
B.ingat(belajar_file, "ingat presiden: presiden pertama indonesia adalah soekarno")
cetak "   -> disimpan ✅"
cetak ""
cetak "2) Tanya (sesi baru, baca dari disk): 'siapa presiden?'"
cetak "   AI: " + B.jawab_dari(belajar_file, "siapa presiden?")
cetak ""
cetak "3) Ajari lagi: 'ingat ibukota: ibukota indonesia adalah jakarta'"
B.ingat(belajar_file, "ingat ibukota: ibukota indonesia adalah jakarta")
cetak "   -> disimpan ✅"
cetak ""
cetak "4) Tanya: 'ibukota indonesia?'"
cetak "   AI: " + B.jawab_dari(belajar_file, "ibukota indonesia?")
cetak ""
cetak "5) Lupa: 'lupa ibukota' lalu tanya lagi"
B.lupa(belajar_file, "ibukota")
cetak "   AI: " + B.jawab_dari(belajar_file, "ibukota indonesia?")
cetak ""
cetak "6) Isi file belajar (persist):"
cetak berkas.baca_file(belajar_file)
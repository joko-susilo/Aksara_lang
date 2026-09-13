impor "berkas.ak" sbg berkas
impor "pintar.ak" sbg P
impor "pipeline.ak" sbg pl

fakta_file = "examples/ai_live/fakta_uji.txt"
korpus_file = "examples/ai_live/korpus_persona.txt"

berkas.hapus_file(fakta_file)
berkas.tambah_ke_file(fakta_file, "presiden=presiden pertama indonesia adalah soekarno\n")
berkas.tambah_ke_file(fakta_file, "soekarno=soekarno memimpin tahun 1945 sampai 1967\n")

kb = ["_human_words": "admin", "_human_reply": "oke", "_greet_words": "halo hai", "_greet_reply": "Halo",
      "_default": "belum paham"]

isi = berkas.baca_file(korpus_file)
pipe = pl.latih(isi, 100, 12, 24, 1, 1, 60, 0.02, 0, benar)
fun generator(pesan) { balik pl.ucap(pipe, pesan, 20, 0.4) }

cetak "== UJI INFERENSI BERANTAI =="
cetak "Q1: siapakah presiden pertama?"
cetak "A1: " + P.jawab_pintar(kb, "siapakah presiden pertama?", generator, fakta_file, korpus_file)
cetak ""
cetak "Q2: kapan ia memimpin?"
cetak "A2: " + P.jawab_pintar(kb, "kapan ia memimpin?", generator, fakta_file, korpus_file)

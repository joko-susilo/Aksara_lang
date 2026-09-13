# ==========================================
# AI Super Pintar Aksara v2 — konteks + memori (hemat)
# ==========================================
# 1) Percakapan mengikuti topik ('itu apa?' -> jawab topik terakhir)
# 2) Memori persist di file kecil lintas sesi
# 3) 'lupakan' buat clear, 'kamu ingat apa' buat cek memori

impor "asisten.ak" sbg A
impor "pipeline.ak" sbg pl
impor "berkas.ak" sbg f

memori_file = "examples/ai_live/memori_ai.txt"

kb = ["_human_words": "admin petugas orang manusia",
    "_human_reply": "Baik, saya siapkan bantuan dari tim. Sebentar ya. 📞",
    "_greet_words": "halo hai pagi siang malam assalamu",
    "_greet_reply": "Halo! Saya asisten Anda. Tanya apa saja.",
    "hitung": "Sebut angka + operasi, misal 'berapa 12 dikali 8'.",
    "berapa": "Coba tulis seperti '12 dikali 8' atau '100 - 35'.",
    "terjemah": "Sebut satu kata, saya coba padankan (indonesia/inggris).",
    "bahasa": "Bahasa Indonesia itu satu algoritma pemersatu yang indah. Tanya kata apa pun, saya bantu.",
    "waktu": "Saya offline tanpa jam, tapi saya bantu logika & hitungan.",
    "cara": "Saya AI ringan berbasis bahasa Aksara: offline, hemat daya, tanpa akun.",
    "siapa": "Saya asisten teks kecil: privasi terjaga, tanpa internet.",
    "_default": "Saya belum paham. Coba: salam, hitung, waktu, terjemah, atau cara."]

isi = f.baca_file("examples/ai_live/korpus_persona.txt")
pipe = pl.latih(isi, 100, 12, 24, 1, 1, 120, 0.02, 0, benar)
fun generator(pesan) { balik pl.ucap(pipe, pesan, 20, 0.4) }

cetak "== AI Aksara v2 — konteks & memori =="
cetak ""
# Sesi 1
cetak "SESI 1:"
cetak ">> bahasa itu apa?"
cetak A.balas_pintar(kb, "bahasa itu apa?", generator, memori_file)
cetak ">> itu apa maksudnya?"          # follow-up konteks
cetak A.balas_pintar(kb, "itu apa maksudnya?", generator, memori_file)
cetak ""
# Sesi 2 (memori dimuat dari file — jalankan ulang file ini)
cetak "SESI 2 (memori dari disk):"
cetak ">> kamu ingat topik tadi gak?"
cetak A.balas_pintar(kb, "kamu ingat topik tadi gak?", generator, memori_file)
cetak ""
cetak ">> lupakan semuanya"
cetak A.balas_pintar(kb, "lupakan semuanya", generator, memori_file)
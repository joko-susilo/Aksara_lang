# ==========================================
# REPL: Chat interaktif dengan AI Super Pintar Aksara
# ==========================================
# Ketik pertanyaan langsung, AI balas. 'keluar' untuk stop.
# Mode otomatis buat test (tanpa input pengguna).

impor "asisten.ak" sbg A
impor "pipeline.ak" sbg pl
impor "berkas.ak" sbg f

kb = ["_human_words": "admin petugas orang manusia",
    "_human_reply": "Baik, saya siapkan bantuan dari tim. Sebentar ya. 📞",
    "_greet_words": "halo hai pagi siang malam assalamu",
    "_greet_reply": "Halo! Saya asisten Anda. Tanya apa saja — saya coba bantu.",
    "hitung": "Sebut angka + operasi, misal: 'berapa 12 dikali 8' atau '100 - 35'.",
    "berapa": "Coba tulis seperti '12 dikali 8' atau '100 - 35', saya hitung.",
    "waktu": "Saya offline tanpa jam, tapi saya bantu logika & hitungan Anda.",
    "terjemah": "Sebut satu kata, saya coba padankan (indonesia/inggris).",
    "cara": "Saya AI teks ringan berbasis bahasa Aksara: offline, hemat daya, tanpa akun.",
    "siapa": "Saya asisten teks kecil: jernih, privasi terjaga, tanpa internet.",
    "_default": "Saya belum paham. Coba: salam, hitung, waktu, terjemah, atau cara."]

isi = f.baca_file("examples/ai_live/korpus_persona.txt")
pipe = pl.latih(isi, 100, 12, 24, 1, 1, 120, 0.02, 0, benar)

fun generator(pesan) {
    balik pl.ucap(pipe, pesan, 20, 0.4)
}

cetak "== REPL AI Aksara — ketik pesan, 'keluar' untuk berhenti =="
cetak ""

# Mode otomatis (untuk test tanpa input manual)
uji = [
    "halo",
    "berapa 25 dikali 4?",
    "siapa kamu?",
]
untuk i dalam 0 .. panjang(uji) - 1 {
    cetak ">> " + uji[i]
    cetak A.balas_pintar(kb, uji[i], generator)
    cetak ""
}

cetak "== (Interaktif: jalankan dengan aksara repl lalu ketik manual) =="
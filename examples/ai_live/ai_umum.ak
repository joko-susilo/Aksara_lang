# ==========================================
# CONTOH: AI Super Pintar "Aksara" — asisten umum (netral, bukan brand)
# ==========================================
# Persona netral & offline; 3 lapis penalaran; kosakata 415B.

impor "asisten.ak" sbg A
impor "pipeline.ak" sbg pl
impor "berkas.ak" sbg f

# ---------- Knowledge base (netral; kunci "_" = pengaturan) ----------
kb = ["_human_words": "admin petugas orang manusia",
    "_human_reply": "Baik, saya siapkan bantuan dari tim. Sebentar ya. 📞",
    "_greet_words": "halo hai pagi siang malam assalamu",
    "_greet_reply": "Halo! Saya asisten Anda. Tanya apa saja — saya coba bantu.",
    "hitung": "Sebut angka + operasi, misal: 'berapa 12 dikali 8' atau '100 - 35'.",
    "berapa": "Ayo hitung: tulis seperti '12 dikali 8' atau '100 - 35', saya bantu operasinya.",
    "waktu": "Saya offline tanpa jam, tapi saya bantu logika & hitungan Anda.",
    "terjemah": "Sebut satu kata, saya coba padankan (indonesia/inggris).",
    "cara": "Saya AI teks ringan berbasis bahasa Aksara: offline, hemat daya, tanpa akun.",
    "siapa": "Saya asisten teks kecil: jernih, privasi terjaga, tanpa internet.",
    "_default": "Saya belum paham. Coba: salam, hitung, waktu, terjemah, atau cara."]

# ---------- generator fallback (korpus BERSIH persona umum) ----------
isi = f.baca_file("examples/ai_live/korpus_persona.txt")
pipe = pl.latih(isi, 100, 12, 24, 1, 1, 120, 0.02, 0, benar)

fun generator(pesan) {
    balik pl.ucap(pipe, pesan, 20, 0.4)
}

cetak "== AI Super Pintar Aksara (asisten umum) =="
cetak ""
pertanyaan = [
    "halo, ada orang?",
    "12 dikali 8 berapa?",
    "berapa 100 - 35?",
    "siapa kamu?",
    "tujuh dikali tiga?",
]
untuk i dalam 0 .. panjang(pertanyaan) - 1 {
    cetak "Tanya : " + pertanyaan[i]
    cetak "AI    : " + A.balas_pintar(kb, pertanyaan[i], generator)
    cetak ""
}
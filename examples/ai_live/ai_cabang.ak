# ==========================================
# AI Aksara v3 — logika bercabang multi-kondisi
# ==========================================

impor "asisten.ak" sbg A
impor "pipeline.ak" sbg pl
impor "berkas.ak" sbg f

memori_file = "examples/ai_live/memori_ai3.txt"

kb = ["_human_words": "admin petugas orang manusia",
    "_human_reply": "Baik, saya siapkan bantuan tim. Sebentar ya. 📞",
    "_greet_words": "halo hai pagi siang malam assalamu",
    "_greet_reply": "Halo! Saya asisten Anda. Tanya apa saja.",
    # aturan bercabang multi-kondisi
    "_rules": [
        [["and", "paket&harga", ["paket", "harga"]], "Ada 5 paket: FREE/WEB/LITE/PRO/PREMIUM. Harga mulai Rp0 s/d Rp349rb/bulan."],
        [["and", "paket&kuota", ["paket", "kuota"]], "Kuota: FREE 50, WEB 300, LITE 300, PRO 3000, PREMIUM 10000 pesan/hari."],
        [["and", "paket&aktivasi", ["paket", "aktivasi"]], "Aktivasi paket: pilih di dashboard, bayar via GoPay, dikonfirmasi admin."],
        [["or", "paket", ["paket"]], "Paket Csoto: FREE Rp0, WEB Rp50rb, LITE Rp99rb, PRO Rp199rb, PREMIUM Rp349rb/bulan."],
        [["or", "kuota", ["kuota", "limit", "pesan per hari"]], "Kuota per hari: 1 pesan masuk dijawab AI = 1 kuota. Balasan AI gratis."],
        [["or", "aktivasi", ["aktivasi", "hubungkan", "cara aktif"]], "Aktivasi: daftar di csoto.web.id, hubungkan WhatsApp/Telegram."],
    ],
    "waktu": "Saya offline tanpa jam, tapi saya bantu logika & hitungan.",
    "terjemah": "Sebut satu kata, saya coba padankan.",
    "siapa": "Saya asisten teks kecil: privasi terjaga, tanpa internet.",
    "_default": "Saya belum paham. Coba tanya paket, harga, kuota, aktivasi, atau hitung."]

isi = f.baca_file("examples/ai_live/korpus_persona.txt")
pipe = pl.latih(isi, 100, 12, 24, 1, 1, 120, 0.02, 0, benar)
fun generator(pesan) { balik pl.ucap(pipe, pesan, 20, 0.4) }

cetak "== AI Aksara v3 — logika bercabang =="
cetak ""
q = [
    "halo",
    "berapa harga paket pro?",
    "kuota paket premium berapa?",
    "paket dan aktivasi gimana?",
    "12 dikali 6 berapa?",
    "siapa kamu?",
    "cara aktivasi gimana?",
]
untuk i dalam 0 .. panjang(q) - 1 {
    cetak "Q: " + q[i]
    cetak "A: " + A.balas_pintar(kb, q[i], generator, memori_file)
    cetak ""
}
impor "cabang.ak" sbg C
impor "teks.ak" sbg t

# aturan: [kondisi, jawaban] ; kondisi: [modus, label, [kata...]]
aturan = [
    [["and", "paket & harga", ["paket", "harga"]], "Ada 5 paket: FREE/WEB/LITE/PRO/PREMIUM. Harga mulai Rp0 s/d Rp349rb/bulan."],
    [["and", "paket & kuota", ["paket", "kuota"]], "Kuota: FREE 50, WEB 300, LITE 300, PRO 3000, PREMIUM 10000 pesan/hari."],
    [["or", "harga", ["harga", "biaya", "berapaan"]], "Harga: FREE Rp0, WEB Rp50rb, LITE Rp99rb, PRO Rp199rb, PREMIUM Rp349rb."],
    [["or", "kuota", ["kuota", "pesan per hari", "limit"]], "Kuota per hari: 1 pesan masuk dijawab AI = 1 kuota."],
    [["and", "paket & aktivasi", ["paket", "aktivasi"]], "Aktivasi paket: pilih di dashboard, bayar via GoPay, dikonfirmasi admin."],
    [["or", "paket", ["paket"]], "Paket Csoto: FREE Rp0, WEB Rp50rb, LITE Rp99rb, PRO Rp199rb, PREMIUM Rp349rb/bulan."],
    [["or", "aktivasi", ["aktivasi", "cara aktif", "hubungkan"]], "Aktivasi: daftar di csoto.web.id, hubungkan WhatsApp/Telegram."],
    [["or", "default", ["isi"]], "Saya belum paham. Coba tanya paket, harga, kuota, atau aktivasi."],
]

cetak "== Tes logika bercabang =="
q = [
    "berapa harga paket pro?",
    "kuota paket premium berapa?",
    "gimana cara aktivasi?",
    "paket dan aktivasi gimana?",
    "ada paket berapa aja?",
]
untuk i dalam 0 .. panjang(q) - 1 {
    cetak "Q: " + q[i]
    j = C.eval(aturan, t.huruf_kecil(q[i]))
    jika j == nil { cetak "  A: (tidak cocok)" }
    lain { cetak "  A: " + j }
    cetak ""
}
# ==========================================
# CONTOH: AI Super Pintar "Aksara" — chat CS dengan teknologi Aksara
# ==========================================
# Penalaran 3 lapis + kosakata 415B + KB data toko. Offline, di HP.

impor "asisten.ak" sbg A
impor "pipeline.ak" sbg pl
impor "berkas.ak" sbg f

# ---------- Knowledge base (data toko) ----------
kb = ["harga": "Paket: FREE Rp0 (50 pesan/hari), WEB Rp50rb, LITE Rp99rb, PRO Rp199rb, PREMIUM Rp349rb per bulan. Trial 7 hari gratis tanpa kartu.",
    "fitur": "Fitur Csoto: balas chat 24/7, knowledge base toko, handoff ke admin, broadcast promo, nomor resmi WhatsApp Business API.",
    "integrasi": "Aktivasi WhatsApp: ambil Access Token, Phone Number ID dari Meta Business Manager, lalu tempel di halaman Platform. Telegram: pakai token BotFather.",
    "jam": "Bot membalas 24/7. Di luar jam buka, gunakan offline reply di dashboard.",
    "broadcast": "Broadcast WA maks 100 penerima sekali kirim (jeda 4-8 dtk, pakai template Meta). Telegram gratis maks 300 penerima.",
    "biaya": "Biaya Meta: service gratis s/d 30 Sept 2026, marketing ±Rp586/pesan, utility ±Rp356. Dibayar langsung ke Meta, bukan Csoto.",
    "bayar": "Pembayaran paket manual via GoPay; konfirmasi admin. Biaya instalasi sekali Rp200rb (opsional, tanpa pendampingan gratis).",
    "kuota": "Kuota = 1 pesan masuk yang dijawab AI (per akun per hari). Balasan AI & broadcast gratis. Reset tengah malam.",
    "default": "Saya belum paham pertanyaan itu. Coba: harga, fitur, cara aktivasi, broadcast, kuota, atau biaya Meta ya 🙏"]

# ---------- generator fallback (pipeline mini) ----------
isi = f.baca_file("examples/ai_live/korpus/korpus_minilm.txt")
pipe = pl.latih(isi, 250, 20, 40, 1, 1, 100, 0.01, 0, benar)

fun generator(pesan) {
    balik "[lihat pipeline] " + pl.ucap(pipe, pesan, 20, 0.4)
}

# ---------- Sesi chat ----------
cetak "== AI Super Pintar Aksara — CS Otomatis Csoto =="
cetak ""
pertanyaan = [
    "halo, ada orang gak?",
    "berapa harga paket premium?",
    "gimana cara aktivasi whatsapp?",
    "broadcast di telegram bayar?",
    "kuota gimana dihitung?",
    "kenapa aku tanya sinus?",
]
untuk i dalam 0 .. panjang(pertanyaan) - 1 {
    cetak "Tanya : " + pertanyaan[i]
    cetak "AI    : " + A.balas_pintar(kb, pertanyaan[i], generator)
    cetak ""
}

cetak "== Kecepatan & ukuran =="
cetak "Pipeline (model int8 + tokenizer) : ringan di HP"
cetak "Kosakata 415B + KB tersusun lokal  : tanpa internet"
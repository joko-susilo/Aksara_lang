# ==========================================
# KB_KAya - Pustaka Standar Aksara: Knowledge Base kaya (multi-kategori)
# ==========================================
# Sumber: knowledge-base-csoto.md (data bisnis asli)
# Struktur: tiap kategori punya [kata kunci..., jawaban].
# Kata kunci diambil pakai sinonim & normalisasi bahasa ID.

kb_rich = [
    # --- PROFIL & FITUR ---
    [["csoto", "cs oto", "apa itu", "platform", "layanan"], "Csoto adalah layanan customer service otomatis berbasis AI untuk UMKM Indonesia. AI membalas chat pelanggan di WhatsApp dan Telegram 24/7 sesuai pengetahuan toko."],
    [["fitur", "keunggulan", "kemampuan", "bisa apa"], "Fitur Utama: (1) Balas chat otomatis 24 jam, (2) Knowledge Base toko, (3) Handoff ke manusia saat pelanggan minta admin, (4) Dashboard pantau chat, (5) Broadcast promo, (6) WhatsApp Business API resmi Meta."],
    [["handoff", "admin", "manusia", "petugas"], "Handoff: bila pelanggan mengetik 'admin', 'mau bicara orang', atau 'petugas', bot berhenti membalas dan pesan diteruskan ke nomor admin. Bot aktif lagi otomatis setelah 2 jam."],

    # --- HARGA & PAKET ---
    [["harga", "paket", "biaya", "tarif", "cost", "bayar"], "Paket Csoto: FREE Rp0 (50 pesan/hari, trial 7 hari tanpa kartu), WEB Rp50rb/bulan (300 pesan/hari), LITE Rp99rb (300), PRO Rp199rb (3000), PREMIUM Rp349rb (10000)."],
    [["gratis", "free", "trial", "coba"], "Plan GRATIS: Rp0, 50 pesan/hari, trial 7 hari tanpa kartu kredit. Setelah trial habis AI berhenti membalas sampai akun di-upgrade."],
    [["instalasi", "aktivasi", "fee", "satu kali"], "Biaya instalasi/aktivasi sekali Rp200.000 untuk pendampingan WhatsApp Business API (WABA). Pendaftaran mandiri tanpa pendampingan tidak dikenai biaya."],

    # --- KUOTA ---
    [["kuota", "limit", "pesan per hari", "batas"], "Kuota = 1 pesan masuk yang dijawab AI (per akun per hari). Balasan AI & broadcast tidak menghabiskan kuota. Reset otomatis tiap hari jam 00.00 WIB."],
    [["habis", "kuota habis"], "Jika kuota habis, bot tetap menerima chat dan mengirim pemberitahuan kuota habis; tidak ada pesan yang hilang."],

    # --- BROADCAST ---
    [["broadcast", "promo", "kirim massal", "pengumuman"], "Broadcast: kirim promo ke pelanggan yang pernah chat. WA maksimal 100 penerima sekali kirim (jeda 4-8 detik, pakai template Meta). Telegram gratis maksimal 300 penerima (jeda 1-3 detik)."],
    [["template", "meta", "biaya meta", "waba"], "Biaya Meta 2026: Service gratis s/d 30 Sept 2026 (setelahnya ±Rp356/pesan), Marketing ±Rp586/pesan, Utility & Auth ±Rp356/pesan. Dibayar langsung oleh pelanggan ke Meta, bukan ke Csoto."],

    # --- CARA DAFTAR ---
    [["daftar", "sign up", "cara mulai", "aktivasi"], "Cara daftar: (1) Daftar gratis di csoto.web.id, (2) Login & buat toko, (3) Aktivasi WhatsApp Business API (Access Token, Phone Number ID dari Meta), (4) Opsional bot Telegram, (5) Set otak AI & Knowledge Base, (6) Daftar nomor admin."],
    [["whatsapp bisnis", "aktivasi whatsapp", "integrasi whatsapp", "whatsapp", "wa", "nomor"], "Integrasi WhatsApp: gunakan WhatsApp Business API resmi (Meta Cloud API) — bukan bot tidak resmi, aman dari blokir. Dapatkan Access Token + Phone Number ID dari Meta Business Manager."],
    [["telegram", "tg", "bot token"], "Integrasi Telegram: hubungkan token bot dari BotFather di halaman Platform. Telegram gratis untuk broadcast dan tetap 24/7."],
]
# ==========================================
# CONTOH: AI Chat CSOTO (hibrida) — akurat + generatif, offline, di HP.
# ==========================================
# 1) FAKTA dari knowledge base (jawaban pasti, keyword-matching sederhana)
# 2) FALLBACK generatif dari mini LM (BPE+int8) buat pertanyaan terbuka
# Semua lokal: tanpa internet, tanpa API orang.

impor "berkas.ak" sbg f
impor "teks.ak" sbg t
impor "pipeline.ak" sbg pl

# ---------- Knowledge base ringkas ----------
# struktur: kamus kunci -> jawaban (sintaks: [kunci: nilai])
faq = ["harga": "Harga: PLAN FREE gratis 50 pesan/hari. PLAN PRO mulai Rp99.000/bulan. Lihat di halaman harga.",
    "cara daftar": "Daftar gratis di csoto.web.id/login. Cukup email + password, langsung trial 7 hari.",
    "whatsapp": "Integrasi WhatsApp: scan QR dari dashboard -> status connected -> bot langsung aktif.",
    "telegram": "Integrasi Telegram: masukin bot token dari BotFather -> connect -> bot aktif.",
    "fitur": "Fitur: balas chat otomatis, broadcast promosi, offline reply, handoff ke CS manusia, QRIS.",
    "jam buka": "Toko otomatis balas 24/7, di luar jam buka pakai offline reply.",
    "bayar": "Pembayaran lewat QRIS atau transfer; bukti diverifikasi lalu layanan diaktifkan.",
    "default": "Hmm, yang itu belum ada di basis pengetahuan saya. Coba tanya soal harga, fitur, WA/Telegram, atau bayar."]

# ---------- Siapkan model generatif mini ----------
isi = f.baca_file("examples/ai_live/korpus/korpus_minilm.txt")
pipe = pl.latih(isi, 250, 20, 40, 1, 1, 100, 0.01, 0, benar)

# ---------- Muat kosakata 415 byte (untuk tokenisasi) ----------
vokab = pl.muat_kosakata()

fun balas(pesan) {
    rendah = t.huruf_kecil(pesan)
    daftar_kunci = kunci(faq)
    untuk idx dalam 0 .. panjang(daftar_kunci) - 1 {
        kunci_faq = daftar_kunci[idx]
        jika kunci_faq != "default" dan t.mengandung(rendah, kunci_faq) {
            balik faq[kunci_faq]
        }
    }
    # fallback generatif
    balik "[AI] " + pl.ucap(pipe, pesan, 28, 0.4)
}

cetak "== AI Chat CSOTO (mode otomatis, 5 tanya) =="
pertanyaan = [
    "berapa harga robotnya?",
    "gimana cara daftar?",
    "bisa pake telegram nggak?",
    "jam bukanya kapan?",
    "cara bayarnya gimana?",
]
untuk i dalam 0 .. panjang(pertanyaan) - 1 {
    cetak ""
    cetak "Tanya : " + pertanyaan[i]
    cetak "AI    : " + balas(pertanyaan[i])
}

cetak ""
cetak "== Ukur =="
cetak "Model int8: ~0.8 MB + tokenizer — proses ringan di Termux/HP."
cetak "Kosakata terkompres: " + panjang(pl.tokenkan_kosakata(vokab, "csoto indonesia")) + " token (vocab 415B)"
# ==========================================
# CHAT GPT ALIAS AKsara — antarmuka percakapan interaktif
# ==========================================
# Jalankan: python3 -m aksara examples/ai_live/chatgpt_ak.ak
# (atan via jalankan_chat.sh). Ketik 'keluar' untuk berhenti.

impor "chat.ak" sbg C
impor "pipeline.ak" sbg pl
impor "berkas.ak" sbg b
impor "teks.ak" sbg t
impor "kb_rich.ak" sbg KBR
impor "kb_lookup.ak" sbg KBL
impor "bahasa_id.ak" sbg BID
impor "ngobrol.ak" sbg N
impor "pakar.ak" sbg PKAR
impor "hitung.ak" sbg H

# --- konfigurasi ---
fakta_file = "examples/ai_live/chat_fakta.txt"
riwayat = "examples/ai_live/chat_sejarah.txt"
korpus_file = "examples/ai_live/korpus_persona.txt"

kb = ["_human_words": "admin petugas orang manusia",
    "_human_reply": "Baik, saya alihkan ke tim kami ya. 📞",
    "_greet_words": "halo hai pagi siang malam assalamu",
    "_greet_reply": "Halo! Saya Asisten Aksara. Tanya apa saja: hitung, KB, atau ngobrol.",
    "_default": "Hmm, saya belum paham. Coba tanya lagi dengan lebih jelas ya 🙏"]

# --- model generatif (kecil, hemat) ---
isi = b.baca_file(korpus_file)
pipe = pl.latih(isi, 120, 10, 20, 1, 1, 80, 0.02, 0, benar)
fun gen(pesan) { balik pl.ucap(pipe, pesan, 18, 0.5) }

# --- layar pembuka ---
cetak "============================================"
cetak "  ASISTEN AKsara — ChatGPT miniature (offline)"
cetak "  Ketik 'keluar' untuk berhenti."
cetak "============================================"
cetak ""

selama benar {
    pesan = masukan(">> ")
    jika t.potong_teks(pesan) == "keluar" atau t.potong_teks(pesan) == "exit" {
        cetak "Sampai jumpa! 👋"
        henti
    }
    jika t.potong_teks(pesan) == "" {
        lanjut
    }
    # 1) cek pakar (coding / bug hunting / stack)
    jawaban_pakar = PKAR.jawab(pesan)
    # hanya pakai jika "asal pakar" (kalimat jawaban bukan generic "belum paham")
    stack_pakar = PKAR.cari_stack(pesan)
    jika stack_pakar != nil {
        cetak "Aksara(PAKAR): " + jawaban_pakar
        cetak ""
        lanjut
    }
    # 2) chat umum (hitung dulu — angka jelas)
    # 2a) hitung lokal
    hh = H.hitung(pesan)
    jika hh != nil {
        cetak "Aksara: Hasilnya " + hh[0] + " (" + hh[1] + ")"
        cetak ""
        lanjut
    }
    # 2b) KB kaya (knowledge base bisnis)
    norm_pesan = BID.normalisasi(pesan)
    cari_kb = KBL.cari(KBR.kb_rich, norm_pesan)
    jika cari_kb != nil {
        cetak "Aksara: " + cari_kb[0]
        cetak ""
        lanjut
    }
    # 2c) chat utama
    jawaban = C.bicara(kb, pesan, gen, fakta_file, korpus_file, riwayat, "x")
    cetak "Aksara: " + jawaban
    cetak ""
}
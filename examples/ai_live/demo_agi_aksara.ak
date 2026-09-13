# ==========================================
# DEMO LOOP AGI NATIVE (magi.ak di Aksara) — otak mini-LM v4 lokal + RAG
# ==========================================
# Siklus: seed memori -> retrieval -> pikir (model_v4/llm) -> refleksi.

impor "perpikir.ak" sbg AG
impor "model_v4.ak" sbg M
impor "llm.ak" sbg LL
impor "proses.ak" sbg P
impor "berkas.ak" sbg b

JALAN_MEM = "/tmp/ak_agimem.json"
jika b.apakah_ada(JALAN_MEM) { b.hapus_file(JALAN_MEM) }

cetak "=== SEED MEMORI (RAG) ==="
AG.ingat(JALAN_MEM, "f1", "Csoto adalah layanan customer service otomatis berbasis AI untuk UMKM Indonesia, membalas chat di WhatsApp dan Telegram.")
AG.ingat(JALAN_MEM, "f2", "Harga paket Telegram Csoto Rp49 ribu per bulan tanpa biaya per pesan.")
AG.ingat(JALAN_MEM, "f3", "Bahasa Aksara adalah bahasa pemrograman AI pertama dari Indonesia, bisa memanggil LLM dan model mini sendiri.")
cetak "  memori awal: " + AG.terakhir(JALAN_MEM)

# --- muat otak mini-LM v4 (lokal, offline) ---
cetak "=== MUAT OTAK MINI-LM v4 ==="
model4 = M.baca_serial("examples/ai_live/artifak/model_v4.pkl")
bpe4 = M.baca_serial("examples/ai_live/artifak/bpe_v4.pkl")
cetak "  model dimuat, siap berpikir"

# otak lokal (mini-LM) — pakai global model4/bpe4
fun gen_lokal(pesan) {
    ids = M.ubah_id(bpe4, pesan)
    out = M.tulis(model4, ids[0..5], 20, 0.7, 0)
    balik M.balik_teks(bpe4, out)
}
# otak LLM (kalau GROQ_API_KEY ada)
fun gen_llm(pesan) {
    balik LL.tanya(pesan)
}

kunci_l = P.env_ambil("GROQ_API_KEY")
otak = gen_lokal
nama_otak = "mini-LM v4 (lokal)"
jika panjang(kunci_l) > 0 {
    otak = gen_llm
    nama_otak = "llm (API)"
}

# --- LOOP PIKIR ---
cetak ""
cetak "=== PERPIKIR (otak: " + nama_otak + ") ==="
hasil1 = AG.pikir("apa itu csoto?", otak, JALAN_MEM)
cetak "  KONTEKS yang direcall: " + hasil1["konteks"]
cetak "  JAWABAN: " + hasil1["jawaban"]

hasil2 = AG.pikir("berapa harga paket telegram?", otak, JALAN_MEM)
cetak "  JAWABAN: " + hasil2["jawaban"]

cetak ""
cetak "=== REFLEKSI ==="
cetak "  memori setelah 2 pertanyaan: " + AG.terakhir(JALAN_MEM)
cetak "  (setiap tanya-jawab otomatis tersimpan = belajar dari pengalaman)"
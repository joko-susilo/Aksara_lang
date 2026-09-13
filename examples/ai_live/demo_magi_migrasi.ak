# ==========================================
# DEMO MIGRASI MAGI -> Bahasa Aksara (magi.ak + perpikir.ak + cari.ak)
# ==========================================
# Satu skrip, memakai SEMUA organ MAGI versi Aksara: konstitusi, penjaga
# nurani, loop pikir (RAG), refleksi, kalibrasi.

impor "magi.ak" sbg M
impor "perpikir.ak" sbg AG
impor "model_v4.ak" sbg V
impor "berkas.ak" sbg b

JALAN_MEM = "/tmp/ak_magi_mem.json"
JALAN_KAL = "/tmp/ak_magi_kal.json"
jika b.apakah_ada(JALAN_MEM) { b.hapus_file(JALAN_MEM) }
jika b.apakah_ada(JALAN_KAL) { b.hapus_file(JALAN_KAL) }

cetak "=== 1) KONSTITUSI (nilai MAGI) ==="
untuk n dalam M.konstitusi() {
    cetak "  • " + n
}

cetak "=== 2) PENJAGA NURANI (pantangan) ==="
bankal = "temuan: bocor nomor kartu user 4111..."
aman = "temuan: IDOR di /api/v1/users/5"
cetak "  'nomor kartu' boleh lewat? " + M.jaga(bankal)
cetak "  'idor' boleh lewat? " + M.jaga(aman)

cetak "=== 3) LOOP PIKIR (RAG + otak mini-LM v4) ==="
AG.ingat(JALAN_MEM, "f1", "Aksara adalah bahasa pemrograman AI pertama dari Indonesia, bisa memanggil LLM dan model mini sendiri.")
AG.ingat(JALAN_MEM, "f2", "Mini-LM v4 adalah model transformernya yang ditulis dari nol, dirto degan backprop terverifikasi.")

model4 = V.baca_serial("examples/ai_live/artifak/model_v4.pkl")
bpe4 = V.baca_serial("examples/ai_live/artifak/bpe_v4.pkl")

fun gen_lokal(pesan) {
    ids = V.ubah_id(bpe4, pesan)
    out = V.tulis(model4, ids[0..5], 18, 0.7, 0)
    balik V.balik_teks(bpe4, out)
}
hasil = AG.pikir("apa itu mini lm v4?", gen_lokal, JALAN_MEM)
cetak "  konteks: " + hasil["konteks"]
cetak "  jawaban: " + hasil["jawaban"]

cetak "=== 4) REFLEKSI (simpan pelajaran) ==="
pel = M.refleksi(JALAN_MEM, "apa itu mini lm v4?", hasil["jawaban"])
cetak "  tersimpan: " + pel

cetak "=== 5) KALIBRASI ==="
M.kalibrasi(JALAN_KAL, "saran-cname", 1)
M.kalibrasi(JALAN_KAL, "saran-blind-traversal", 0)
l = M.laporan(JALAN_KAL)
cetak "  total saran dinilai: " + l["total"] + ", oke: " + l["oke"]

cetak ""
cetak "=== MAGI VERSI AKsara SELESAI ==="
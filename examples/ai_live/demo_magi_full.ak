# ==========================================
# DEMO MIGRASI PENUH MAGI -> Aksara (organ lengkap)
# ==========================================

impor "magi.ak" sbg M
impor "perpikir.ak" sbg AG
impor "model_v4.ak" sbg V
impor "berkas.ak" sbg b
impor "json.ak" sbg j
impor "waktu.ak" sbg W

JALAN_MEM = "/tmp/ak_mem_full.json"
JALAN_KAL = "/tmp/ak_kal_full.json"
jika b.apakah_ada(JALAN_MEM) { b.hapus_file(JALAN_MEM) }
jika b.apakah_ada(JALAN_KAL) { b.hapus_file(JALAN_KAL) }

cetak "=== MUAT OTAK ==="
model4 = V.baca_serial("examples/ai_live/artifak/model_v4.pkl")
bpe4 = V.baca_serial("examples/ai_live/artifak/bpe_v4.pkl")
fun gen(pesan) {
    ids = V.ubah_id(bpe4, pesan)
    out = V.tulis(model4, ids[0..5], 18, 0.7, 0)
    balik V.balik_teks(bpe4, out)
}

cetak "=== SINKRON MEMORI .huntingx -> Aksara ==="
dimuat_h = M.muat_huntingx("/root/.huntingx/custom_playbooks.json", JALAN_MEM)
cetak "  pelajaran huntingx ditarik: " + dimuat_h

cetak "=== SOS (cari jalan saat buntu) ==="
hasil_s = M.sos(JALAN_MEM, "tidak ada temuan, semua endpoint ditolak", gen)
cetak "  arah dari memori: " + hasil_s["arah"]

cetak "=== REFLEKSI + CRYSTAL (simpan sama 2x = terbukti) ==="
AG.ingat(JALAN_MEM, "l1", "pelajaran: selalu mulai pasif lalu aktif")
AG.ingat(JALAN_MEM, "l1", "pelajaran: selalu mulai pasif lalu aktif")
M.refleksi(JALAN_MEM, "coba belajar", "contoh hasil refleksi")

kristal = M.crystal(JALAN_MEM, 2)
cetak "  pelajaran terbukti (>=2x): " + teks(panjang(kristal))
untuk kr dalam kristal { cetak "  * " + kr }

cetak "=== KALIBRASI + DECAY ==="
M.kalibrasi(JALAN_KAL, "saran-a", 1)
M.kalibrasi(JALAN_KAL, "saran-b", 0)
waktu_lalu = 90 * 86400
isi_cur = j.urai(b.baca_file(JALAN_KAL))
isi_cur[0]["waktu"] = W.detik_sekarang() - waktu_lalu
b.tulis_file(JALAN_KAL, j.ubah(isi_cur))
dec = M.decay(JALAN_KAL, 30)
cetak "  decay: total " + dec["total"] + ", dingin " + dec["dingin"]

cetak "=== BRIEFING ==="
ringkas = M.briefing(JALAN_MEM, gen)
cetak "  narasi: " + ringkas["narasi"]

cetak ""
cetak "=== MIGRASI PENUH MAGI -> AKsara SELESAI ==="
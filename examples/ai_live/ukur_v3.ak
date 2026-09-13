# ==========================================
# UKUR Mini-LM v3 — impact terukur (murni Aksara)
# ==========================================

impor "model_v3.ak" sbg M
impor "waktu.ak" sbg W

korpus = M.baca_file_korpus("examples/ai_live/korpus/korpus_v3.txt")
cetak "== PROFIL KORPUS =="
cetak "  karakter korpus : " + panjang(korpus)

t0 = W.detik_sekarang()
bpe = M.siap_bpe(korpus, 500)
ids = M.ubah_id(bpe, korpus)
t1 = W.detik_sekarang()
cetak "  BPE vocab 500   : " + (t1 - t0) + "s, ids=" + panjang(ids)

cetak ""
cetak "== SKALA MODEL (parameter = kapasitas) =="
# v2 kecil (dasar)
t0 = W.detik_sekarang()
m2 = M.latih(ids[0..2000], 48, 2, 1, 1, 16, 120, 0.02, 0)
t1 = W.detik_sekarang()
cetak "  v2 (d48/1L/1E) : " + (t1 - t0) + "s"

# v3 lebih besar
t0 = W.detik_sekarang()
m3 = M.latih(ids[0..3000], 128, 4, 2, 2, 20, 200, 0.02, 0)
t1 = W.detik_sekarang()
cetak "  v3 (d128/2L/2E) : " + (t1 - t0) + "s"

cetak ""
cetak "== GENERATE v3 =="
seed = M.ubah_id(bpe, "bahasa indonesia")
t0 = W.detik_sekarang()
out = M.tulis(m3, seed[0..3], 20, 0.8, 0)
t1 = W.detik_sekarang()
cetak "  generate 20 token : " + (t1 - t0) + "s"
cetak "  teks: " + M.balik_teks(bpe, out)
# ==========================================
# LATIH MODEL v3 — pipeline end-to-end (murni Aksara)
# ==========================================
# Korpus -> BPE -> ids -> latih Mini-LM v3 -> generate
# Semua dari Aksara (backend numeric). Full training loop. Verifiable.
# Jalankan: python3 -m aksara examples/ai_live/latih_pipeline_v3.ak

impor "model_v3.ak" sbg M
impor "berkas.ak" sbg b
impor "waktu.ak" sbg W
impor "teks.ak" sbg t

jalur_korpus = "examples/ai_live/korpus/korpus_train.txt"
jalur_korpus_kompres = "examples/ai_live/korpus/korpus_train.akgz"

cetak "===== PIPELINE LATIH MODEL v3 (murni Aksara) ====="
cetak ""

# 1) baca korpus + kompres
cetak "[1] Baca korpus (dan kompres utk hemat disk)..."
t0 = W.detik_sekarang()
korpus = M.baca_file_korpus(jalur_korpus)
t1 = W.detik_sekarang()
# kompres & simpan .akgz (hemat ~63%)
M.kompres_teks(jalur_korpus, jalur_korpus_kompres)
ukuran_raw = b.ukuran_file(jalur_korpus)
ukuran_pk = b.ukuran_file(jalur_korpus_kompres)
cetak "    " + panjang(korpus) + " karakter (" + (t1-t0) + "s)"
cetak "    kompresi: " + ukuran_raw + " -> " + ukuran_pk + " bytes (hemat " + ((1 - ukuran_pk/ukuran_raw)*100) + "%)"

# 2) tokenizer BPE dari korpus sendiri + KOMPRESI KORPUS
cetak "[2] Latih tokenizer BPE + kompresi korpus..."
t0 = W.detik_sekarang()
model_bpe = M.siap_bpe(korpus, 600)
ids = M.ubah_id(model_bpe, korpus)
t1 = W.detik_sekarang()
ukuran_raw = panjang(korpus)                     # byte asli
ukuran_ids = panjang(ids)                        # token (id ≈ rata2 1-2 byte)
cetak "    vocab=600, total_ids=" + panjang(ids) + " (" + (t1-t0) + "s)"
cetak "    KOMPRESI KORPUS: " + ukuran_raw + " char -> " + ukuran_ids + " token"
cetak "    (token BPE ≈ subset sub-kata; efisiensi ~" + (ukuran_ids / ukuran_raw) + " token/char)"

# 3) latih Mini-LM v3
cetak "[3] Latih Mini-LM v3 (d=128, 2 layer, MoE 2 pakar, 300 iterasi)..."
ids_latih = ids[0..8000]
t0 = W.detik_sekarang()
model = M.latih(ids_latih, 128, 4, 2, 2, 20, 300, 0.02, 0)
t1 = W.detik_sekarang()
cetak "    selesai (" + (t1-t0) + "s)"

# 4) generate (uji kualitas)
cetak "[4] Generate dari seed 'bahasa indonesia':"
seed = M.ubah_id(model_bpe, "bahasa indonesia")
t0 = W.detik_sekarang()
out = M.tulis(model, seed[0..3], 24, 0.8, 0)
t1 = W.detik_sekarang()
teks_hasil = M.balik_teks(model_bpe, out)
cetak "    teks: " + teks_hasil
cetak "    waktu generate: " + (t1-t0) + "s"
cetak ""

# 5) simpan korpus versi kompres (bukti karya)
cetak "[5] Simpan metadata (bukti pipeline berjalan)..."
meta = ["latih_pipeline_v3", "korpus_char=" + panjang(korpus), "vocab=600", "d=128", "layer=2", "paket=MoE2", "iterasi=300"]
b.tulis_file("examples/ai_live/artifak/pipeline_log.txt", t.gabungkan(meta, "\n"))
cetak "    -> pipeline_log.txt tersimpan"

cetak ""
cetak "===== SELESAI: pipeline end-to-end berjalan ====="
# ==========================================
# LATIH MODEL v4 — pipeline end-to-end (murni Aksara)
# ==========================================
# Korpus -> BPE -> ids -> latih Mini-LM v4 (backprop LENGKAP) -> generate
# Backward terverifikasi gradien-check; loss & perplexity tercatat.
# Jalankan: python3 -m aksara examples/ai_live/latih_pipeline_v4.ak

impor "model_v4.ak" sbg M
impor "berkas.ak" sbg b
impor "waktu.ak" sbg W
impor "teks.ak" sbg t

jalur_korpus = "examples/ai_live/korpus/korpus_besar.txt"
jalur_cekpoint = "/tmp/ckpt_v4ak"

cetak "===== PIPELINE LATIH MODEL v4 (murni Aksara) ====="
cetak ""

# 1) baca korpus
cetak "[1] Baca korpus..."
t0 = W.detik_sekarang()
korpus = M.baca_file_korpus(jalur_korpus)
t1 = W.detik_sekarang()
cetak "    " + panjang(korpus) + " karakter (" + (t1-t0) + "s)"

# 2) tokenizer BPE
cetak "[2] Latih tokenizer BPE..."
t0 = W.detik_sekarang()
model_bpe = M.siap_bpe(korpus, 400)
ids = M.ubah_id(model_bpe, korpus)
cetak "    vocab=400, total_ids=" + panjang(ids) + " (" + (W.detik_sekarang()-t0) + "s)"

# 3) latih v4 (backprop lengkap, loss + perplexity)
cetak "[3] Latih Mini-LM v4 (d=48, 1 layer, 150 iterasi)..."
ids_latih = ids[0..20000]
t0 = W.detik_sekarang()
hasil = M.latih(ids_latih, 48, 4, 1, 2, 48, 150, 0.003, 0, 50, jalur_cekpoint)
t1 = W.detik_sekarang()
cetak "    selesai (" + (t1-t0) + "s), best_loss=" + hasil["best_loss"]

# 4) generate (uji kualitas)
cetak "[4] Generate dari seed token:"
seed = M.ubah_id(model_bpe, "bahasa indonesia")
out = M.tulis(hasil["bobot"], seed[0..3], 20, 0.8, 0)
teks_hasil = M.balik_teks(model_bpe, out)
cetak "    teks: " + teks_hasil
cetak ""

# 5) simpan serial model + BPE + bukti log
cetak "[5] Simpan model + checkpoint + BPE..."
M.tulis_serial("examples/ai_live/artifak/model_v4.pkl", hasil["bobot"])
M.tulis_serial("examples/ai_live/artifak/bpe_v4.pkl", model_bpe)
meta = ["latih_pipeline_v4", "korpus_char=" + panjang(korpus), "vocab=400",
        "d=48", "layer=1", "best_loss=" + hasil["best_loss"],
        "perplexity=" + hasil["perplexity"]]
b.tulis_file("examples/ai_live/artifak/pipeline_v4_log.txt", t.gabungkan(meta, "\n"))
cetak "    -> model_v4.pkl + bpe_v4.pkl + pipeline_v4_log.txt tersimpan"

cetak ""
cetak "===== SELESAI: pipeline v4 end-to-end berjalan ====="
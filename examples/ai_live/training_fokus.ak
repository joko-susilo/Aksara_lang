# ==========================================
# TRAINING FOKUS — model dengan korpus 441KB (murni Aksara)
# ==========================================
# Korpus domain (bug hunting + python + aksara + JS + Kotlin) terkompres.
# Baca .akxz -> BPE -> latih Mini-LM v3 -> evaluasi kualitas.

impor "model_v3.ak" sbg M
impor "berkas.ak" sbg b
impor "waktu.ak" sbg W

jalur_akxz = "examples/ai_live/korpus/korpus_maks.akxz"

cetak "===== TRAINING MODEL FOKUS (murni Aksara) ====="
cetak ""

# 1) baca korpus terkompres
cetak "[1] Baca korpus .akxz (LZMA, terkompres)..."
t0 = W.detik_sekarang()
korpus = M.baca_korpus_lzma(jalur_akxz)
t1 = W.detik_sekarang()
cetak "    " + panjang(korpus) + " karakter (" + (t1-t0) + "s)"
cetak "    ukuran file: " + b.ukuran_file(jalur_akxz) + " bytes terkompres"

# 2) BPE tokenizer
cetak "[2] Latih tokenizer BPE (vocab 500)..."
t0 = W.detik_sekarang()
model_bpe = M.siap_bpe(korpus, 500)
ids = M.ubah_id(model_bpe, korpus)
t1 = W.detik_sekarang()
cetak "    " + panjang(ids) + " token (" + (t1-t0) + "s)"

# 3) training Mini-LM v3 — lebih besar dari sebelum (lebih banyak data)
cetak "[3] Latih Mini-LM v3 (d=128, 4 kepala, 2 layer, MoE 2)..."
ids_latih = ids[0 .. 20000]
t0 = W.detik_sekarang()
model = M.latih(ids_latih, 128, 4, 2, 2, 20, 500, 0.02, 0)
t1 = W.detik_sekarang()
cetak "    selesai (" + (t1-t0) + "s)"

# 4) evaluasi kualitas: generate beberapa seed domain
cetak "[4] Generate (uji kualitas):"
antara_awal = [
    ["bug hunting", "Bug hunting adalah"],
    ["python", "Python adalah bahasa"],
    ["aksara", "Aksara adalah bahasa"],
    ["javascript", "JavaScript adalah bahasa"],
    ["kotlin", "Kotlin adalah bahasa"],
]
untuk i dalam 0 .. panjang(antara_awal) - 1 {
    seed_teks = antara_awal[i][1]
    seed = M.ubah_id(model_bpe, seed_teks)
    t0 = W.detik_sekarang()
    out = M.tulis(model, seed[0..5], 16, 0.5, 0)
    t1 = W.detik_sekarang()
    teks = M.balik_teks(model_bpe, out)
    cetak "  [" + antara_awal[i][0] + "] " + teks
    cetak "        (" + (t1-t0) + "s)"
}

cetak ""
cetak "===== SELESAI ====="
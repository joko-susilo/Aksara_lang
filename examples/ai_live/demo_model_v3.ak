# ==========================================
# DEMO Mini-LM v3 — murni Aksara (executable asli)
# ==========================================
# Model bahasa kita sendiri: BPE vocab + multi-head + layer + MoE.
# Jalankan: python3 -m aksara examples/ai_live/demo_model_v3.ak

impor "model_v3.ak" sbg M

korpus = M.baca_file_korpus("examples/ai_live/korpus/korpus_v3.txt")
cetak "Korpus: " + panjang(korpus) + " karakter"
cetak ""

cetak "== 1. Siapkan BPE tokenizer (kita sendiri) =="
bpe = M.siap_bpe(korpus, 400)
ids_korpus = M.ubah_id(bpe, korpus)
cetak "  ids korpus: " + panjang(ids_korpus)
cetak ""

cetak "== 2. Latih Mini-LM v3 (murni Aksara) =="
# potong ids supaya latihan cepat di demo
ids_potong = ids_korpus[0 .. 4000]
model = M.latih(ids_potong, 64, 4, 2, 2, 20, 200, 0.02, 0)
cetak "  model siap (d=64, 4 kepala, 2 layer, 2 pakar)"
cetak ""

cetak "== 3. Model menulis (generate dari seed) =="
seed = M.ubah_id(bpe, "bahasa indonesia")
hasil_kata = M.tulis(model, seed[0..3], 18, 0.8, 0)
cetak "  ids: " + hasil_kata
cetak "  teks: " + M.balik_teks(bpe, hasil_kata)
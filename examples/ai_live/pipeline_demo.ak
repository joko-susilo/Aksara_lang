# ==========================================
# CONTOH: Pipeline Mini LM v2 — dari korpus sampai jadi teks (end-to-end)
# ==========================================
# BPE -> Mini LM -> (quantisasi int8 opsional) -> model menulis sendiri.

impor "berkas.ak" sbg f
impor "pipeline.ak" sbg pl

isi = f.baca_file("examples/ai_live/korpus.txt")

cetak "== 1. Latih pipeline (BPE + Mini LM, mode kata) =="
pipe = pl.latih(isi, 300, 32, 48, 2, 1, 250, 0.01, 0, salah)
cetak pl.laporan(pipe)

cetak ""
cetak "== 2. Tokenisasi kalimat pakai BPE buatan sendiri =="
ids = pl.tokenkan(pipe, "bahasa indonesia dipakai oleh ilmu")
cetak "IDs: " + ids
cetak "Jumlah token: " + panjang(ids)

cetak ""
cetak "== 3. Model menulis (asli, float) =="
cetak pl.ucap(pipe, "bahasa indonesia", 18, 0.8)

cetak ""
cetak "== 4. Latih ulang + quantisasi int8 =="
pipe_q = pl.latih(isi, 300, 32, 48, 2, 1, 250, 0.01, 1, benar)
cetak pl.laporan(pipe_q)

cetak ""
cetak "== 5. Model int8 menulis (dequant otomatis) =="
cetak pl.ucap(pipe_q, "bahasa indonesia", 18, 0.8)
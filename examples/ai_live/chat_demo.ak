# ==========================================
# CONTOH: AI Chat Mini — model dari nol, offline, di HP.
# ==========================================
# Bukan API orang: LM+BPE+MoE kita; "chat" = model lanjutkan ucapan
# dari prompt (nukleus generatif lokal). Ringan, tanpa internet.

impor "berkas.ak" sbg f
impor "pipeline.ak" sbg pl

isi = f.baca_file("examples/ai_live/korpus/korpus_minilm.txt")

cetak "== Siapkan model (BPE + LM + int8) =="
pipe = pl.latih(isi, 300, 24, 48, 2, 1, 150, 0.01, 0, benar)
cetak pl.laporan(pipe)

cetak ""
cetak "== Chat Mini (mode otomatis, 4 putaran) =="
balasan = pl.ucap(pipe, "csoto adalah alat untuk", 32, 0.5)
cetak "1. Tanya  : csoto adalah? "
cetak "   Jawab  : " + balasan

balasan = pl.ucap(pipe, "belajar bahasa pemrograman indonesia", 32, 0.5)
cetak "2. Tanya  : bagaimana belajar aksara? "
cetak "   Jawab  : " + balasan

balasan = pl.ucap(pipe, "balas chat otomatis untuk umkm", 32, 0.5)
cetak "3. Tanya  : apa itu chat otomatis? "
cetak "   Jawab  : " + balasan

balasan = pl.ucap(pipe, "teknologi membantu manusia bekerja", 32, 0.5)
cetak "4. Tanya  : peran teknologi? "
cetak "   Jawab  : " + balasan

cetak ""
cetak "Model ringan: 0.08 MB int8 + tokenizer — jalan di HP entry (Termux)."
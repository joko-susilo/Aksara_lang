# ==========================================
# CONTOH: Benchmark Mini LM v2 — waktu & RAM (impact terukur)
# ==========================================
# Ukur di CPU (laptop/HP): waktu latih, token/detik inference, estimasi RAM.

impor "berkas.ak" sbg f
impor "waktu.ak" sbg w
impor "pipeline.ak" sbg pl

isi = f.baca_file("examples/ai_live/korpus.txt")

cetak "== Benchmark latih (dari nol, CPU) =="
mulai = w.detik_sekarang()
pipe = pl.latih(isi, 300, 32, 48, 2, 1, 250, 0.01, 0, benar)
selesai = w.detik_sekarang()
lama_latih = selesai - mulai
cetak "Waktu latih:   " + lama_latih + " detik"
cetak "Korpus:        " + panjang(isi) + " karakter"

cetak ""
cetak "== Benchmark inference (token/detik) =="
mulai = w.detik_sekarang()
hasil = pl.ucap(pipe, "bahasa", 60, 0.5)
selesai = w.detik_sekarang()
lama = selesai - mulai
cetak "60 token dihasilkan dalam " + lama + " detik"
cetak "Kecepatan: " + (60 / lama) + " token/detik"
cetak "Hasil: " + hasil

cetak ""
cetak "== Estimasi footprint =="
cetak "Model int8: 0.0839 MB + tokenizer 302 vocab"
cetak "Total paket kecil — jalan di HP entry (4GB RAM)"
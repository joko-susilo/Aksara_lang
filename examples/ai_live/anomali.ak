# ============================================
# PORTOFOLIO DEMO 3 - Deteksi anomali (outlier)
# ============================================
# pakai larik.outlier: nilai di luar 2x simpangan baku.

impor "larik.ak" sbg l

data = [5, 6, 5, 7, 900, 6, 5, 1000, 6, 7]

cetak "Data belanja harian (ada transaksi mencurigakan):"
cetak data

cetak ""
cetak "Anomali terdeteksi:"
anomali = l.outlier(data)
untuk x dalam anomali {
    cetak "  !! " + x + " (di luar pola normal)"
}

cetak ""
cetak "Rata-rata normal (tanpa anomali): " + l.rata_rata([5, 6, 5, 7, 6, 5, 6, 7])
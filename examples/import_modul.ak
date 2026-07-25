cetak "=== UJI IMPOR MODUL PYTHON ==="

# 1. Impor math
impor "math" sbg m
cetak "1. Akar 16 = " + m.sqrt(16)
cetak "   Pi = " + m.pi

# 2. Impor os
impor "os" sbg os
cetak "2. Direktori saat ini: " + os.getcwd()

# 3. Impor random
impor "random" sbg acak
cetak "3. Angka acak 1-100: " + acak.randint(1, 100)

# 4. Impor datetime
impor "datetime" sbg dt
sekarang = dt.datetime.now()
cetak "4. Waktu sekarang: " + sekarang

cetak "=== SELESAI ==="

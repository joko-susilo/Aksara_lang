# Membuat kamus
data = ["nama": "Budi", "umur": 30]

# Akses nilai
cetak "Nama: " + data["nama"]
cetak "Umur: " + data["umur"]

# Kamus angka
angka = [1: "satu", 2: "dua", 3: "tiga"]
cetak "Angka 2: " + angka[2]

# Kamus dalam variabel
kunci = "nama"
cetak "Via variabel: " + data[kunci]

# Update nilai
data["umur"] = 31
cetak "Umur baru: " + data["umur"]

# Tambah pasangan baru
data["kota"] = "Jakarta"
cetak "Kota: " + data["kota"]

cetak "=== SELESAI ==="

data = ["nama": "Budi", "umur": 30]

cetak "Kunci: " + kunci(data)
cetak "Nilai: " + nilai(data)
cetak "Ada nama? " + ada(data, "nama")
cetak "Ada kota? " + ada(data, "kota")
cetak "Kosong? " + kosong(data)

tambah(data, "kota", "Jakarta")
cetak "Setelah tambah: " + kunci(data)

hapus(data, "umur")
cetak "Setelah hapus: " + kunci(data)

cetak "Dapatkan: " + dapatkan(data, "nama", "?")
cetak "Dapatkan missing: " + dapatkan(data, "x", "tidak ada")

salinan = salin(data)
cetak "Salinan: " + kunci(salinan)

cetak "=== SELESAI ==="

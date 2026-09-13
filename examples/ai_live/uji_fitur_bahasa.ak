# ==========================================
# UJI FITUR BAHASA BERU — proses, regex, paralel, uji, paket
# ==========================================

impor "proses.ak" sbg P
impor "regex.ak" sbg R
impor "paralel.ak" sbg PA
impor "uji.ak" sbg U
impor "paket.ak" sbg K

cetak "=== 1) PROSES ==="
kel = P.jalankan(["echo", "halo dari proses"])
cetak "  jalankan => kode=" + kel["kode"] + ", keluar='" + kel["keluar"].strip() + "'"
cetak "  env PATH ada: " + (panjang(P.env_ambil("PATH")) > 0)

cetak "=== 2) REGEX ==="
cetak "  cari angka: " + teks(R.ada("[0-9]+", "harga 50000 rupiah"))
cetak "  ganti: " + R.ganti("[0-9]+", "XXX", "harga 50000 rupiah")
cetak "  sema co: " + teks(panjang(R.sema_co("[A-Z][a-z]+", "Halo Dunia Aksara")))

cetak "=== 3) UJI framework ==="
U.harus(6 * 7, 42, "6*7=42")
U.harus_benar("a" == "a", "string sama")
U.hampir(1.0 / 3.0, 0.3333, "1/3", 0.001)
cetak "  3 asersi LULUS"

cetak "=== 4) PARALEL ==="
tugas1 = [["sleep", "0.2"], ["sleep", "0.2"], ["sleep", "0.2"]]
ok1 = PA.jalan_berapa(tugas1, 3)
cetak "  3 tugas paralel sukses: " + ok1

cetak "=== 5) PAKET ==="
cetak "  jumlah modul stdlib: " + panjang(K.daftar())
cetak "  ada 'berkas.ak': " + teks(K.ada("berkas"))
cetak "  ada 'nuklir.ak': " + teks(K.ada("nuklir"))

cetak "=== SEMUA FITUR BARU DIUJI ==="
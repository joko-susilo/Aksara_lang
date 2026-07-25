cetak "Membuat pola segitiga angka:"
baris = 1

selama baris <= 5 {
    teks_baris = ""
    untuk j dalam 1 .. baris {
        # Menguji apakah parser mendukung penggabungan string atau operasi kompleks
        teks_baris = teks_baris + "*"
    }
    cetak teks_baris
    baris = baris + 1
}


# ==========================================
# CSV - Pustaka Standar Aksara: CSV
# ==========================================

impor "csv" sbg csv
impor "builtins" sbg b

fun baca(jalan) {
    f = b.open(jalan)
    baca = csv.reader(f)
    isi = []
    untuk baris dalam baca {
        isi = dorong(isi, baris)
    }
    f.close()
    balik isi
}

fun tulis(jalan, baris_baris) {
    f = b.open(jalan, "w")
    penulis = csv.writer(f)
    untuk baris dalam baris_baris {
        penulis.writerow(baris)
    }
    f.close()
}

fun baca_kamus(jalan) {
    f = b.open(jalan)
    baca = csv.DictReader(f)
    isi = []
    untuk baris dalam baca {
        isi = dorong(isi, baris)
    }
    f.close()
    balik isi
}
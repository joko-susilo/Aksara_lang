# ============================================
# PORTOFOLIO DEMO 2 - Klasifikasi: sentimen ulasan
# ============================================
# pakai builtin jenis() (klasifikasi leksikon Indonesia).

impor "teks.ak" sbg t

ulasan = [
    "Produknya bagus dan keren, sangat suka",
    "Pengiriman lambat dan buruk, kecewa sekali",
    "Mantap, kualitas luar biasa untuk harganya",
    "Payah, boros dan cepat rusak",
    "Biasa saja, tidak ada yang istimewa",
]

# Label harapan (truth)
label = ["positif", "negatif", "positif", "negatif", "netral"]

cetak "== Klasifikasi sentimen ulasan =="
cocok = 0
untuk i dalam 0 .. panjang(ulasan) - 1 {
    has = jenis(ulasan[i])
    tanda = ""
    jika has == label[i] {
        cocok = cocok + 1
        tanda = "v"
    } lain {
        tanda = "x"
    }
    cetak "[" + tanda + "] '" + t.potong_teks(ulasan[i][0..20]) + "...' -> " + has + " (harap: " + label[i] + ")"
}

akurasi = cocok / panjang(ulasan)
cetak ""
cetak "Akurasi: " + akurasi * 100 + "% (" + cocok + "/" + panjang(ulasan) + ")"
cetak "Judul: contoh klasifikasi teks berbahasa Indonesia otomatis"
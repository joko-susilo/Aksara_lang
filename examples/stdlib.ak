# Demo Pustaka Standar Aksara

impor "teks.ak" sbg t
impor "mtk.ak" sbg m
impor "koleksi.ak" sbg k
impor "berkas.ak" sbg b

cetak "== TEKS =="
s = "  Halo Dunia  "
cetak t.huruf_besar(s)
cetak t.huruf_kecil(s)
cetak t.potong_teks(s)
cetak t.gabungkan(["apel", "mangga", "jeruk"], ", ")
cetak t.ganti("a-b-c", "-", "+")
cetak t.mengandung("halo dunia", "dunia")
cetak t.awalan("halo dunia", "halo")
cetak t.akhiran("halo dunia", "dunia")
cetak t.balik_teks("aksara")
cetak t.sub_teks("abcdefgh", 2, 5)

cetak "== MTK =="
cetak m.mutlak(-9)
cetak m.pangkat(2, 10)
cetak m.akar(16)
cetak m.bulatkan(3.6)
cetak m.bulat_atas(3.1)
cetak m.genap(4)
cetak m.ganjil(7)
cetak m.terbesar([3, 9, 1])
cetak m.terkecil([3, 9, 1])

cetak "== KOLEKSI =="
cetak k.urutkan([5, 2, 8, 1])
cetak k.urutkan_balik([5, 2, 8, 1])
cetak k.unik([1, 2, 2, 3, 3, 3])
cetak k.balik_list([1, 2, 3])
cetak k.gabung_list([1, 2], [3, 4])
cetak k.cari_indeks([10, 20, 30], 20)
cetak k.hitung([1, 2, 2, 2], 2)
cetak k.potong([1, 2, 3, 4, 5], 1, 3)
cetak k.hapus_index([1, 2, 3, 4], 2)

cetak "== BERKAS =="
jalan = "/tmp/opencode/std_demo.txt"
b.tulis_file(jalan, "baris satu\nbaris dua\n")
cetak b.apakah_ada(jalan)
cetak b.baca_file(jalan)
b.tambah_ke_file(jalan, "baris tiga\n")
cetak b.baca_baris(jalan)
cetak b.ukuran_file(jalan)
b.hapus_file(jalan)
cetak b.apakah_ada(jalan)

cetak "OK"
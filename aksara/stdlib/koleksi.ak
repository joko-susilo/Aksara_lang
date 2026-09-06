# ==========================================
# KOLEKSI - Pustaka Standar Aksara: Daftar & Kamus
# ==========================================

impor "builtins" sbg b

fun urutkan(daftar) {
    balik b.sorted(daftar)
}

fun urutkan_balik(daftar) {
    hasil = b.sorted(daftar)
    balik balik_list(hasil)
}

fun unik(daftar) {
    hasil = []
    untuk x dalam daftar {
        jika bukan ada(hasil, x) {
            hasil = dorong(hasil, x)
        }
    }
    balik hasil
}

fun balik_list(daftar) {
    hasil = []
    untuk x dalam daftar {
        hasil = [x] + hasil
    }
    balik hasil
}

fun gabung_list(a, b) {
    hasil = []
    untuk x dalam a { hasil = dorong(hasil, x) }
    untuk y dalam b { hasil = dorong(hasil, y) }
    balik hasil
}

fun cari_indeks(daftar, x) {
    untuk i dalam 0 .. panjang(daftar) - 1 {
        jika daftar[i] == x {
            balik i
        }
    }
    balik -1
}

fun hitung(daftar, x) {
    jumlah = 0
    untuk item dalam daftar {
        jika item == x { jumlah = jumlah + 1 }
    }
    balik jumlah
}

fun potong(daftar, awal, akhir) {
    balik daftar[awal..akhir]
}

fun hapus_index(daftar, indeks) {
    hasil = []
    untuk i dalam 0 .. panjang(daftar) - 1 {
        jika i != indeks {
            hasil = dorong(hasil, daftar[i])
        }
    }
    balik hasil
}
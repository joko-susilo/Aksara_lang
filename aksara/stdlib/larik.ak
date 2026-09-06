
# ==========================================
# LARIK - Standard Library Aksara
# Array & Matematika dalam Bahasa Indonesia
# ==========================================

# --- Statistik Dasar ---
fun rata_rata(data) {
    total = 0
    untuk n dalam data {
        total = total + n
    }
    balik total / panjang(data)
}

fun jumlah(data) {
    total = 0
    untuk n dalam data {
        total = total + n
    }
    balik total
}

fun maksimum(data) {
    terbesar = data[0]
    untuk n dalam data {
        jika n > terbesar {
            terbesar = n
        }
    }
    balik terbesar
}

fun minimum(data) {
    terkecil = data[0]
    untuk n dalam data {
        jika n < terkecil {
            terkecil = n
        }
    }
    balik terkecil
}

fun rentang(data) {
    balik maksimum(data) - minimum(data)
}

# --- Transformasi ---
fun normalisasi(data) {
    min_val = minimum(data)
    max_val = maksimum(data)
    hasil = []
    untuk n dalam data {
        hasil = dorong(hasil, (n - min_val) / (max_val - min_val))
    }
    balik hasil
}

fun skala(data, faktor) {
    hasil = []
    untuk n dalam data {
        hasil = dorong(hasil, n * faktor)
    }
    balik hasil
}

# --- Prediksi ---
fun tebak(data) {
    n = panjang(data)
    jika n < 2 {
        balik data
    }
    selisih = 0
    untuk i dalam 1 .. n - 1 {
        selisih = selisih + (data[i] - data[i-1])
    }
    rata = selisih / (n - 1)
    balik [data[n-1] + rata, data[n-1] + 2 * rata]
}

# --- Pengelompokan ---
fun kelompok(data, jumlah) {
    jika panjang(data) <= jumlah {
        balik [data]
    }
    min_val = minimum(data)
    max_val = maksimum(data)
    lebar = (max_val - min_val) / jumlah
    
    hasil = []
    untuk i dalam 0 .. jumlah - 1 {
        hasil = dorong(hasil, [])
    }
    
    untuk n dalam data {
        idx = bulat((n - min_val) / lebar)
        jika idx >= jumlah {
            idx = jumlah - 1
        }
        dorong(hasil[idx], n)
    }
    balik hasil
}

# --- Statistik lanjutan ---
fun median(data) {
    n = panjang(data)
    jika n == 0 { balik nil }
    urut = koleksi_urutkan(data)
    tengah = n / 2
    jika genap_bulat(n) {
        balik (urut[bulat(tengah) - 1] + urut[bulat(tengah)]) / 2
    } lain {
        balik urut[bulat(tengah)]
    }
}

fun koleksi_urutkan(daftar) {
    hasil = daftar[0 .. panjang(daftar) - 1]
    n = panjang(hasil)
    untuk i dalam 0 .. n - 2 {
        untuk j dalam 0 .. n - 2 {
            jika hasil[j] > hasil[j + 1] {
                sementara = hasil[j]
                hasil[j] = hasil[j + 1]
                hasil[j + 1] = sementara
            }
        }
    }
    balik hasil
}

fun genap_bulat(x) {
    balik x % 2 == 0
}

fun variansi(data) {
    rata = rata_rata(data)
    total = 0
    untuk n dalam data {
        total = total + (n - rata) * (n - rata)
    }
    balik total / panjang(data)
}

fun simpangan_baku(data) {
    balik variansi(data) ** 0.5
}

fun outlier(data) {
    rata = rata_rata(data)
    sd = simpangan_baku(data)
    hasil = []
    untuk n dalam data {
        jika n > rata + 2 * sd atau n < rata - 2 * sd {
            hasil = dorong(hasil, n)
        }
    }
    balik hasil
}

fun pola(data) {
    n = panjang(data)
    jika n < 2 { balik data }
    selisih = data[1] - data[0]
    untuk i dalam 2 .. n - 1 {
        jika data[i] - data[i - 1] != selisih {
            balik "Tidak ada pola"
        }
    }
    balik data[n - 1] + selisih
}

fun frekuensi(data) {
    jika panjang(data) == 0 { balik [] }
    hasil = [data[0]: 1]
    untuk i dalam 1 .. panjang(data) - 1 {
        item = data[i]
        jika ada(hasil, item) {
            hasil[item] = hasil[item] + 1
        } lain {
            hasil[item] = 1
        }
    }
    balik hasil
}

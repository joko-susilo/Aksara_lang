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

fun median(data) {
    n = panjang(data)
    jika n % 2 == 1 {
        balik data[(n-1)/2]
    } lain {
        balik (data[n/2 - 1] + data[n/2]) / 2
    }
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
    // akar dari variansi
    balik variansi(data) ** 0.5
}

# --- Transformasi ---
fun normalisasi(data) {
    min_val = minimum(data)
    max_val = maksimum(data)
    hasil = []
    untuk n dalam data {
        hasil[panjang(hasil)] = (n - min_val) / (max_val - min_val)
    }
    balik hasil
}

fun skala(data, faktor) {
    hasil = []
    untuk n dalam data {
        hasil[panjang(hasil)] = n * faktor
    }
    balik hasil
}

# --- Prediksi ---
fun tebak(data) {
    n = panjang(data)
    jika n < 2 { balik data }
    selisih = 0
    untuk i dalam 1..n {
        selisih = selisih + (data[i] - data[i-1])
    }
    rata = selisih / (n - 1)
    balik [data[n-1] + rata, data[n-1] + 2 * rata]
}

# --- Pengelompokan ---
fun kelompok(data, jumlah) {
    jika panjang(data) <= jumlah { balik [data] }
    min_val = minimum(data)
    max_val = maksimum(data)
    lebar = (max_val - min_val) / jumlah
    
    hasil = []
    untuk i dalam 0..jumlah {
        hasil[i] = []
    }
    
    untuk n dalam data {
        idx = bulat((n - min_val) / lebar)
        jika idx >= jumlah { idx = jumlah - 1 }
        hasil[idx][panjang(hasil[idx])] = n
    }
    balik hasil
}

# --- Deteksi ---
fun outlier(data) {
    // Deteksi anomali sederhana (di luar 2x simpangan baku)
    rata = rata_rata(data)
    sd = simpangan_baku(data)
    hasil = []
    untuk n dalam data {
        jika n > rata + 2*sd atau n < rata - 2*sd {
            hasil[panjang(hasil)] = n
        }
    }
    balik hasil
}

fun pola(data) {
    // Cek apakah deret aritmatika
    n = panjang(data)
    jika n < 2 { balik data }
    selisih = data[1] - data[0]
    untuk i dalam 2..n {
        jika data[i] - data[i-1] != selisih {
            balik "Tidak ada pola"
        }
    }
    balik data[n-1] + selisih
}

# --- Frekuensi ---
fun frekuensi(data) {
    hasil = ["": 0]
    untuk item dalam data {
        jika ada(hasil, item) {
            hasil[item] = hasil[item] + 1
        } lain {
            hasil[item] = 1
        }
    }
    balik hasil
}

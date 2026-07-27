
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
    jika n < 2 {
        balik data
    }
    selisih = 0
    untuk i dalam 1..n {
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
    untuk i dalam 0..jumlah {
        hasil[i] = []
    }
    
    untuk n dalam data {
        idx = bulat((n - min_val) / lebar)
        jika idx >= jumlah {
            idx = jumlah - 1
        }
        hasil[idx][panjang(hasil[idx])] = n
    }
    balik hasil
}

# ==========================================
# UJI STANDARD LIBRARY LARIK
# ==========================================

# Salin fungsi dari larik.ak (sementara, sampai impor .ak jadi)
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

# ============ TES ============
data = [10, 20, 30, 40, 50]
cetak "Data: " + data
cetak "Rata-rata: " + rata_rata(data)
cetak "Jumlah: " + jumlah(data)
cetak "Maksimum: " + maksimum(data)
cetak "Minimum: " + minimum(data)
cetak "Prediksi: " + tebak(data)

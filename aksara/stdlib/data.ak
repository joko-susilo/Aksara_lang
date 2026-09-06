# ==========================================
# DATA - Pustaka Standar Aksara: Data & Metrik (AI-first)
# ==========================================

fun bagi(daftar, rasio) {
    n = panjang(daftar)
    batas = bulat(n * rasio)
    pelatihan = []
    uji = []
    untuk i dalam 0 .. n - 1 {
        jika i < batas {
            pelatihan = dorong(pelatihan, daftar[i])
        } lain {
            uji = dorong(uji, daftar[i])
        }
    }
    balik [pelatihan, uji]
}

fun akurasi(nyata, prediksi) {
    sesuai = 0
    n = panjang(nyata)
    untuk i dalam 0 .. n - 1 {
        jika bulat(nyata[i]) == bulat(prediksi[i]) {
            sesuai = sesuai + 1
        }
    }
    balik sesuai / n
}

fun galat_rata(nyata, prediksi) {
    total = 0
    n = panjang(nyata)
    untuk i dalam 0 .. n - 1 {
        selisih = nyata[i] - prediksi[i]
        jika selisih < 0 { selisih = -selisih }
        total = total + selisih
    }
    balik total / n
}

fun ambil_selisih(daftar) {
    hasil = []
    untuk i dalam 1 .. panjang(daftar) - 1 {
        hasil = dorong(hasil, daftar[i] - daftar[i-1])
    }
    balik hasil
}
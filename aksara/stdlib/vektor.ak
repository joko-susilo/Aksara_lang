# ==========================================
# VEKTOR - Pustaka Standar Aksara: Vektor & Kemiripan (AI)
# ==========================================
# Operasi vektor sederhana, murni Aksara — untuk fitur & pencarian mirip.

fun dot(a, b) {
    total = 0
    untuk i dalam 0 .. panjang(a) - 1 {
        total = total + a[i] * b[i]
    }
    balik total
}

fun norma(v) {
    balik mt_akar(dot(v, v))
}

fun mt_akar(x) {
    balik x ** 0.5
}

fun normalisasi(v) {
    n = norma(v)
    hasil = []
    jika n > 0 {
        untuk x dalam v {
            hasil = dorong(hasil, x / n)
        }
    } lain {
        balik v
    }
    balik hasil
}

fun kosinus(a, b) {
    na = norma(a)
    nb = norma(b)
    jika na == 0 atau nb == 0 {
        balik 0
    }
    balik dot(a, b) / (na * nb)
}

fun jumlah(daftar) {
    total = 0
    untuk x dalam daftar { total = total + x }
    balik total
}
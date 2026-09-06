# ==========================================
# MTK - Pustaka Standar Aksara: Matematika
# ==========================================

impor "math" sbg mt
impor "builtins" sbg b
impor "random" sbg r

fun mutlak(x) {
    jika x < 0 { balik -x }
    balik x
}

fun pangkat(x, y) {
    balik x ** y
}

fun akar(x) {
    balik mt.sqrt(x)
}

fun bulatkan(x) {
    balik mt.floor(x + 0.5)
}

fun bulat_atas(x) {
    balik mt.ceil(x)
}

fun bulat_bawah(x) {
    balik mt.floor(x)
}

fun terbesar(daftar) {
    balik b.max(daftar)
}

fun terkecil(daftar) {
    balik b.min(daftar)
}

fun genap(x) {
    balik x % 2 == 0
}

fun ganjil(x) {
    balik x % 2 == 1
}

fun acak(bawah, atas) {
    balik r.randint(bawah, atas)
}

fun pilihan_terbanyak(daftar) {
    terbanyak = nil
    najumlah = 0
    untuk x dalam daftar {
        jumlah_x = 0
        untuk y dalam daftar {
            jika y == x { jumlah_x = jumlah_x + 1 }
        }
        jika jumlah_x > najumlah {
            najumlah = jumlah_x
            terbanyak = x
        }
    }
    balik terbanyak
}
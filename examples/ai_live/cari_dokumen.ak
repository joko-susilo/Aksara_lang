# ============================================
# PORTOFOLIO DEMO 4 - Pencarian dokumen mirip (vektor + kosinus)
# ============================================
# Bag-of-words sederhana: dokumen → vektor kata → kosinus kemiripan.

impor "vektor.ak" sbg v
impor "teks.ak" sbg t

dokumen = [
    "bahasa pemrograman indonesia untuk belajar kode",
    "pencurian data pengguna jadi ancaman keamanan siber",
    "prakiraan cuaca hujan lebat di jakarta",
    "belajar machine learning dengan bahasa indonesia",
    "hujan badai melanda wilayah utara malam ini",
]

# Kosakata global (fitur vektor)
kata = ["bahasa", "pemrograman", "belajar", "machine", "cuaca", "hujan",
        "keamanan", "data", "indonesia", "kode"]

fun vektorkan(teks) {
    vektor = []
    untuk k dalam kata {
        jika t.mengandung(teks, k) {
            vektor = dorong(vektor, 1)
        } lain {
            vektor = dorong(vektor, 0)
        }
    }
    balik vektor
}

pustaka = []
untuk d dalam dokumen {
    pustaka = dorong(pustaka, vektorkan(d))
}

query = "belajar machine learning bahasa indonesia"
vq = vektorkan(query)

cetak "Kueri: '" + query + "'"
cetak ""
terbaik = 0
skor_terbaik = 0
untuk i dalam 0 .. panjang(pustaka) - 1 {
    s = v.kosinus(vq, pustaka[i])
    cetak "  dokumen " + i + " -> kemiripan " + bulat(s * 100) + "%"
    jika s > skor_terbaik {
        skor_terbaik = s
        terbaik = i
    }
}
cetak ""
cetak "Paling mirip: dokumen " + terbaik + " => '" + dokumen[terbaik] + "'"
# ==========================================
# UJI - Pustaka Standar Aksara: Framework pengujian
# ==========================================
# Asersi yang melempar galat (kini dengan lokasi [baris N]).
# Pemakaian:
#   impor "uji.ak" sbg U
#   U.harus(kali(6,7), 42, "kali(6,7)")
#   U.harus_benar(1 < 2, "matematika wajar")
#   U.jalan("examples/uji/")   # jalankan semua file berakhiran uji_.ak

impor "proses.ak" sbg P

fun harus(nilai, harapan, label = "") {
    jika nilai == harapan {
        balik benar
    }
    galat "uji GAGAL: " + label
}

fun harus_benar(kondisi, label = "") {
    jika kondisi {
        balik benar
    }
    galat "uji GAGAL: " + label
}

fun harus_salah(kondisi, label = "") {
    jika bukan kondisi {
        balik benar
    }
    galat "uji GAGAL (harus salah): " + label
}

fun hampir(nilai, harapan, label = "", toleransi = 0.0001) {
    selisih0 = nilai - harapan
    jika selisih0 < 0 { selisih0 = -selisih0 }
    jika selisih0 <= toleransi {
        balik benar
    }
    galat "uji hampir GAGAL: " + label
}

fun jalan(folder, akhiran = "uji_") {
    daftar = P.glob(folder + "*.ak")
    jumlah_ok = 0
    jumlah_gagal = 0
    untuk f dalam daftar {
        nama_f = teks(f)
        jika bukan teks.mengandung(nama_f, akhiran) { lanjut }
        hasil = P.jalankan(["python3", "-m", "aksara", f])
        jika hasil["kode"] == 0 {
            jumlah_ok = jumlah_ok + 1
        } lain {
            jumlah_gagal = jumlah_gagal + 1
            cetak "  GAGAL: " + f
        }
    }
    cetak "UJI: " + jumlah_ok + " ok, " + jumlah_gagal + " gagal (file berakhiran '" + akhiran + "')"
    balik jumlah_gagal
}
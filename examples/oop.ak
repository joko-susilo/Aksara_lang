kelas Rekening {
    fun buat(pemilik, saldo_awal) {
        ini.pemilik = pemilik
        ini.saldo = saldo_awal
    }
    fun tabung(jumlah) {
        ini.saldo = ini.saldo + jumlah
        balik ini.saldo
    }
    fun tarik(jumlah) {
        jika jumlah <= ini.saldo {
            ini.saldo = ini.saldo - jumlah
            balik benar
        }
        balik salah
    }
    fun info() {
        balik "Rekening " + ini.pemilik + " saldo " + ini.saldo
    }
}

rek = Rekening.buat("Andi", 100000)
cetak rek.info()
cetak rek.tabung(50000)
cetak rek.saldo
cetak rek.tarik(25000)
cetak rek.info()
cetak rek.tarik(999999999)
cetak rek.info()
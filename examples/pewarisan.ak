# OOP: Pewarisan (inheritance)
kelas Kendaraan {
    fun buat(merk) {
        ini.merk = merk
    }
    fun roda() {
        balik 0
    }
    fun deskripsi() {
        balik ini.merk + " " + ini.roda() + " roda"
    }
}

kelas Mobil dari Kendaraan {
    fun roda() {
        balik 4
    }
}

kelas Motor dari Kendaraan {
    fun roda() {
        balik 2
    }
}

m = Mobil.buat("Toyota")
mo = Motor.buat("Honda")
cetak m.deskripsi()
cetak mo.deskripsi()
cetak m.merk
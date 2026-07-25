fun bagi(a, b) {
    jika b == 0 {
        galat "Pembagi tidak boleh nol!"
    }
    balik a / b
}

coba {
    bagi(10, 0)
} kecuali sebagai e {
    cetak "Error: " + e
}

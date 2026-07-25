cetak "Simulasi pencarian angka dengan selama:"
angka = 1

selama angka <= 10 {
    jika angka == 4 {
        cetak "Lewati angka 4"
        angka = angka + 1
        lanjut
    }
    
    jika angka == 8 {
        cetak "Berhenti di angka 8"
        henti
    }

    cetak angka
    angka = angka + 1
}

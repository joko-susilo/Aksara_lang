fungsi sapa_pengguna(nama):
    jika nama == "Admin" dan benar:
        cetak("Selamat datang kembali, Master!")
    atau_jika nama == "Tamu":
        cetak("Silakan nikmati akses terbatas.")
    selain:
        cetak("Halo, " + nama + "!")

sapa_pengguna("Budi")

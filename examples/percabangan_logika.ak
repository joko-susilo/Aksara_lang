cetak "=== Uji Kombinasi Logika ==="
punya_tiket = benar
punya_identitas = salah

jika punya_tiket dan punya_identitas {
    cetak "Silakan masuk ke area konser."
} atau_jika punya_tiket atau punya_identitas {
    cetak "Data belum lengkap, mohon verifikasi ulang."
} lain {
    cetak "Dilarang masuk! Tidak punya tiket dan identitas."
}

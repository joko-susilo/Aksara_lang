cetak "=== Uji Percabangan Bersarang ==="
nilai_ujian = 85
kehadiran = 90

jika nilai_ujian >= 75 {
    cetak "Status: Lulus Ujian"
    
    jika kehadiran >= 85 {
        cetak "Predikat: Sangat Baik (Kehadiran Memenuhi)"
    } lain {
        cetak "Predikat: Baik, tapi perlu tingkatkan kehadiran"
    }
    
} lain {
    cetak "Status: Tidak Lulus"
}

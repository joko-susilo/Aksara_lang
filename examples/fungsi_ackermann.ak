fun ackermann(m, n) {
    jika m == 0 {
        balik n + 1
    } atau_jika m > 0 dan n == 0 {
        balik ackermann(m - 1, 1)
    } lain {
        balik ackermann(m - 1, ackermann(m, n - 1))
    }
}

cetak "Menghitung Ackermann(2, 2):"
cetak ackermann(2, 2)

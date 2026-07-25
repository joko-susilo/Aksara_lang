fun fibonacci(n) {
    jika n <= 1 {
        balik n
    }
    balik fibonacci(n - 1) + fibonacci(n - 2)
}

cetak "Hasil Fibonacci ke-7:"
cetak fibonacci(7)

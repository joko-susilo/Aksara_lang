cetak "Deret angka 1 sampai 15 (Kelipatan 3 atau 5):"

untuk i dalam 1 .. 15 {
    jika i % 3 == 0 dan i % 5 == 0 {
        cetak "FizzBuzz"
    } atau_jika i % 3 == 0 {
        cetak "Fizz"
    } atau_jika i % 5 == 0 {
        cetak "Buzz"
    } lain {
        cetak i
    }
}

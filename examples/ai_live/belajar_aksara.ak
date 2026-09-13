# ==========================================
# PELAJARAN 1 — Pemrograman Aksara dari Nol
# ==========================================
# Jalankan: python3 -m aksara examples/ai_live/belajar_aksara.ak

cetak "======== PELAJARAN 1: Variabel & Tipe ========"
nama = "Aksara"
angka = 12
desimal = 3.14
boo = benar
kosong = nil
cetak "String : " + nama
cetak "Angka  : " + angka
cetak "Desimal: " + desimal
cetak "Boolean: " + boo
cetak "Null   : " + kosong

# Daftar & kamus
cetak ""
cetak "======== PELAJARAN 2: Daftar & Kamus ========"
buah = ["apel", "mangga", "durian"]
cetak "Daftar buah: " + buah
cetak "Panjang: " + panjang(buah)
cetak "Index pertama: " + buah[0]
cetak "Terakhir: " + buah[panjang(buah) - 1]

# Kamus pakai [kunci: nilai]
profil = ["nama": "Joko", "umur": 30]
cetak "Profil nama: " + profil["nama"]
cetak "Kunci: " + kunci(profil)

# Rangku dalam string template
cetak ""
cetak "======== PELAJARAN 3: String & Template ========"
cetak "Nama saya {nama} dan saya berumur {profil[\"umur\"]} tahun"
cetak "String digabung: " + nama + " indah"
cetak ""
cetak "======== PELAJARAN 4: Percabangan ========"
umur = 17
jika umur >= 17 {
    cetak "Dewasa"
} atau_jika umur >= 13 {
    cetak "Remaja"
} lain {
    cetak "Anak-anak"
}

cetak ""
cetak "======== PELAJARAN 5: Perulangan ========"
cetak "for 1..3:"
untuk i dalam 1..3 {
    cetak "  i = " + i
}
cetak "foreach:"
untuk b dalam buah {
    cetak "  buah: " + b
}
cetak "while:"
n = 0
selama n < 3 {
    cetak "  n = " + n
    n = n + 1
}

cetak ""
cetak "======== PELAJARAN 6: Fungsi ========"
fun sapa(nama) {
    balik "Halo " + nama + "!"
}
cetak sapa("Bos Joko")

fun tambah(a, b = 10) {
    balik a + b
}
cetak "tambah(5): " + tambah(5)
cetak "tambah(5, 20): " + tambah(5, 20)

cetak ""
cetak "======== PELAJARAN 7: Boolean & Logika ========"
x = 5
jika x > 3 dan x < 10 {
    cetak "x antara 3-10 (DAN)"
}
jika x == 5 atau x == 100 {
    cetak "x adalah 5 atau 100 (ATAU)"
}
jika bukan (x == 0) {
    cetak "x bukan nol (BUKAN)"
}

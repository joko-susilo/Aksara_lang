

Dokumentasi Bahasa Pemrograman Aksara
Aksara adalah bahasa pemrograman berbasis bahasa Indonesia yang dirancang sebagai Source-to-Source Compiler atau Transpiler yang berjalan di atas bahasa Python. Proyek ini dioptimalkan untuk penggunaan di lingkungan Termux pada perangkat Android.
🚀 Fitur Utama
• Sintaks Bahasa Indonesia: Menggunakan kata kunci bahasa Indonesia yang natural untuk logika pemrograman.Mesin Transpiler Aman (Regex): Menggunakan modul re dengan pola word boundary (\b) untuk memastikan penggantian kata kunci tidak merusak nama variabel pengguna.Penanganan Error Kustom: Pesan kesalahan (error) telah diterjemahkan ke dalam bahasa Indonesia agar lebih ramah pengguna dan informatif, lengkap dengan informasi nomor baris.Eksekusi Global (CLI): Aksara dapat dijalankan dari direktori mana pun di terminal menggunakan perintah aksara <nama_file.ak>.Ekosistem Python: Aksara dapat menggunakan seluruh library dan pustaka yang ada di Python secara langsung.📚 Kamus Kata Kunci (Keyword Mapping)
Aksara memetakan sintaks Python ke dalam istilah bahasa Indonesia berikut:

Kategori
Aksara
Python

Logika & Alur
jika, atau_jika, selain_itu
if, elif, else

Perulangan
untuk, selama, di_dalam, rentang
for, while, in, range

Kontrol
hentikan, lanjutkan, kembalikan
break, continue, return

Fungsi & Kelas
fungsi, kelas, sebagai
def, class, as

Error Handling
coba, kecuali, akhirnya, bangkitkan
try, except, finally, raise

Input/Output
cetak, masukan, panjang
print, input, len

Tipe Data
bulat, desimal, teks, daftar, kamus_data
int, float, str, list, dict

Boolean & Nilai
benar, salah, kosong
True, False, None

Operator Logika
dan, atau, bukan
and, or, not


🛠️ Instalasi di Termux
Aksara menggunakan skrip instalasi otomatis untuk memudahkan distribusi dan penggunaan secara global.
1. Buka terminal Termux dan masuk ke folder proyek aksara_lang.Jalankan skrip instalasi:Skrip ini akan menyalin file mesin utama ke /data/data/com.termux/files/usr/bin/ dan memberikan izin eksekusi secara otomatis.💻 Cara Penggunaan
Simpan kode Anda dengan ekstensi .ak atau .aksara. Contoh file program.ak:
fungsi sapa(nama):
    cetak("Halo " + nama + "!")

nama_user = masukan("Siapa nama Anda? ")
sapa(nama_user)

angka = bulat(masukan("Masukkan angka: "))
jika angka % 2 == 0:
    cetak("Ini adalah angka genap")
selain_itu:
    cetak("Ini adalah angka ganjil")

Jalankan program melalui terminal:
aksara program.ak

⚠️ Penanganan Kesalahan (Error Handling)
Aksara akan memberikan informasi kesalahan dalam bahasa Indonesia jika terjadi masalah pada kode Anda:
• [Kesalahan Sintaks]: Muncul jika ada kesalahan penulisan, seperti tanda kutip yang belum ditutup.[Variabel Tidak Dikenal]: Muncul jika Anda menggunakan variabel yang belum dibuat.[Kesalahan Indentasi]: Muncul jika penggunaan spasi atau tab tidak konsisten.[Kesalahan Logika]: Muncul pada masalah eksekusi seperti pembagian dengan nol.🏗️ Struktur Arsitektur
Proyek ini menggunakan model All-in-One, di mana seluruh kamus dan mesin transpiler disatukan dalam satu file tunggal untuk menghindari error ModuleNotFoundError saat dijalankan secara global. Mesin ini membaca argumen baris perintah secara dinamis menggunakan sys.argv.

───

Kontributor: Dikembangkan sebagai proyek belajar pemrograman Python dan arsitektur bahasa pemrograman

# 🇮🇩 Aksara — Bahasa Pemrograman Indonesia

 "Saya cinta bahasa Indonesia."

**Aksara** adalah bahasa pemrograman modern dengan sintaks Indonesia, l.

---

## 🚀 Instalasi

```bash
pip install git+https://github.com/joko-susilo/Aksara_lang.git

Syarat: Python 3.8+
Fitur

· I/O: cetak, masukan
· Tipe Data: String, Angka, Boolean, List, Kamus, nil
· Operasi: Aritmatika, Perbandingan, Logika
· Variabel: Assignment, akses indeks, slice
· Percabangan: jika, atau_jika, lain
· Perulangan: ulang, selama, untuk, henti, lanjut
· Fungsi: fun, balik
· Error: coba, kecuali, akhirnya, galat
· Interop: impor modul Python
. String Template
. Null Coalescing
. Iterasi List
. #AI Built-in

Aksara punya fitur AI bawaan tanpa install library!

| Fitur | Fungsi | Contoh |
|-------|--------|--------|
| `tebak(data)` | Prediksi angka | `tebak([1,2,3])` → `[4,5]` |
| `jenis(teks)` | Sentimen teks | `jenis("bagus!")` → `positif` |
| `ringkas(teks)` | Ringkasan | `ringkas(teks_panjang)` |
| `kelompok(data, n)` | Clustering | `kelompok([1,2,10,11], 2)` |

### Contoh
```aksara
cetak tebak([10, 20, 30])          // [40, 50]
cetak jenis("keren banget!")       // positif
cetak ringkas("Kalimat panjang...") // Ringkasan
cetak kelompok([1,2,10,11], 2)     // [[1,2],[10,11]]
```
# 🇮🇩 Aksara — Bahasa Pemrograman Indonesia

"Saya cinta bahasa Indonesia."

**Aksara** adalah bahasa pemrograman modern dengan sintaks bahasa Indonesia,
berjalan di atas Python 3.8+ (interpreter + transpiler ke Python), nyaman
digunakan di Termux (Android).

Dokumentasi lengkap: [docs/aksara.md](docs/aksara.md)

---

## 🚀 Instalasi

### Linux / Windows / macOS
```bash
pip install aksara-lang
```

### Termux (Android)
```bash
# Install NumPy (wajib untuk fitur AI)
pkg install python-numpy

# Lalu install Aksara
pip install aksara-lang
```

## 💻 Mulai cepat

```aksara
fun sapa(nama) {
    balik "Halo " + nama + "!"
}

untuk i dalam 1..3 {
    cetak sapa("teman ke-" + i)
}
```

```bash
aksara program.ak
```

## Fitur inti

· I/O: `cetak`, `masukan`
· Tipe data: angka, string + template `{var}`, boolean, daftar, kamus, `nil`
· Operator: aritmatika, perbandingan, logika (`dan`, `atau`, `bukan`), null-coalescing `??`
· Variabel: assignment, akses indeks, slice inklusif (`data[1..3]`)
· Percabangan: `jika`, `atau_jika`, `lain`
· Perulangan: `ulang`, `selama`, `untuk a..b` (rentang inklusif), `untuk x dalam daftar`, `henti`, `lanjut`
· Fungsi: `fun`, `balik` (ber-closure)
· Kesalahan: `coba`, `kecuali [Tipe] sebagai e`, `akhirnya`, `galat`
· Interop: `impor "modul" sbg nama` (modul Python) dan `impor "larik.ak"` (file Aksara)
· Kompiler: `aksara file.ak -c` menghasilkan Python murni dari program Aksara

## 🤖 AI Built-in (tanpa library tambahan)

| Fitur | Fungsi | Contoh |
|-------|--------|--------|
| `tebak(data)` | Prediksi 2 langkah (regresi linear) | `tebak([10, 20, 30])` → `[50.0, 60.0]` |
| `jenis(teks)` | Sentimen teks | `jenis("bagus!")` → `positif` |
| `ringkas(teks)` | Ringkasan | `ringkas(teks_panjang)` |
| `kelompok(data, n)` | Clustering | `kelompok([1,2,10,11], 2)` → `[[1, 2], [10, 11]]` |

Ada pula `frekuensi`, `normalisasi`, `korelasi`, `cari_mirip`, `rekomendasi`,
`encode`, `acak_cerdas`, `deteksi_bahasa`, `periksa_ejaan`, `auto_label`,
`urutkan_ai`, `cluster_teks`, `ubah_gaya`, `ekstrak_entitas`,
`simulasi_keputusan`, `rangking_tfidf`, `pca`, `jaring_syaraf`.

## 🧪 Pengembangan

```bash
pip install pytest
pytest tests/
```

## 🏗️ Arsitektur

```
lexer → parser → AST → interpreter (jalan langsung)
                    └→ compiler (AST → Python)
```

Bagian AI ada di `aksara/ai/`, pustaka standar array di `stdlib/larik.ak`.

---

Dikembangkan sebagai proyek belajar pemrograman Python dan arsitektur bahasa pemrograman.
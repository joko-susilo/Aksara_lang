# Dokumentasi Bahasa Pemrograman Aksara

Aksara adalah bahasa pemrograman berbasis bahasa Indonesia yang berjalan di atas
Python. Kode sumber Aksara diurai menjadi AST lalu dijalankan oleh *interpreter*
(tree-walker), atau dikompilasi menjadi Python murni (*transpiler*).

Proyek ini dioptimalkan untuk Python 3.8+ dan nyaman dipakai di Termux (Android).

---

## Pemasangan

```bash
# Linux / Windows / macOS
pip install aksara-lang

# Termux (Android) — NumPy dipakai fitur AI
pkg install python-numpy
pip install aksara-lang
```

Setelah terpasang, perintah `aksara` tersedia global.

## Mulai Cepat

Simpan dengan ekstensi `.ak` (mis. `program.ak`):

```aksara
# komentar diawali tanda pagar
fun sapa(nama) {
    balik "Halo " + nama + "!"
}

nama_user = masukan("Siapa nama Anda? ")
cetak sapa(nama_user)

angka = bulat(masukan("Masukkan angka: "))
jika angka % 2 == 0 {
    cetak "Angka genap"
} lain {
    cetak "Angka ganjil"
}
```

Jalankan:

```bash
aksara program.ak
```

Blok kode memakai kurung kurawal `{ }` (bukan indentasi). Baris-baris di dalam
satu blok tidak wajib menyatu; penulisan bebas seperti contoh berikut:

```aksara
cetak "ini masih satu blok dengan if"
```

## Referensi Bahasa

### Komentar

Awali dengan `#` sampai akhir baris:

```aksara
# ini komentar
cetak "halo"  # komentar di akhir baris
```

### Tipe Data Dasar

| Tipe | Nilai | Contoh |
|------|-------|--------|
| Angka | bilangan bulat atau desimal | `42`, `3.14`, `-7` |
| String | teks dalam kutip ganda | `"halo"` |
| Boolean | `benar` / `salah` | `benar` |
| Nil | tidak ada nilai | `nil` |
| Daftar | list berurutan | `[1, 2, 3]` |
| Kamus | pasangan kunci-nilai | `["a": 1, "b": 2]` |

String mendukung escape: `\n` (baris baru), `\t` (tab), `\"` (kutip),
`\\` (garis miring), `\uXXXX` (Unicode):

```aksara
cetak "baris\nbaru"
cetak "cinta \u2764"   # cinta ❤
```

#### String Template

Di dalam string, `{nama_variabel}` disisipi nilainya:

```aksara
nama = "Aksara"
versi = 2
cetak "{nama} versi {versi}"   # Aksara versi 2
```

### Variabel

Assignment memakai `=`; operator gabungan `+=`, `-=`, `*=`, `/=`, `%=`
mengubah dan menetapkan sekaligus. Variabel bisa dipakai tanpa deklarasi tipe:

```aksara
nama = "Eka"
umur = 30
umur += 1          # 31
skor *= 2
hasil = [10, 20]
profil = ["nama": nama, "umur": umur]
```

`cetak` menerima beberapa argumen (dipisah spasi saat dicetak), dan string
bisa memakai kutip tunggal atau ganda:

```aksara
cetak "Nilai:", skor, "poin"   # Nilai: ... poin
teks = 'kutip tunggal juga boleh'
```

### Operator

| Kategori | Operator |
|----------|----------|
| Aritmatika | `+ - * / % **` |
| Perbandingan | `== != < > <= >=` |
| Logika | `dan`, `atau`, `bukan` |
| Null Coalescing | `??` |

Catatan: `+` yang salah satu operand-nya string akan menyatukan keduanya
sebagai teks. Umum aja: khusus string, `*` bisa mengulang (`"ha" * 3`).

```aksara
cetak "Nilai: " + 5        # Nilai: 5
cetak benar dan salah      # False
nama = nil
cetak nama ?? "Tanpa nama" # Tanpa nama
```

### Daftar (List)

```aksara
buat = []
buah = ["apel", "mangga", "jeruk"]
cetak buah[0]        # apel
buah[1] = "pisang"   # ubah elemen
```

#### Slice (tambahan)

Potongan `a..b` bersifat **inklusif** di kedua ujungnya:

```aksara
data = [10, 20, 30, 40, 50]
cetak data[1..3]   # [20, 30, 40]
cetak data[2..]    # [30, 40, 50]
cetak data[..2]    # [10, 20, 30]
```

### Kamus (Dict)

```aksara
profil = ["nama": "Eka", "umur": 30]
cetak profil["nama"]       # Eka
profil["kota"] = "Jakarta"
cetak kunci(profil)        # ['nama', 'umur', 'kota']
```

### Percabangan

```aksara
jika skor >= 90 {
    cetak "A"
} atau_jika skor >= 80 {
    cetak "B"
} lain {
    cetak "C"
}
```

### Perulangan

#### `ulang` — sejumlah kali

```aksara
ulang 3 { cetak "beep" }
```

#### `untuk` — atas rentang

Rentang `a..b` inklusif (termasuk `b`):

```aksara
untuk i dalam 1..5 {
    cetak i          # 1 2 3 4 5
}
```

#### `untuk` — atas daftar

```aksara
untuk item dalam [10, 20, 30] {
    cetak item
}
```

#### `selama` — selama kondisi benar

```aksara
x = 5
selama x > 0 {
    cetak x
    x = x - 1
}
```

`henti` (break) menghentikan perulangan, `lanjut` (continue) melompat ke
iterasi berikutnya:

```aksara
untuk i dalam 1..10 {
    jika i == 2 { lanjut }
    jika i == 5 { henti }
    cetak i        # 1 3 4
}
```

### Fungsi

```aksara
fun tambah(a, b) {
    balik a + b
}

cetak tambah(3, 4)   # 7
```

- Deklarasi: `fun nama(param, ...) { ... }`
- Kembalian: `balik ekspresi`
- Tanpa `balik`, fungsi mengembalikan `nil`.
- Fungsi memakai *closure*: bisa membaca variabel dari lingkup pembuatnya.
- Parameter bisa punya nilai default; pemanggilan bisa memakai kata kunci:

```aksara
fun sapa(nama, sapaan = "Halo") {
    balik sapaan + ", " + nama
}

cetak sapa("Budi")            # Halo, Budi
cetak sapa("Budi", "Yo")      # Yo, Budi
cetak sapa("Budi", sapaan = "Assalamu")   # Assalamu, Budi
# Builtin juga: jaring_syaraf(X, y, hidden = 8, iterasi = 500)
```

### Kelas & Objek (OOP)

Deklarasi kelas dengan `kelas`; isi dengan `fun` (metode). Di dalam metode,
`ini` merujuk objek yang memanggil (mirip `self`). Konstruktor adalah metode
yang dipanggil lewat `NamaKelas.metode(...)` — membuat objek baru, menjalankan
metodenya, lalu mengembalikan objek tsb.

```aksara
kelas Rekening {
    fun buat(pemilik, saldo_awal) {
        ini.pemilik = pemilik
        ini.saldo = saldo_awal
    }
    fun tabung(jumlah) {
        ini.saldo = ini.saldo + jumlah
        balik ini.saldo
    }
    fun info() {
        balik "Rekening " + ini.pemilik + " saldo " + ini.saldo
    }
}

rek = Rekening.buat("Andi", 100000)
cetak rek.info()          # Rekening Andi saldo 100000
cetak rek.tabung(50000)   # 150000
cetak rek.saldo           # 150000
```

Aturan:
- `kelas Nama { ... }` memuat metode (fungsi).
- Panggilan `NamaKelas.metoda(args)` = konstruktor (mengembalikan objek).
- Panggilan `objek.metoda(args)` memanggil metode pada instance.
- `ini.atribut = nilai` membaca/menulis atribut objek.
- Metode dapat memanggil metode lain pada objek yang sama (`ini.metode()`).

#### Pewarisan (inheritance)

`kelas Anak dari Induk { ... }` menurunkan metode induk; metode senama akan
menimpa (override). Di dalam metode, `induk.metode(...)` memanggil versi
induk (super), bahkan bertingkat:

```aksara
kelas Bentuk {
    fun buat(nama) { ini.nama = nama }
    fun luas() { balik 0 }
}
kelas Persegi dari Bentuk {
    fun buat(sisi) {
        induk.buat("persegi")
        ini.sisi = sisi
    }
    fun luas() { balik induk.luas() + ini.sisi * ini.sisi }
}
p = Persegi.buat(5)
cetak p.luas()          # 25
```

Contoh lengkap: `examples/oop.ak`, `examples/pewarisan.ak`.

### Kesalahan

Melempar galat:

```aksara
jika saldo < 0 {
    galat "Saldo tidak boleh negatif"
}
```

Menangkap galat — `coba`, `kecuali` (dengan atau tanpa tipe), `akhirnya`:

```aksara
coba {
    x = 10 / 0
} kecuali [ZeroDivisionError] sebagai e {
    cetak "tertangkap: " + e
} kecuali sebagai e {
    cetak "galat lain: " + e
} akhirnya {
    cetak "selalu dijalankan"
}
```

Tipe error yang bisa dipakai: tipe Python apa pun, mis. `ValueError`,
`TypeError`, `IndexError`, `KeyError`, `NameError`, `RuntimeError`.

### Impor

Memuat modul Python:

```aksara
impor "os" sbg os
cetak os.getcwd()

impor "math" sbg mt
cetak mt.sqrt(16)
```

Memuat file sumber Aksara lain (mis. isi `stdlib/larik.ak`):

```aksara
impor "larik.ak" sbg lk
data = [10, 20, 30, 40, 50]
cetak lk.rata_rata(data)
```

### Fungsi Bawaan (Builtins)

| Kelompok | Fungsi |
|----------|--------|
| I/O | `cetak(...)`, `masukan(prompt)` |
| Konversi | `bulat(x)`, `desimal(x)`, `teks(x)`, `daftar(...)` |
| Koleksi | `panjang(x)`, `dorong(daftar, x)` |
| Kamus | `kunci`, `nilai`, `isi`, `ada`, `kosong`, `hapus`, `tambah`, `gabung`, `salin`, `bersihkan`, `dapatkan`, `tukar` |
| AI | `tebak`, `jenis`, `ringkas`, `kelompok`, `frekuensi`, `normalisasi`, `korelasi`, `cari_mirip`, `rekomendasi`, `encode`, `acak_cerdas`, `deteksi_bahasa`, `periksa_ejaan`, `auto_label`, `urutkan_ai`, `cluster_teks`, `ubah_gaya`, `ekstrak_entitas`, `simulasi_keputusan`, `rangking_tfidf`, `pca`, `jaring_syaraf` |

Fungsi buatan sendiri bisa menaungi builtin yang namanya sama.

### Pustaka Standar

Modul-modul dalam folder `stdlib/` (dipakai lewat `impor "modul.ak" sbg x`):

| Modul | Isi |
|-------|-----|
| `teks.ak` | String: `huruf_besar`, `huruf_kecil`, `potong_teks`, `pisahkan`, `gabungkan`, `ganti`, `mengandung`, `awalan`, `akhiran`, `balik_teks`, `cari`, `jumlah_kata`, `judul`, `cek_kosong`, `ulang_teks`, `sub_teks` |
| `mtk.ak` | Matematika: `mutlak`, `pangkat`, `akar`, `bulatkan`, `bulat_atas`, `bulat_bawah`, `genap`, `ganjil`, `terbesar`, `terkecil`, `acak`, `pilihan_terbanyak` |
| `koleksi.ak` | Daftar: `urutkan`, `urutkan_balik`, `unik`, `balik_list`, `gabung_list`, `cari_indeks`, `hitung`, `potong`, `hapus_index` |
| `berkas.ak` | File: `baca_file`, `baca_baris`, `tulis_file`, `tambah_ke_file`, `apakah_ada`, `hapus_file`, `ukuran_file`, `folder_sekarang`, `daftar_folder`, `wujud_folder` |
| `waktu.ak` | Waktu: `detik_sekarang`, `waktu_teks`, `waktu_teks_kustom`, `tahun`, `bulan`, `hari`, `jam`, `menit`, `detik`, `tidur` |
| `ml.ak` | Machine Learning: `latih`, `ramal` (regresi), `latih_klasifikasi`, `ramal_klasifikasi` (softmax) |
| `model.ak` | Simpan/muat model: `simpan(model, jalan)`, `muat(jalan)` (JSON) |
| `vektor.ak` | Vektor: `dot`, `norma`, `normalisasi`, `kosinus`, `jumlah` |
| `data.ak` | Data & metrik AI: `bagi`, `akurasi`, `galat_rata`, `ambil_selisih` |
| `json.ak` | JSON: `urai(teks)`, `ubah(data)`, `ubah_indah(data)` |
| `csv.ak` | CSV: `baca(jalan)`, `tulis(jalan, baris)`, `baca_kamus(jalan)` |
| `web.ak` | HTTP: `dapat`, `dapat_teks`, `dapat_json`, `kirim`, `status`, `header` *(butuh `requests`)* |
| `llm.ak` | LLM: `tanya`, `ringkas_teks`, `terjemahkan`, `tulis_kode`, `tulis_puisi` (format OpenAI-compatible; butuh `requests` + API key) |
| `larik.ak` | Statistik array: `rata_rata`, `jumlah`, `maksimum` (`terbesar`), `minimum`, `rentang`, `median`, `variansi`, `simpangan_baku`, `normalisasi`, `skala`, `tebak`, `kelompok`, `outlier`, `pola`, `frekuensi` |

Contoh portofolio AI (dengan output terukur): lihat `PORTFOLIO.md` dan
demo di `examples/ai_live/`.

Contoh:

```aksara
impor "teks.ak" sbg t
impor "mtk.ak" sbg m
impor "berkas.ak" sbg b

cetak t.judul("halo dunia")          # Halo Dunia
cetak m.akar(16)                      # 4.0
cetak b.baca_file("catatan.txt")      # isi file
```

Contoh lengkap: `examples/stdlib.ak`.

### Panggil LLM dari Bahasa Aksara

Modul `llm.ak` menghubungkan Aksara dengan model bahasa (format
OpenAI-compatible: Groq, OpenAI, Gemini, Ollama lokal):

```bash
GROQ_API_KEY=sk-... aksara program.ak
```

```aksara
impor "llm.ak" sbg llm

cetak llm.tulis_puisi("bahasa pemrograman Indonesia")
cetak llm.terjemahkan("Halo dunia", "Jawa")
```

Contoh agent (AI menulis program Aksara lalu menjalankannya):
`examples/ai_live/agent_ak.ak`. Demo dasar: `examples/ai_live/llm.ak`.

## Perintah CLI

```bash
aksara                    # masuk REPL interaktif
aksara program.ak        # jalankan
aksara program.ak -t     # tampilkan token hasil lexer
aksara program.ak -a     # tampilkan AST
aksara program.ak -c     # kompilasi ke Python (output di stdout)
aksara -v                # versi
```

### REPL Interaktif

Tanpa argumen file, Aksara membuka REPL:

```
aksara> 1 + 1
2
aksara> nama = "Eka"
aksara> "Halo " + nama
'Halo Eka'
aksara> x = 5
aksara> jika x > 3 {
...    cetak "besar"
... }
besar
```

- Ekspresi murni otomatis dicetak nilainya; boolean tampil `benar`/`salah`.
- Environment persisten: variabel & fungsi bertahan antar baris.
- Blok `{ }` yang belum seimbang memunculkan prompt lanjutan `...`.
- Fungsi panjang bisa ditulis dalam mode blok: baris awal `:`, akhiri `:EOF`.
- Keluar dengan `keluar`, `quit`, `exit`, `:q`, atau Ctrl-D.
- Jika didukung sistem, riwayat panah atas/bawah (readline) tersedia.

#### Perintah REPL

| Perintah | Fungsi |
|----------|--------|
| `:help` | tampilkan bantuan |
| `:vars` | tampilkan variabel & fungsi yang terdefinisi |
| `:reset` | hapus semua variabel & fungsi |
| `:load <file.ak>` | muat & jalankan file Aksara |
| `:history` | tampilkan riwayat perintah |
| `:q` / `:quit` | keluar dari REPL |

## Arsitektur

```
program.ak
    │
    ▼
  Lexer (aksara/lexer/tokenizer.py)   teks → token
    │
    ▼
 Parser (aksara/parser/parser.py)     token → AST (aksara/ast/nodes.py)
    │
    ├───────────────► Interpreter (aksara/interpreter/evaluator.py)
    │                    eksekusi langsung, environment ber-scope
    │
    └───────────────► Compiler (aksara/compiler/python.py)
                         AST → kode Python murni
```

- **Interpreter**: evaluator pohon (tree-walker) dengan environment berantai
  (`aksara/interpreter/environment.py`) untuk closure di fungsi.
- **Compiler**: menyusun AST menjadi Python yang setara semantik, termasuk
  rentang inklusif, `??`, string template, dan impor modul `.ak` (dimuat
  lewat runtime pada saat program dijalankan).
- **AI builtin**: `aksara/ai/*` (prediksi, NLP, clustering, dsb.) — opsional
  memakai NumPy pada sebagian modul.
- Model file: paket Python satu proyek; CLI via `[project.scripts] aksara`.

## Menjalankan Tes

```bash
pip install pytest
pytest tests/
```

Berisi uji lexer, parser, kesetaraan interpreter↔kompiler, dan regresi.

## Keterbatasan & Peta Jalan

- String hanya kutip ganda & tunggal; belum ada apit tiga baris.
- `cetak` memakai beberapa argumen (dipisah spasi); multi-baris string belum.
- Tidak ada tuple; daftar dan kamus sudah cukup untuk mayoritas kasus.
- Pesan error interpreter berbahasa Indonesia; hasil kompilasi memakai pesan
  Python asli.
- Peta jalan: rilis 0.6.0 (stabilkan API), dokumentasi lengkap, contoh lebih
  banyak, dan optimasi numerik lewat NumPy.

---

Kontributor: dikembangkan sebagai proyek belajar pemrograman Python dan
arsitektur bahasa pemrograman.
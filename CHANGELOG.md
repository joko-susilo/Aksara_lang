# Changelog

Semua perubahan penting proyek Aksara dicatat di sini.
Format mengikuti [Keep a Changelog](https://keepachangelog.com/id/1.1.0/);
versi mengikuti [Semantic Versioning](https://semver.org/).

## [0.10.0] - 2026-09-06

### Ditambahkan
- Pemanggilan fungsi dengan **kata kunci (kwargs)** dan **nilai default
  parameter**: `fun f(a, b = 2)` + `f(1, b = 9)`; berlaku untuk fungsi,
  metode, konstruktor, dan builtin (mis. `jaring_syaraf(..., iterasi=500)`).
- Stdlib praktis: `json.ak` (urai/ubah), `csv.ak` (baca/tulis/kamus),
  `web.ak` (HTTP via `requests`).
- String yang memuat `{`/`}` non-template (mis. JSON) tidak lagi salah
  diurai sebagai template.
- Contoh & tes baru (total 100 tes).

## [0.9.0] - 2026-09-06

### Ditambahkan — Visi AI-first
- Parsing OOP selesai: pewarisan `kelas Anak dari Induk`, override, dan
  `induk.metode(...)` (super) bertingkat. (0.8.0 menambah kelas/`ini`.)
- Stdlib AI: `ml.ak` (`latih`, `ramal`) dan `data.ak` (`bagi`, `akurasi`,
  `galat_rata`, `ambil_selisih`).
- `ramal()` di `aksara/ai/jaring_syaraf.py`: prediksi dari model yang
  dilatih; genre jaringan saraf ditingkatkan (standardisasi fitur + init He)
  sehingga benar-benar belajar.
- Builtin baru: `ramal`.
- Contoh `examples/ai_first.ak`, `examples/pewarisan.ak`; tes
  `tests/test_inherits.py`, `tests/test_ai.py` (total 87 tes).

## [0.8.0] - 2026-09-06

### Ditambahkan
- OOP: `kelas`, metode (`fun` di dalam kelas), dan `ini` (self).
  Konstruktor dipanggil lewat `NamaKelas.metode(...)`; instance memakai
  `obj.metode(...)` dan `obj.atribut`.
- Parser: suffix `.atribut`/`(panggil)`/`[indeks]` kini berlaku juga untuk
  `ini` (via `_lanjut_suffix`).
- Runtime OOP baru `aksara/interpreter/oop.py` (KelasValue, ObjekAksara)
  dipakai bersama oleh interpreter dan hasil kompilasi.
- Contoh `examples/oop.ak`, tes `tests/test_oop.py` (total 77 tes).

## [0.7.0] - 2026-09-06

### Ditambahkan
- Pustaka standar (.ak) di `stdlib/`: `teks.ak`, `mtk.ak`, `koleksi.ak`,
  `berkas.ak`, `waktu.ak` (di samping `larik.ak`).
- Builtin `dorong(daftar, x)` untuk menambahkan elemen ke daftar.
- Contoh `examples/stdlib.ak` dan tes `tests/test_stdlib.py`
  (total 70 tes).

### Diperbaiki
- `larik.ak`: `normalisasi`, `skala`, `kelompok` (dan fungsi yang memakai
  pola append) kini berfungsi berkat `dorong`.

## [0.6.2] - 2026-09-06

### Ditambahkan
- Perintah REPL: `:help`, `:vars`, `:reset`, `:load <file.ak>`,
  `:history`, `:q`/`:quit`.
- Riwayat panah atas/bawah via readline bila tersedia.
- Perintah REPL ikut tercatat di `:history`.
- `tests/test_repl.py` bertambah (total 63 tes).

## [0.6.1] - 2026-09-06

### Ditambahkan
- REPL interaktif: `aksara` tanpa argumen file membuka prompt `aksara>`,
  environment persisten antar baris, nilai ekspresi murni dicetak otomatis
  (boolean tampil `benar`/`salah`), blok multi-baris dicari hingga `{ }`
  seimbang, mode blok panjang dengan baris `:` diakhiri `:EOF`.
  Keluar dengan `keluar`/`quit`/`exit` atau Ctrl-D.
- Literal boolean/null dan `bukan` kini bisa menjadi awal statement
  (`benar dan salah` valid); `tests/test_repl.py` (8 tes).

### Diperbaiki
- Output `cetak` di REPL dialihkan ke aliran REPL (tidak bocor ke stdout).

## [0.6.0] - 2026-09-06

### Ditambahkan
- Kompiler Aksara → Python kini lengkap: semua node AST didukung
  (boolean, daftar & kamus, slice inklusif, `??`, perulangan, `jika/elif`,
  `coba/kecuali/finally`, impor modul Python & file `.ak`, builtin
  diimpor otomatis).
- CLI: flag `-c` / `--compile` untuk mencetak hasil kompilasi Python.
- Escape string: `\n`, `\t`, `\"`, `\\`, `\uXXXX` (lexer + `ast.literal_eval`).
- `untuk ... dalam <ekspresi>` kini menerima ekspresi umum: literal daftar,
  hasil pemanggilan fungsi, dan rentang dengan batas variabel.
- `Fungsi.__call__` untuk memanggil fungsi Aksara dari Python luar (interop
  modul lokal).
- Dokumentasi lengkap ditulis ulang (`docs/aksara.md`) dan README
  diperbarui.
- Suite pengujian: `tests/test_compiler.py`, `tests/test_hardening.py`,
  `tests/conftest.py` (total 48 tes).

### Diperbaiki
- Interpreter: `henti`/`lanjut` kini benar-benar keluar/melanjutkan
  perulangan (sebelumnya tertelan di evaluasi blok).
- Interpreter: `balik` di dalam blok `coba` tidak lagi tertangkap oleh
  `kecuali` sebagai error.
- Interpreter: fungsi buatan pengguna kini menaungi builtin senama.
- Interpreter: `AksesIndeks` meneruskan tipe error asli, sehingga
  `kecuali [IndexError]` berfungsi.
- Interpreter: assignment ke atribut objek Python (`obj.nama = ...`)
  diperbaiki.
- Stdlib `larik.ak` kini ikut ter-package dan bisa ditemukan dari folder
  paket saat pemasangan `pip`.

### Proyek
- Versi 0.6.0.
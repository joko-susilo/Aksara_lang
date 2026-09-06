# 🧠 Portofolio AI — Bahasa Aksara

Kumpulan kerja AI yang ditulis dalam **Aksara** (bahasa pemrograman Indonesia,
AI-first). Semua output di bawah adalah **hasil eksekusi asli** (`aksara <nama.ak>`),
bukan ilustrasi.

Bahasa Aksara: https://github.com/joko-susilo/Aksara_lang

---

## 1. Regresi — Estimasi harga rumah

**Masalah:** dari data luas ruangan (m²) → harga (juta Rupiah), latih model,
simpan ke file, muat lagi, lalu ramal luas baru.

**Kode** (`examples/ai_live/regresi_rumah.ak`):

```aksara
impor "ml.ak" sbg ml
impor "model.ak" sbg mo
impor "data.ak" sbg d

X = [[30], [40], [50], [60], [70], [80], [90], [100]]
y = [45, 60, 75, 90, 105, 120, 135, 150]

model = ml.latih(X, y, 8, 1000, 0.1)   # jaringan saraf numpy, deterministik
cetak "Galat rata-rata: " + d.galat_rata(y, ml.ramal(model, X))

mo.simpan(model, "model_rumah.aksm")
model2 = mo.muat("model_rumah.aksm")
cetak ml.ramal(model2, [[95], [110], [150]])
```

**Hasil asli:**

```
== Latih jaringan saraf (8 data) ==
Galat rata-rata di data latih: 0.006462499999997817

== Prediksi luas baru ==
Luas 95 m2 -> sekitar 142 juta
Luas 110 m2 -> sekitar 164 juta
Luas 150 m2 -> sekitar 224 juta
```

**Yang ditunjukkan:** latih jaringan saraf, ukur galat, persistensi model,
prediksi generalisasi. Nilai mendekati hubungan linear 1.5 juta/m².

---

## 2. Klasifikasi — Sentimen ulasan (Bahasa Indonesia)

**Masalah:** tentukan sentimen ulasan produk (positif/negatif/netral) otomatis.

**Kode** (`examples/ai_live/sentimen.ak`):

```aksara
ulasan = [
    "Produknya bagus dan keren, sangat suka",       # harap: positif
    "Pengiriman lambat dan buruk, kecewa sekali",   # harap: negatif
    "Biasa saja, tidak ada yang istimewa",          # harap: netral
]

cocok = 0
untuk i dalam 0 .. panjang(ulasan) - 1 {
    has = jenis(ulasan[i])
    jika has == label[i] { cocok = cocok + 1 }
}
cetak "Akurasi: " + (cocok / panjang(ulasan)) * 100 + "%"
```

**Hasil asli:**

```
[v] 'Produknya bagus dan k...' -> positif (harap: positif)
[v] 'Pengiriman lambat dan...' -> negatif (harap: negatif)
[v] 'Mantap, kualitas luar...' -> positif (harap: positif)
[v] 'Payah, boros dan cepa...' -> negatif (harap: negatif)
[v] 'Biasa saja, tidak ada...' -> netral (harap: netral)

Akurasi: 100.0% (5/5)
```

**Yang ditunjukkan:** klasifikasi teks NLP Indonesia, evaluasi akurasi,
including contoh netral (not-a-simple-two-class).

---

## 3. Deteksi anomali

**Masalah:** temukan transaksi mencurigakan dalam data belanja harian.

**Kode** (`examples/ai_live/anomali.ak`): memakai `larik.outlier` —
nilai di luar 2× simpangan baku.

**Hasil asli:**

```
Data belanja harian:
[5, 6, 5, 7, 900, 6, 5, 1000, 6, 7]

Anomali terdeteksi:
  !! 1000 (di luar pola normal)

Rata-rata normal (tanpa anomali): 5.875
```

**Yang ditunjukkan:** statistik (rata-rata, variansi, simpangan baku),
deteksi outlier ala standar (2σ), dan "membersihkan" data sebelum analisis.

---

## 4. Pencarian dokumen mirip (vektor + kosinus)

**Masalah:** dari 5 dokumen, cari mana yang paling mirip dengan kueri — via
bag-of-words → vektor → kesamaan kosinus.

**Kode** (`examples/ai_live/cari_dokumen.ak`): membangun vektor fitur manual,
`vektor.kosinus` untuk kemiripan.

**Hasil asli:**

```
Kueri: 'belajar machine learning bahasa indonesia'

  dokumen 0 -> kemiripan 67%
  dokumen 1 -> kemiripan 0%
  dokumen 2 -> kemiripan 0%
  dokumen 3 -> kemiripan 100%
  dokumen 4 -> kemiripan 0%

Paling mirip: dokumen 3 => 'belajar machine learning dengan bahasa indonesia'
```

**Yang ditunjukkan:** dasar *information retrieval* / semantic-lite — vektor
fitur + metrik kemiripan, tanpa library eksternal.

---

## 5. Integrasi LLM (butuh API key)

`examples/ai_live/llm.ak` & `agent_ak.ak` — memanggil model bahasa (Groq/
OpenAI-compatible) dan **membiarkan AI menulis program Aksara lalu
menjalankannya dari dalam Aksara**. Butuh `GROQ_API_KEY`.

```bash
GROQ_API_KEY=sk-... aksara examples/ai_live/agent_ak.ak
```

---

## Cara menjalankan ulang

```bash
pip install aksara-lang numpy requests
aksara examples/ai_live/regresi_rumah.ak
aksara examples/ai_live/sentimen.ak
aksara examples/ai_live/anomali.ak
aksara examples/ai_live/cari_dokumen.ak
```

Tanpa perlu GPU/server — jalan di laptop atau HP (Termux).

---

*Ditulis dengan bahasa Indonesia dgn hasil terukur — portofolio AI + bahasa
pemrograman AI-first.*
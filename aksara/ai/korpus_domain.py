# Copyright 2026 Joko Susilo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Korpus DOMAIN fokus (untuk training model sendiri): bug hunting, Python,
Aksara, JavaScript, Kotlin — ditulis Bahasa Indonesia naratif.

Berisi kalimat-kalimat pengetahuan (bukan instruksi berbahaya) — menjelaskan
konsep, metodologi, dan prinsip kerja. Cocok untuk melatih Mini-LM supaya
model belajar fluent di ranah ini.
"""

SENTENSI = [
    # --- BUG HUNTING & KEAMANAN (defensif/metodologi) ---
    "Bug hunting adalah proses mencari kerentanan pada perangkat lunak dan melaporkannya secara bertanggung jawab.",
    "Bug bounty adalah program yang memberikan hadiah kepada peneliti keamanan yang menemukan celah.",
    "Langkah pertama bug hunting adalah membaca ruang lingkup dan aturan program dengan teliti.",
    "Recon pasif dilakukan tanpa menyentuh target, misalnya enumerasi subdomain dan melihat arsip wayback.",
    "IDOR terjadi ketika objek milik pengguna lain bisa diakses dengan mengubah identitas pada permintaan.",
    "Pengujian IDOR dilakukan dengan membandingkan respons akun pertama dan akun kedua.",
    "XSS adalah celah injeksi skrip pada halaman web akibat input yang tidak diolah dengan benar.",
    "SQL injection terjadi ketika input dijalankan sebagai bagian dari perintah database.",
    "Laporan yang baik menjelaskan dampak, langkah reproduksi, dan bukti yang jelas.",
    "Jangan pernah mengeksploitasi kerentanan untuk keuntungan pribadi. Laporkan dengan jujur.",
    "Penetration testing menguji keamanan sistem dengan izin pemilik dan ruang lingkup yang jelas.",
    "SSRF terjadi ketika server diminta mengakses sumber daya internal tanpa validasi URL.",
    "Otentikasi adalah cara memverifikasi siapa pengguna, sedangkan otorisasi menentukan apa yang boleh dilakukan.",
    "Rate limit melindungi sistem dari serangan berulang seperti percobaan kata sandi.",
    "Menjaga kerahasiaan data adalah tanggung jawab setiap pengembang aplikasi.",

    # --- PYTHON ---
    "Python adalah bahasa pemrograman yang mudah dibaca dan cocok untuk pemula.",
    "Variabel di Python dibuat dengan menulis nama lalu tanda sama dengan nilai.",
    "Daftar di Python ditulis dengan kurung siku dan bisa diisi berbagai jenis data.",
    "Fungsi di Python didefinisikan dengan kata kunci def diikuti nama fungsi.",
    "Kamus di Python menyimpan pasangan kunci dan nilai dengan kurung kurawal.",
    "Perulangan for di Python mengunjungi setiap elemen pada urutan data.",
    "Modul numpy menyediakan operasi matematika pada larik yang efisien.",
    "Try dan except di Python menangani kesalahan agar program tidak berhenti mendadak.",
    "Lambda di Python adalah fungsi anonim satu baris yang praktis.",
    "List comprehension adalah cara ringkas membuat daftar baru dari daftar lain.",

    # --- AKSARA ---
    "Aksara adalah bahasa pemrograman Indonesia yang dibuat untuk kecerdasan buatan.",
    "Di Aksara, output dicetak dengan kata cetak diikuti teks atau angka.",
    "Variabel di Aksara ditulis dengan nama lalu tanda sama dengan nilai.",
    "Fungsi di Aksara didefinisikan dengan kata kunci fun diikuti nama fungsi.",
    "Perulangan untuk di Aksara mengunjungi rentang angka atau daftar.",
    "Percabangan jika dan atau_jika di Aksara digunakan untuk pilihan kondisi.",
    "Modul di Aksara diimpor dengan kata impor dan diberi nama dengan sbg.",
    "Aksara bisa memanggil pustaka Python lewat impor untuk tugas numerik.",
    "Model bahasa Aksara bisa dilatih dari teks Indonesia tanpa API pihak lain.",
    "Kosakata Aksara dikompresi dengan BPE agar hemat memori di perangkat kecil.",

    # --- JAVASCRIPT ---
    "JavaScript adalah bahasa pemrograman yang berjalan di peramban dan server.",
    "Variabel di JavaScript dideklarasikan dengan let atau const.",
    "Fungsi panah di JavaScript ditulis dengan tanda panah setelah parameter.",
    "Async dan await di JavaScript menangani operasi yang membutuhkan waktu.",
    "Promise adalah objek yang mewakili hasil operasi asinkron di masa depan.",
    "Daftar di JavaScript memiliki metode map, filter, dan reduce.",
    "Node.js menjalankan JavaScript di sisi server.",
    "Document query selector digunakan untuk mengambil elemen di halaman web.",
    "Objek di JavaScript menyimpan kunci dan nilai dalam kurung kurawal.",
    "DOM adalah representasi struktur halaman web yang bisa diubah dengan JavaScript.",

    # --- KOTLIN & ANDROID ---
    "Kotlin adalah bahasa modern untuk pengembangan aplikasi Android.",
    "Val di Kotlin menyatakan nilai yang tidak bisa diubah, sedangkan var bisa diubah.",
    "Fungsi di Kotlin ditulis dengan kata kunci fun diikuti nama fungsi.",
    "Nullable di Kotlin ditandai dengan tanda tanya setelah tipe data.",
    "When di Kotlin adalah ekspresi percabangan yang fleksibel.",
    "Coroutine di Kotlin menjalankan pekerjaan asinkron secara ringan.",
    "RecyclerView menampilkan daftar panjang di Android dengan efisien.",
    "View model menyimpan data antarmuka agar bertahan saat layar diputar.",
    "Room adalah lapisan penyimpanan database untuk aplikasi Android.",
    "Activity adalah komponen layar utama pada aplikasi Android.",
]


def korpus_domain():
    """Kembalikan satu string korpus domain (Indonesia naratif)."""
    import random
    # urutkan stabil (deterministik) supaya bisa direproduksi
    return "\n\n".join("".join(s) for s in SENTENSI if s)


def distribusi():
    """Acak distribusi topik untuk laporan (jumlah kalimat per topik)."""
    topik = {
        "bug hunting": 15, "python": 10, "aksara": 10,
        "javascript": 10, "kotlin": 10,
    }
    return topik
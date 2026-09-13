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

"""Kosakata Bahasa Indonesia — sumber leksikon umum (akar nyata).

Daftar akar kata Bahasa Indonesia sehari-hari + kata serapan & generik.
Gabung dengan kata-kata dari korpus aplikasi sendiri oleh modul pemakai.
File ini memuat leksikon inti (tanpa imbuhan sintetis yg ngarang).
"""

AKAR_KATA = [
    # inti (satu-dua suku kata)
    "air", "api", "abu", "tanah", "batu", "kayu", "daun", "bunga", "buah",
    "akar", "padi", "jagung", "padi", "ikan", "ayam", "sapi", "kuda",
    "kucing", "anjing", "ular", "burung", "udang", "kepiting", "kerang",
    # tubuh & orang
    "mata", "telinga", "hidung", "mulut", "gigi", "lidah", "tangan", "kaki",
    "kepala", "rambut", "kulit", "dada", "perut", "otak", "darah", "jantung",
    "paru", "orang", "bapak", "ibu", "kakak", "adik", "paman", "bibi",
    "anak", "cucu", "suami", "istri", "teman", "sahabat", "rekan",
    # tempat & waktu
    "rumah", "jalan", "pasar", "toko", "kantor", "sekolah", "kota", "desa",
    "pulau", "gunung", "sungai", "lautan", "pantai", "hutan", "sawah",
    "hari", "malam", "pagi", "siang", "sore", "bulan", "tahun", "minggu",
    "tanggal", "waktu", "jam", "menit", "detik",
    # arah & posisi
    "atas", "bawah", "depan", "belakang", "kiri", "kanan", "tengah",
    "dalam", "luar", "dekat", "jauh", "atas", "bawah",
    # warna & sifat
    "putih", "hitam", "merah", "kuning", "hijau", "biru", "ungu", "cokelat",
    "besar", "kecil", "panjang", "pendek", "tinggi", "rendah", "berat",
    "ringan", "cepat", "lambat", "kuat", "lemah", "baru", "lama", "benar",
    "salah", "baik", "buruk", "jelas", "gelap", "terang", "bersih", "kotor",
    "sehat", "sakit", "manis", "asin", "pahit", "asam", "pedas",
    # kerja (kata dasar)
    "makan", "minum", "tidur", "bangun", "kerja", "main", "belajar", "baca",
    "tulis", "hitung", "lihat", "dengar", "rasa", "cium", "pegang", "sentuh",
    "jalan", "lari", "lompat", "duduk", "diri", "pulang", "pergi", "datang",
    "bicara", "salam", "tanya", "jawab", "beri", "ambil", "simpan", "buang",
    "tarik", "dorong", "angkat", "jatuh", "rusak", "tumbuh", "hidup", "mati",
    "lahir", "turut", "ikut", "bantu", "tolong", "cari", "temu", "buka",
    "tutup", "nyalakan", "matikan", "kirim", "terima", "bayar", "beli",
    "jual", "hitung", "ukur", "timbang", "potong", "pukul", "lempar",
    "tangkap", "pegang", "genggam", "pilih", "pindah", "ubah", "ganti",
    # nomor & umum
    "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan",
    "sembilan", "sepuluh", "seratus", "ribu", "juta", "miliar", "nol",
    "semua", "banyak", "sedikit", "selalu", "tidak", "pernah", "kadang",
    "kata", "huruf", "kalimat", "suara", "bunyi", "nama", "angka", "warna",
    # serapan & teknologi
    "mobile", "data", "internet", "aplikasi", "sistem", "program", "kode",
    "layanan", "pembayaran", "transaksi", "produk", "pelanggan", "promo",
    "bisnis", "usaha", "laporan", "keuangan", "internet", "server",
    "whatsapp", "telegram", "bot", "pintar", "otomatis", "digital",
]


def ambil_akar_kata():
    """Kembalikan daftar akar kata unik terurut."""
    return sorted(set(w.lower() for w in AKAR_KATA if w.isalpha()))


def ukuran():
    return len(ambil_akar_kata())
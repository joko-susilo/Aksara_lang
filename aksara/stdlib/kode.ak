# ==========================================
# KODE - Pustaka Standar Aksara: asisten bantu coding (seperti AI dev)
# ==========================================
# Jawab pertanyaan pemrograman ringan: pola, saran, contoh kode.
# Dioptimasi untuk ranah CPU + hemat: cuma rule+template, tanpa LLM besar.

impor "teks.ak" sbg t

# KB kecil soal pemrograman (pattern -> jawaban)
kb_kode = [
    [["python", "loop", "perulangan"], "Python: perulangan pakai 'for i in range(n)' atau 'for x in daftar'. Contoh:\nfor i dalam 1..3 { cetak i }"],
    [["variabel", "variable"], "Variabel: tempat menyimpan nilai. Di Aksara: nama = nilai. Contoh: harga = 5000; cetak harga"],
    [["fungsi", "function", "def"], "Fungsi: blok kode yang bisa dipanggil ulang. Aksara: fun nama(args) { ... balik hasil }"],
    [["error", "bug", "gagal", "galat"], "Langkah debug: (1) baca pesan error baris terakhir, (2) cek tipe variabel, (3) isolasi bagian yang gagal, (4) cetak nilai tengah utk verifikasi."],
    [["ai", "neural", "jaringan", "model"], "Membuat AI dari nol: tentukan input X dan target y, pilih arsitektur (jaringan syaraf), latih, lalu ramal. Lihat modul ml.ak di Aksara."],
    [["kecepatan", "performa", "optimasi", "cepat"], "Optimasi CPU: gunakan operasi vektor (NumPy), hindari loop berulang, cache hasil, dan kompres bobot (int8) agar hemat memori."],
    [["memori", "ram", "ringan", "hemat"], "Hemat memori: quantisasi int8 (4x lebih kecil), kosakata BPE kompak, dan MoE (hanya aktifkan sebagian pakar)."],
]

fun bantu_code(pesan) {
    rendah = t.huruf_kecil(pesan)
    untuk i dalam 0 .. panjang(kb_kode) - 1 {
        entri = kb_kode[i]
        kunci_list = entri[0]
        untuk j dalam 0 .. panjang(kunci_list) - 1 {
            jika t.mengandung(rendah, kunci_list[j]) {
                balik entri[1]
            }
        }
    }
    balik nil
}
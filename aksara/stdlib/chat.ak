# ==========================================
# CHAT - Pustaka Standar Aksara: Mesin Percakapan ala ChatGPT (offline)
# ==========================================
# Fitur:
#   1. Multi-putaran: konteks percakapan diingat (history N terakhir)
#   2. Memori riwayat disimpan ke file (persist lintas sesi)
#   3. Jawab lewat otak pintar (pintar.ak)
#   4. Ringkas konteks (hemat memori: simpan ringkas topik)
# Kompresi: history disimpan ringkas "T:.../A:...", dipotong 6 terakhir.

impor "berkas.ak" sbg b
impor "teks.ak" sbg t
impor "pintar.ak" sbg P

fun _muat_riwayat(jalan) {
    jika bukan b.apakah_ada(jalan) {
        balik []
    }
    isi = b.baca_file(jalan)
    balik t.pisahkan(isi, "\n")
}

fun _simpan_riwayat(jalan, daftar_baris) {
    gabung = t.gabungkan(daftar_baris, "\n")
    b.tulis_file(jalan, gabung)
}

# Catat satu putaran [pertanyaan, jawaban]
fun catat(jalan, pertanyaan, jawaban) {
    baru = "T:" + pertanyaan + "|A:" + jawaban
    daftar = _muat_riwayat(jalan)
    dorong(daftar, baru)
    # potong hanya 6 terakhir (hemat file)
    jika panjang(daftar) > 6 {
        daftar_baru = []
        mulai = panjang(daftar) - 6
        untuk i dalam mulai .. panjang(daftar) - 1 {
            dorong(daftar_baru, daftar[i])
        }
        daftar = daftar_baru
    }
    _simpan_riwayat(jalan, daftar)
}

# Ringkas konteks dari riwayat -> string pendek utk disuntik
fun ringkas_konteks(jalan) {
    daftar = _muat_riwayat(jalan)
    hasil = ""
    untuk i dalam 0 .. panjang(daftar) - 1 {
        bagian = t.pisahkan(daftar[i], "|A:")
        jika panjang(bagian) >= 2 {
            hasil = hasil + "User: " + t.ganti(bagian[0], "T:", "") + "\n"
            hasil = hasil + "AI: " + bagian[1] + "\n"
        }
    }
    balik hasil
}

# Langkah penuh: jawab + simpan riwayat
fun bicara(kb, pesan, generator, jalan_fakta, jalan_korpus, jalan_riwayat, jalan_konteks) {
    # ekstrak konteks sebelumnya + pesan (jadi query konteksual)
    konteks = ringkas_konteks(jalan_riwayat)
    pertanyaan_penuh = pesan
    jika konteks != "" dan panjang(konteks) > 0 {
        # injeksi konteks ke KB sementara (konteks sebagai info)
        # (cara hemat: cukup ja') — kita gunakan langsung pesan
        # tap konteks untuk follow-up ambigu
        jika _ambigu(pesan) {
            pertanyaan_penuh = konteks + " " + pesan
        }
    }
    jawaban = P.jawab_pintar(kb, pertanyaan_penuh, generator, jalan_fakta, jalan_korpus)
    catat(jalan_riwayat, pesan, jawaban)
    balik jawaban
}

# deteksi pertanyaan ambigu (butuh konteks)
fun _ambigu(pesan) {
    rendah = t.huruf_kecil(pesan)
    jika t.mengandung(rendah, "itu") atau t.mengandung(rendah, "terus") atau t.mengandung(rendah, "dia") atau t.mengandung(rendah, "kenapa") atau t.mengandung(rendah, "gimana dengan") {
        balik benar
    }
    balik salah
}

# hapus riwayat (reset percakapan)
fun reset_riwayat(jalan) {
    b.hapus_file(jalan)
}
# ==========================================
# BELAJAR v2 - Pustaka Standar Aksara: pembelajaran mandiri (murni Aksara)
# ==========================================
# Semua logika: simpan fakta, lupa, jawab dari memori, retrain mini-LM.
# Python hanya saluran; kecerdasan ada di AKsARa.

impor "teks.ak" sbg t
impor "berkas.ak" sbg b
impor "pipeline.ak" sbg pl
impor "asisten.ak" sbg A

fun asisten_bot(kb, pesan, generator) {
    balik A.balas_pintar(kb, pesan, generator)
}

# ---------- util ----------
fun _cari(s, c) {
    untuk i dalam 0 .. panjang(s) - 1 {
        jika s[i] == c {
            balik i
        }
    }
    balik -1
}

fun _baca(jalan) {
    hasil = []
    jika bukan b.apakah_ada(jalan) {
        balik hasil
    }
    baris = b.baca_baris(jalan)
    untuk i dalam 0 .. panjang(baris) - 1 {
        bar = baris[i]
        pos = _cari(bar, "=")
        jika pos > 0 {
            topik = t.sub_teks(bar, 0, pos - 1)
            jwb = t.sub_teks(bar, pos + 1, panjang(bar) - 1)
            dorong(hasil, [topik, jwb])
        }
    }
    balik hasil
}

# ---------- kompleks ----------
fun ingat(jalan, pesan) {
    # "ingat <topik>: <jawaban>"
    pisah = t.pisahkan(pesan, ":")
    jika panjang(pisah) < 2 {
        balik "Format: ingat <topik>: <jawaban>"
    }
    kepala = t.ganti(t.huruf_kecil(t.potong_teks(pisah[0])), "ingat ", "")
    jwb = t.potong_teks(pisah[1])
    b.tambah_ke_file(jalan, kepala + "=" + jwb + "\n")
    balik "Oke, saya ingat: " + kepala + " -> " + jwb + " 🧠"
}

fun lupa(jalan, topik) {
    jika bukan b.apakah_ada(jalan) {
        balik "Tidak ada yang perlu dilupakan."
    }
    baris = b.baca_baris(jalan)
    baru = ""
    n = 0
    untuk i dalam 0 .. panjang(baris) - 1 {
        bar = baris[i]
        pos = _cari(bar, "=")
        dihapus = salah
        jika pos > 0 {
            tp = t.sub_teks(bar, 0, pos - 1)
            jika t.mengandung(t.huruf_kecil(tp), t.huruf_kecil(t.potong_teks(topik))) {
                dihapus = benar
                n = n + 1
            }
        }
        jika bukan dihapus {
            baru = baru + bar + "\n"
        }
    }
    b.tulis_file(jalan, baru)
    balik "Sudah saya lupakan (" + n + " fakta). 🧹"
}

fun jawab_dari(jalan, pesan) {
    pasangan = _baca(jalan)
    rendah = t.huruf_kecil(pesan)
    untuk i dalam 0 .. panjang(pasangan) - 1 {
        jika t.mengandung(rendah, pasangan[i][0]) {
            balik pasangan[i][1]
        }
    }
    balik nil
}

# ---------- retrain mini-LM dengan fakta baru (pembelajaran mendalam) ----------
fun retrain(jalan_korpus, jalan_fakta, jalan_model) {
    dasar = b.baca_file(jalan_korpus)
    fakta = _baca(jalan_fakta)
    tambahan = ""
    untuk i dalam 0 .. panjang(fakta) - 1 {
        tambahan = tambahan + fakta[i][0] + " itu " + fakta[i][1] + ". "
        tambahan = tambahan + "apa itu " + fakta[i][0] + "? " + fakta[i][1] + ". "
    }
    korpus_baru = dasar + " " + tambahan
    pipe = pl.latih(korpus_baru, 120, 16, 24, 1, 1, 60, 0.02, 0, benar)
    # simpan pipeline ke file (sebagai checkpoint sederhana)
    b.tulis_file(jalan_model, "korpus=" + panjang(korpus_baru) + "|fakta=" + panjang(fakta) + "\n")
    balik "Retrain selesai: korpus " + panjang(korpus_baru) + " char, fakta " + panjang(fakta)
}

# ---------- pintu masuk bot / REPL ----------
fun jawab_bot(pesan, jalan_fakta, jalan_korpus, kb, generator) {
    rendah = t.huruf_kecil(t.potong_teks(pesan))
    jika t.awalan(rendah, "ingat ") {
        balik ingat(jalan_fakta, pesan)
    }
    jika t.awalan(rendah, "lupa ") {
        balik lupa(jalan_fakta, t.sub_teks(rendah, 5, panjang(rendah) - 1))
    }
    jika t.awalan(rendah, "retrain") {
        balik retrain(jalan_korpus, jalan_fakta, "examples/ai_live/checkpoint.txt")
    }
    # jawab dari memori lebih dulu, lalu asisten
    fakta_jawab = jawab_dari(jalan_fakta, pesan)
    jika fakta_jawab != nil {
        balik fakta_jawab
    }
    balik asisten_bot(kb, pesan, generator)
}
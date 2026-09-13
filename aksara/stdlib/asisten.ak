# ==========================================
# ASISTEN v2 - Pustaka Standar Aksara: AI Pintar + Konteks + Memori
# ==========================================
# Semua dari sebelumnya + :
#   - KONTEKS topik terakhir (follow-up "itu/terus/kenapa" dijawab pakai topik)
#   - MEMORI persistent (file kecil) lintas sesi
#   - LOGIKA CABANG (multi-kondisi) via fungsi cabang(_)
# Hemat: state cuma 1 baris teks di file, bukan database.

impor "teks.ak" sbg t
impor "hitung.ak" sbg H
impor "berkas.ak" sbg b
impor "cabang.ak" sbg C

_konteks = ""

fun _pisahkan(daftar) {
    balik t.pisahkan(t.ganti(daftar, ",", " "), " ")
}

fun _ada_kata(bank, pesan) {
    untuk i dalam 0 .. panjang(bank) - 1 {
        w = bank[i]
        jika w != "" dan t.mengandung(pesan, w) {
            balik benar
        }
    }
    balik salah
}

# ---------- SIMPAN/MUAT memori (file ringkas) ----------
fun simpan_memori(jalan, topik) {
    b.tulis_file(jalan, topik)
}

fun muat_memori(jalan) {
    jika b.apakah_ada(jalan) {
        balik b.baca_file(jalan)
    }
    balik ""
}

fun buang_memori(jalan) {
    b.hapus_file(jalan)
    _konteks = ""
}

# ---------- DETEKSI follow-up (permalink) ----------
fun _kata_followup(rendah) {
    # "itu", "terus", "kenapa", "maksudnya", "gimana tadi"
    jika _ada_kata(["itu apa", "apakah itu", "apa itu", "itu bagaimana"], rendah) {
        balik benar
    }
    jika _ada_kata(["terus gimana", "terus bagaimana", "lalu"], rendah) {
        balik benar
    }
    balik salah
}

# ---------- INTI ----------
fun balas_pintar(kb, pesan, generator, jalan_memori = "") {
    rendah = t.huruf_kecil(t.potong_teks(pesan))

    # 0) perintah memory
    jika _ada_kata(["lupakan", "reset", "clear"], rendah) {
        buang_memori(jalan_memori)
        balik "Oke, memori saya saya kosongkan. Mulai lagi ya. 🧹"
    }
    jika _ada_kata(["kamu ingat", "kamu tahu topik", "tadi aku tanya"], rendah) {
        jika _konteks != "" {
            balik "Topik terakhir yang kita bicarakan: \"" + _konteks + "\". Ada yang mau dilanjutin?"
        }
        balik "Belum ada topik tersimpan. Tanya apa saja dulu ya."
    }

    # 1) handoff manusia
    human = kb["_human_words"]
    jika human != "" dan _ada_kata(_pisahkan(human), rendah) {
        balik kb["_human_reply"]
    }

    # 2) sapaan
    sapa = kb["_greet_words"]
    jika sapa != "" dan _ada_kata(_pisahkan(sapa), rendah) {
        balik kb["_greet_reply"]
    }

    # 2.5) follow-up pakai konteks (sebelum hitung/KB)
    jika _kata_followup(rendah) dan _konteks != "" {
        kunci_k = kunci(kb)
        untuk i dalam 0 .. panjang(kunci_k) - 1 {
            kunci_faq = kunci_k[i]
            jika bukan t.awalan(kunci_faq, "_") dan t.mengandung(_konteks, kunci_faq) {
                balik kb[kunci_faq] + " (kembali ke topik: " + _konteks + ")"
            }
        }
        balik "Topik terakhir saya: \"" + _konteks + "\". Coba pertanyaan yang lebih spesifik ya."
    }

    # 3) logika bercabang (multi-kondisi) — sebelum hitung
    jika jalan_memori == "" dan ada(kb, "_rules") {
        atur = kb["_rules"]
        jika atur != nil {
            r = C.eval(atur, rendah)
            jika r != nil {
                balik r
            }
        }
    }

    # 3.5) hitung (nol penyimpanan)
    hh = H.hitung(pesan)
    jika hh != nil {
        balik "Hasilnya: " + hh[0] + "  (" + hh[1] + ")"
    }

    # 4) knowledge base
    daftar = kunci(kb)
    untuk i dalam 0 .. panjang(daftar) - 1 {
        kf = daftar[i]
        jika bukan t.awalan(kf, "_") dan t.mengandung(rendah, kf) {
            _konteks = kf
            jika jalan_memori != "" {
                simpan_memori(jalan_memori, kf)
            }
            balik kb[kf]
        }
    }

    # 5) generator fallback
    jika generator != nil {
        hasil = generator(pesan)
        jika hasil != "" {
            balik hasil
        }
    }

    # 6) default
    balik kb["_default"]
}
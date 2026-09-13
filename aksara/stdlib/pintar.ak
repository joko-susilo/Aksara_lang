# ==========================================
# PINTAR - Pustaka Standar Aksara: Otak AI (orchestrator semua lapis)
# ==========================================
# Urutan nalar:
#   1) sapaan/handoff
#   2) hitung dasar + lanjutan (persen, rata-rata, konversi unit, prioritas)
#   3) konteks topik (memori sesi)
#   4) belajar (fakta tersimpan)
#   5) logika bercabang (_rules)
#   6) knowledge base
#   7) generator fallback
#   8) default
# Pakai internal belajar.ak & asisten.ak tapi dengan urutan yang lebih tajam.

impor "teks.ak" sbg t
impor "hitung.ak" sbg H
impor "berkas.ak" sbg b
impor "cabang.ak" sbg C
impor "belajar.ak" sbg B
impor "asisten.ak" sbg A
impor "semantik.ak" sbg S
impor "inferensi.ak" sbg INF
impor "bahasa_id.ak" sbg BID

_konteks_topik = ""

fun _ada_kata(bank, pesan) {
    untuk i dalam 0 .. panjang(bank) - 1 {
        w = bank[i]
        jika w != "" dan t.mengandung(pesan, w) {
            balik benar
        }
    }
    balik salah
}

fun _pisahkan(daftar) {
    balik t.pisahkan(t.ganti(daftar, ",", " "), " ")
}

# hitung lanjutan -> string jawaban (atau nil)
fun _hitung_lanjut(pesan) {
    # persen
    prs = H.persen(pesan)
    jika prs != nil {
        balik "Persentase: " + prs[0] + "  (" + prs[1] + ")"
    }
    # rata-rata
    rr = H.rata_rata(pesan)
    jika rr != nil {
        balik "Rata-rata: " + rr[0] + "  (dari " + rr[1] + ")"
    }
    # konversi unit (hanya klaim bila pola jelas)
    ku = H.konversi_unit(pesan)
    jika ku != nil {
        balik "Konversi " + ku[0] + " " + ku[1] + " -> belum tersedia hasil penuh (klaim dibatasi)."
    }
    balik nil
}

# logika gabungan (AND / OR)
fun logika_bener(pesan) {
    # "kucing dan anjing" -> ya keduanya
    jika t.mengandung(pesan, " dan ") {
        balik benar
    }
    jika t.mengandung(pesan, " atau ") {
        balik benar
    }
    balik salah
}

# ================= INTI =================
fun jawab_pintar(kb, pesan, generator, jalan_fakta, jalan_korpus) {
    # 0.5) normalisasi bahasa Indonesia (santai->baku)
    pesan_norm = BID.normalisasi(pesan)
    rendah = t.huruf_kecil(t.potong_teks(pesan_norm))

    # 0) perintah belajar/lupa/retrain
    jika t.awalan(rendah, "ingat ") {
        balik B.ingat(jalan_fakta, pesan)
    }
    jika t.awalan(rendah, "lupa ") {
        balik B.lupa(jalan_fakta, t.sub_teks(rendah, 5, panjang(rendah) - 1))
    }
    jika t.awalan(rendah, "retrain") {
        balik B.retrain(jalan_korpus, jalan_fakta, "examples/ai_live/checkpoint.txt")
    }

    # 1) handoff
    human = kb["_human_words"]
    jika human != "" dan _ada_kata(_pisahkan(human), rendah) {
        balik kb["_human_reply"]
    }

    # 2) sapaan
    sapa = kb["_greet_words"]
    jika sapa != "" dan _ada_kata(_pisahkan(sapa), rendah) {
        balik kb["_greet_reply"]
    }

    # 3) hitung dasar
    hh = H.hitung(pesan)
    jika hh != nil {
        balik "Hasilnya: " + hh[0] + "  (" + hh[1] + ")"
    }

    # 3.5) hitung lanjutan (persen/rata-rata)
    hasil_lanjut = _hitung_lanjut(pesan)
    jika hasil_lanjut != nil {
        balik hasil_lanjut
    }

    # 4) belajar (memori fakta)
    fk = B.jawab_dari(jalan_fakta, pesan)
    jika fk != nil {
        # tangkap topik yang cocok (kata terakhir sebelum '=' req) -> simpan konteks
        daftar_fk = B._baca(jalan_fakta)
        untuk idx dalam 0 .. panjang(daftar_fk) - 1 {
            jika t.mengandung(rendah, daftar_fk[idx][0]) {
                _konteks_topik = daftar_fk[idx][0]
                henti
            }
        }
        balik fk
    }

    # 4.5) konteks sesi (pertanyaan follow-up)
    jika _ada_kata(["itu apa", "terus", "maksudnya", "kenapa"], rendah) dan _konteks_topik != "" {
        daftar_k = kunci(kb)
        untuk i dalam 0 .. panjang(daftar_k) - 1 {
            kf = daftar_k[i]
            jika bukan t.awalan(kf, "_") dan t.mengandung(_konteks_topik, kf) {
                balik kb[kf] + " (konteks: " + _konteks_topik + ")"
            }
        }
    }

    # 6) logika bercabang
    jika ada(kb, "_rules") {
        rr = C.eval(kb["_rules"], rendah)
        jika rr != nil {
            balik rr
        }
    }

    # 7) knowledge base + simpan konteks
    daftar = kunci(kb)
    untuk i dalam 0 .. panjang(daftar) - 1 {
        kf = daftar[i]
        jika bukan t.awalan(kf, "_") dan t.mengandung(rendah, kf) {
            _konteks_topik = kf
            balik kb[kf]
        }
    }

    # 7.5) semantic matching (on-the-fly, hemat RAM, ony when exact match fails)
    hasil_sem = S.cocok(kb, rendah, 0.3, 1)
    jika panjang(hasil_sem) > 0 {
        skor_sem = hasil_sem[0][1]
        kunci_sem = hasil_sem[0][0]
        jika skor_sem >= 0.3 {
            _konteks_topik = kunci_sem
            balik kb[kunci_sem] + " (dekat makna: " + kunci_sem + ")"
        }
    }

    # 7.9) inferensi berantai (fallback terakhir sebelum generator)
    pesan_inf = pesan
    jika _konteks_topik != "" {
        jika _ada_kata([" ia", " dia", "beliau", "mereka"], rendah) {
            pesan_inf = t.ganti(rendah, " ia", " " + _konteks_topik)
            pesan_inf = t.ganti(pesan_inf, " dia", " " + _konteks_topik)
        }
    }
    hasil_inf = INF.cari(jalan_fakta, pesan_inf, 2)
    jika hasil_inf != nil dan panjang(hasil_inf) > 0 {
        balik hasil_inf[0] + "  [" + hasil_inf[1] + "]"
    }

    # 8) generator fallback
    jika generator != nil {
        g = generator(pesan)
        jika g != "" {
            balik g
        }
    }

    # 9) default
    balik kb["_default"]
}
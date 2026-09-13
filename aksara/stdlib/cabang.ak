# ==========================================
# CABANG - Pustaka Standar Aksara: Logika bercabang multi-kondisi
# ==========================================
# Evaluasi beberapa kondisi & gabungan AND/OR untuk pilih jawaban.
# Hemat: murni logika/rule (nol storage besar).

impor "teks.ak" sbg t

# cek apakah pesan mengandung SEMUA kata (AND)
fun AND(pesan, kata_daftar) {
    untuk i dalam 0 .. panjang(kata_daftar) - 1 {
        jika bukan t.mengandung(pesan, kata_daftar[i]) {
            balik salah
        }
    }
    balik benar
}

# cek apakah pesan mengandung SALAH SATU kata (OR)
fun OR(pesan, kata_daftar) {
    untuk i dalam 0 .. panjang(kata_daftar) - 1 {
        jika t.mengandung(pesan, kata_daftar[i]) {
            balik benar
        }
    }
    balik salah
}

# Evaluasi rule: daftar aturan [kondisi_ptr, jawaban]
# kondisi_ptr: [modus, kw_pesan, kata_list]
#   modus "and"/"or"; kw_pesan dicari di pesan; kata_list kata kunci
fun eval(aturan, pesan) {
    untuk i dalam 0 .. panjang(aturan) - 1 {
        baris = aturan[i]         # [kondisi, jawaban]
        kondisi = baris[0]
        modus = kondisi[0]
        kata_list = kondisi[1]
        kata_ada = kondisi[2]

        # kombinasikan kata pesan + kata kunci penunjang
        cocok = salah
        jika modus == "and" {
            cocok = AND(pesan, kata_ada) dan t.mengandung(pesan, kata_ada[0])
        } atau_jika modus == "or" {
            cocok = OR(pesan, kata_ada)
        }
        jika cocok {
            balik baris[1]   # jawaban
        }
    }
    balik nil
}
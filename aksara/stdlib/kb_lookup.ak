# ==========================================
# KB_LOOKUP - Pustaka Standar Aksara: cari jawaban dari KB kaya
# ==========================================
# 1) Cocok eksak kata kunci (baku, sudah dinormalisasi)
# 2) Fallback: cocok semantik antar-kata kunci
# 3) Multi-kata kunci (tiap kategori punya daftar sinonim)

impor "teks.ak" sbg t
impor "semantik.ak" sbg S

fun cari(kb_rich, pesan) {
    # 1) cocok eksak: entri dgn total panjang kata kunci cocok terbesar (spesifik menang)
    terbaik = nil
    skor_best = 0
    untuk i dalam 0 .. panjang(kb_rich) - 1 {
        entri = kb_rich[i]
        kunci_list = entri[0]
        cocok = 0
        untuk j dalam 0 .. panjang(kunci_list) - 1 {
            jika t.mengandung(pesan, kunci_list[j]) {
                cocok = cocok + panjang(kunci_list[j])
            }
        }
        jika cocok > skor_best {
            skor_best = cocok
            terbaik = [entri[-1], kunci_list[0]]
        }
    }
    jika skor_best > 0 {
        balik terbaik
    }
    # 2) fallback semantik antar-kata kunci
    untuk i dalam 0 .. panjang(kb_rich) - 1 {
        entri = kb_rich[i]
        kunci_list = entri[0]
        untuk j dalam 0 .. panjang(kunci_list) - 1 {
            skor = S.skor(kunci_list[j], pesan)
            jika skor >= 0.35 {
                balik [entri[-1], kunci_list[j]]
            }
        }
    }
    balik nil
}
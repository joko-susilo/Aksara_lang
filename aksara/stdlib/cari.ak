# ==========================================
# CARI - Pustaka Standar Aksara: Memori Vektor (RAG native)
# ==========================================
# Simpan pengetahuan berlabel + embedding -> cari terdekat secara kosinus.
# Backend numerik: aksara/ai/embed.py (feature-hash, offline).
# Dipakai perpikir.ak (loop AGI native).

impor "aksara.ai.embed" sbg eb
impor "json.ak" sbg j
impor "berkas.ak" sbg b
impor "teks.ak" sbg t

UKURAN_VEKTOR = 256
AMBANG_COCOK = 0.15

# ---------- tulis ----------
fun simpan(jalan, label, isi_teks) {
    catatan = []
    jika b.apakah_ada(jalan) {
        catatan = j.urai(b.baca_file(jalan))
    }
    v = eb.vektor_teks(isi_teks, UKURAN_VEKTOR)
    dorong(catatan, ["label": teks(label), "teks": teks(isi_teks), "v": v])
    b.tulis_file(jalan, j.ubah(catatan))
    balik panjang(catatan)
}

# ---------- baca ----------
fun cari(jalan, pertanyaan, k = 3, ambang = AMBANG_COCOK) {
    catatan = []
    jika b.apakah_ada(jalan) {
        catatan = j.urai(b.baca_file(jalan))
    }
    jika panjang(catatan) == 0 { balik [] }

    qv = eb.vektor_teks(pertanyaan, UKURAN_VEKTOR)
    daftar_v = []
    untuk i dalam catatan {
        dorong(daftar_v, i["v"])
    }
    hasil = eb.terdekat(qv, daftar_v, k, ambang)

    keluar = []
    untuk pasangan dalam hasil {
        # pasangan = [indeks, skor]
        indeks_i = pasangan[0]
        dorong(keluar, ["label": catatan[indeks_i]["label"],
                        "teks": catatan[indeks_i]["teks"],
                        "skor": pasangan[1]])
    }
    balik keluar
}

# ---------- konteks utk prompt ----------
fun konteks(jalan, pertanyaan, k = 3, ambang = AMBANG_COCOK) {
    hasil = cari(jalan, pertanyaan, k, ambang)
    baris = []
    untuk r dalam hasil {
        pot = t.potong_teks(r["teks"])
        jika panjang(pot) > 160 { pot = t.sub_teks(pot, 0, 160) }
        dorong(baris, "[" + r["label"] + "] " + pot)
    }
    jika panjang(baris) == 0 { balik "" }
    balik t.gabungkan(baris, "\n")
}

fun jumlah(jalan) {
    jika bukan b.apakah_ada(jalan) { balik 0 }
    catatan = j.urai(b.baca_file(jalan))
    balik panjang(catatan)
}
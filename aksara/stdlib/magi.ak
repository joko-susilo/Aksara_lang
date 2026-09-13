# ==========================================
# MAGI - Pustaka Standar Aksara: otak evolusi diri (versi Aksara)
# ==========================================
# Migrasi organ MAGI dari Python (huntingx/core/magi.py) ke Bahasa Aksara.
# Organ yang sudah hidup:
#   - konstitusi(): nilai & pantangan (alignment layer)
#   - jaga(): penjaga nurani — tolak teks yang kena pantangan
#   - refleksi(): simpan pelajaran dari tanya-jawab ke memori vektor
#   - kalibrasi()/laporan(): telusuri skor saran (helped/missed)
# Loop pikir + RAG di module perpikir.ak + cari.ak.

impor "cari.ak" sbg C
impor "waktu.ak" sbg W
impor "teks.ak" sbg t
impor "berkas.ak" sbg b
impor "json.ak" sbg j

# ---- KONSTITUSI ----
KONSTITUSI = [
    "klaim=bukti: jangan nyatakan tanpa bukti nyata",
    "hormati scope program & hukum; otorisasi wajib",
    "anti-informative: temuan tanpa dampak nyata tak layak",
    "proteksi kepentingan manusia banyak",
    "jujur tentang batasan; tidak over-sell severity",
]

PANTANGAN = [
    "nomor kartu", "nomor telepon user", "alamat user",
    "kata sandi", "token rahasia user", "kk ",
]

fun konstitusi() {
    balik KONSTITUSI
}

fun pantangan() {
    balik PANTANGAN
}

# ---- PENJAGA NURANI ----
fun jaga(kalimat) {
    rend = t.huruf_kecil(teks(kalimat))
    untuk p dalam PANTANGAN {
        jika t.mengandung(rend, p) {
            balik salah
        }
    }
    balik benar
}

# ---- REFLEKSI ----
fun refleksi(memori, pertanyaan, jawaban) {
    jam = W.waktu_teks()
    ringkas = t.potong_teks(teks(jawaban))
    jika panjang(ringkas) > 90 { ringkas = t.sub_teks(ringkas, 0, 90) }
    isi = "PELAJARAN [" + jam + "] " + teks(pertanyaan) + " => " + ringkas
    C.simpan(memori, "pelajaran", isi)
    balik isi
}

# ---- KALIBRASI ----
fun kalibrasi(jalan, sumber, skor) {
    catatan = []
    jika b.apakah_ada(jalan) {
        catatan = j.urai(b.baca_file(jalan))
    }
    dorong(catatan, ["sumber": teks(sumber), "skor": skor,
                     "waktu": W.detik_sekarang()])
    b.tulis_file(jalan, j.ubah(catatan))
    balik panjang(catatan)
}

fun laporan(jalan) {
    total = 0
    oke = 0
    jika b.apakah_ada(jalan) {
        untuk c dalam j.urai(b.baca_file(jalan)) {
            total = total + 1
            jika c["skor"] > 0 { oke = oke + 1 }
        }
    }
    balik ["total": total, "oke": oke]
}

# ---- DECAY (memory dingin = prioritas rendah) ----
fun decay(jalan, hari_batas = 30) {
    # jalan: ledger JSON [{waktu, teks}]; tandai yang tua dgn "dingin": benar
    catatan = []
    jika b.apakah_ada(jalan) {
        catatan = j.urai(b.baca_file(jalan))
    }
    sekarang = W.detik_sekarang()
    dingin = 0
    untuk c dalam catatan {
        jika c["waktu"] == nil { lanjut }
        w = c["waktu"]
        # ledger kalibrasi menyimpan detik numerik (W.detik_sekarang)
        tua = (sekarang - w) / 86400.0
        jika tua > hari_batas {
            c["dingin"] = benar
            dingin = dingin + 1
        } lain {
            c["dingin"] = salah
        }
    }
    b.tulis_file(jalan, j.ubah(catatan))
    balik ["total": panjang(catatan), "dingin": dingin]
}

# ---- CRYSTAL (pelajaran terbukti berulang) ----
fun crystal(jalan_memori, ambang = 2) {
    # hitung teks yang muncul >= ambang kali di memori vektor
    catatan = []
    jika b.apakah_ada(jalan_memori) {
        catatan = j.urai(b.baca_file(jalan_memori))
    }
    pembilang = []
    untuk c dalam catatan {
        ketemu = salah
        untuk p dalam pembilang {
            jika p["teks"] == c["teks"] {
                p["n"] = p["n"] + 1
                ketemu = benar
            }
        }
        jika bukan ketemu {
            dorong(pembilang, ["teks": teks(c["teks"]), "n": 1])
        }
    }
    terbukti = []
    untuk p dalam pembilang {
        jika p["n"] >= ambang {
            dorong(terbukti, p["teks"])
        }
    }
    balik terbukti
}

# ---- SOS (jalan pintas saat buntu) ----
fun sos(memori, situasi, generator, k = 3) {
    konteks = C.konteks(memori, situasi, k)
    prompt = "Situasi buntu: " + situasi + "\nPengalaman serupa:\n" + konteks
    prompt = prompt + "\nBeri 3 ARAH EKSPLORASI baru yang belum dicoba. Nomor 1., 2., 3."
    jawaban = generator(prompt)
    C.simpan(memori, "sos:" + t.potong_teks(situasi), "Buntu: " + situasi + " => " + jawaban)
    balik ["arah": jawaban, "konteks": konteks]
}

# ---- BRIEFING (bicara duluan dari ingatan) ----
fun briefing(memori, generator, k = 3) {
    konteks = C.konteks(memori, "pelajaran pengalaman kerja terakhir", k)
    prompt = "Buat briefing singkat hari ini (maks 6 baris):\nFOKUS: <prioritas>\nCOBA: <teknik>\nHINDARI: <pantangan>\n\nKonstitusi:\n"
    prompt = prompt + t.gabungkan(KONSTITUSI, "\n") + "\n\nIngatan terakhir:\n" + konteks
    narasi = generator(prompt)
    balik ["narasi": narasi, "konteks": konteks]
}

# ---- SINKRON .huntingx -> memori vektor Aksara ----
fun muat_huntingx(jalan_json, memori) {
    # custom_playbooks.json: {playbook: [{lesson, ...}]}
    data = []
    jika b.apakah_ada(jalan_json) {
        data = j.urai(b.baca_file(jalan_json))
    }
    dimuat = 0
    untuk kunci_pb dalam data {
        untuk lesson dalam data[kunci_pb] {
            C.simpan(memori, "huntingx:" + teks(kunci_pb), teks(lesson["lesson"]))
            dimuat = dimuat + 1
        }
    }
    balik dimuat
}
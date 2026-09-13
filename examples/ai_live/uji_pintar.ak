# ==========================================
# UJI KAPABILITAS — Otak Pintar Aksara (auto-test penuh)
# ==========================================
# Menjalankan 12 skenario, menilai benar/salah, report skor. Semua Aksara.

impor "pintar.ak" sbg P
impor "pipeline.ak" sbg pl
impor "berkas.ak" sbg f
impor "teks.ak" sbg t

fakta_file = "examples/ai_live/kb_pintar.txt"
korpus_file = "examples/ai_live/korpus_persona.txt"
jika f.apakah_ada(fakta_file) {
    f.hapus_file(fakta_file)
}

kb = ["_human_words": "admin petugas orang manusia",
    "_human_reply": "Baik, saya siapkan bantuan tim. Sebentar ya.",
    "_greet_words": "halo hai pagi siang malam assalamu",
    "_greet_reply": "Halo! Saya asisten Anda. Tanya apa saja.",
    "hitung": "Sebut angka + operasi.",
    "waktu": "Saya offline tanpa jam.",
    "terjemah": "Sebut kata, saya padankan.",
    "negara": "Indonesia adalah negara kepulauan terbesar di dunia.",
    "ibukota": "Ibukota Indonesia adalah Jakarta.",
    "_default": "Saya belum paham. Coba tanya salam, hitung, negara, ibukota, atau fakta baru."]

isi = f.baca_file(korpus_file)
pipe = pl.latih(isi, 100, 12, 24, 1, 1, 120, 0.02, 0, benar)
fun generator(pesan) { balik pl.ucap(pipe, pesan, 20, 0.4) }

# Skenario: [pertanyaan, kata kunci yang harus ada di jawaban]
uji = [
    ["halo", "Halo"],
    ["berapa 12 dikali 8?", "96"],
    ["20 persen dari 80 berapa?", "16"],
    ["rata-rata dari 10 20 30 40?", "25"],
    ["negara indonesia bagaimana?", "kepulauan"],
    ["apa ibukota indonesia?", "Jakarta"],
    ["ingat planet: mars adalah planet keempat dari matahari", "mars"],
    ["planet keempat itu apa?", "mars"],
    ["lupa planet", "lupa"],
    ["tujuh kali tiga berapa?", "21"],
]

cetak "== AUTO-TEST OTAK PINTAR AKsara =="
cetak ""

hitung_benar = 0
untuk i dalam 0 .. panjang(uji) - 1 {
    q = uji[i][0]
    wajib = uji[i][1]
    j = P.jawab_pintar(kb, q, generator, fakta_file, korpus_file)
    lulus = t.mengandung(t.huruf_kecil(j), t.huruf_kecil(wajib))
    jika lulus {
        hitung_benar = hitung_benar + 1
        cetak "[v] " + q
    } lain {
        cetak "[x] " + q
    }
    cetak "      -> " + j
}

cetak ""
cetak "SKOR: " + hitung_benar + "/" + panjang(uji)
cetak "Akurasi: " + ((hitung_benar / panjang(uji)) * 100) + "%"
# ==========================================
# PERPIKIR - Pustaka Standar Aksara: Loop AGI native (MAGI di dalam bahasa)
# ==========================================
# Siklus: ingat(seed) -> cari(konteks/retrieval) -> pikir(generator/otak)
#         -> jawab -> REFLEKSI (simpan Q->A = belajar).
# Otak pluggable: model_v4.ak (mini-LM lokal) ATAU llm.ak (API). Cukup ganti
# fungsi generator (closure) saat pemanggilan.

impor "cari.ak" sbg C
impor "waktu.ak" sbg W
impor "teks.ak" sbg t
impor "berkas.ak" sbg b
impor "json.ak" sbg j

fun ingat(jalan, label, isi) {
    balik C.simpan(jalan, label, isi)
}

fun cari_konteks(jalan, pertanyaan, k = 3) {
    balik C.konteks(jalan, pertanyaan, k)
}

fun bangun_prompt(pertanyaan, konteks) {
    k = konteks
    jika k == "" { k = "(belum ada memori relevan)" }
    balik "Jawab pertanyaan berikut ringkas dgn FAKTA dari KONTEKS bila ada; " +
          "kalau tak ada fakta, jujur bilang tak tahu.\n\nKONTEKS:\n" + k +
          "\n\nPERTANYAAN: " + pertanyaan + "\nJAWABAN:"
}

fun pikir(pertanyaan, generator, memori_jalan, k = 3) {
    konteks = C.konteks(memori_jalan, pertanyaan, k)
    prompt = bangun_prompt(pertanyaan, konteks)
    jawaban = generator(prompt)
    # REFLEKSI: simpan tanya-jawab ke memori vektor (belajar dari pengalaman)
    jam = W.waktu_teks()
    refleksi = "[" + jam + "] Tanya: " + pertanyaan + " -> Jawab: " + jawaban
    C.simpan(memori_jalan, "Q:" + t.potong_teks(pertanyaan), refleksi)
    balik ["jawaban": jawaban, "konteks": konteks]
}

# kajian pertanyaan + jawaban terakhir utk inspeksi
fun terakhir(jalan, k = 3) {
    balik C.jumlah(jalan)
}
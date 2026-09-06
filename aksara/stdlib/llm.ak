# ==========================================
# LLM - Pustaka Standar Aksara: Interaksi dengan Model Bahasa (LLM)
# ==========================================
# Format OpenAI-compatible (Groq, OpenAI, Gemini, Ollama lokal).
# API key dibaca dari variabel lingkungan (default: GROQ_API_KEY).

impor "requests" sbg req
impor "os" sbg os

ALAMAT_BALAASAN = "https://api.groq.com/openai/v1/chat/completions"
MODEL_BAWAAN = "llama-3.3-70b-versatile"

fun kunci_api(nama = "GROQ_API_KEY") {
    kunci = os.environ.get(nama)
    jika kunci == nil { balik "" }
    balik kunci
}

fun tanya(pesan, model = MODEL_BAWAAN, kunci = nil, alamat = ALAMAT_BALAASAN) {
    jika kunci == nil atau kunci == "" {
        kunci = kunci_api()
        jika kunci == "" {
            galat "API key belum diset. Isi variabel lingkungan GROQ_API_KEY."
        }
    }
    payload = ["model": model, "messages": [["role": "user", "content": pesan]]]
    header = ["Authorization": "Bearer " + kunci, "Content-Type": "application/json"]
    resp = req.post(alamat, headers = header, json = payload)
    hasil = resp.json()
    balik hasil["choices"][0]["message"]["content"]
}

fun ringkas_teks(teks, model = MODEL_BAWAAN, kunci = nil) {
    balik tanya("Ringkas teks berikut jadi maksimal 2 kalimat:\n" + teks, model, kunci)
}

fun terjemahkan(teks, bahasa = "Inggris", model = MODEL_BAWAAN, kunci = nil) {
    balik tanya("Terjemahkan teks berikut ke bahasa " + bahasa + ":\n" + teks, model, kunci)
}

fun bersihkan_kode(teks) {
    kode = teks
    jika teks.find("```") >= 0 {
        buka = teks.find("\n")
        tutup = teks.rfind("```")
        kode = teks[buka + 1 .. tutup - 2]
    }
    balik kode
}

fun tulis_kode(soal, model = MODEL_BAWAAN, kunci = nil) {
    hasil = tanya(
        "Jawab HANYA kode bahasa pemrograman Aksara (sintaks Indonesia, tanpa markdown, tanpa penjelasan).\n" +
        "Soal: " + soal,
        model, kunci
    )
    balik bersihkan_kode(hasil)
}

fun tulis_puisi(tema, model = MODEL_BAWAAN, kunci = nil) {
    balik tanya("Tulis puisi pendek tentang " + tema, model, kunci)
}
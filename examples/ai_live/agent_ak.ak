# Demo LLM: minta AI menulis & menjalankan program Aksara sendiri.
#
# Butuh API key:  GROQ_API_KEY=sk-... aksara contoh_agent.ak
# (Groq gratis di https://console.groq.com)

impor "llm.ak" sbg llm
impor "berkas.ak" sbg f

soal = "Buat fungsi bernama selesaikan yang menerima daftar angka dan " +
       "mengembalikan total semua angka genap di dalam daftar. " +
       "Gunakan bahasa Aksara (fun selesaikan(daftar))."

cetak ">> Meminta AI menulis kode Aksara..."
kode = llm.tulis_kode(soal)
cetak ">> Kode yang dihasilkan:"
cetak kode

jalan = "/tmp/opencode/larutan_ai.ak"
f.tulis_file(jalan, kode)

cetak ">> Memuat & menjalankan kode hasil AI..."
impor "/tmp/opencode/larutan_ai.ak" sbg ai
cetak "Hasil untuk [1, 2, 3, 4, 5, 6]: " + ai.selesaikan([1, 2, 3, 4, 5, 6])
# Copyright 2026 Joko Susilo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""PAKAR — AI ahli terbatas (domain fokus, hemat ekstra).

Strategi tantangan "70B-domains ekuivalen di ROM kecil":
    - hanya 2 bahasa lisan : Indonesia + Inggris
    - hanya 4 stack kode   : Python, Aksara, Kotlin, Android
    - knowledge base padat dari stdlib AKsara yang BENAR-BENAR ada

Semua jawaban konkret (contoh bisa dijalankan), bukan template kosong.
"""

# ------- peta fitur AKsara (dari stdlib asli) -------
AKSARA_FITUR = {
    "fungsi": "func pakai 'fun nama(...) { ... }'. Contoh: fun sapa(n) { balik n }",
    "variabel": "var pakai 'nama = nilai'. Contoh: harga = 5000",
    "impor": "modul pakai: impor 'modul' sbg nama",
    "cetak": "output pakai 'cetak teks'",
    "rata_rata": "larik.rata_rata([...]) -> rata-rata angka",
    "jumlah": "larik.jumlah([...]) -> total",
    "maksimum": "larik.maksimum([...]) -> nilai terbesar",
    "minimum": "larik.minimum([...]) -> nilai terkecil",
    "median": "larik.median([...]) -> nilai tengah",
    "variansi": "larik.variansi([...]) -> sebaran data",
    "simpangan_baku": "larik.simpangan_baku([...]) -> akar variansi",
    "outlier": "larik.outlier([...]) -> nilai di luar 2*std",
    "kelompok": "kelompok(data, n) -> clustering sederhana",
    "tebak": "tebak([...]) -> prediksi 2 langkah (regresi)",
    "jenis": "jenis(teks) -> sentimen positif/negatif/netral",
    "ringkas": "ringkas(teks) -> ringkasan",
    "periksa_ejaan": "periksa_ejaan(kata) -> cek ejaan",
    "deteksi_bahasa": "deteksi_bahasa(teks) -> tebak bahasa",
    "huruf_besar": "teks.huruf_besar(s) -> UPPERCASE",
    "huruf_kecil": "teks.huruf_kecil(s) -> lowercase",
    "potong_teks": "teks.potong_teks(s) -> hilangkan spasi tepi",
    "pisahkan": "teks.pisahkan(s, p) -> split string",
    "gabungkan": "teks.gabungkan(daftar, pemisah) -> join",
    "ganti": "teks.ganti(s, lama, baru) -> replace",
    "cari": "teks.cari(s, kata) -> posisi pertama",
}

KOTLIN_FITUR = {
    "variabel": "val x = 5 (immutable) / var y = 5 (mutable)",
    "fungsi": "fun nama(a: Int, b: Int): Int { return a + b }",
    "list": "val list = listOf(1, 2, 3) / mutableListOf(...)",
    "null": "nullable pakai ?: val s: String? = null",
    "when": "when(x) { 1 -> ... else -> ... } (switch modern)",
    "class": "class Mahasiswa(val nama: String, val npm: String)",
    "lambda": "val kali = { a: Int, b: Int -> a * b }",
    "scope": "let / apply / run / with (scope functions)",
    "android_activity": "Activity: onCreate(savedInstanceState: Bundle?) { setContentView(R.layout.activity_main) }",
}

PYTHON_FITUR = {
    "variabel": "nama = nilai (tanpa deklarasi tipe)",
    "list": "daftar = [1, 2, 3]; daftar.append(4)",
    "dict": "kamus = {'kunci': 'nilai'}; kamus['kunci']",
    "loop": "for i in range(5): ... / for x in daftar: ...",
    "fungsi": "def nama(a, b): return a + b",
    "lambda": "kali = lambda a, b: a * b",
    "listcomprehension": "[x**2 for x in range(10)]",
    "error": "try / except: coba-blok yang bisa gagal",
    "numpy": "import numpy as np; arr = np.array([1,2])",
}

ANDROID_FITUR = {
    "activity": "Activity = layar. Manifes mendeklarasikannya.",
    "recyclerview": "RecyclerView = daftar scrollable + adapter.",
    "coroutine": "Coroutine = async ringan: launch { ... } / suspend fun",
    "room": "Room = ORM database lokal SQLite.",
    "retrofit": "Retrofit = HTTP client API.",
    "viewmodel": "ViewModel = data UI bertahan saat rotasi.",
}

JS_FITUR = {
    "variabel": "let (bisa diubah) / const (tetap). Hindari var.",
    "fungsi": "const f = (a, b) => a + b;  // arrow function",
    "async": "async/await: const data = await fetch(url)",
    "promise": "Promise: .then() / .catch(), atau async-await",
    "array": "arr.map(x => x*2), filter, reduce — more ringkas",
    "object": "const obj = { kunci: 'nilai' }; obj.kunci",
    "node": "Node.js: Javascript di server, npm untuk paket",
    "dom": "document.querySelector('#id') → elemen HTML",
}

BUGHUNT_FITUR = {
    "recon": "Recon pasif dulu: subdomain enum, wayback/cdx, tech-detect, robots/sitemap. Jangan langsung nge-judge.",
    "scope": "WAJIB: baca program/scope dulu. Jangan test di luar aset yang diizinkan. Itu aturan emas.",
    "idor": "IDOR = akses objek user lain. Tes tanpa presesi: ganti ID, bandingkan respons akun A vs B, tanpa ngedownload massal.",
    "xss": "XSS = injeksi script ke output. Uji reflected/stored. Laporkan dampak nyata, jangan hanya alert(1).",
    "sql_injection": "SQLi = input dijalankan sebagai query. ' OR '1'='1. Konfirmasi impact (auth bypass/read), bukan sekadar error.",
    "auth": "Tes auth: user enumeration (beda respons), brute-force rate limit, token binding, session fixation.",
    "ssrf": "SSRF = server dicolong request ke internal. Butuh endpoint fetch URL & validasi kembali balik.",
    "report": "Laporan yang diterima: title dari impact root, bukti konkret + steps, akui limitasi, severity konservatif.",
    "api": "API: test object-level auth (BOLA/BOPLA), mass assignment, rate limit, IDOR di endpoint JSON.",
    "idor_akun": "Tanpa akun biasanya Low; akun = jalan ke IDOR High. Buat 2 akun test untuk banding.",
}

NORMA_ID = [
    "hanya test di scope yang diizinkan",
    "verifikasi impact, jangan overclaim severity",
    "jangan exfiltrasi data produksi/massa",
    "laporkan, jangan exploit untuk keuntungan pribadi",
]

# deteksi bahasa tanya (Indonesia vs Inggris) ringkas
def cek_bahasa(t):
    kata_id = ["berapa", "bagaimana", "apa", "gimana", "pake", "buat", "cara"]
    t_low = t.lower()
    for k in kata_id:
        if k in t_low:
            return "id"
    return "en"


def cari_stack(t):
    t_low = t.lower()
    if ("bug" in t_low or "hunt" in t_low or "report" in t_low or "lapor" in t_low or
            "idor" in t_low or "xss" in t_low or "ssrf" in t_low or "recon" in t_low):
        return "bug_hunt", BUGHUNT_FITUR
    for s, f in [("android", ANDROID_FITUR), ("kotlin", KOTLIN_FITUR),
                 ("python", PYTHON_FITUR), ("aksara", AKSARA_FITUR),
                 ("javascript", JS_FITUR), ("js", JS_FITUR)]:
        if s in t_low:
            return s, f
    return None, None


def _cocok_topic(t_low, fitur):
    """Cocokkan t_low ke topik fitur. Pertama eksak, lalu longgar (awalan kata)."""
    # 1) eksak
    for topik in fitur:
        if topik in t_low:
            return topik
    # 2) longgar: kata query ada di dalam kunci, atau kunci di query
    kata_query = [w for w in t_low.replace("_", "").split() if len(w) > 3]
    for topik in fitur:
        topik_pol = topik.replace("_", "")
        if topik_pol in kata_query or len(topik) > 3 and topik_pol in t_low.replace(" ", ""):
            return topik
        for w in kata_query:
            if w in topik_pol and len(w) >= 4:
                return topik
    return None


def _pasangkan(stack, fitur, t_low):
    """Cocokkan topik; khusus bug_hunt & aksara pakai kata longgar."""
    if stack == "bug_hunt":
        map_loose = {
            "recon": ["recon", "langkah pertama", "mulai", "pertama", "enum"],
            "report": ["report", "laporan", "cara laporkan", "baik"],
        }
        for topik, kata in map_loose.items():
            for w in kata:
                if w in t_low:
                    return topik
    if stack == "aksara":
        if " fun " in t_low or t_low.startswith("fun ") or t_low.endswith("fun"):
            return "fungsi"
    return _cocok_topic(t_low, fitur)


def jawab(t):
    lang = cek_bahasa(t)
    stack, fitur = cari_stack(t)
    t_low = t.lower()

    if fitur:
        topik = _pasangkan(stack, fitur, t_low)
        if topik:
            return fitur[topik]
        daftar = ", ".join(list(fitur.keys())[:8])
        return ("Belum paham topik itu. Yang saya kuasai di " + stack + ": " + daftar +
                ". Coba tanya yang spesifik."
                if lang == "id" else
                "Topik yang saya kuasai di " + stack + ": " + daftar + ".")

    return ("Aku AI Makasar: fokus Indonesia. Kuasai Python, Aksara, Kotlin, "
            "JavaScript, Android, dan Bug Hunting (metodologi). Tanya soal itu ya."
            if lang == "id" else
            "Aku AI fokus Indonesia. Kuasai Python, Aksara, Kotlin, "
            "JavaScript, Android, dan Bug Hunting (metodologi).")


def daftar_pakar():
    return {
        "bahasa": ["indonesia", "english"],
        "stack": ["python", "aksara", "kotlin", "android", "javascript", "bug_hunt"],
        "fitur_aksara": len(AKSARA_FITUR),
        "fitur_kotlin": len(KOTLIN_FITUR),
        "fitur_python": len(PYTHON_FITUR),
        "fitur_android": len(ANDROID_FITUR),
        "fitur_js": len(JS_FITUR),
        "fitur_bug": len(BUGHUNT_FITUR),
    }
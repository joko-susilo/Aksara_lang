
# kamus.py
# Berisi daftar pemetaan kata kunci Aksara ke sintaks Python menggunakan regex (\b)

KAMUS_AKSARA = {
    # Fungsi & Logika Utama
    r"\bfungsi\b": "def",
    r"\bkembalikan\b": "return",
    r"\bcetak\b": "print",
    # Percabangan
    r"\bjika\b": "if",
    r"\batau_jika\b": "elif",
    r"\bselain\b": "else",
    # Perulangan (Loops)
    r"\buntuk\b": "for",
    r"\bdalam\b": "in",
    r"\bselama\b": "while",
    r"\brentang\b": "range",
    # Nilai Boolean & Logika
    r"\bbenar\b": "True",
    r"\bsalah\b": "False",
    r"\bdan\b": "and",
    r"\batau\b": "or",
    r"\bbukan\b": "not",
}

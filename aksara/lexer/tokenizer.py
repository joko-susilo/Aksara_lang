import re
from aksara.lexer.tokens import Token, KATA_KUNCI

# Pola regex untuk setiap jenis token (diurutkan dari yang paling spesifik)
TOKEN_SPEC = [
    ("KOMENTAR",    r"#[^\n]*"),                    # Komentar: # sampai akhir baris
    ("STRING",      r'"[^"]*"'),                    # String: "..." (tidak mendukung escape dulu)
    ("ANGKA",       r"\d+(\.\d+)?"),  
    ("TITIK_DUA",    r":"),
    ("OPERATOR", r"==|!=|<=|>=|\.\.|\?\?|[+\-*/<>=]"), # Operator: multi-karakter dulu, lalu tunggal
    ("KURUNG_KUWAL", r"[{}]"),  
    ("KURUNG_SIKU", r"[\[\]]"),    
    ("KURUNG",      r"[()]"),
    ("KOMA",        r","),                       # Kurung biasa ( )
    ("TITIK",       r"\."),                         # Titik untuk akses atribut (setelah OPERATOR ..)
    ("NAMA",        r"[a-zA-Z_][a-zA-Z0-9_]*"),     # Nama variabel/fungsi (juga menangkap kata kunci)
    ("BARIS_BARU",  r"\n"),                         # Baris baru
    ("SPASI",       r"[ \t\r]+"),                   # Spasi, tab, carriage return (diabaikan)
]

# Kompilasi semua pola menjadi satu regex besar
PATTERN = "|".join(f"(?P<{nama}>{pola})" for nama, pola in TOKEN_SPEC)
REGEX = re.compile(PATTERN)

def tokenize(kode: str) -> list[Token]:
    """
    Memecah string kode sumber menjadi daftar Token.
    Mengabaikan spasi dan komentar.
    Mendeteksi kata kunci dan mengubah tipe token dari 'NAMA' ke 'KATA_KUNCI' jika cocok.
    """
    tokens = []
    baris = 1
    kolom = 1

    for m in REGEX.finditer(kode):
        jenis = m.lastgroup
        nilai = m.group()

        if jenis == "SPASI":
            # Update posisi saja, abaikan token
            for ch in nilai:
                if ch == '\n':
                    baris += 1
                    kolom = 1
                else:
                    kolom += 1
            continue

        if jenis == "BARIS_BARU":
            baris += 1
            kolom = 1
            continue

        if jenis == "KOMENTAR":
            # Update kolom dan baris (jika ada baris baru di dalamnya? Tidak, komentar hanya sampai akhir baris)
            kolom += len(nilai)
            continue

        # Catat posisi awal token
        token_baris = baris
        token_kolom = kolom

        # Cek apakah token NAMA sebenarnya adalah kata kunci
        if jenis == "NAMA" and nilai in KATA_KUNCI:
            jenis = "KATA_KUNCI"

        # Tambahkan token ke daftar
        tokens.append(Token(jenis, nilai, token_baris, token_kolom))

        # Update posisi setelah token
        for ch in nilai:
            if ch == '\n':
                baris += 1
                kolom = 1
            else:
                kolom += 1

    # Token EOF untuk menandai akhir
    tokens.append(Token("EOF", "", baris, kolom))
    return tokens

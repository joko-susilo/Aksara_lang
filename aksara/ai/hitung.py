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

"""Penalaran hitung lokal (Bahasa Indonesia) — dari logika, nol penyimpanan.

Memahami frasa angka Indonesia & operator:
  "12 dikali 8", "100 - 35", "12 * 8", "bagi", "tambah", "kurang", "per",
  angka tertulis (dua belas, seratus lima) sampai sepuluh ribu.

Tidak butuh file/DB — hemat ruang total.
"""

_ANGKA = {
    "nol": 0, "satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5,
    "enam": 6, "tujuh": 7, "delapan": 8, "sembilan": 9, "sepuluh": 10,
    "sebelas": 11, "duabelas": 12, "tigabelas": 13, "empatbelas": 14,
    "limabelas": 15, "enambelas": 16, "tujuhbelas": 17, "delapanbelas": 18,
    "sembilanbelas": 19, "duapuluh": 20, "tigapuluh": 30, "empatpuluh": 40,
    "limapuluh": 50, "enampuluh": 60, "tujuhpuluh": 70, "delapanpuluh": 80,
    "sembilanpuluh": 90, "seratus": 100,
}


def _kata_ke_angka(t):
    """Konversi kata angka (sejauh yang dipahami) -> bilangan."""
    t = t.strip().lower()
    if t.isdigit():
        return float(t)
    if t in _ANGKA:
        return float(_ANGKA[t])
    # "dua puluh lima", "seratus dua"
    pot = t.split()
    total = 0.0
    cur = 0.0
    for w in pot:
        if w in ("puluh", "ratus", "ribu", "juta"):
            cur = max(cur, 1) * {  # style decimal helper
                "puluh": 10, "ratus": 100, "ribu": 1000, "juta": 1_000_000}[w]
            total += cur
            cur = 0
        elif w in _ANGKA:
            cur += _ANGKA[w]
    total += cur
    return total if total else None


_RE_OP = [
    ("dikali", "kali", "*"), ("tambah", "+"), ("kurang", "-"),
    ("dibagi", "bagi", "per", "/"),
]


def hitung(teks):
    """Coba ekstrak operasi dari kalimat; kembalikan (hasil, penjelasan) atau None."""
    t = teks.lower().replace(",", "")
    # cari pola dua angka di sekitar operator
    hasil = None
    pembagi = "/"
    pengali = None

    def cari_op(ops):
        for op in sorted(ops, key=len, reverse=True):
            if op in t:
                return op
        return None

    import re
    # PRIORITAS pola digit: "12 dikali 8", "100 - 35", "7 * 3"
    for op_romaji, fn in [
        ("dikali", lambda a, b: a * b), ("kali", lambda a, b: a * b),
        ("tambah", lambda a, b: a + b), ("kurang", lambda a, b: a - b),
        ("dibagi", lambda a, b: a / b if b else None), ("bagi", lambda a, b: a / b if b else None),
        ("per", lambda a, b: a / b if b else None)]:
        pola = re.search(r"(\d+)\s*" + op_romaji + r"\s*(\d+)", t)
        if pola:
            a = float(pola.group(1)); b = float(pola.group(2))
            h = fn(a, b)
            if h is not None:
                return h, f"{a} {op_romaji} {b}"
    # operator simbolik
    for op, fn in [("*", lambda a, b: a * b), ("+", lambda a, b: a + b),
                   ("-", lambda a, b: a - b), ("/", lambda a, b: a / b)]:
        m = re.search(r"(-?[\d ,.]+)\s*" + re.escape(op) + r"\s*(-?[\d ,.]+)", t)
        if m:
            a = float(m.group(1).replace(",", "").strip())
            b = float(m.group(2).replace(",", "").strip())
            if op == "/" and b == 0:
                return None, None
            return fn(a, b), f"{a} {op} {b}"
    # frasa angka tertulis: "tujuh dikali tiga", "dua belas tambah lima"
    for op_romaji, fn in [("dikali", lambda a, b: a * b), ("kali", lambda a, b: a * b),
                           ("tambah", lambda a, b: a + b), ("kurang", lambda a, b: a - b),
                           ("bagi", lambda a, b: a / b if b else None),
                           ("per", lambda a, b: a / b if b else None)]:
        pola = re.search(
            r"([a-z ]+?)\s*" + op_romaji + r"\s*([a-z ]+?)(?:\?|$)", t)
        if pola:
            a = _kata_ke_angka(pola.group(1))
            b = _kata_ke_angka(pola.group(2))
            if a is not None and b is not None:
                h = fn(a, b)
                if h is not None:
                    return h, f"{a} {op_romaji} {b}"
    return None, None

# --- Kemampuan lanjutan (murni python sederhana, dipakai via stdlib .ak) ---

TOK_ANGKA = ["nol","satu","dua","tiga","empat","lima","enam","tujuh","delapan",
             "sembilan","sepuluh","sebelas"]

def kata_ke_angka_tunggal(w):
    return float(TOK_ANGKA.index(w)) if w in TOK_ANGKA else None

def konversi_unit(teks):
    """'5 km berapa meter' -> (nilai, satuan_asal, satuan_tujuan)."""
    import re
    t = teks.lower()
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(km|m|cm|mm|kg|g|jam|menit)\s*(?:konversi|ke|berapa)\s*([a-z]+)", t)
    if m:
        val = float(m.group(1).replace(",", "."))
        return val, m.group(2), m.group(3)
    return None

def persen(teks):
    """'20 persen dari 80' -> 16.0, '80 kurang 20 persen' -> 64.0."""
    import re
    t = teks.lower()
    m = re.search(r"(\d+)\s*(?:persen|%)\s*dari\s*(\d+)", t)
    if m:
        return float(m.group(1)) / 100.0 * float(m.group(2)), f"{m.group(1)}% dari {m.group(2)}"
    return None

def rata_rata(teks):
    """'rata rata dari 10 20 30 40' -> 25.0"""
    import re
    t = teks.lower()
    m = re.search(r"rata.?(?:-)?rata.*?dari\s*([\d ,]+)", t)
    if m:
        vals = [float(x) for x in re.findall(r"\d+", m.group(1))]
        if vals:
            return sum(vals)/len(vals), m.group(1).replace(" ", ", ")
    return None

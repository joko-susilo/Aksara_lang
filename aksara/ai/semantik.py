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

"""Semantik lokal — paham makna tanpa model raksasa.

Ide: buat vektor kata dari *struktur huruf* (n-gram) + stemmer bahasa Indonesia
(hilangkan imbuhan akhir umum), lalu ukur kemiripan kosinus antara
pertanyaan & entri KB. Bukan sama persis — tapi "dekat maknanya".

Hemat: vektor dibangun on-the-fly dari kamus kecil; tanpa model bahasa besar.
"""

import math

# ---------- stemmer Indonesia sederhana (imbuhan akhir) ----------
_SUF = ["kan", "an", "kan", "nya", "kah", "lah", "tah",
        "wan", "wati", "man", "i", "s", "mu", "ku", "mu", "ku"]

def _stem(kata):
    k = kata.lower()
    for s in sorted(_SUF, key=len, reverse=True):
        if len(k) > len(s) + 2 and k.endswith(s):
            return k[:-len(s)]
    return k


def _n_gram(kata, n=3):
    """Ekstrak n-gram dari kata (huruf hanyut)."""
    k = kata.lower()
    if len(k) <= n:
        return {k}
    return {k[i:i+n] for i in range(len(k) - n + 1)}


def vektor_kata(kata):
    """Vektor feature dari kata: frekuensi n-gram (char)."""
    from collections import Counter
    k = kata.lower()
    fitur = {}
    for n in (2, 3):
        for g in _n_gram(k, n):
            fitur[g] = fitur.get(g, 0) + 1
    # tandai awal/akhir
    fitur["^" + k[:2]] = 1
    fitur[k[-2:] + "$"] = 1
    return fitur


def kosinus(a, b):
    """Kosinus antara dua dict vektor."""
    if not a or not b:
        return 0.0
    dot = 0.0
    na = 0.0
    nb = 0.0
    for k, v in a.items():
        dot += v * b.get(k, 0.0)
        na += v * v
    for v in b.values():
        nb += v * v
    if na == 0 or nb == 0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


# ---------- sinonim Indonesia ----------
SINONIM = {
    "biaya": "bayar", "bayar": "bayar", "pembayaran": "bayar",
    "tagihan": "bayar", "duit": "bayar", "uang": "bayar",
    "aktif": "waktu", "online": "waktu", "hidup": "waktu",
    "jam": "waktu", "hari": "waktu", "setiap": "waktu",
    "promosi": "broadcast", "promo": "broadcast", "massal": "broadcast",
    "kirim_massal": "broadcast", "broadcast": "broadcast",
    "daftar": "activasi", "daftarkan": "activasi", "mulai": "activasi",
    "ongkir": "jarak", "dekat": "jarak", "jauh": "jarak",
}

def _normalisasi(kata):
    """Normalkan sinonim dulu, baru stem. Jadi sinonim tak terpotong."""
    k = kata.lower()
    k = SINONIM.get(k, k)  # sinonim dulu
    return _stem(k)         # baru stem


def dokumen_vektor(kata_daftar):
    """Gabungkan vektor beberapa kata (fitur union, setelah stemming + sinonim)."""
    gab = {}
    for k in kata_daftar:
        norm = _normalisasi(k)
        for f, v in vektor_kata(norm).items():
            gab[f] = gab.get(f, 0) + v
        # bonus bentuk asli
        for f, v in vektor_kata(k).items():
            gab[f] = gab.get(f, 0) + v * 0.3
    return gab


def skor_kesamaan(pertanyaan, entri):
    """Skor kesamaan semantik query vs entri. Best-of doc vs single-word."""
    import re
    KATA_TANYA = {"apa", "bagaimana", "gimana", "kapan", "dimana", "siapa",
                  "mengapa", "kenapa", "berapa", "mana", "bisa", "tidak",
                  "adalah", "itu", "ini", "untuk", "dari", "dalam", "dengan",
                  "saya", "kamu", "ia", "belum", "sedang", "lagi",
                  "halo", "hai", "assalamu", "ya", "nya"}
    q_bersih = re.sub(r"[^a-z\s]", "", pertanyaan.lower())
    e_bersih = re.sub(r"[^a-z\s]", "", entri.lower())
    q_kata = [k for k in q_bersih.split() if len(k) > 1 and k not in KATA_TANYA]
    e_kata = [k for k in e_bersih.split() if len(k) > 1 and k not in KATA_TANYA]
    if not q_kata or not e_kata:
        return 0.0
    # full doc similarity
    vq = dokumen_vektor(q_kata)
    ve = dokumen_vektor(e_kata)
    skor_doc = kosinus(vq, ve)
    # best single-word cosine
    skor_word = 0.0
    for qw in q_kata:
        vw = dokumen_vektor([qw])
        for ew in e_kata:
            s = kosinus(vw, dokumen_vektor([ew]))
            if s > skor_word:
                skor_word = s
    return max(skor_doc, skor_word)


def cocok_kb(pertanyaan, kb, ambang=0.35, jumlah=1):
    """Bandingkan pertanyaan dengan semua entri KB; balik entri terdekat.

    kb: dict {kunci: teks_jawaban}. Kembalikan list (kunci, skor) turun.
    """
    q = pertanyaan.lower()
    hasil = []
    for k, teks in kb.items():
        if k.startswith("_"):
            continue
        skor = skor_kesamaan(q, teks)
        # tambah bobot bila kata kunci muncuk langsung
        if k in q:
            skor += 0.5
        hasil.append((k, skor))
    hasil.sort(key=lambda x: -x[1])
    return hasil[:jumlah]
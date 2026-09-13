"""Inferensi berantai — AI menjawab dengan menghubungkan fakta-fakta.

Contoh:
  fakta1: "presiden = presiden pertama indonesia adalah soekarno"
  fakta2: "soekarno = soekarno memimpin tahun 1945 s/d 1967"
  tanya: "kapan presiden pertama memimpin?"
  -> cari "presiden" -> dapat "presiden pertama indonesia adalah soekarno"
  -> cari "soekarno" -> dapat "soekarno memimpin tahun 1945 s/d 1967"
  -> jawab dengan menggabungkan

Hemat: traversal graph dari file fakta kecil, tanpa embedding.
"""

import os


def baca_fakta(jalan):
    if not os.path.exists(jalan):
        return []
    hasil = []
    for baris in open(jalan, encoding="utf-8", errors="ignore"):
        baris = baris.strip()
        if not baris:
            continue
        if "=" in baris:
            t, _, j = baris.partition("=")
            hasil.append((t.strip().lower(), j.strip()))
    return hasil


def cari_fakta(fakta, query):
    """Cari fakta yang menyebut query (match longgar)."""
    q = query.lower()
    hasil = []
    for topik, jawab in fakta:
        if topik in q or q in topik or any(w in jawab.lower() for w in q.split() if len(w) > 3):
            hasil.append((topik, jawab))
    return hasil


def inferensi(jalan, pertanyaan, kedalaman=2):
    """Coba menjawab dengan menghubungkan fakta-fakta (berantai 1-2 langkah)."""
    fakta = baca_fakta(jalan)
    q = pertanyaan.lower()
    q_kata = set(w for w in q.split() if len(w) > 3)

    # langkah 1: cari fakta langsung yang menyebut query
    langsung = cari_fakta(fakta, q)
    if not langsung:
        return None, None

    # langkah 2: jenis pertanyaan (kapan = cari fakta lain; siapa/apa = fakta langsung)
    is_kapan = "kapan" in q or "tahun" in q or "kapan" in q

    # langkah 3: cari fakta yang topiknya = entitas baru (chain lewat topik)
    terhubung = []
    seen = set()
    for topik, jawab in langsung:
        for ent in jawab.lower().split():
            ent_bersih = ent.strip(".,;:")
            if len(ent_bersih) > 3 and ent_bersih not in q_kata and ent_bersih not in seen:
                seen.add(ent_bersih)
                for t2, j2 in fakta:
                    if t2.lower() == ent_bersih and (t2, j2) not in langsung:
                        terhubung.append((t2, j2))
                        break

    if terhubung:
        gabungan = "; ".join([j for _, j in langsung[:1]] + [j for _, j in terhubung[:1]])
        penjelasan = "dari fakta: " + " | ".join(
            [f'"{t}"→"{j[:40]}"' for t, j in langsung[:1] + terhubung[:1]])
        return gabungan, penjelasan

    return langsung[0][1], f"dari fakta langsung: \"{langsung[0][0]}\""
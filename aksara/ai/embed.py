# Copyright 2026 Joko Susilo
# Licensed under the Apache License, Version 2.0 (the "License");
"""Embedding vektor ringan utk RAG/memori Aksara — backend numerik.

Feature-hash: teks -> vektor dens (dimensi D) via hashing n-gram karakter.
Tanpa model pretrained (jalan offline, murni Python stdlib). Cukup utk
retrieval sederhana (cari.emd / perpikir.ak), bukan utk semantik canggih.
"""

import re


def _ngram(teks, n=3):
    teks_n = re.sub(r"\s+", " ", teks).lower()
    ngram = [teks_n[i:i + n] for i in range(max(0, len(teks_n) - n + 1))]
    # rusak kata kosong
    kata = re.findall(r"[a-z0-9]+", teks_n)
    return ngram + kata


def vektor_teks(teks, dim=256, benih=42):
    """Feature-hash sign: vektor float list panjang `dim`."""
    v = [0.0] * dim
    for g in _ngram(teks):
        # hash deterministik (FNV-1a kecil) -> index + tanda
        h = benih
        for b in g.encode("utf-8"):
            h = ((h ^ b) * 16777619) & 0xFFFFFFFF
        idx = h % dim
        tanda = 1.0 if (h & 1) else -1.0
        v[idx] += tanda
    # normalisasi
    norma = sum(x * x for x in v) ** 0.5
    if norma > 0:
        v = [x / norma for x in v]
    return v


def kosinus(a, b):
    """Kemiripan kosinus dua vektor."""
    if not a or not b or len(a) != len(b):
        return 0.0
    atas = sum(x * y for x, y in zip(a, b))
    n_a = sum(x * x for x in a) ** 0.5
    n_b = sum(y * y for y in b) ** 0.5
    if n_a <= 0 or n_b <= 0:
        return 0.0
    return atas / (n_a * n_b)


def terdekat(vektor, daftar, k=5, ambang=0.15):
    """Balik [(indeks, skor)] terdekat di `daftar` (list vektor), ambang skor."""
    skor = [(i, kosinus(vektor, v)) for i, v in enumerate(daftar)]
    skor = [s for s in skor if s[1] >= ambang]
    skor.sort(key=lambda s: -s[1])
    return skor[:k]


if __name__ == "__main__":
    dim = 64
    a = vektor_teks("harga paket telegram csoto", dim)
    b = vektor_teks("biaya layanan whatsapp", dim)
    c = vektor_teks("resep mie goreng", dim)
    print("konteks a-b:", round(kosinus(a, b), 3))
    print("konteks a-c:", round(kosinus(a, c), 3))
    assert kosinus(a, b) > kosinus(a, c), "harusnya topik layanan lebih mirip"
    print("EMBED OK")
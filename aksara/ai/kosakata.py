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

"""Kosakata Bahasa Indonesia + Kompresor — kata dikemas seekecil mungkin.

Dari daftar kata (plain text) -> vocab BPE (compact integer) -> kompresi
ekstra (zlib). Ukur rasio: teks asli vs vocab BPE vs kompresi gzip.

Komponen:
  baca_kata(jalan)        : baca file kata (1 kata/baris), bersihkan.
  buat_vocab(kata, ukuran): BPE dari daftar kata -> peta token->id.
  simpan_compact(...)     : bytes BPE (dasar + merges) -> int16 + zlib.
  ukuran(...)             : estimasi byte.
"""

import zlib
import struct

from . import tokenizer_bpe as bpe


def baca_kata(jalan):
    """Baca daftar kata (satu per baris), return daftar unik terurut."""
    kata = set()
    for baris in open(jalan, encoding="utf-8", errors="ignore"):
        w = baris.strip().lower()
        if w.isalpha() and len(w) > 1:
            kata.add(w)
    return sorted(kata)


def buat_vocab(kata, ukuran_vokab=350):
    """Bangun vocab BPE dari DAFTAR KATA (jadi token = gabungan sub-kata).

    Kembalikan kamus model bpe (kode merges + dasar) + peta.
    """
    teks = "\n".join(kata)
    model = bpe.latih(teks, ukuran_vokab=ukuran_vokab)
    return model


def peta_kata(model, kata):
    """Terjemahkan daftar kata -> daftar id BPE (semua kata bisa diwakili)."""
    peta = bpe._buat_peta(model)
    hasil = []
    for w in kata:
        ids = bpe.ubah_ke_id(model, w, peta=peta)
        hasil.append((w, ids))
    return hasil


def simpan_compact(model, kata):
    """Seriuskan model ke bytes kecil: dasar (str) + merges (idx int16) + zlib.

    Format: [jumlah_dasar][chars masing][jumlah_merges][idx pasangan][zlib payload]
    Kembalikan bytes + metadata ukuran.
    """
    dasar = model["dasar"]
    merges = model["kode"]  # list pasangan string
    peta = bpe._buat_peta(model)
    # daftar token unik baris
    token_daftar = list(dasar) + sorted(
        set(a + b for (a, b) in merges) | set(a for (a, b) in merges) | set(b for (a, b) in merges))
    indeks = {t: i for i, t in enumerate(token_daftar)}

    # payload: daftar kata dalam bentuk id
    payload_ids = []
    for w in kata:
        wids = [indeks.get(t, 0) for t in bpe.ubah_ke_id(model, w, peta=peta)]
        payload_ids.append((len(wids), wids))

    # serialize
    buf = bytearray()
    # token strings (utf-8, length-prefixed)
    buf += struct.pack(">H", len(token_daftar))
    for t in token_daftar:
        tb = t.encode("utf-8")
        buf += struct.pack(">H", len(tb)) + tb
    # merges (indeks pasangan)
    buf += struct.pack(">H", len(merges))
    for a, b in merges:
        buf += struct.pack(">HH", indeks[a], indeks[b])
    # kata payload (jumlah kata, lalu tiap kata: len + ids uint16)
    buf += struct.pack(">I", len(payload_ids))
    for n, ids in payload_ids:
        buf += struct.pack(">H", n) + b"".join(struct.pack(">H", i) for i in ids)
    raw = bytes(buf)
    return raw, {"raw_bytes": len(raw), "zlib_bytes": len(zlib.compress(raw, 9))}


def ukuran_bytes(aset):
    """Ukuran berbagai representasi (dalam byte)."""
    return {k: len(v) if isinstance(v, (bytes, bytearray)) else 0 for k, v in aset.items()}
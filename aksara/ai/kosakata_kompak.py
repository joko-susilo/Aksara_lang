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

"""Kosakata Indonesia terkompres — gabung leksikon + korpus, BPE + zlib.

Alur jujur (tanpa sintesis ngarang):
  1. kata = leksikon (akar asli) ∪ kata unik dari korpus aplikasi.
  2. simpan vocab BPE (dasar + merges) dalam bits, lalu zlib level 9.
  3. ukur rasio & verifikasi roundtrip.

Optimal (format v2):
  - dasar: 1 string utuh (char unik), length-prefix sekali.
  - merges: pasangan index varint (anatomi token = a+b, bisa direkonstruksi).
  - token list TIDAK disimpan (diturunkan dari dasar + merges).
  - zlib level 9.

Kembalikan bytes + statistik agar dampak terukur.
"""

import zlib

from . import tokenizer_bpe as bpe


def _varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _baca_varint(data, p):
    n = 0
    shift = 0
    while True:
        b = data[p]
        p += 1
        n |= (b & 0x7F) << shift
        if not (b & 0x80):
            return n, p
        shift += 7


def gabung_kata(leksikon, korpus_path=None):
    """Gabung kata dari leksikon + korpus (1 baris = 1 kata)."""
    kata = set(leksikon)
    if korpus_path:
        for baris in open(korpus_path, encoding="utf-8", errors="ignore"):
            w = baris.strip().lower()
            if w.isalpha() and len(w) > 1:
                kata.add(w)
    return sorted(kata)


def kompres_vocab(kata, ukuran_vokab=400):
    """Bangun vocab BPE, serikan ultra-compact (tanpa daftar token)."""
    teks = "\n".join(kata)
    model = bpe.latih(teks, ukuran_vokab=ukuran_vokab)
    dasar = model["dasar"]
    peta = {c: i for i, c in enumerate(dasar)}

    # merges: hanya pasangan yang index-nya sudah terdefinisi (a,b = a+b)
    merges = []
    for a, b in model["kode"]:
        ia = peta.get(a, -1)
        ib = peta.get(b, -1)
        if ia >= 0 and ib >= 0:
            merges.append((ia, ib))
            # hasil a+b jadi token baru (index berikutnya)
            peta.setdefault(a + b, len(peta))

    buf = bytearray()
    # 1) dasar sebagai satu string utf-8 (prefix panjang)
    dasar_str = "".join(dasar).encode("utf-8")
    buf += _varint(len(dasar)) + _varint(len(dasar_str)) + dasar_str
    # 2) jumlah merges + pasangan varint
    buf += _varint(len(merges))
    for ia, ib in merges:
        buf += _varint(ia) + _varint(ib)

    zlib_bytes = zlib.compress(bytes(buf), 9)
    return zlib_bytes, {"token": len(peta), "merges": len(merges),
                        "raw_bytes": len(buf), "zlib_bytes": len(zlib_bytes)}


def dekompres_vocab(data):
    """Balik dari bytes zlib -> (dasar, merges) BPE model."""
    buf = zlib.decompress(data)
    p = 0
    n_dasar, p = _baca_varint(buf, p)
    ln_str, p = _baca_varint(buf, p)
    dasar_str = buf[p:p+ln_str].decode(); p += ln_str
    if len(dasar_str) != n_dasar:
        raise ValueError("header dasar tidak konsisten")
    dasar = list(dasar_str)
    token_list = list(dasar)
    peta = {c: i for i, c in enumerate(dasar)}
    n_merges, p = _baca_varint(buf, p)
    merges = []
    for _ in range(n_merges):
        ia, p = _baca_varint(buf, p)
        ib, p = _baca_varint(buf, p)
        a = token_list[ia]; b = token_list[ib]
        merges.append((a, b))
        token_list.append(a + b)
        peta.setdefault(a + b, len(token_list) - 1)
    return {"dasar": dasar, "kode": merges}
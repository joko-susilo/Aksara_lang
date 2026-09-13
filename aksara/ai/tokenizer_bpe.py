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

"""BPE Tokenizer Bahasa Indonesia — dibangun dari nol (numpy murni).

Fondasi kompresi Mini LM v2: vocab sub-kata dilatih DARI KORPUS SENDIRI
(bukan tokenizer Inggris/umum). Tagihan: lebih banyak makna per token =>
ukuran model turun, kecepatan naik.

Pemakaian dari Aksara:
    impor "aksara.ai.tokenizer_bpe" sbg bpe
    tok = bpe.latih(korpus, ukuran_vokab = 256)
    ids = bpe.ubah_ke_id(tok, "bahasa pemrograman")
    teks = bpe.ubah_ke_teks(tok, ids)
"""

import json

_EW = "\x02"  # penanda akhir kata (sentinel byte, tak muncul di teks normal)


def _kata_awal(teks):
    """Tokenisasi kata murni + akhiran karakter (basis BPE)."""
    import re
    return re.findall(r"\S+", teks)


def _jumlah_pasangan(daftar_awal):
    """Hitung frekuensi tiap pasangan token yang bersebelahan."""
    pasangan = {}
    for baris in daftar_awal:
        for a, b in zip(baris, baris[1:]):
            kunci = (a, b)
            pasangan[kunci] = pasangan.get(kunci, 0) + 1
    return pasangan


def latih(teks, ukuran_vokab=256, max_utf8_kar=256):
    """Bangun vocab BPE dari korpus teks.

    Kembalikan kamus: {kode: [sub-token1, sub-token2, ...]} + set token dasar.
    """
    import re
    # token dasar = karakter utf-8 byte (maks max_utf8_kar token umum)
    base_kar = set(teks)
    # batasi ke token byte paling umum supaya vocab kecil
    hitung = {}
    for c in teks:
        hitung[c] = hitung.get(c, 0) + 1
    terurut = sorted(hitung.keys(), key=lambda c: -hitung[c])
    dasar = terurut[:max_utf8_kar]
    # sisa karakter entah jadi token "lain" ([[UNK]])
    daftar_awal = []
    for kata in _kata_awal(teks):
        baris = []
        for c in kata:
            if c in dasar:
                baris.append(c)
            else:
                baris.append("[[UNK]]")
        baris.append(_EW)
        daftar_awal.append(baris)

    gabungan = []
    set_tok = list(dasar)
    for _ in range(ukuran_vokab - len(set_tok)):
        pasangan = _jumlah_pasangan(daftar_awal)
        if not pasangan:
            break
        pemenang = max(pasangan, key=pasangan.get)
        a, b = pemenang
        gabungan.append(pemenang)
        set_tok.append(a + b)
        baru = []
        for baris in daftar_awal:
            i = 0
            hasil = []
            while i < len(baris):
                if i < len(baris) - 1 and baris[i] == a and baris[i + 1] == b:
                    hasil.append(a + b)
                    i += 2
                else:
                    hasil.append(baris[i])
                    i += 1
            baru.append(hasil)
        daftar_awal = baru

    return {"kode": gabungan, "dasar": dasar, "ukuran_vokab": len(set_tok)}


def _terapkan_kode(baris, kode):
    """Terapkan daftar penggabungan BPE ke satu baris token."""
    # kode: list pasangan diurutkan dari paling awal digabung (urutan latih)
    for a, b in reversed(kode):
        i = 0
        hasil = []
        while i < len(baris):
            if i < len(baris) - 1 and baris[i] == a and baris[i + 1] == b:
                hasil.append(a + b)
                i += 2
            else:
                hasil.append(baris[i])
                i += 1
        baris = hasil
    return baris


def ubah_ke_id(model, teks, peta=None):
    """Teks -> daftar id token (pakai vocab model)."""
    if peta is None:
        peta = _buat_peta(model)
    ids = []
    for kata in _kata_awal(teks):
        baris = list(kata) + [_EW]
        baris = _terapkan_kode(baris, model["kode"])
        for t in baris:
            ids.append(peta.get(t, peta["[[UNK]]"]))
    return ids


def ubah_ke_teks(model, ids, balik_peta=None):
    """Daftar id token -> teks asli."""
    if balik_peta is None:
        inv = {v: k for k, v in _buat_peta(model).items()}
    else:
        inv = balik_peta
    butir = []
    for i in ids:
        t = inv.get(int(i), "[[UNK]]")
        if t == _EW:
            butir.append(" ")
        elif t.endswith(_EW):
            butir.append(t[:-len(_EW)])
            butir.append(" ")
        elif t == "[[UNK]]":
            butir.append("?")
        else:
            butir.append(t)
    hasil = "".join(butir)
    # rapikan spasi berlebih yang lahir dari penanda akhir kata
    return " ".join(hasil.split())


def _buat_peta(model):
    idx = 0
    peta = {}
    for t in model["dasar"]:
        peta[t] = idx
        idx += 1
    for token in sorted(set(
        a + b for (a, b) in model["kode"]
    ) | set(a for (a, b) in model["kode"]) | set(b for (a, b) in model["kode"])):
        if token not in peta:
            peta[token] = idx
            idx += 1
    for (a, b) in model["kode"]:
        t = a + b
        if t not in peta:
            peta[t] = idx
            idx += 1
    if "[[UNK]]" not in peta:
        peta["[[UNK]]"] = idx
        idx += 1
    if _EW not in peta:
        peta[_EW] = idx
        idx += 1
    return peta


def info(model):
    """Ringkasan vokabulari untuk laporan terukur."""
    vokab = len(set(_buat_peta(model).keys()))
    return {
        "ukuran_vokab": vokab,
        "jumlah_penggabungan": len(model["kode"]),
        "karakter_dasar": len(model["dasar"]),
    }
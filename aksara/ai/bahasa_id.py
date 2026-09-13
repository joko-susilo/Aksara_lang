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

"""Parameter Bahasa Indonesia — pemahaman tata bahasa & budaya.

Komponen:
  1. stem_afiks  : hapus awalan me/mem/men/meng/ber/ter/di/ke/pe + akhiran
  2. deteksi_kalimat_tanya : interogatif (apakah/berapa/kapan/dimana/siapa)
  3. deteksi_negasi : "nggak/tidak/tanpa" & negasi budaya Indonesia
  4. ejaan_baku  : koreksi kecil (gak->tidak, aja->saja)
  5. kata_serapan : daftar serapan umum untuk pemahaman konteks
Hemat: tabel kecil string, nol model besar.
"""

# Awalan (prefix); panjang->pendek biar greppy dulu
AWALAN = ["memper", "mempe", "meng", "mem", "men", "ber", "ter",
          "diper", "di", "ke", "pe", "pen", "peng", "se", "me"]

# Akhiran (suffix)
AKHIRAN = ["kan", "an", "inya", "kah", "lah", "tah", "nya", "mu", "ku", "i", "s"]

# Interogatif bahasa Indonesia
KATA_TANYA = ["apakah", "berapa", "kapan", "di mana", "dimana", "siapa",
              "mengapa", "kenapa", "mana", "bagaimana", "gimana", "apa"]

# Negasi bahasa Indonesia (formal & percakapan)
NEGASI = ["tidak", "nggak", "gak", "tak", "bukan", "tanpa", "belum",
          "jangan", "mustahil", "ngga"]

# Serapan umum untuk memahami konteks santai/campuran
SERAPAN = {
    "gak": "tidak", "nggak": "tidak", "ngga": "tidak", "ga": "tidak",
    "aja": "saja", "deh": "saja", "dong": "dulu", "kok": "rasanya",
    "banget": "sangat", "gue": "saya", "lu": "kamu", "kamu sekalian": "kalian",
    "cuma": "hanya", "sekalian": "sambil", "sudah": "telah", "udah": "telah",
}


def stem_afiks(kata, kamus_rendah=None):
    """Hapus afiks bahasa Indonesia, kembalikan akar kandidat.

    Tidak memakai kamus jika None (hanya heuristic morfologis).
    Mengembalikan daftar kandidat akar (dari yang paling mungkin).
    """
    k = kata.lower()
    akar = k
    hasil = [k]

    for aw in AWALAN:
        if k.startswith(aw) and len(k) > len(aw) + 2:
            # aturan gabungan konsonan: men + p pandi -> mencan... (hanya sederhana)
            inti = k[len(aw):]
            for akh in AKHIRAN:
                if inti.endswith(akh) and len(inti) > len(akh) + 1:
                    hasil.append(inti[:-len(akh)])
            hasil.append(inti)
            break

    # coba tanpa akhiran (mis. kata benda yang ber-akhiran an/nya)
    for akh in AKHIRAN:
        if k.endswith(akh) and len(k) > len(akh) + 2:
            hasil.append(k[:-len(akh)])

    # dedupe panjang->pendek urut
    unik = list(dict.fromkeys(hasil))
    return unik


def adalah_kalimat_tanya(teks):
    k = teks.lower().strip()
    if k.endswith("?"):
        return True
    for w in KATA_TANYA:
        if w in k:
            return True
    return False


def adalah_negasi(teks):
    k = teks.lower()
    for w in NEGASI:
        if w in k:
            return True
    return False


def normalisasi_santai(teks):
    """Ubah kata santai ke baku (gak->tidak, aja->saja), termasuk posisi awal/akhir."""
    import re
    k = " " + teks + " "
    for s in sorted(SERAPAN, key=len, reverse=True):
        k = re.sub(r" " + re.escape(s) + r"([\s.,!?])", " " + SERAPAN[s] + r"\1", k)
    return k.strip()


def info(teks):
    """Ringkas ciri kalimat untuk debugging/laporan."""
    return {
        "tanya": adalah_kalimat_tanya(teks),
        "negasi": adalah_negasi(teks),
        "kata_inti": stem_afiks(teks)[0],
        "normal": normalisasi_santai(teks)[:120],
    }
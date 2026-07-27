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

def ringkas(teks, maks_kalimat=3):
    """Ringkasan teks sederhana berdasarkan kalimat terpenting"""
    # Pecah ke kalimat
    kalimat = teks.replace("!", ".").replace("?", ".").split(". ")
    kalimat = [k.strip() for k in kalimat if len(k.strip()) > 10]
    
    if len(kalimat) <= maks_kalimat:
        return teks
    
    # Hitung skor tiap kalimat (berdasarkan kata kunci)
    kata_penting = ["penting", "utama", "kunci", "hasil", "kesimpulan", "adalah", "yaitu", "dengan", "ini", "itu"]
    
    skor = []
    for k in kalimat:
        s = len(k)  # kalimat panjang = penting
        for kata in kata_penting:
            if kata in k.lower():
                s += 10  # bonus kata penting
        skor.append(s)
    
    # Ambil kalimat dengan skor tertinggi
    indeks_terbaik = sorted(range(len(skor)), key=lambda i: skor[i], reverse=True)[:maks_kalimat]
    indeks_terbaik.sort()
    
    hasil = ". ".join([kalimat[i] for i in indeks_terbaik]) + "."
    return hasil

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

def jenis(teks):
    """Klasifikasi sentimen sederhana"""
    positif = ["bagus", "keren", "mantap", "suka", "hebat", "baik", "senang", "indah", "cantik", "luar biasa", "oke", "recommended"]
    negatif = ["jelek", "buruk", "kecewa", "sedih", "marah", "payah", "bosen", "bosan", "rugi", "sampah", "tolol", "gagal"]
    
    teks = teks.lower()
    skor = 0
    
    for kata in positif:
        if kata in teks:
            skor = skor + 1
    
    for kata in negatif:
        if kata in teks:
            skor = skor - 1
    
    if skor > 0:
        return "positif"
    elif skor < 0:
        return "negatif"
    else:
        return "netral"

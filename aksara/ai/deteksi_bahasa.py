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
def deteksi_bahasa(teks):
    """Deteksi bahasa dari teks (Indonesia, Sunda, Jawa, Inggris)"""
    kamus = {
        "sunda": ["kumaha", "damang", "teh", "mah", "ieu", "eta"],
        "jawa": ["piye", "kabare", "iki", "iku", "tenan"],
        "indonesia": ["yang", "dan", "di", "ini", "itu", "adalah"],
        "inggris": ["the", "is", "are", "and", "you", "this"]
    }
    
    teks = teks.lower()
    skor = {}
    
    for bahasa, kata_list in kamus.items():
        skor[bahasa] = 0
        for kata in kata_list:
            if kata in teks:
                skor[bahasa] = skor[bahasa] + 1
    
    terbaik = "indonesia"
    skor_terbaik = 0
    for bahasa, s in skor.items():
        if s > skor_terbaik:
            skor_terbaik = s
            terbaik = bahasa
    
    return terbaik

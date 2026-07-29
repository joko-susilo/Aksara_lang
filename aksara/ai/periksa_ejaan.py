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
def periksa_ejaan(teks):
    """Koreksi ejaan sederhana (kamus terbatas)"""
    koreksi = {
        "aq": "aku",
        "loe": "kamu",
        "gk": "tidak",
        "ga": "tidak",
        "yg": "yang",
        "dg": "dengan",
        "tp": "tetapi",
        "tdk": "tidak",
        "blm": "belum",
        "sdh": "sudah"
    }
    
    kata_list = teks.split(" ")
    hasil = []
    
    for kata in kata_list:
        if kata.lower() in koreksi:
            hasil.append(koreksi[kata.lower()])
        else:
            hasil.append(kata)
    
    return " ".join(hasil)

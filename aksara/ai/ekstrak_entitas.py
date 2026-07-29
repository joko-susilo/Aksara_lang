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

def ekstrak_entitas(teks):
    """Ekstrak entitas (nama, tempat, angka) dari teks"""
    import re
    
    hasil = {
        "angka": [],
        "tempat": ["Jakarta", "Bandung", "Surabaya", "Medan", "Bali"],
        "nama": []
    }
    
    # Ekstrak angka
    angka_list = re.findall(r'\d+', teks)
    hasil["angka"] = [int(a) for a in angka_list]
    
    # Ekstrak tempat
    for tempat in hasil["tempat"]:
        if tempat.lower() in teks.lower():
            hasil["tempat"] = [tempat]
            break
    
    return hasil

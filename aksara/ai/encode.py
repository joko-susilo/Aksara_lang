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
def encode(data):
    """One-hot encoding sederhana"""
    # Ambil semua kategori unik
    kategori = []
    for item in data:
        if item not in kategori:
            kategori.append(item)
    
    # Encode setiap item
    hasil = []
    for item in data:
        encoded = []
        for k in kategori:
            if item == k:
                encoded.append(1)
            else:
                encoded.append(0)
        hasil.append(encoded)
    
    return {"kategori": kategori, "encoded": hasil}

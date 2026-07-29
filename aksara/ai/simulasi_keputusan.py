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

def simulasi_keputusan(kondisi, riwayat):
    """Simulasi keputusan berdasarkan riwayat"""
    if not riwayat:
        return "Tidak ada data"
    
    # Hitung probabilitas transisi sederhana
    transisi = {}
    for i in range(len(riwayat)-1):
        key = riwayat[i]
        if key not in transisi:
            transisi[key] = []
        transisi[key].append(riwayat[i+1])
    
    if kondisi in transisi:
        # Return opsi paling sering
        opsi = transisi[kondisi]
        return max(set(opsi), key=opsi.count)
    
    return "Tidak diketahui"

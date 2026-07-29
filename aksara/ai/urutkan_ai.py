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
def urutkan_ai(data):
    """Sorting cerdas (pilih metode terbaik)"""
    n = len(data)
    
    # Data kecil → bubble sort
    if n <= 10:
        for i in range(n):
            for j in range(n-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data
    
    # Data besar → quick sort sederhana
    if n <= 1:
        return data
    
    pivot = data[n//2]
    kiri = [x for x in data if x < pivot]
    tengah = [x for x in data if x == pivot]
    kanan = [x for x in data if x > pivot]
    
    return urutkan_ai(kiri) + tengah + urutkan_ai(kanan)

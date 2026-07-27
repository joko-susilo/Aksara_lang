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

def tebak(data_list):
    """Prediksi 2 angka selanjutnya dari deret (regresi linear sederhana)"""
    n = len(data_list)
    if n < 2:
        return data_list
    
    # Hitung rata-rata x dan y
    x_mean = sum(range(n)) / n
    y_mean = sum(data_list) / n
    
    # Hitung slope (w) dan intercept (b)
    num = sum((i - x_mean) * (data_list[i] - y_mean) for i in range(n))
    den = sum((i - x_mean) ** 2 for i in range(n))
    
    if den == 0:
        return [data_list[-1], data_list[-1]]
    
    w = num / den
    b = y_mean - w * x_mean
    
    # Prediksi 2 langkah ke depan
    hasil = [w * (n + i) + b for i in range(1, 3)]
    return [round(x, 2) for x in hasil]
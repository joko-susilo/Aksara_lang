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

import numpy as np

def korelasi(x, y):
    """Hitung korelasi Pearson antara dua variabel"""
    if len(x) != len(y) or len(x) < 2:
        return 0
    
    x = np.array(x)
    y = np.array(y)
    
    # Rumus Pearson
    n = len(x)
    atas = n * np.sum(x * y) - np.sum(x) * np.sum(y)
    bawah = np.sqrt((n * np.sum(x**2) - np.sum(x)**2) * (n * np.sum(y**2) - np.sum(y)**2))
    
    if bawah == 0:
        return 0
    
    return round(atas / bawah, 4)

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
import math

def rangking_tfidf(dokumen, kueri):
    """TF-IDF ranking sederhana"""
    # Tokenisasi sederhana
    docs_token = [d.lower().split() for d in dokumen]
    kueri_token = kueri.lower().split()
    
    # Hitung TF
    skor = []
    for doc in docs_token:
        s = 0
        for kata in kueri_token:
            tf = doc.count(kata) / len(doc) if len(doc) > 0 else 0
            
            # IDF sederhana
            df = sum(1 for d in docs_token if kata in d)
            idf = math.log(len(docs_token) / (df + 1)) + 1
            
            s += tf * idf
        skor.append(round(s, 4))
    
    return skor

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
def auto_label(data):
    """Auto labeling berdasarkan kata kunci"""
    label = []
    
    for teks in data:
        teks_lower = teks.lower()
        
        if "rusak" in teks_lower or "jelek" in teks_lower or "kecewa" in teks_lower:
            label.append("negatif")
        elif "bagus" in teks_lower or "keren" in teks_lower or "puas" in teks_lower:
            label.append("positif")
        else:
            label.append("netral")
    
    return label

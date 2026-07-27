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


from dataclasses import dataclass

@dataclass
class Token:
    """Representasi token dengan informasi posisi di kode sumber."""
    tipe: str       # Jenis token: 'KATA_KUNCI', 'NAMA', 'ANGKA', 'STRING', 'OPERATOR', 'KURUNG', 'KURUNG_KUWAL', 'EOF'
    nilai: str      # Teks asli token
    baris: int      # Nomor baris (mulai dari 1)
    kolom: int      # Posisi kolom (mulai dari 1)

    def __repr__(self):
        return f"Token({self.tipe!r}, {self.nilai!r}, baris={self.baris}, kolom={self.kolom})"

# Daftar kata kunci resmi Aksara (versi pendek)
KATA_KUNCI = [
    # Kontrol alur
    "jika", "atau_jika", "lain",
    # Perulangan
    "ulang", "untuk", "dalam", "selama",
    # Fungsi
    "fun", "balik",
    # Output
    "cetak",
    # Kontrol loop
    "henti", "lanjut",
    # Boolean dan null
    "benar", "salah", "nil",
    # Modul
    "impor", "sbg",
    "dan","atau","bukan",
    # Error
    "coba","kecuali","akhirnya",
    "sebagai","galat"
]

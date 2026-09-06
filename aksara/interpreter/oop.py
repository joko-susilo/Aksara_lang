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

"""Runtime OOP Aksara.

Nilai kelas dan objek dinyatakan lewat `KelasValue` dan `ObjekAksara`.
Kontrak metode: `metode(ini, *argumen)` — `ini` adalah objek pemanggil,
dimasukkan secara implisit oleh bahasa.
"""


class KelasValue:
    """Sebuah kelas Aksara: nama + kamus metode {nama: callable(ini, *args)}.

    Bila punya induk, kamus metode digabung (metode anak menimpa induk).
    Metode induk tetap bisa dipanggil lewat objek `_PranalaInduk` (super).
    """

    def __init__(self, nama: str, metode: dict, induk=None):
        self.nama = nama
        self.induk = induk if isinstance(induk, KelasValue) else None
        if self.induk is not None:
            self.metode = {**self.induk.metode, **metode}
        else:
            self.metode = dict(metode)

    def __getattr__(self, nama):
        # Panggilan Kelas.metode(...) = konstruktor: buat objek, jalankan
        # metode, kembalikan objek.
        if nama in self.metode:
            return _Pabrik(self, nama)
        raise AttributeError(f"Kelas '{self.nama}' tidak memiliki metode '{nama}'")

    def __repr__(self):
        d = f" dari {self.induk.nama}" if self.induk else ""
        return f"Kelas {self.nama}{d}"


class _Pabrik:
    """Konstruktor terkait: Kelas.metode(args) -> ObjekAksara."""

    def __init__(self, kelas, nama):
        self.kelas = kelas
        self.nama = nama

    def __call__(self, *argumen):
        obj = ObjekAksara(self.kelas)
        self.kelas.metode[self.nama](obj, *argumen)
        return obj


class ObjekAksara:
    """Objek instance Aksara: atribut + referensi kelas."""

    def __init__(self, kelas):
        self.kelas = kelas
        self.data = {}

    def __getattr__(self, nama):
        if nama in self.kelas.metode:
            return _MetodeTerikat(self, nama)
        if nama in self.data:
            return self.data[nama]
        raise AttributeError(f"Objek '{self.kelas.nama}' tidak memiliki '{nama}'")

    def __setattr__(self, nama, nilai):
        if nama in ("kelas", "data"):
            object.__setattr__(self, nama, nilai)
        else:
            self.data[nama] = nilai

    def __contains__(self, nama):
        return nama in self.data or nama in self.kelas.metode

    def __repr__(self):
        return f"Objek {self.kelas.nama} {self.data}"


class _MetodeTerikat:
    """Metode terikat pada instance: objek.metode(args).

    `kelas` opsional menentukan sumber kamus metode (mis. kelas induk untuk
    super). Nilai None berarti memakai kelas objek itu sendiri.
    """

    def __init__(self, obj, nama, kelas=None):
        self.obj = obj
        self.nama = nama
        self.kelas = kelas

    def __call__(self, *argumen):
        sumber = self.kelas if self.kelas is not None else self.obj.kelas
        return sumber.metode[self.nama](self.obj, *argumen)

    def __repr__(self):
        return f"<metode {self.nama} terikat>"


class MetodeInterp:
    """Pembungkus metode berbody AST Aksara agar memenuhi kontrak (ini, *args)."""

    def __init__(self, fungsi_node, closure, evaluator, kelas_asal=None):
        self.fungsi = fungsi_node  # DefinisiFungsi
        self.closure = closure
        self.eval = evaluator
        self.kelas_asal = kelas_asal

    def __call__(self, ini, *argumen):
        return self.eval.panggil_metode(
            self.fungsi, ini, argumen, self.closure, self.kelas_asal
        )


def def_kelas(nama: str, metode: dict) -> KelasValue:
    """Membangun KelasValue; dipakai hasil kompilasi."""
    return KelasValue(nama, metode)


class _PranalaInduk:
    """Proxy untuk panggil metode induk: `induk.metode(args)`."""

    def __init__(self, obj, kelas_induk):
        self.obj = obj
        self.kelas = kelas_induk

    def __getattr__(self, nama):
        if self.kelas is None:
            raise AttributeError(f"Tidak ada induk yang bisa dipanggil")
        if nama in self.kelas.metode:
            return _MetodeTerikat(self.obj, nama, self.kelas)
        raise AttributeError(f"Induk '{self.kelas.nama}' tidak memiliki '{nama}'")

    def __repr__(self):
        nama_induk = self.kelas.nama if self.kelas else "Tidak ada"
        return f"<induk {nama_induk}>"
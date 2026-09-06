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

from aksara.ast.nodes import (
    Angka, AksesAtribut, AksesIndeks, Assign, Balik, Boolean, Cetak, Coba,
    Daftar, DefinisiFungsi, Galat, Henti, Impor, ImporLokal, Jika, Kamus,
    Lanjut, NamaVariabel, Nil, OperasiBiner, OperasiUnary, PanggilFungsi,
    Selama, Slice, String, Ulangi, Untuk,
)
from aksara.interpreter.builtins import BUILTINS

IMPORAN = "    "

# Builtin yang padanannya lurus ke fungsi bawaan Python.
PY_BUILTIN = {
    "cetak":   "print",
    "panjang": "len",
    "masukan": "input",
    "bulat":   "int",
    "desimal": "float",
    "teks":    "str",
}

# Nama fungsi asli di modul builtins untuk tiap kata kunci builtin.
BUILTIN_FUNC = {nama: fn.__name__ for nama, fn in BUILTINS.items() if hasattr(fn, "__name__")}


class AksaraCompiler:
    """Menyusun AST Aksara menjadi kode Python yang setara.

    Semantik mengikuti `aksara.interpreter.evaluator`:
    * rentang a..b dan slice n[m..x] bersifat INKLUSIF (ujung ditambah 1);
    * operator ?? (null coalescing) mengevaluasi sisi kiri tepat sekali;
    * builtin Aksara diimpor ulang otomatis jika dipakai;
    * impor file .ak lokal dimuat lewat runtime aksara (SimpleNamespace).
    """

    def __init__(self):
        self._indent = 0
        self._builtin_pakai = set()
        self._perlu_muat_lokal = False
        self._perlu_tambah = False

    # ------------------------------------------------------------------
    # API publik
    # ------------------------------------------------------------------
    def compile_program(self, ast_list) -> str:
        self._reset()
        badan = "\n".join(self._statemen(ast_list))
        prakata = self._prakata()
        if prakata:
            return prakata + "\n\n" + badan
        return badan

    # ------------------------------------------------------------------
    # Ekspresi
    # ------------------------------------------------------------------
    def _expr(self, node) -> str:
        if isinstance(node, Angka):
            return str(node.nilai)

        if isinstance(node, String):
            return repr(node.nilai)

        if isinstance(node, Boolean):
            return "True" if node.nilai else "False"

        if isinstance(node, Nil):
            return "None"

        if isinstance(node, NamaVariabel):
            return node.nama

        if isinstance(node, Daftar):
            return "[" + ", ".join(self._expr(el) for el in node.elemen) + "]"

        if isinstance(node, Kamus):
            isi = ", ".join(
                f"{self._expr(k)}: {self._expr(v)}" for k, v in node.pasangan
            )
            return "{" + isi + "}"

        if isinstance(node, OperasiBiner):
            return self._expr_biner(node)

        if isinstance(node, OperasiUnary):
            if node.op == "-":
                return f"(-({self._expr(node.ekspresi)}))"
            if node.op == "bukan":
                return f"(not ({self._expr(node.ekspresi)}))"
            raise NotImplementedError(f"Operator unary '{node.op}' belum didukung kompiler")

        if isinstance(node, PanggilFungsi):
            return self._expr_panggil(node)

        if isinstance(node, AksesIndeks):
            return f"({self._expr(node.objek)})[{self._expr(node.indeks)}]"

        if isinstance(node, AksesAtribut):
            return f"({self._expr(node.objek)}).{node.atribut}"

        if isinstance(node, Slice):
            mula = self._expr(node.mulai) if node.mulai is not None else ""
            akhir = ""
            if node.akhir is not None:
                akhir = f"{self._expr(node.akhir)} + 1"
            return f"({self._expr(node.objek)})[{mula}:{akhir}]"

        raise NotImplementedError(
            f"Kompilasi ekspresi belum didukung untuk {type(node).__name__}"
        )

    def _expr_biner(self, node) -> str:
        kiri = self._expr(node.kiri)
        kanan = self._expr(node.kanan)
        op = node.op

        if op == "??":
            # Null coalescing: evaluasi kiri sekali saja.
            return f"((lambda __ak: __ak if __ak is not None else {kanan})({kiri}))"

        if op == "+":
            # Interpreter: bila salah satu operand string, gabungkan sebagai string.
            self._perlu_tambah = True
            return f"_ak_tambah({kiri}, {kanan})"

        peta = {
            "-": "-", "*": "*", "/": "/", "%": "%", "**": "**",
            "==": "==", "!=": "!=", "<": "<", ">": ">", "<=": "<=", ">=": ">=",
            "dan": "and", "atau": "or",
        }
        if op not in peta:
            raise NotImplementedError(f"Operator '{op}' belum didukung kompiler")
        return f"({kiri} {peta[op]} {kanan})"

    def _expr_panggil(self, node) -> str:
        args = ", ".join(self._expr(a) for a in node.argumen)

        if isinstance(node.fungsi, NamaVariabel):
            nama = node.fungsi.nama
            if nama in BUILTINS:
                self._builtin_pakai.add(nama)
            if nama in PY_BUILTIN:
                return f"{PY_BUILTIN[nama]}({args})"
            return f"{nama}({args})"

        return f"{self._expr(node.fungsi)}({args})"

    # ------------------------------------------------------------------
    # Statement
    # ------------------------------------------------------------------
    def _statemen(self, daftar_statement) -> list:
        """Mengubah daftar statement menjadi baris kode (dipisah baris kosong)."""
        hasil = []
        for s in daftar_statement:
            if hasil:
                hasil.append("")
            hasil.extend(self._stmt(s))
        return hasil

    def _blok(self, daftar_statement) -> list:
        """Mengubah daftar statement menjadi baris dengan indentasi +1."""
        self._indent += 1
        try:
            baris = self._statemen(daftar_statement)
            if not baris:
                baris = [self._pad() + "pass"]
        finally:
            self._indent -= 1
        return baris

    def _pad(self) -> str:
        return IMPORAN * self._indent

    def _stmt(self, node) -> list:
        pad = self._pad()

        if isinstance(node, Cetak):
            return [f"{pad}print({self._expr(node.ekspresi)})"]

        if isinstance(node, Assign):
            return [f"{pad}{self._target(node.target)} = {self._expr(node.nilai)}"]

        if isinstance(node, Balik):
            ekspr = self._expr(node.ekspresi) if node.ekspresi is not None else ""
            return [f"{pad}return {ekspr}"]

        if isinstance(node, Henti):
            return [f"{pad}break"]

        if isinstance(node, Lanjut):
            return [f"{pad}continue"]

        if isinstance(node, Galat):
            return [f"{pad}raise RuntimeError(str({self._expr(node.pesan)}))"]

        if isinstance(node, Selama):
            return [f"{pad}while {self._expr(node.kondisi)}:"] + self._blok(node.blok)

        if isinstance(node, Ulangi):
            return [f"{pad}for _ in range({self._expr(node.jumlah)}):"] + self._blok(node.blok)

        if isinstance(node, Untuk):
            return [self._header_untuk(node, pad)] + self._blok(node.blok)

        if isinstance(node, Jika):
            return self._stmt_jika(node, pad)

        if isinstance(node, DefinisiFungsi):
            param = ", ".join(node.parameter)
            return [f"{pad}def {node.nama}({param}):"] + self._blok(node.blok)

        if isinstance(node, Coba):
            return self._stmt_coba(node, pad)

        if isinstance(node, Impor):
            last = node.nama_modul.rsplit(".", 1)[-1]
            if node.alias and node.alias != last and node.alias != node.nama_modul:
                return [f"{pad}import {node.nama_modul} as {node.alias}"]
            return [f"{pad}import {node.nama_modul}"]

        if isinstance(node, ImporLokal):
            self._perlu_muat_lokal = True
            return [f"{pad}{node.alias} = _muat_aksara({node.nama_file!r})"]

        # Statement ekspresi murni (daftar/kamus/literal/nama dsb.)
        return [f"{pad}{self._expr(node)}"]

    def _target(self, node) -> str:
        if isinstance(node, NamaVariabel):
            return node.nama
        if isinstance(node, AksesIndeks):
            return f"({self._expr(node.objek)})[{self._expr(node.indeks)}]"
        if isinstance(node, AksesAtribut):
            return f"({self._expr(node.objek)}).{node.atribut}"
        raise NotImplementedError(
            f"Target assignment '{type(node).__name__}' belum didukung"
        )

    def _header_untuk(self, node, pad) -> str:
        if node.akhir is None:
            return f"{pad}for {node.var} in {self._expr(node.mulai)}:"
        mula = self._expr(node.mulai)
        akhir = self._expr(node.akhir)
        return f"{pad}for {node.var} in range(int({mula}), int({akhir}) + 1):"

    def _stmt_jika(self, node, pad) -> list:
        baris = [f"{pad}if {self._expr(node.kondisi)}:"] + self._blok(node.blok_jika)
        for cabang in node.cabang_lain:
            if isinstance(cabang, Jika):
                baris += [f"{pad}elif {self._expr(cabang.kondisi)}:"] + self._blok(cabang.blok_jika)
            else:
                baris += [f"{pad}else:"] + self._blok(cabang)
        return baris

    def _stmt_coba(self, node, pad) -> list:
        baris = [f"{pad}try:"] + self._blok(node.blok_coba)
        for cabang in node.kecuali_list:
            if cabang.tipe_error:
                header = f"{pad}except {cabang.tipe_error} as __ak_err:"
            else:
                header = f"{pad}except Exception as __ak_err:"
            baris.append(header)
            if cabang.var_error:
                baris.append(f"{IMPORAN * (self._indent + 1)}{cabang.var_error} = str(__ak_err)")
            self._indent += 1
            try:
                baris += self._statemen(cabang.blok)
            finally:
                self._indent -= 1
        if node.akhirnya is not None:
            baris += [f"{pad}finally:"] + self._blok(node.akhirnya)
        return baris

    # ------------------------------------------------------------------
    # Prakata: penolong impor lokal + impor builtin ekstra
    # ------------------------------------------------------------------
    def _prakata(self) -> str:
        bagian = []
        if self._perlu_muat_lokal:
            bagian.append(_PENOLONG_IMPOR_LOKAL)
        if self._perlu_tambah:
            bagian.append(_PENOLONG_TAMBAH)
        if self._builtin_pakai:
            impor_baru = []
            for nama in sorted(self._builtin_pakai):
                if nama in PY_BUILTIN:
                    continue
                fungsi = BUILTIN_FUNC.get(nama, nama)
                if fungsi == nama:
                    impor_baru.append(f"from aksara.interpreter.builtins import {nama}")
                else:
                    impor_baru.append(f"from aksara.interpreter.builtins import {fungsi} as {nama}")
            bagian.append("\n".join(impor_baru))
        return "\n\n".join(bagian)

    def _reset(self):
        self._indent = 0
        self._builtin_pakai = set()
        self._perlu_muat_lokal = False
        self._perlu_tambah = False


_PENOLONG_TAMBAH = ("def _ak_tambah(a, b):\n"
                    "    if isinstance(a, str) or isinstance(b, str):\n"
                    "        return str(a) + str(b)\n"
                    "    return a + b\n")


_PENOLONG_IMPOR_LOKAL = '''import os as __os, types as __types


def _muat_aksara(nama_file):
    """Memuat file .ak lewat runtime aksara saat program dijalankan."""
    from aksara.lexer.tokenizer import tokenize
    from aksara.parser.parser import Parser
    from aksara.interpreter.environment import Environment
    from aksara.interpreter.evaluator import evaluate

    for jalur in (f"stdlib/{nama_file}", nama_file):
        if __os.path.exists(jalur):
            with open(jalur, encoding="utf-8") as f:
                kode = f.read()
            ast = Parser(tokenize(kode)).parse_program()
            env = Environment()
            for stmt in ast:
                evaluate(stmt, env)
            return __types.SimpleNamespace(**env.vars)
    raise ImportError(f"Tidak dapat menemukan '{nama_file}'")
'''
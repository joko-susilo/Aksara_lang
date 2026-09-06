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

"""REPL (Read-Eval-Print Loop) interaktif untuk Aksara."""

import contextlib
import re
import sys

from aksara.ast.nodes import (AksesAtribut, AksesIndeks, Angka, Assign, Balik,
                              Boolean, Cetak, Coba, Daftar, DefinisiFungsi,
                              Galat, Henti, Impor, ImporLokal, Jika, Kamus,
                              Lanjut, Nil, OperasiBiner, PanggilFungsi,
                              Selama, String, Ulangi, Untuk, NamaVariabel)
from aksara.lexer.tokenizer import tokenize
from aksara.parser.parser import Parser
from aksara.interpreter.environment import Environment
from aksara.interpreter.evaluator import evaluate

TIPE_STATEMENT = (Assign, Balik, Cetak, Coba, DefinisiFungsi, Galat, Henti,
                  Impor, ImporLokal, Jika, Lanjut, Selama, Ulangi, Untuk)

PROMPT = "aksara> "
PROMPT_LANJUT = "... "
PROMPT_HEREDOC = ":   "

_POLOSKAN_STRING = re.compile(r'"(?:[^"\\]|\\.)*"')


class Repl:
    """Loop baca-evaluasi-cetak dengan environment yang persisten."""

    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.env = Environment()

    # ------------------------------------------------------------------
    # Input (dengan deteksi blok belum tertutup)
    # ------------------------------------------------------------------
    def _baca_multi_line(self) -> str:
        """Membaca satu 'unit' kode: bisa beberapa baris sampai { tutup."""
        teks = self._baca_baris(PROMPT)
        if teks is None:
            return None

        # Mode heredoc: baris pertama persis ':' → baca sampai ':EOF'.
        if teks.strip() == ":":
            blok = []
            while True:
                baris_in = self._baca_baris(PROMPT_HEREDOC)
                if baris_in is None or baris_in.strip() == ":EOF":
                    break
                blok.append(baris_in)
            return "\n".join(blok)

        baris = [teks]
        while not self._blok_tertutup(baris):
            baris_lanjut = self._baca_baris(PROMPT_LANJUT)
            if baris_lanjut is None:
                break
            baris.append(baris_lanjut)
        return "\n".join(baris)

    def _baca_baris(self, prompt) -> str:
        if self._moda_tty:
            try:
                inp = input(prompt)
            except EOFError:
                return None
            except KeyboardInterrupt:
                self.stdout.write("\n")
                return None
        else:
            inp = self.stdin.readline()
            if not inp:
                return None
            self.stdout.write(prompt)
            self.stdout.write(inp)
            self.stdout.flush()
            inp = inp.rstrip("\n")
        return inp

    @staticmethod
    def _blok_tertutup(baris) -> bool:
        """True bila kurung kurawal/kurung/siku di baris sudah seimbang."""
        teks = "\n".join(baris)
        # Abaikan string agar { } di dalam literal tidak dihitung.
        teks = _POLOSKAN_STRING.sub('""', teks)
        buka = teks.count("{") + teks.count("(") + teks.count("[")
        tutup = teks.count("}") + teks.count(")") + teks.count("]")
        return buka <= tutup

    @property
    def _moda_tty(self):
        return self.stdin.isatty()

    # ------------------------------------------------------------------
    # Eksekusi
    # ------------------------------------------------------------------
    def _jalankan(self, kode: str):
        """Parsing + evaluasi; mencetak nilai ekspresi terakhir bila murni."""
        try:
            tokens = tokenize(kode)
            ast = Parser(tokens).parse_program()
        except SyntaxError as e:
            return str(e), None

        # Jika AST kosong (mis. komentar saja) → tak ada yang dievaluasi.
        if not ast:
            return None, None

        nilai = None
        terakhir_bukan_statement = None
        try:
            with contextlib.redirect_stdout(self.stdout):
                for node in ast:
                    nilai = evaluate(node, self.env)
                    terakhir_bukan_statement = not self._adalah_pernyataan(node)
        except Exception as e:
            return f"{type(e).__name__}: {e}", None

        # Perlihatkan nilai bila baris terakhir adalah ekspresi murni.
        if terakhir_bukan_statement and nilai is not None:
            self._cetak_nilai(nilai)
        return None, None

    @staticmethod
    def _adalah_pernyataan(node):
        """True bila node adalah statement (jangan dicetak ulang di REPL)."""
        return isinstance(node, TIPE_STATEMENT)

    # ------------------------------------------------------------------
    # Loop utama
    # ------------------------------------------------------------------
    def jalan(self) -> int:
        banner = (
            "Aksara v{ver} — ketik kode Aksara. Baris berawalan ':' membuka "
            "mode blok panjang (akhiri ':EOF').\n"
            "'keluar' atau Ctrl-D untuk keluar.\n"
        )
        self.stdout.write(banner.format(
            ver=self._versi()
        ))
        while True:
            kode = self._baca_multi_line()
            if kode is None or kode.strip() in ("keluar", "quit", "exit"):
                break
            if kode.strip() == "":
                continue

            err, _ = self._jalankan(kode)
            if err:
                self.stdout.write(err + "\n")
                continue

        self.stdout.write("\n")
        return 0

    def _cetak_nilai(self, nilai):
        if isinstance(nilai, bool):
            teks = "benar" if nilai else "salah"
        elif nilai is None:
            teks = "nil"
        else:
            teks = repr(nilai)
        self.stdout.write(teks + "\n")

    @staticmethod
    def _versi() -> str:
        from aksara import __version__
        return __version__


def main_repl() -> int:
    """Entry point REPL: dipanggil saat CLI tanpa argumen file."""
    return Repl(sys.stdin, sys.stdout).jalan()


if __name__ == "__main__":
    sys.exit(main_repl())
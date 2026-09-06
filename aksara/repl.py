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
import os
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

# Izinkan readline kalau tersedia (Linux / Termux).
try:
    import readline as _readline  # noqa: F401
    _READLINE_AVAILABLE = True
except ImportError:
    _READLINE_AVAILABLE = False

_TULIS_BANTUAN = """\
Perintah REPL:
  :help              tampilkan bantuan ini
  :vars              tampilkan variabel & fungsi yang terdefinisi
  :reset             hapus semua variabel & fungsi
  :load <file.ak>    muat & jalankan file Aksara
  :history           tampilkan riwayat perintah
  :q / :quit         keluar dari REPL

Penulisan kode:
  - Blok pakai kurung kurawal { } (bukan indentasi).
  - Ekspresi murni dicetak otomatis (mis. '1 + 1' → 2).
  - Baris ':' diakhiri ':EOF' untuk blok panjang.
  - 'keluar' atau Ctrl-D untuk keluar.
"""


class Repl:
    """Loop baca-evaluasi-cetak dengan environment yang persisten."""

    def __init__(self, stdin, stdout):
        self.stdin = stdin
        self.stdout = stdout
        self.env = Environment()
        self.riwayat: list[str] = []

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
        if inp is not None:
            self.riwayat.append(inp)
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
    # Perintah internal REPL (awalan ':')
    # ------------------------------------------------------------------
    def _proses_perintah(self, kode: str) -> bool | None:
        """Proses perintah ':...'. Kembalikan True jika merupakan perintah."""
        baris = kode.strip()
        if not baris.startswith(":"):
            return False

        bagian = baris.split(None, 1)
        perintah = bagian[0].lower()
        arg = bagian[1] if len(bagian) > 1 else ""

        if perintah in (":q", ":quit"):
            return None  # tanda keluar

        if perintah == ":help":
            self.stdout.write(_TULIS_BANTUAN)
            return True

        if perintah == ":vars":
            self._tampilkan_vars()
            return True

        if perintah == ":reset":
            self.env = Environment()
            self.stdout.write("Environment di-reset.\n")
            return True

        if perintah == ":load":
            return self._muat_file(arg)

        if perintah == ":history":
            self._tampilkan_riwayat()
            return True

        self.stdout.write(f"Perintah tidak dikenal: {perintah}\n")
        self.stdout.write("Ketik ':help' untuk daftar perintah.\n")
        return True

    def _tampilkan_vars(self):
        vars_env = self.env.vars
        if not vars_env:
            self.stdout.write("(kosong — belum ada variabel/fungsi)\n")
            return
        for nama in sorted(vars_env.keys()):
            val = vars_env[nama]
            tipe = type(val).__name__
            self.stdout.write(f"  {nama}: {tipe} = {val!r}\n")

    def _tampilkan_riwayat(self):
        if not self.riwayat:
            self.stdout.write("(riwayat kosong)\n")
            return
        panjang = len(self.riwayat)
        for i, baris in enumerate(self.riwayat, 1):
            self.stdout.write(f"  {i:4d}  {baris}\n")

    def _muat_file(self, jalur: str) -> bool | None:
        jalur = jalur.strip()
        if not jalur:
            self.stdout.write("Penggunaan: :load <file.ak>\n")
            return True
        jalur = os.path.expanduser(jalur)
        if not os.path.isfile(jalur):
            self.stdout.write(f"File tidak ditemukan: {jalur}\n")
            return True
        try:
            with open(jalur, "r", encoding="utf-8") as f:
                kode = f.read()
            err, _ = self._jalankan(kode)
            if err:
                self.stdout.write(f"Galat di {jalur}:\n  {err}\n")
        except Exception as e:
            self.stdout.write(f"Gagal membaca {jalur}: {e}\n")
        return True

    # ------------------------------------------------------------------
    # Eksekusi kode Aksara
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
            "Aksara v{ver} — ketik kode Aksara. ':help' untuk bantuan.\n"
            "'keluar' atau Ctrl-D untuk keluar.\n"
        )
        self.stdout.write(banner.format(ver=self._versi()))
        while True:
            kode = self._baca_multi_line()
            if kode is None or kode.strip() in ("keluar", "quit", "exit"):
                break
            if kode.strip() == "":
                continue

            # Perintah internal REPL (:help, :vars, dll.)
            hasil = self._proses_perintah(kode)
            if hasil is None:
                break  # :q / :quit
            if hasil:
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
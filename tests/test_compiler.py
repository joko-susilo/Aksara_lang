from aksara.lexer.tokenizer import tokenize
from aksara.parser.parser import Parser
from aksara.compiler.python import AksaraCompiler


def kompilasi(kode: str) -> str:
    ast = Parser(tokenize(kode)).parse_program()
    return AksaraCompiler().compile_program(ast)


# ------------------------------------------------------------------
# Unit: ekspresi & statement dasar
# ------------------------------------------------------------------
def test_kompilasi_cetak():
    py = kompilasi('cetak "halo"')
    assert py == "print('halo')"


def test_kompilasi_aritmetika_dan_prioritas():
    py = kompilasi("cetak 2 + 3 * 4")
    assert "_ak_tambah(2, (3 * 4))" in py


def test_kompilasi_null_coalescing():
    py = kompilasi("y = x ?? 5")
    assert "if __ak is not None else 5" in py


def test_kompilasi_jika_elif_lain():
    py = kompilasi(
        'jika x > 5 { cetak "besar" } '
        'atau_jika x == 5 { cetak "sama" } '
        'lain { cetak "kecil" }'
    )
    assert "if (x > 5):" in py
    assert "elif (x == 5):" in py
    assert "else:" in py


def test_kompilasi_untuk_rentang_inklusif():
    py = kompilasi("untuk i dalam 1..5 { cetak i }")
    assert "for i in range(int(1), int(5) + 1):" in py


def test_kompilasi_untuk_daftar():
    py = kompilasi("untuk x dalam daftar { cetak x }")
    assert "for x in daftar:" in py


def test_kompilasi_selama():
    py = kompilasi("selama x < 3 { x = x + 1 }")
    assert "while (x < 3):" in py


def test_kompilasi_fungsi():
    py = kompilasi("fun tambah(a, b) { balik a + b }")
    assert "def tambah(a, b):" in py
    assert "return _ak_tambah(a, b)" in py


def test_kompilasi_coba_kecuali_akhirnya():
    py = kompilasi(
        'coba { x = 10 / 0 } '
        'kecuali [ZeroDivisionError] sebagai e { cetak e } '
        'akhirnya { cetak "done" }'
    )
    assert "try:" in py
    assert "except ZeroDivisionError as __ak_err:" in py
    assert "e = str(__ak_err)" in py
    assert "finally:" in py


def test_kompilasi_kamus():
    py = kompilasi('k = ["a": 1, "b": 2]')
    assert "{'a': 1, 'b': 2}" in py


def test_kompilasi_slice_inklusif():
    py = kompilasi("cetak data[1..3]")
    assert "(data)[1:3 + 1]" in py


def test_kompilasi_impor_modul_python():
    py = kompilasi('impor "os" sbg os')
    assert py.strip() == "import os"


def test_kompilasi_bangunkan_galat():
    py = kompilasi('galat "pesan"')
    assert "raise RuntimeError(str('pesan'))" in py


def test_kompilasi_builtin_ai_diimpor():
    py = kompilasi("cetak tebak([1, 2, 3])")
    assert "from aksara.interpreter.builtins import tebak" in py
    assert "print(tebak([1, 2, 3]))" in py


def test_kompilasi_tambah_string_dan_angka():
    py = kompilasi('cetak "a" + 1')
    assert "def _ak_tambah(a, b):" in py
    assert "_ak_tambah('a', 1)" in py


# ------------------------------------------------------------------
# End-to-end: hasil interpreter == hasil kompilasi
# ------------------------------------------------------------------
import io
import contextlib

from aksara.interpreter.evaluator import evaluate
from aksara.interpreter.environment import Environment


def keluaran_interp(kode: str, inp: str = "") -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        env = Environment()
        for node in Parser(tokenize(kode)).parse_program():
            evaluate(node, env)
    return buf.getvalue()


def keluaran_kompilasi(kode: str) -> str:
    py = kompilasi(kode)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(py, "<test>", "exec"), {"__name__": "__main__"})
    return buf.getvalue()


def cek_setara(kode):
    assert keluaran_interp(kode) == keluaran_kompilasi(kode)


def test_setara_percabangan():
    cek_setara(
        'x = 5\n'
        'jika x > 5 { cetak "besar" } '
        'atau_jika x == 5 { cetak "sama" } '
        'lain { cetak "kecil" }'
    )


def test_setara_perulangan_untuk_selama():
    cek_setara(
        'total = 0\n'
        'untuk i dalam 1..10 { total = total + i }\n'
        'cetak total\n'
        'x = 3\n'
        'selama x > 0 {\n'
        '  cetak x\n'
        '  x = x - 1\n'
        '}'
    )


def test_setara_fungsi():
    cek_setara(
        'fun faktorial(n) {\n'
        '  jika n <= 1 { balik 1 }\n'
        '  balik n * faktorial(n - 1)\n'
        '}\n'
        'cetak faktorial(5)'
    )


def test_setara_null_coalescing():
    cek_setara(
        'a = nil\n'
        'cetak a ?? "default"\n'
        'b = "ada"\n'
        'cetak b ?? "default"'
    )


def test_setara_list_dan_slice():
    cek_setara(
        'data = [1, 2, 3, 4, 5]\n'
        'cetak data[0]\n'
        'cetak data[1..3]\n'
        'cetak data[2..]\n'
        'cetak data[..3]'
    )


def test_setara_galat_dan_coba():
    cek_setara(
        'coba {\n'
        '  x = 10 / 0\n'
        '} kecuali [ZeroDivisionError] {\n'
        '  cetak "tertangkap"\n'
        '} akhirnya {\n'
        '  cetak "selesai"\n'
        '}'
    )


def test_setara_henti_lanjut():
    cek_setara(
        'untuk i dalam 1..10 {\n'
        '  jika i == 2 { lanjut }\n'
        '  jika i == 5 { henti }\n'
        '  cetak i\n'
        '}'
    )


def test_setara_impor_builtin_kamus():
    cek_setara(
        'k = ["satu": 1, "dua": 2]\n'
        'cetak kunci(k)\n'
        'cetak ada(k, "satu")'
    )
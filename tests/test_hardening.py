import io
import contextlib

from aksara.lexer.tokenizer import tokenize
from aksara.parser.parser import Parser
from aksara.compiler.python import AksaraCompiler
from aksara.interpreter.evaluator import evaluate
from aksara.interpreter.environment import Environment


def kompilasi(kode: str) -> str:
    return AksaraCompiler().compile_program(Parser(tokenize(kode)).parse_program())


def keluaran_interp(kode: str) -> str:
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


# ------------------------------------------------------------------
# Escape string
# ------------------------------------------------------------------
def test_lexer_string_escape_satu_token():
    tokens = tokenize('cetak "a\\nb"')
    tok = [t for t in tokens if t.tipe == "STRING"]
    assert len(tok) == 1
    assert tok[0].nilai == '"a\\nb"'


def test_escape_baris_baru():
    assert keluaran_interp('cetak "a\\nb"') == "a\nb\n"
    cek_setara('cetak "a\\nb"')


def test_escape_tab_dan_kutip():
    assert keluaran_interp('cetak "ta\\tb \\" dalam"') == "ta\tb \" dalam\n"
    cek_setara('cetak "ta\\tb \\" dalam"')


def test_escape_unicode():
    assert keluaran_interp('cetak "cinta \\u2764"') == "cinta \u2764\n"
    cek_setara('cetak "cinta \\u2764"')


def test_template_dengan_escape():
    kode = 'x = 5\ncetak "nilai {x} \\n beres"'
    assert keluaran_interp(kode) == "nilai 5 \n beres\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# Regresi alur kontrol (bug yang diperbaiki)
# ------------------------------------------------------------------
def test_henti_dalam_blok_jika():
    kode = (
        'untuk i dalam 1..10 {\n'
        '  jika i == 3 { henti }\n'
        '  cetak i\n'
        '}'
    )
    assert keluaran_interp(kode) == "1\n2\n"
    cek_setara(kode)


def test_lanjut_dalam_blok_jika():
    kode = (
        'untuk i dalam 1..5 {\n'
        '  jika i == 3 { lanjut }\n'
        '  cetak i\n'
        '}'
    )
    assert keluaran_interp(kode) == "1\n2\n4\n5\n"
    cek_setara(kode)


def test_balik_dalam_coba():
    kode = (
        'fun hitung(x) {\n'
        '  coba {\n'
        '    balik x / 2\n'
        '  } kecuali sebagai e {\n'
        '    balik 0\n'
        '  }\n'
        '}\n'
        'cetak hitung(21)\n'
        'cetak hitung("5")\n'
    )
    assert keluaran_interp(kode) == "10.5\n0\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# AksesIndeks melempar tipe asli (agar kecuali [IndexError] bekerja)
# ------------------------------------------------------------------
def test_kecuali_indeks_error():
    kode = (
        'coba {\n'
        '  a = [1, 2]\n'
        '  b = a[10]\n'
        '} kecuali [IndexError] {\n'
        '  cetak "tertangkap indeks"\n'
        '}'
    )
    assert keluaran_interp(kode) == "tertangkap indeks\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# Fungsi user menaungi builtin
# ------------------------------------------------------------------
def test_fungsi_user_menaungi_builtin():
    kode = (
        'fun jumlah(data) {\n'
        '  total = 0\n'
        '  untuk n dalam data { total = total + n }\n'
        '  balik total\n'
        '}\n'
        'data = [10, 20, 30]\n'
        'cetak jumlah(data)'
    )
    assert keluaran_interp(kode) == "60\n"
    cek_setara(kode)


def test_builtin_kamus_tetap_bekerja_saat_tidak_dinaungi():
    kode = 'k = ["satu": 1]\ncetak kunci(k)\ncetak ada(k, "satu")'
    assert keluaran_interp(kode) == "['satu']\nTrue\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# Assignment atribut objek Python
# ------------------------------------------------------------------
def test_assign_atribut_objek():
    kode = (
        'impor "types" sbg t\n'
        'obj = t.SimpleNamespace()\n'
        'obj.nama = "aksara"\n'
        'cetak obj.nama\n'
        'obj.nama = obj.nama + " v2"\n'
        'cetak obj.nama\n'
    )
    assert keluaran_interp(kode) == "aksara\naksara v2\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# Impor lokal: modul .ak dipanggil dari kode terkompilasi
# ------------------------------------------------------------------
def test_impor_lokal_fungsi_bisa_dipanggil():
    kode = (
        'impor "larik.ak" sbg lk\n'
        'data = [1, 2, 3, 4]\n'
        'cetak lk.jumlah(data)\n'
        'cetak lk.maksimum(data)'
    )
    assert keluaran_interp(kode) == "10\n4\n"
    cek_setara(kode)
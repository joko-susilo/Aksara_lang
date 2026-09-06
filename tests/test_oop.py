import io
import contextlib

from aksara.lexer.tokenizer import tokenize
from aksara.parser.parser import Parser
from aksara.compiler.python import AksaraCompiler
from aksara.interpreter.evaluator import evaluate
from aksara.interpreter.environment import Environment
from aksara.ast.nodes import DefinisiKelas, Ini


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
    assert keluaran_interp(kode) == keluaran_kompilasi(kode), keluaran_kompilasi(kode)


# ------------------------------------------------------------------
# Parser
# ------------------------------------------------------------------
def test_parse_kelas():
    kode = 'kelas X { fun a(p) { ini.p = p } fun b() { balik ini.p } }'
    ast = Parser(tokenize(kode)).parse_program()
    assert isinstance(ast[0], DefinisiKelas)
    assert ast[0].nama == "X"
    assert [m.nama for m in ast[0].metode] == ["a", "b"]


# ------------------------------------------------------------------
# Perilaku
# ------------------------------------------------------------------
def test_oop_konstruktor_dan_metode():
    kode = (
        'kelas Mobil {\n'
        '  fun buat(merk, cc) {\n'
        '    ini.merk = merk\n'
        '    ini.cc = cc\n'
        '  }\n'
        '  fun deskripsi() { balik "Mobil " + ini.merk + " " + ini.cc }\n'
        '}\n'
        'm = Mobil.buat("Toyota", 1500)\n'
        'cetak m.deskripsi()\n'
        'cetak m.merk\n'
    )
    assert keluaran_interp(kode) == "Mobil Toyota 1500\nToyota\n"
    cek_setara(kode)


def test_oop_atribut_mutable():
    kode = (
        'kelas Kotak {\n'
        '  fun buat(isi) { ini.isi = isi }\n'
        '}\n'
        'k = Kotak.buat(1)\n'
        'k.isi = 99\n'
        'cetak k.isi\n'
    )
    assert keluaran_interp(kode) == "99\n"
    cek_setara(kode)


def test_oop_dua_instance_independen():
    kode = (
        'kelas Titik {\n'
        '  fun buat(x, y) {\n'
        '    ini.x = x\n'
        '    ini.y = y\n'
        '  }\n'
        '}\n'
        'a = Titik.buat(1, 2)\n'
        'b = Titik.buat(10, 20)\n'
        'cetak a.x\n'
        'cetak b.y\n'
        'a.x = 50\n'
        'cetak a.x\n'
        'cetak b.x\n'
    )
    assert keluaran_interp(kode) == "1\n20\n50\n10\n"
    cek_setara(kode)


def test_oop_metode_memanggil_metode():
    kode = (
        'kelas Kalkulator {\n'
        '  fun buat() { ini.total = 0 }\n'
        '  fun tambah(x) {\n'
        '    ini.total = ini.total + x\n'
        '    balik ini.lihat()\n'
        '  }\n'
        '  fun lihat() { balik ini.total }\n'
        '}\n'
        'k = Kalkulator.buat()\n'
        'cetak k.tambah(5)\n'
        'cetak k.tambah(7)\n'
        'cetak k.lihat()\n'
    )
    assert keluaran_interp(kode) == "5\n12\n12\n"
    cek_setara(kode)


def test_oop_galat_metode():
    kode = (
        'kelas X {\n'
        '  fun buat() {}\n'
        '}\n'
        'x = X.buat()\n'
        'coba {\n'
        '  a = x.tak_ada\n'
        '} kecuali sebagai e {\n'
        '  cetak "galat ditangkap"\n'
        '}\n'
    )
    assert "galat ditangkap\n" in keluaran_interp(kode)
    cek_setara(kode)


def test_ini_d_i_kompilasi():
    py = kompilasi('kelas X { fun a() { balik ini.x } }')
    assert "def _X_a(ini):" in py
    assert "return (ini).x" in py
    assert "KelasValue('X'" in py
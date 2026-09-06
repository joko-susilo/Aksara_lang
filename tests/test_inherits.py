import io
import contextlib

from aksara.lexer.tokenizer import tokenize
from aksara.parser.parser import Parser
from aksara.compiler.python import AksaraCompiler
from aksara.interpreter.evaluator import evaluate
from aksara.interpreter.environment import Environment
from aksara.ast.nodes import DefinisiKelas, Induk


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


def test_parse_kelas_dari():
    kode = 'kelas Anak dari Induk { fun a() {} }'
    ast = Parser(tokenize(kode)).parse_program()
    assert isinstance(ast[0], DefinisiKelas)
    assert ast[0].induk == "Induk"


def test_warisi_metode_dan_atribut():
    kode = (
        'kelas H {\n'
        '  fun buat(x) { ini.x = x }\n'
        '  fun ambil() { balik ini.x }\n'
        '}\n'
        'kelas A dari H {}\n'
        'a = A.buat(42)\n'
        'cetak a.ambil()\n'
        'cetak a.x\n'
    )
    assert keluaran_interp(kode) == "42\n42\n"
    cek_setara(kode)


def test_override_metode():
    kode = (
        'kelas H {\n'
        '  fun buat() {}\n'
        '  fun suara() { balik "h" }\n'
        '}\n'
        'kelas A dari H {\n'
        '  fun suara() { balik "a" }\n'
        '}\n'
        'kelas B dari H {\n'
        '  fun suara() { balik "b" }\n'
        '}\n'
        'cetak A.buat().suara()\n'
        'cetak B.buat().suara()\n'
        'cetak H.buat().suara()\n'
    )
    assert keluaran_interp(kode) == "a\nb\nh\n"
    cek_setara(kode)


def test_induk_super():
    kode = (
        'kelas Bentuk {\n'
        '  fun buat(nama) { ini.nama = nama }\n'
        '  fun luas() { balik 0 }\n'
        '  fun info() { balik ini.nama + "=" + ini.luas() }\n'
        '}\n'
        'kelas Persegi dari Bentuk {\n'
        '  fun buat(sisi) {\n'
        '    induk.buat("persegi")\n'
        '    ini.sisi = sisi\n'
        '  }\n'
        '  fun luas() { balik induk.luas() + ini.sisi * ini.sisi }\n'
        '}\n'
        'p = Persegi.buat(5)\n'
        'cetak p.info()\n'
    )
    assert keluaran_interp(kode) == "persegi=25\n"
    cek_setara(kode)


def test_induk_tiga_tingkat():
    kode = (
        'kelas A {\n'
        '  fun buat() {}\n'
        '  fun namaku() { balik "A" }\n'
        '}\n'
        'kelas B dari A {\n'
        '  fun namaku() { balik induk.namaku() + "B" }\n'
        '}\n'
        'kelas C dari B {\n'
        '  fun namaku() { balik induk.namaku() + "C" }\n'
        '}\n'
        'cetak C.buat().namaku()\n'
        'cetak B.buat().namaku()\n'
    )
    assert keluaran_interp(kode) == "ABC\nAB\n"
    cek_setara(kode)


def test_kompilasi_induk_node():
    py = kompilasi('kelas K dari H { fun a() { balik induk.a() } }')
    assert "_ak_induk(ini, K)" in py
    assert "KelasValue('K'" in py
    assert ", H)" in py
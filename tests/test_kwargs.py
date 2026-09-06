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
    assert keluaran_interp(kode) == keluaran_kompilasi(kode), keluaran_kompilasi(kode)


def eksekusi(kode: str) -> str:
    """Jalankan lewat interpreter; tangkap error jadi teks."""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            env = Environment()
            for node in Parser(tokenize(kode)).parse_program():
                evaluate(node, env)
    except Exception as e:
        return f"{type(e).__name__}: {e}"
    return buf.getvalue()


# ------------------------------------------------------------------
# Nilai default parameter
# ------------------------------------------------------------------
def test_default_parameter():
    kode = (
        'fun sapa(nama, sapaan = "Halo") {\n'
        '  balik sapaan + ", " + nama\n'
        '}\n'
        'cetak sapa("Budi")\n'
        'cetak sapa("Budi", "Yo")\n'
    )
    assert keluaran_interp(kode) == "Halo, Budi\nYo, Budi\n"
    cek_setara(kode)


def test_default_multiple():
    kode = (
        'fun kotak(a, b = 2, c = 3) { balik a + b + c }\n'
        'cetak kotak(1)\n'
        'cetak kotak(1, 10)\n'
        'cetak kotak(10, 20, 30)\n'
    )
    assert keluaran_interp(kode) == "6\n14\n60\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# Panggilan keyword
# ------------------------------------------------------------------
def test_kwarg():
    kode = (
        'fun profesi(nama, jabatan = "staf") {\n'
        '  balik nama + " = " + jabatan\n'
        '}\n'
        'cetak profesi("Eka")\n'
        'cetak profesi("Eka", jabatan = "manajer")\n'
    )
    assert keluaran_interp(kode) == "Eka = staf\nEka = manajer\n"
    cek_setara(kode)


def test_kwarg_campur_posisional():
    kode = (
        'fun suku(a, b = 0, c = 0) { balik a * 100 + b * 10 + c }\n'
        'cetak suku(1, c = 9)\n'
        'cetak suku(1, 2, c = 9)\n'
    )
    assert keluaran_interp(kode) == "109\n129\n"
    cek_setara(kode)


def test_kwarg_builtin_python():
    kode = (
        'model = jaring_syaraf([[1],[2],[3],[4]], [10,20,30,40], hidden = 8, iterasi = 500, laju = 0.1)\n'
        'cetak ramal(model, [[5]])\n'
    )
    hasil = keluaran_interp(kode)
    assert "49." in hasil or "50." in hasil
    cek_setara(kode)


# ------------------------------------------------------------------
# Error
# ------------------------------------------------------------------
def test_kwarg_tak_dikenal():
    out = eksekusi('fun f(a) { balik a }\nf(1, zzz = 2)\n')
    assert "tidak mengenal argumen 'zzz'" in out


def test_argumen_kurang():
    out = eksekusi('fun f(a, b) { balik a + b }\nf(1)\n')
    assert "butuh argumen 'b'" in out


def test_terlalu_banyak():
    out = eksekusi('fun f(a) { balik a }\nf(1, 2)\n')
    assert isinstance(out, str) and "posisional" in out


# ------------------------------------------------------------------
# Metode + kwargs
# ------------------------------------------------------------------
def test_metode_default_dan_kwarg():
    kode = (
        'kelas Kotak {\n'
        '  fun buat(panjang, lebar = 10) {\n'
        '    ini.panjang = panjang\n'
        '    ini.lebar = lebar\n'
        '  }\n'
        '  fun luas() { balik ini.panjang * ini.lebar }\n'
        '}\n'
        'a = Kotak.buat(5)\n'
        'b = Kotak.buat(5, lebar = 4)\n'
        'cetak a.luas()\n'
        'cetak b.luas()\n'
    )
    assert keluaran_interp(kode) == "50\n20\n"
    cek_setara(kode)
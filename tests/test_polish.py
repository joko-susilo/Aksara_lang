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


# ------------------------------------------------------------------
# Operator gabungan
# ------------------------------------------------------------------
def test_augmented_assign():
    kode = (
        "x = 10\n"
        "x += 5\n"
        "cetak x\n"
        "x -= 2\n"
        "cetak x\n"
        "x *= 3\n"
        "cetak x\n"
        "x /= 4\n"
        "cetak x\n"
        "x %= 7\n"
        "cetak x\n"
    )
    assert keluaran_interp(kode) == "15\n13\n39\n9.75\n2.75\n"
    cek_setara(kode)


def test_augmented_string():
    kode = (
        's = "ab"\n'
        "s *= 3\n"
        "cetak s\n"
        's += "cd"\n'
        "cetak s\n"
    )
    assert keluaran_interp(kode) == "ababab\nabababcd\n"
    cek_setara(kode)


def test_augmented_dalam_loop():
    kode = (
        "total = 0\n"
        "untuk i dalam 1..5 {\n"
        "  total += i\n"
        "}\n"
        "cetak total\n"
    )
    assert keluaran_interp(kode) == "15\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# cetak multi-argumen
# ------------------------------------------------------------------
def test_cetak_multi_argumen():
    kode = (
        'cetak "akurasi:", 0.95, "%"\n'
        'cetak 1, 2, 3\n'
    )
    assert keluaran_interp(kode) == "akurasi: 0.95 %\n1 2 3\n"
    cek_setara(kode)


def test_cetak_ekspresi_tetap():
    kode = 'x = 5\ncetak "x + 1 =", x + 1\n'
    assert keluaran_interp(kode) == "x + 1 = 6\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# Kutip tunggal
# ------------------------------------------------------------------
def test_kutip_tunggal():
    kode = (
        "a = 'halo'\n"
        'cetak a\n'
        'b = \'teks "dal" oke\'\n'
        "cetak b\n"
        'cetak \'a\' + "b"\n'
    )
    assert keluaran_interp(kode) == 'halo\nteks "dal" oke\nab\n'
    cek_setara(kode)


def test_kutip_tunggal_escape():
    kode = "cetak 'baris\\nbaru'\n"
    assert keluaran_interp(kode) == "baris\nbaru\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# Simpan / muat model (model.ak)
# ------------------------------------------------------------------
def test_model_simpan_muat(tmp_path):
    jalan = (tmp_path / "model.aksm").as_posix()
    kode = (
        'impor "ml.ak" sbg ml\n'
        'impor "model.ak" sbg mo\n'
        'm1 = ml.latih([[1],[2],[3],[4]], [10,20,30,40])\n'
        f'mo.simpan(m1, "{jalan}")\n'
        'm2 = mo.muat("' + jalan + '")\n'
        'a = ml.ramal(m1, [[5]])\n'
        'b = ml.ramal(m2, [[5]])\n'
        'cetak a\n'
        'cetak b\n'
        'cetak a[0] == b[0]\n'
    )
    hasil = keluaran_interp(kode)
    assert "True" in hasil
    cek_setara(kode)
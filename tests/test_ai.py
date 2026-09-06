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
# Model latih-ramal (argumen posisional; opsional default)
# ------------------------------------------------------------------
def test_latih_dan_ramal():
    kode = (
        'model = jaring_syaraf([[1],[2],[3],[4]], [10,20,30,40], 8, 500, 0.1)\n'
        'cetak ramal(model, [[5]])\n'
    )
    hasil = keluaran_interp(kode)
    assert "49." in hasil or "50." in hasil
    cek_setara(kode)


# ------------------------------------------------------------------
# ml.ak stdlib
# ------------------------------------------------------------------
def test_ml_stdlib():
    kode = (
        'impor "ml.ak" sbg ml\n'
        'impor "data.ak" sbg d\n'
        'model = ml.latih([[1],[2],[3]], [2,4,6])\n'
        'pred = ml.ramal(model, [[4]])\n'
        'cetak pred\n'
        'cetak d.akurasi([1, 1, 1, 0], [1, 1, 0, 0])\n'
        'cetak d.galat_rata([10,20], [12,18])\n'
    )
    hasil = keluaran_interp(kode)
    assert "[8.0" in hasil or "[7." in hasil  # prediksi mendekati 8
    assert "0.75" in hasil  # akurasi (3/4)
    assert "2.0" in hasil   # galat rata (|10-12|+|20-18|)/2 = 2
    cek_setara(kode)


# ------------------------------------------------------------------
# data.ak: bagi, ambil_selisih
# ------------------------------------------------------------------
def test_data_bagi():
    kode = (
        'impor "data.ak" sbg d\n'
        'b = d.bagi([1,2,3,4,5,6,7,8,9,10], 0.6)\n'
        'cetak b[0]\n'
        'cetak b[1]\n'
    )
    assert "[1, 2, 3, 4, 5, 6]" in keluaran_interp(kode)
    assert "[7, 8, 9, 10]" in keluaran_interp(kode)
    cek_setara(kode)


def test_data_ambil_selisih():
    kode = (
        'impor "data.ak" sbg d\n'
        'cetak d.ambil_selisih([1, 3, 6, 10])\n'
    )
    assert keluaran_interp(kode) == "[2, 3, 4]\n"
    cek_setara(kode)
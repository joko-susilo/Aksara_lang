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
# Koma penutup (trailing comma)
# ------------------------------------------------------------------
def test_koma_penutup_list():
    kode = (
        "x = [\n"
        "  1,\n"
        "  2,\n"
        "  3,\n"
        "]\n"
        "cetak x\n"
    )
    assert keluaran_interp(kode) == "[1, 2, 3]\n"
    cek_setara(kode)


def test_koma_penutup_kamus_dan_panggilan():
    kode = (
        "k = [\n"
        "  \"a\": 1,\n"
        "  \"b\": 2,\n"
        "]\n"
        "cetak k[\"a\"]\n"
        "cetak panjang([\n"
        "  \"x\",\n"
        "  \"y\",\n"
        "])\n"
    )
    assert keluaran_interp(kode) == "1\n2\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# vektor.ak
# ------------------------------------------------------------------
def test_vektor_dot_norma_kosinus():
    kode = (
        'impor "vektor.ak" sbg v\n'
        "cetak v.dot([1, 2, 3], [4, 5, 6])\n"
        "cetak v.norma([3, 4])\n"
        "cetak v.kosinus([1, 0], [0, 1])\n"
        "cetak v.kosinus([1, 0], [2, 0])\n"
        "cetak v.normalisasi([3, 4])\n"
    )
    assert keluaran_interp(kode) == "32\n5.0\n0.0\n1.0\n[0.6, 0.8]\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# larik.ak: fungsi statistik lanjutan
# ------------------------------------------------------------------
def test_larik_median_variansi_outlier():
    kode = (
        'impor "larik.ak" sbg l\n'
        "cetak l.median([3, 1, 2])\n"
        "cetak l.median([4, 1, 3, 2])\n"
        "cetak l.variansi([1, 2, 3, 4])\n"
        "cetak l.outlier([1, 1, 1, 1, 1, 10000])\n"
        "cetak l.frekuensi([\"a\", \"b\", \"a\", \"c\"])\n"
    )
    out = keluaran_interp(kode)
    assert "2" in out.splitlines()[0]       # median [3,1,2] -> 2
    assert "2.5" in out.splitlines()[1]     # median [4,1,3,2] -> 2.5
    assert "1.25" in out.splitlines()[2]    # variansi [1..4] -> 1.25
    assert "[10000]" in out               # outlier
    assert "'a': 2" in out                  # frekuensi
    cek_setara(kode)


# ------------------------------------------------------------------
# Klasifikasi (jaringan saraf softmax)
# ------------------------------------------------------------------
def test_klasifikasi_akurasi():
    kode = (
        'impor "ml.ak" sbg ml\n'
        "X = [[1,1],[1,2],[2,1],[2,2],\n"
        "     [8,1],[9,1],[8,2],[9,2],\n"
        "     [8,8],[9,8],[8,9],[9,9]]\n"
        "y = [0,0,0,0, 1,1,1,1, 2,2,2,2]\n"
        "model = ml.latih_klasifikasi(X, y, 10, 1500, 0.3)\n"
        "pred = ml.ramal_klasifikasi(model, X)\n"
        "cetak pred\n"
        "cocok = 0\n"
        "untuk i dalam 0..panjang(y)-1 {\n"
        "  jika pred[i] == y[i] { cocok = cocok + 1 }\n"
        "}\n"
        "cetak cocok\n"
        "cetak ml.ramal_klasifikasi(model, [[8.1, 9.2], [1.5, 1.5]])\n"
    )
    out = keluaran_interp(kode)
    assert "[2, 0]" in out          # baru -> besar & kecil
    assert "12\n" in out            # semua data latih cocok
    cek_setara(kode)


def test_portofolio_regresi_deterministik(tmp_path):
    jalan = (tmp_path / "m.aksm").as_posix()
    kode = (
        'impor "ml.ak" sbg ml\n'
        'impor "model.ak" sbg mo\n'
        'model = ml.latih([[30],[40],[50],[60]], [45,60,75,90], 8, 1000, 0.1)\n'
        f'mo.simpan(model, "{jalan}")\n'
        'm2 = mo.muat("' + jalan + '")\n'
        'a = ml.ramal(m2, [[95]])\n'
        'cetak a[0]\n'
        'cetak a[0] > 130 dan a[0] < 160\n'
    )
    out = keluaran_interp(kode)
    assert "True" in out
    cek_setara(kode)
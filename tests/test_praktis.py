import io
import contextlib

from aksara.lexer.tokenizer import tokenize
from aksara.parser.parser import Parser
from aksara.compiler.python import AksaraCompiler
from aksara.interpreter.evaluator import evaluate
from aksara.interpreter.environment import Environment


def keluaran_interp(kode: str) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        env = Environment()
        for node in Parser(tokenize(kode)).parse_program():
            evaluate(node, env)
    return buf.getvalue()


def kompilasi(kode: str) -> str:
    return AksaraCompiler().compile_program(Parser(tokenize(kode)).parse_program())


def keluaran_kompilasi(kode: str) -> str:
    py = kompilasi(kode)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(py, "<test>", "exec"), {"__name__": "__main__"})
    return buf.getvalue()


def cek_setara(kode):
    assert keluaran_interp(kode) == keluaran_kompilasi(kode), keluaran_kompilasi(kode)


# ------------------------------------------------------------------
# json.ak
# ------------------------------------------------------------------
def test_json_urai():
    kode = (
        'impor "json.ak" sbg j\n'
        'data = j.urai("{\\"nama\\": \\"Eka\\", \\"umur\\": 30}")\n'
        'cetak data["nama"]\n'
    )
    assert keluaran_interp(kode) == "Eka\n"
    cek_setara(kode)


def test_json_ubah():
    kode = (
        'impor "json.ak" sbg j\n'
        'cetak j.ubah(["apel", "mangga"])\n'
    )
    assert keluaran_interp(kode) == '["apel", "mangga"]\n'
    cek_setara(kode)


# ------------------------------------------------------------------
# csv.ak
# ------------------------------------------------------------------
def test_csv_tulis_dan_baca(tmp_path):
    jalan = (tmp_path / "tabel.csv").as_posix()
    kode = (
        f'impor "csv.ak" sbg c\n'
        f'c.tulis("{jalan}", [["nama", "nilai"], ["A", "1"], ["B", "2"]])\n'
        f'cetak c.baca("{jalan}")\n'
        f'cetak c.baca_kamus("{jalan}")[0]["nama"]\n'
    )
    hasil = keluaran_interp(kode)
    assert "['A', '1']" in hasil
    assert "A" in hasil
    cek_setara(kode)


# ------------------------------------------------------------------
# String berisi kurung kurawal (json) bukan template
# ------------------------------------------------------------------
def test_kurawal_di_string_bukan_template():
    kode = 'x = 5\ncetak "nilai {x}"\ncetak "json: {\\"a\\": 1}"\n'
    assert keluaran_interp(kode) == "nilai 5\njson: {\"a\": 1}\n"
    cek_setara(kode)
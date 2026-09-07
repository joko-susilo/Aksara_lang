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


def test_mini_lm_mode_kata_deterministik():
    kode = (
        'impor "mini_lm.ak" sbg m\n'
        'teks = "ibu pergi ke pasar membeli ikan. ayah bekerja di kantor. kakak bermain di taman. "\n'
        "model = m.latih_teks(teks, blok = 6, tersembunyi = 16, kepala = 2, lapisan = 1, "
        "iterasi = 40, laju = 0.01, benih = 0, kata = benar)\n"
        'a = m.tulis(model, "ibu pergi", panjang = 6, suhu = 0)\n'
        "cetak a\n"
        'cetak a == m.tulis(model, "ibu pergi", panjang = 6, suhu = 0)\n'
    )
    out = keluaran_interp(kode)
    lines = out.splitlines()
    assert lines[1] == "True"          # deterministik (suhu=0, benih tetap)
    assert lines[0].startswith("ibu pergi")
    cek_setara(kode)


def test_mini_lm_belajar_kata():
    """Setelah latihan sederhana, token yang dihasilkan berasal dari kosakata."""
    kode = (
        'impor "mini_lm.ak" sbg m\n'
        'teks = "kucing makan ikan. kucing minum susu. kucing tidur di rumah. "\n'
        "model = m.latih_teks(teks, blok = 6, tersembunyi = 16, kepala = 2, lapisan = 1, "
        "iterasi = 60, laju = 0.01, benih = 0, kata = benar)\n"
        'cetak m.tulis(model, "kucing", panjang = 8, suhu = 0)\n'
    )
    out = keluaran_interp(kode)
    vokab = {"kucing", "makan", "ikan", "minum", "susu", "tidur",
             "di", "rumah", "."}
    for k in out.strip().split():
        dasar = k.strip(".,!?")
        assert dasar in vokab, k
import io
import os
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
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            env = Environment()
            for node in Parser(tokenize(kode)).parse_program():
                evaluate(node, env)
    except Exception as e:
        return f"{type(e).__name__}: {e}"
    return buf.getvalue()


def test_llm_modul_dimuat():
    out = eksekusi('impor "llm.ak" sbg llm\ncetak llm.kunci_api("TAK_ADA_DEFAULT_SESUATU")\n')
    assert "cetak llm" not in out  # hanya memastikan tanpa error jaringan
    assert "400" not in out


def test_kunci_api_dari_env(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "kunci-rahasia-xyz")
    out = eksekusi('impor "llm.ak" sbg llm\ncetak llm.kunci_api()\n')
    assert "kunci-rahasia-xyz" in out
    cek_setara('impor "llm.ak" sbg llm\ncetak llm.kunci_api()\n')


def test_kunci_api_kosong_tanpa_env(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    out = eksekusi('impor "llm.ak" sbg llm\ncetak llm.kunci_api()\n')
    assert out.strip() == ""


def test_tanya_tanpa_kunci_galat(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    out = eksekusi('impor "llm.ak" sbg llm\ncetak llm.tanya("halo")\n')
    assert "GROQ_API_KEY" in out


def test_bersihkan_kode_tanpa_fence():
    out = eksekusi(
        'impor "llm.ak" sbg llm\n'
        'cetak llm.bersihkan_kode("fun x() { balik 1 }")\n'
    )
    assert out.strip() == "fun x() { balik 1 }"
    cek_setara('impor "llm.ak" sbg llm\ncetak llm.bersihkan_kode("fun x() { balik 1 }")\n')


def test_bersihkan_kode_dengan_fence():
    kode_sumber = (
        '```aksara\n'
        'fun selesaikan(x) {\n'
        '    balik x + 1\n'
        '}\n'
        '```'
    )
    out = eksekusi(
        'impor "llm.ak" sbg llm\n'
        'cetak llm.bersihkan_kode("' + kode_sumber.replace("\n", "\\n").replace('"', '\\"') + '")\n'
    )
    assert "fun selesaikan(x)" in out
    assert "```" not in out
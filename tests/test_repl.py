import io

from aksara.repl import Repl


def jalankan_repl(perintah: str) -> str:
    stdin = io.StringIO(perintah)
    stdout = io.StringIO()
    Repl(stdin, stdout).jalan()
    return stdout.getvalue()


def test_ekspresi_dicetak_otomatis():
    out = jalankan_repl("1 + 1\nkeluar\n")
    assert "aksara> 1 + 1\n2\n" in out


def test_statement_tidak_dicetak_ganda():
    out = jalankan_repl('cetak "halo"\nkeluar\n')
    baris_halo = [b for b in out.splitlines() if b == "halo"]
    assert len(baris_halo) == 1


def test_assignment_tidak_dicetak():
    out = jalankan_repl("x = 5\nx * 2\nkeluar\n")
    assert "aksara> x = 5\naksara> x * 2\n10\n" in out


def test_environment_persisten():
    out = jalankan_repl("x = 5\nx * 2\nkeluar\n")
    assert "10\n" in out


def test_boolean_bahasa_indonesia():
    out = jalankan_repl("1 != 2\nkeluar\n")
    assert "benar\n" in out


def test_blok_multi_line():
    out = jalankan_repl(
        "jika x > 3 {\n"
        "  cetak \"besar\"\n"
        "}\n"
        "x = 5\n"
        "jika x > 3 {\n"
        "  cetak \"besar\"\n"
        "}\n"
        "keluar\n"
    )
    assert "besar\n" in out


def test_heredoc_definisi_fungsi():
    out = jalankan_repl(
        ":\n"
        "fun kali(a, b) {\n"
        "  balik a * b\n"
        "}\n"
        ":EOF\n"
        "kali(6, 7)\n"
        "keluar\n"
    )
    assert "42\n" in out


def test_error_tidak_mematikan_repl():
    out = jalankan_repl(
        "x = 10 / 0\n"
        'cetak "masih hidup"\n'
        "keluar\n"
    )
    assert "ZeroDivisionError" in out
    assert "masih hidup\n" in out
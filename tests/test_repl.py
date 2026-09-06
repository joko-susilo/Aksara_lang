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


def test_perintah_help():
    out = jalankan_repl(":help\nkeluar\n")
    assert ":load <file.ak>" in out
    assert ":reset" in out


def test_perintah_vars():
    out = jalankan_repl("x = 5\nnama = \"Eka\"\n:vars\nkeluar\n")
    assert "x: int = 5" in out
    assert "nama: str =" in out


def test_perintah_reset():
    out = jalankan_repl("x = 5\n:reset\n:vars\nkeluar\n")
    assert "Environment di-reset." in out
    assert "(kosong" in out


def test_perintah_history():
    out = jalankan_repl("1 + 1\n:history\nkeluar\n")
    assert "1 + 1" in out
    assert ":history" in out


def test_perintah_tidak_dikenal():
    out = jalankan_repl(":nuknown\nkeluar\n")
    assert "Perintah tidak dikenal: :nuknown" in out


def test_perintah_quit():
    out = jalankan_repl("1 + 1\n:q\n2 + 2\n")
    assert "2\n" in out
    assert "4\n" not in out  # perintah setelah ':q' tidak dieksekusi


def test_load_file(tmp_path):
    jalan = tmp_path / "mod.ak"
    jalan.write_text('x = 100\ncetak "dimuat {x}"\n', encoding="utf-8")
    out = jalankan_repl(f":load {jalan}\n:vars\nkeluar\n")
    assert "dimuat 100" in out
    assert "x: int = 100" in out
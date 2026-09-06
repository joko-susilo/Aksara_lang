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
    assert keluaran_interp(kode) == keluaran_kompilasi(kode)


# ------------------------------------------------------------------
# teks.ak
# ------------------------------------------------------------------
def test_teks_dasar():
    kode = (
        'impor "teks.ak" sbg t\n'
        'cetak t.huruf_besar("halo")\n'
        'cetak t.huruf_kecil("HALO")\n'
        'cetak t.potong_teks("  x  ")\n'
        'cetak t.gabungkan(["a","b"], "-")\n'
        'cetak t.ganti("a-b", "-", "+")\n'
        'cetak t.balik_teks("aksara")\n'
    )
    assert keluaran_interp(kode) == "HALO\nhalo\nx\na-b\na+b\naraska\n"
    cek_setara(kode)


def test_teks_pemeriksaan():
    kode = (
        'impor "teks.ak" sbg t\n'
        'cetak t.mengandung("halo dunia", "dunia")\n'
        'cetak t.awalan("halo", "ha")\n'
        'cetak t.akhiran("halo", "lo")\n'
        'cetak t.jumlah_kata("satu dua tiga")\n'
        'cetak t.cari("abcdef", "cd")\n'
        'cetak t.cek_kosong("")\n'
        'cetak t.ulang_teks("ha", 3)\n'
        'cetak t.sub_teks("abcdefgh", 2, 5)\n'
        'cetak t.judul("halo dunia")\n'
    )
    assert keluaran_interp(kode) == (
        "True\nTrue\nTrue\n3\n2\nTrue\nhahaha\ncdef\nHalo Dunia\n"
    )
    cek_setara(kode)


# ------------------------------------------------------------------
# mtk.ak
# ------------------------------------------------------------------
def test_mtk():
    kode = (
        'impor "mtk.ak" sbg m\n'
        'cetak m.mutlak(-5)\n'
        'cetak m.pangkat(2, 8)\n'
        'cetak m.akar(9)\n'
        'cetak m.bulatkan(3.6)\n'
        'cetak m.bulat_atas(3.1)\n'
        'cetak m.bulat_bawah(3.9)\n'
        'cetak m.genap(4)\n'
        'cetak m.ganjil(7)\n'
        'cetak m.terbesar([3, 9, 1])\n'
        'cetak m.terkecil([3, 9, 1])\n'
    )
    assert keluaran_interp(kode) == "5\n256\n3.0\n4\n4\n3\nTrue\nTrue\n9\n1\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# koleksi.ak
# ------------------------------------------------------------------
def test_koleksi():
    kode = (
        'impor "koleksi.ak" sbg k\n'
        'cetak k.urutkan([5, 2, 8, 1])\n'
        'cetak k.urutkan_balik([5, 2, 8, 1])\n'
        'cetak k.unik([1, 2, 2, 3, 3])\n'
        'cetak k.balik_list([1, 2, 3])\n'
        'cetak k.gabung_list([1, 2], [3])\n'
        'cetak k.cari_indeks([10, 20, 30], 20)\n'
        'cetak k.hitung([1, 2, 2, 2], 2)\n'
        'cetak k.potong([1, 2, 3, 4, 5], 1, 3)\n'
        'cetak k.hapus_index([1, 2, 3, 4], 2)\n'
    )
    assert keluaran_interp(kode) == (
        "[1, 2, 5, 8]\n[8, 5, 2, 1]\n[1, 2, 3]\n"
        "[3, 2, 1]\n[1, 2, 3]\n1\n3\n[2, 3, 4]\n[1, 2, 4]\n"
    )
    cek_setara(kode)


# ------------------------------------------------------------------
# berkas.ak
# ------------------------------------------------------------------
def test_berkas(tmp_path):
    jalan = (tmp_path / "arsip.txt").as_posix()
    kode = (
        f'impor "berkas.ak" sbg b\n'
        f'b.tulis_file("{jalan}", "satu\\ndua\\n")\n'
        f'cetak b.apakah_ada("{jalan}")\n'
        f'cetak b.baca_file("{jalan}")\n'
        f'b.tambah_ke_file("{jalan}", "tiga\\n")\n'
        f'cetak b.baca_baris("{jalan}")\n'
        f'cetak b.ukuran_file("{jalan}")\n'
        f'b.hapus_file("{jalan}")\n'
        f'cetak b.apakah_ada("{jalan}")\n'
    )
    hasil = keluaran_interp(kode)
    assert "True\nsatu\ndua\n" in hasil
    assert "['satu', 'dua', 'tiga', '']" in hasil
    assert "False\n" in hasil
    cek_setara(kode)


# ------------------------------------------------------------------
# dorong (builtin append)
# ------------------------------------------------------------------
def test_dorong_builtin():
    kode = "x = [1, 2]\ndorong(x, 3)\ncetak x\ncetak dorong([], 9)\n"
    assert keluaran_interp(kode) == "[1, 2, 3]\n[9]\n"
    cek_setara(kode)


# ------------------------------------------------------------------
# larik.ak (normalisasi/skala/kelompok yang sebelumnya rusak)
# ------------------------------------------------------------------
def test_larik_normalisasi_dan_skala():
    kode = (
        'impor "larik.ak" sbg lk\n'
        'cetak lk.normalisasi([10, 20, 30, 40])\n'
        'cetak lk.skala([1, 2, 3], 10)\n'
        'cetak lk.kelompok([1, 2, 10, 11], 2)\n'
    )
    hasil = keluaran_interp(kode)
    assert "[0.0, 0.3333333333333333, 0.6666666666666666, 1.0]" in hasil
    assert "[10, 20, 30]" in hasil
    assert "[[1, 2], [10, 11]]" in hasil
    cek_setara(kode)
from aksara.lexer.tokenizer import tokenize
from aksara.parser.parser import Parser
from aksara.ast import nodes

def test_parse_cetak():
    kode = 'cetak "halo"'
    tokens = tokenize(kode)
    ast = Parser(tokens).parse_program()
    assert len(ast) == 1
    assert isinstance(ast[0], nodes.Cetak)

def test_parse_jika_lengkap():
    kode = """
    jika x > 5 {
        cetak "besar"
    } atau_jika x == 5 {
        cetak "sama"
    } lain {
        cetak "kecil"
    }
    """
    tokens = tokenize(kode)
    ast = Parser(tokens).parse_program()
    assert len(ast) == 1
    node = ast[0]
    assert isinstance(node, nodes.Jika)
    assert len(node.cabang_lain) == 2  # atau_jika dan lain

def test_parse_fun():
    kode = """
    fun sapa(nama) {
        balik "Halo " + nama
    }
    """
    tokens = tokenize(kode)
    ast = Parser(tokens).parse_program()
    assert len(ast) == 1
    assert isinstance(ast[0], nodes.DefinisiFungsi)

def test_parse_impor():
    kode = 'impor "os" sbg os'
    tokens = tokenize(kode)
    ast = Parser(tokens).parse_program()
    assert len(ast) == 1
    assert isinstance(ast[0], nodes.Impor)
    assert ast[0].nama_modul == "os"
    assert ast[0].alias == "os"

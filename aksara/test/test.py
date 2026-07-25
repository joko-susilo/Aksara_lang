from aksara.lexer.tokenizer import tokenize

def test_cetak_string():
    kode = 'cetak "Halo, dunia!"'
    tokens = tokenize(kode)
    assert tokens[0].tipe == "KATA_KUNCI"
    assert tokens[0].nilai == "cetak"
    assert tokens[1].tipe == "STRING"
    assert tokens[1].nilai == '"Halo, dunia!"'
    assert tokens[2].tipe == "EOF"

def test_blok_kurung():
    kode = "jika x > 5 { cetak x }"
    tokens = tokenize(kode)
    tipe_tipe = [t.tipe for t in tokens]
    assert "KURUNG_KUWAL" in tipe_tipe

def test_komentar_diabaikan():
    kode = """
    # ini komentar
    cetak "halo"
    """
    tokens = tokenize(kode)
    nilai_token = [t.nilai for t in tokens if t.tipe != "EOF"]
    assert "# ini komentar" not in nilai_token
    assert '"halo"' in nilai_token

def test_kata_kunci_pendek():
    kode = "fn sapa() { balik 'halo' }"  # string nanti pakai ", tapi ini tes konsep
    tokens = tokenize('fun sapa() { balik "halo" }')
    kata_kunci = [t.nilai for t in tokens if t.tipe == "KATA_KUNCI"]
    assert "fn" in kata_kunci
    assert "balik" in kata_kunci

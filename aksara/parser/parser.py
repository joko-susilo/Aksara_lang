from aksara.ast.nodes import *
from aksara.lexer.tokens import Token

class Parser:
    def __init__(self, tokens: list):
        self.tokens = tokens
        self.pos = 0

    def lihat(self) -> Token:
        return self.tokens[self.pos]

    def ambil(self, tipe=None, nilai=None) -> Token:
        t = self.lihat()
        if tipe and t.tipe != tipe:
            raise SyntaxError(f"Baris {t.baris}, kolom {t.kolom}: Diharapkan token {tipe}, tetapi dapat {t.tipe} ('{t.nilai}')")
        if nilai and t.nilai != nilai:
            raise SyntaxError(f"Baris {t.baris}, kolom {t.kolom}: Diharapkan '{nilai}', tetapi dapat '{t.nilai}'")
        self.pos += 1
        return t

    def parse_program(self) -> list:
        """Mengurai program menjadi daftar statement."""
        statements = []
        while self.lihat().tipe != "EOF":
            statements.append(self.parse_statement())
        return statements

    # ----------------------------------------------------------------------
    # Statement
    # ----------------------------------------------------------------------
    def parse_statement(self):
        t = self.lihat()
        if t.tipe == "KATA_KUNCI":
            if t.nilai == "jika":
                return self.parse_jika()
            elif t.nilai == "ulang":
                return self.parse_ulangi()
            elif t.nilai == "untuk":
                return self.parse_untuk()
            elif t.nilai == "selama":
                return self.parse_selama()
            elif t.nilai == "fun":
                return self.parse_fn()
            elif t.nilai == "cetak":
                return self.parse_cetak()
            elif t.nilai == "balik":
                return self.parse_balik()
            elif t.nilai == "henti":
                self.ambil("KATA_KUNCI", "henti")
                return Henti()
            elif t.nilai == "lanjut":
                self.ambil("KATA_KUNCI", "lanjut")
                return Lanjut()
            elif t.nilai == "impor":
                return self.parse_impor()
            elif t.nilai == "coba":
                return self.parse_coba()
            elif t.nilai == "galat":
                return self.parse_galat()
            else:
                raise SyntaxError(f"Baris {t.baris}: Kata kunci '{t.nilai}' tidak dikenal di awal statement")
        elif t.tipe == "NAMA":
            return self.parse_ekspresi_stmt()
        elif t.tipe in ("ANGKA", "STRING", "KURUNG"):
            return self.parse_ekspresi_stmt()
        elif t.tipe == "KURUNG_SIKU" and t.nilai == "[":
            self.ambil("KURUNG_SIKU", "[")
            elemen = []
            if self.lihat().tipe != "KURUNG_SIKU" or self.lihat().nilai != "]":
                elemen.append(self.parse_ekspresi())
            while self.lihat().tipe == "KOMA":
                self.ambil("KOMA")
                elemen.append(self.parse_ekspresi())
            self.ambil("KURUNG_SIKU", "]")
            return Daftar(elemen)
        else:
            raise SyntaxError(f"Baris {t.baris}: Token tak terduga {t.tipe} ('{t.nilai}')")
        

    def parse_blok(self) -> list:
        """Mengurai blok yang diapit { }."""
        self.ambil("KURUNG_KUWAL", "{")
        statements = []
        while self.lihat().tipe != "KURUNG_KUWAL" or self.lihat().nilai != "}":
            if self.lihat().tipe == "EOF":
                raise SyntaxError("Akhir file tak terduga saat mencari '}'")
            statements.append(self.parse_statement())
        self.ambil("KURUNG_KUWAL", "}")
        return statements

    def parse_jika(self):
        self.ambil("KATA_KUNCI", "jika")
        kondisi = self.parse_ekspresi()
        blok_jika = self.parse_blok()
        cabang = []
        while self.lihat().tipe == "KATA_KUNCI" and self.lihat().nilai in ("atau_jika", "lain"):
            if self.lihat().nilai == "atau_jika":
                self.ambil("KATA_KUNCI", "atau_jika")
                kondisi_elif = self.parse_ekspresi()
                blok_elif = self.parse_blok()
                cabang.append(Jika(kondisi_elif, blok_elif, []))
            elif self.lihat().nilai == "lain":
                self.ambil("KATA_KUNCI", "lain")
                blok_else = self.parse_blok()
                cabang.append(blok_else)
                break
        return Jika(kondisi, blok_jika, cabang)

    def parse_ulangi(self):
        self.ambil("KATA_KUNCI", "ulang")
        jumlah = self.parse_ekspresi()
        blok = self.parse_blok()
        return Ulangi(jumlah, blok)

    def parse_untuk(self):
        self.ambil("KATA_KUNCI", "untuk")
        var = self.ambil("NAMA").nilai
        self.ambil("KATA_KUNCI", "dalam")
        mulai = self.parse_ekspresi()
        if self.lihat().tipe == "OPERATOR" and self.lihat().nilai == "..":
            self.ambil("OPERATOR", "..")
            akhir = self.parse_ekspresi()
        else:
            raise SyntaxError(f"Baris {self.lihat().baris}: Diharapkan '..' untuk rentang")
        blok = self.parse_blok()
        return Untuk(var, mulai, akhir, blok)

    def parse_selama(self):
        self.ambil("KATA_KUNCI", "selama")
        kondisi = self.parse_ekspresi()
        blok = self.parse_blok()
        return Selama(kondisi, blok)

    def parse_fn(self):
        self.ambil("KATA_KUNCI", "fun")
        nama = self.ambil("NAMA").nilai
        self.ambil("KURUNG", "(")
        parameter = []
        if self.lihat().tipe == "NAMA":
            parameter.append(self.ambil("NAMA").nilai)
        while self.lihat().tipe == "KOMA":
            self.ambil("KOMA")                          
            parameter.append(self.ambil("NAMA").nilai)   
        self.ambil("KURUNG", ")")
        blok = self.parse_blok()
        return DefinisiFungsi(nama, parameter, blok)

    def parse_cetak(self):
        self.ambil("KATA_KUNCI", "cetak")
        ekspresi = self.parse_ekspresi()
        return Cetak(ekspresi)

    def parse_balik(self):
        self.ambil("KATA_KUNCI", "balik")
        ekspresi = self.parse_ekspresi()
        return Balik(ekspresi)

    def parse_impor(self):
        self.ambil("KATA_KUNCI", "impor")
        modul_token = self.ambil("STRING")
        nama_modul = modul_token.nilai[1:-1]
        self.ambil("KATA_KUNCI", "sbg")
        alias = self.ambil("NAMA").nilai
        return Impor(nama_modul, alias)

    def parse_ekspresi_stmt(self):
        ekspr = self.parse_ekspresi()
        if self.lihat().tipe == "OPERATOR" and self.lihat().nilai == "=":
        # Pastikan ekspr adalah target yang valid
            if not isinstance(ekspr, (NamaVariabel, AksesIndeks, AksesAtribut)):
                raise SyntaxError(f"Baris {self.lihat().baris}: Target assignment tidak valid")
                
            self.ambil("OPERATOR", "=")
            nilai = self.parse_ekspresi()
        # Gunakan Assign(target_node, nilai) — target_node adalah objek, bukan string
            return Assign(ekspr, nilai)
        return ekspr
    # ----------------------------------------------------------------------
    # Ekspresi (dengan prioritas)
    # ----------------------------------------------------------------------
    def parse_ekspresi(self):
        return self.parse_assignment()

    def parse_assignment(self):
        return self.parse_logika_or()

    def parse_logika_or(self):
        kiri = self.parse_logika_and()
        while self.lihat().tipe == "KATA_KUNCI" and self.lihat().nilai == "atau":
            self.ambil("KATA_KUNCI", "atau")
            kanan = self.parse_logika_and()
            kiri = OperasiBiner(kiri, "atau", kanan)
        return kiri

    def parse_logika_and(self):
        kiri = self.parse_equality()
        while self.lihat().tipe == "KATA_KUNCI" and self.lihat().nilai == "dan":
            self.ambil("KATA_KUNCI", "dan")
            kanan = self.parse_equality()
            kiri = OperasiBiner(kiri, "dan", kanan)
        return kiri

    def parse_equality(self):
        kiri = self.parse_comparison()
        while self.lihat().tipe == "OPERATOR" and self.lihat().nilai in ("==", "!="):
            op = self.ambil("OPERATOR").nilai
            kanan = self.parse_comparison()
            kiri = OperasiBiner(kiri, op, kanan)
        return kiri

    def parse_comparison(self):
        kiri = self.parse_addition()
        while self.lihat().tipe == "OPERATOR" and self.lihat().nilai in ("<", ">", "<=", ">="):
            op = self.ambil("OPERATOR").nilai
            kanan = self.parse_addition()
            kiri = OperasiBiner(kiri, op, kanan)
        return kiri

    def parse_addition(self):
        kiri = self.parse_multiplication()
        while self.lihat().tipe == "OPERATOR" and self.lihat().nilai in ("+", "-"):
            op = self.ambil("OPERATOR").nilai
            kanan = self.parse_multiplication()
            kiri = OperasiBiner(kiri, op, kanan)
        return kiri

    def parse_multiplication(self):
        kiri = self.parse_unary()
        while self.lihat().tipe == "OPERATOR" and self.lihat().nilai in ("*", "/", "%"):
            op = self.ambil("OPERATOR").nilai
            kanan = self.parse_unary()
            kiri = OperasiBiner(kiri, op, kanan)
        return kiri

    def parse_unary(self):
        if self.lihat().tipe == "OPERATOR" and self.lihat().nilai == "-":
            self.ambil("OPERATOR", "-")
            ekspr = self.parse_unary()
            return OperasiUnary("-", ekspr)
        elif self.lihat().tipe == "KATA_KUNCI" and self.lihat().nilai == "bukan":
            self.ambil("KATA_KUNCI", "bukan")
            ekspr = self.parse_unary()
            return OperasiUnary("bukan", ekspr)
        return self.parse_primary()

    def parse_primary(self):
        t = self.lihat()

        # Literal angka
        if t.tipe == "ANGKA":
            token_angka = self.ambil("ANGKA")
            return Angka(token_angka.nilai)

        # Literal string
        elif t.tipe == "STRING":
            token_string = self.ambil("STRING")
            return String(token_string.nilai)

        # Boolean dan nil
        elif t.tipe == "KATA_KUNCI":
            if t.nilai == "benar":
                self.ambil("KATA_KUNCI", "benar")
                return Boolean("benar")
            elif t.nilai == "salah":
                self.ambil("KATA_KUNCI", "salah")
                return Boolean("salah")
            elif t.nilai == "nil":
                self.ambil("KATA_KUNCI", "nil")
                return Nil()
            else:
                raise SyntaxError(f"Baris {t.baris}: Kata kunci '{t.nilai}' tidak dapat digunakan sebagai ekspresi")

        # Nama variabel, akses atribut, pemanggilan fungsi, atau akses indeks
        elif t.tipe == "NAMA":
            nama = self.ambil("NAMA").nilai
            node = NamaVariabel(nama)

            while True:
                if self.lihat().tipe == "TITIK":
                    self.ambil("TITIK")
                    attr = self.ambil("NAMA").nilai
                    node = AksesAtribut(node, attr)
                elif self.lihat().tipe == "KURUNG" and self.lihat().nilai == "(":
                    self.ambil("KURUNG", "(")
                    args = []
                    if self.lihat().tipe != "KURUNG" or self.lihat().nilai != ")":
                        args.append(self.parse_ekspresi())
                        while self.lihat().tipe == "KOMA":
                            self.ambil("KOMA")
                            args.append(self.parse_ekspresi())
                    self.ambil("KURUNG", ")")
                    node = PanggilFungsi(node, args)
                elif self.lihat().tipe == "KURUNG_SIKU" and self.lihat().nilai == "[":
                    self.ambil("KURUNG_SIKU", "[")
                    indeks = self.parse_ekspresi()
                    self.ambil("KURUNG_SIKU", "]")
                    node = AksesIndeks(node, indeks)
                else:
                    break
            return node

        # List literal
        elif t.tipe == "KURUNG_SIKU" and t.nilai == "[":
            self.ambil("KURUNG_SIKU", "[")
            if self.lihat().tipe == "KURUNG_SIKU" and self.lihat().nilai =="]":
                self.ambil("KURUNG_SIKU","]")
                return Daftar([])
            elemen_pertama = self.parse_ekspresi()
            #deteksi kamus
            if self.lihat().tipe == "TITIK_DUA":
                self.ambil("TITIK_DUA")
                nilai = self.parse_ekspresi()
                pasangan = [(elemen_pertama,nilai)]
                
                while self.lihat().tipe == "KOMA":
                    self.ambil("KOMA")
                    kunci = self.parse_ekspresi()
                    self.ambil("TITIK_DUA")
                    nilai = self.parse_ekspresi()
                    pasangan.append((kunci,nilai))
                self.ambil("KURUNG_SIKU","]")
                return Kamus(pasangan)
            else:
                #list biasa
                elemen = [elemen_pertama]
                while self.lihat().tipe == "KOMA":
                    self.ambil("KOMA")
                    elemen.append(self.parse_ekspresi())
                    self.ambil("KURUNG_SIKU","]")
                return Daftar(elemen)
           
        # Ekspresi dalam kurung biasa ( )
        elif t.tipe == "KURUNG" and t.nilai == "(":
            self.ambil("KURUNG", "(")
            ekspr = self.parse_ekspresi()
            self.ambil("KURUNG", ")")
            return ekspr

        else:
            raise SyntaxError(f"Baris {t.baris}: Token tak terduga {t.tipe} ('{t.nilai}') dalam ekspresi")

    def parse_coba(self):
        self.ambil("KATA_KUNCI", "coba")
        blok_coba = self.parse_blok()

        kecuali_cabang = []
        blok_akhirnya = None   # inisialisasi

        # Parsing satu atau lebih blok kecuali
        while self.lihat().tipe == "KATA_KUNCI" and self.lihat().nilai == "kecuali":
            self.ambil("KATA_KUNCI", "kecuali")
            tipe_error = None
            var_error = None

            # Opsional: [TipeError]
            if self.lihat().tipe == "KURUNG_SIKU" and self.lihat().nilai == "[":
                self.ambil("KURUNG_SIKU", "[")
                tipe_error = self.ambil("NAMA").nilai
                self.ambil("KURUNG_SIKU", "]")

            # Opsional: sebagai variabel
            if self.lihat().tipe == "KATA_KUNCI" and self.lihat().nilai == "sebagai":
                self.ambil("KATA_KUNCI", "sebagai")
                var_error = self.ambil("NAMA").nilai

            # Parsing blok kode kecuali
            blok_kecuali = self.parse_blok()
            kecuali_cabang.append(KecualiCabang(tipe_error, var_error, blok_kecuali))

        # Parsing blok akhirnya (opsional, setelah semua kecuali)
        if self.lihat().tipe == "KATA_KUNCI" and self.lihat().nilai == "akhirnya":
            self.ambil("KATA_KUNCI", "akhirnya")
            blok_akhirnya = self.parse_blok()

        return Coba(blok_coba, kecuali_cabang, blok_akhirnya)
    def parse_galat(self):
        self.ambil("KATA_KUNCI","galat")
        pesan = self.parse_ekspresi()
        return Galat(pesan)


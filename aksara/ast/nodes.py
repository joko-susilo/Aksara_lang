from aksara.ast.nodes import *
class ASTNode:
    """Kelas dasar untuk semua node AST."""
    pass

# ---------- Ekspresi ----------
class Angka(ASTNode):
    def __init__(self, nilai: str):
        self.nilai = float(nilai) if '.' in nilai else int(nilai)
    def __repr__(self):
        return f"Angka({self.nilai})"

class String(ASTNode):
    def __init__(self, nilai: str):
        self.nilai = nilai[1:-1]  # hapus kutip
    def __repr__(self):
        return f'String("{self.nilai}")'

class Boolean(ASTNode):
    def __init__(self, nilai: str):
        self.nilai = True if nilai == "benar" else False
    def __repr__(self):
        return f"Boolean({self.nilai})"
        
class Daftar(ASTNode):
    def __init__(self, elemen: list):
        self.elemen = elemen
    def __repr__(self):
        return f"Daftar({self.elemen})"

class Nil(ASTNode):
    def __repr__(self):
        return "Nil"

class NamaVariabel(ASTNode):
    def __init__(self, nama: str):
        self.nama = nama
    def __repr__(self):
        return f"NamaVariabel({self.nama})"

class OperasiBiner(ASTNode):
    def __init__(self, kiri, op: str, kanan):
        self.kiri = kiri
        self.op = op
        self.kanan = kanan
    def __repr__(self):
        return f"OperasiBiner({self.kiri}, {self.op}, {self.kanan})"

class OperasiUnary(ASTNode):
    def __init__(self, op: str, ekspresi):
        self.op = op
        self.ekspresi = ekspresi
    def __repr__(self):
        return f"OperasiUnary({self.op}, {self.ekspresi})"

class PanggilFungsi(ASTNode):
    def __init__(self, fungsi, argumen: list):
        self.fungsi = fungsi   # AST node yang menghasilkan callable (bisa NamaVariabel atau AksesAtribut)
        self.argumen = argumen
    def __repr__(self):
        return f"PanggilFungsi({self.fungsi}, {self.argumen})"

class AksesAtribut(ASTNode):
    def __init__(self, objek, atribut: str):
        self.objek = objek
        self.atribut = atribut
    def __repr__(self):
        return f"AksesAtribut({self.objek}, {self.atribut})"

# ---------- Statement ----------
class Cetak(ASTNode):
    def __init__(self, ekspresi):
        self.ekspresi = ekspresi
    def __repr__(self):
        return f"Cetak({self.ekspresi})"

class Ulangi(ASTNode):
    def __init__(self, jumlah, blok: list):
        self.jumlah = jumlah
        self.blok = blok
    def __repr__(self):
        return f"Ulangi({self.jumlah}, {self.blok})"

class Untuk(ASTNode):
    def __init__(self, var: str, mulai, akhir, blok: list):
        self.var = var
        self.mulai = mulai
        self.akhir = akhir
        self.blok = blok
    def __repr__(self):
        return f"Untuk({self.var}, {self.mulai}..{self.akhir}, {self.blok})"

class Selama(ASTNode):
    def __init__(self, kondisi, blok: list):
        self.kondisi = kondisi
        self.blok = blok
    def __repr__(self):
        return f"Selama({self.kondisi}, {self.blok})"

class Jika(ASTNode):
    def __init__(self, kondisi, blok_jika: list, cabang_lain: list = None):
        # cabang_lain bisa berisi node Jika (untuk atau_jika) atau list statement (untuk lain)
        self.kondisi = kondisi
        self.blok_jika = blok_jika
        self.cabang_lain = cabang_lain if cabang_lain is not None else []
    def __repr__(self):
        return f"Jika({self.kondisi}, {self.blok_jika}, cabang={self.cabang_lain})"

class DefinisiFungsi(ASTNode):
    def __init__(self, nama: str, parameter: list, blok: list):
        self.nama = nama
        self.parameter = parameter
        self.blok = blok
    def __repr__(self):
        return f"DefinisiFungsi({self.nama}({self.parameter}), {self.blok})"

class Balik(ASTNode):
    def __init__(self, ekspresi=None):
        self.ekspresi = ekspresi
    def __repr__(self):
        return f"Balik({self.ekspresi})"

class Henti(ASTNode):
    def __repr__(self):
        return "Henti"

class Lanjut(ASTNode):
    def __repr__(self):
        return "Lanjut"

class Impor(ASTNode):
    def __init__(self, nama_modul: str, alias: str):
        self.nama_modul = nama_modul
        self.alias = alias
    def __repr__(self):
        return f"Impor({self.nama_modul} sebagai {self.alias})"
class AksesIndeks(ASTNode):
    def __init__(self,objek,indeks):
        self.objek = objek
        self.indeks = indeks
    def __repr__(self):
        return f"AksesIndeks({self.objek}[{self.indeks}])"
class Slice(ASTNode):
    def __init__(self, objek, mulai=None, akhir=None):
        self.objek = objek
        self.mulai = mulai      # AST node atau None
        self.akhir = akhir      # AST node atau None
    def __repr__(self):
        m = self.mulai if self.mulai is not None else ""
        a = self.akhir if self.akhir is not None else ""
        return f"Slice({self.objek}[{m}..{a}])"

class Assign(ASTNode):
    def __init__(self, target, nilai):
        self.target = target
        self.nilai = nilai
    def __repr__(self):
        return f"Assign({self.target} = {self.nilai})"
class KecualiCabang(ASTNode):
    def __init__(self,tipe_error,var_error,blok):
        self.tipe_error = tipe_error
        self.var_error = var_error
        self.blok = blok
    def __repr__(self):
        return f"Kecuali({self.jenis_error} sebagai {self.var_error}:{self.blok})"
        
class Coba(ASTNode):
    def __init__(self,blok_coba,kecuali_list,akhirnya):
        self.blok_coba = blok_coba
        self.kecuali_list= kecuali_list
        self.akhirnya =akhirnya
    def __repr__(self):
        return f"Coba(kecuali = {self.kecuali_cabang},akhirnya = {self.akhirnya})"
        
class Galat(ASTNode):
    def __init__(self,pesan):
        self.pesan = pesan
    def __repr__(self):
        return f"Galat({self.pesan})"
        
class Kamus(ASTNode):
    def __init__(self,pasangan):
        self.pasangan = pasangan
    def __repr__(self):
        return f"Kamus({self.pasangan})"

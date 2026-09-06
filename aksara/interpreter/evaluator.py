# Copyright 2026 Joko Susilo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.



import sys as _sys
from aksara.ast.nodes import *
from aksara.interpreter.environment import Environment
from aksara.interpreter.builtins import BUILTINS, aksara_impor
from aksara.interpreter.oop import (KelasValue, ObjekAksara, MetodeInterp,
                                    _PranalaInduk)
import builtins as py_builtins

_MOD = _sys.modules[__name__]

# Exception untuk alur kontrol
class ReturnException(Exception):
    def __init__(self, value=None):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

def _cari_modul_aksara(nama_file) -> str:
    """Mencari file .ak: folder stdlib di dalam paket, ./stdlib, lalu folder kerja."""
    import os
    from aksara import __file__ as jalan_paket
    kandidat = [
        os.path.join(os.path.dirname(jalan_paket), "stdlib", nama_file),
        f"stdlib/{nama_file}",
        nama_file,
    ]
    for jalan in kandidat:
        if os.path.exists(jalan):
            return jalan
    return None


def _nilai_biner(op, kiri, kanan):
    """Terapkan operator aritmetika pada dua nilai (dipakai assign gabungan)."""
    if op == '+':
        if isinstance(kiri, str) or isinstance(kanan, str):
            return str(kiri) + str(kanan)
        return kiri + kanan
    if op == '-':
        return kiri - kanan
    if op == '*':
        return kiri * kanan
    if op == '/':
        return kiri / kanan
    if op == '%':
        return kiri % kanan
    raise SyntaxError(f"Operator gabungan '{op}=' tidak dikenal")


def _tetapkan(target, nilai, env):
    """Menempatkan nilai ke target assignment (variabel/indeks/atribut)."""
    if isinstance(target, NamaVariabel):
        try:
            env.assign(target.nama, nilai)
        except NameError:
            env.define(target.nama, nilai)
    elif isinstance(target, AksesIndeks):
        obj = evaluate(target.objek, env)
        indeks = evaluate(target.indeks, env)
        obj[indeks] = nilai
    elif isinstance(target, AksesAtribut):
        obj = evaluate(target.objek, env)
        setattr(obj, target.atribut, nilai)
    else:
        raise RuntimeError(f"Target assignment tidak didukung: {type(target).__name__}")


def evaluate(node, env):
    """Mengevaluasi sebuah node AST di dalam environment yang diberikan."""

    # --- Literal ---
    if isinstance(node, Angka):
        return node.nilai
    elif isinstance(node, String):
        return node.nilai
    elif isinstance(node, Boolean):
        return node.nilai
    elif isinstance(node, Nil):
        return None

    # --- Variabel ---
    elif isinstance(node, NamaVariabel):
        return env.get(node.nama)

    # --- Operasi ---
    elif isinstance(node, OperasiBiner):
        return eval_biner(node, env)
    elif isinstance(node, OperasiUnary):
        return eval_unary(node, env)

    elif isinstance(node, Ini):
        return env.get("ini")

    elif isinstance(node, Induk):
        return env.get("induk")

    elif isinstance(node, DefinisiKelas):
        induk = None
        if node.induk:
            induk = env.get(node.induk)
        # Bangun metode dulu; kelas_asal dipakai untuk resolusi 'induk'.
        kelas = KelasValue(node.nama, {})
        metode = {}
        for m in node.metode:
            metode[m.nama] = MetodeInterp(m, env, _MOD, kelas)
        # Gabung dengan metode induk (anak menimpa induk).
        gabungan = dict(induk.metode) if induk is not None else {}
        gabungan.update(metode)
        kelas.metode = gabungan
        kelas.induk = induk if induk is not None else None
        env.define(node.nama, kelas)
        return kelas

    # --- Pemanggilan Fungsi & Atribut ---
    elif isinstance(node, PanggilFungsi):
        return eval_panggil_fungsi(node, env)
    elif isinstance(node, AksesAtribut):
        return eval_akses_atribut(node, env)

    # --- Statement ---
    elif isinstance(node, Cetak):
        nilai = [evaluate(e, env) for e in node.argumen]
        print(*nilai)
        return None if not nilai else nilai[-1]
    elif isinstance(node, Ulangi):
        return eval_ulangi(node, env)
    elif isinstance(node, Untuk):
        return eval_untuk(node, env)
    elif isinstance(node, Selama):
        return eval_selama(node, env)
    elif isinstance(node, Jika):
        return eval_jika(node, env)
    elif isinstance(node, DefinisiFungsi):
        fungsi = Fungsi(node.nama, node.parameter, node.blok, env, node.parameter_default)
        env.define(node.nama, fungsi)
        return fungsi
    elif isinstance(node, AksesIndeks):
        obj = evaluate(node.objek, env)
        indeks = evaluate(node.indeks, env)
        # Teruskan tipe error asli (IndexError/KeyError/dst) supaya kecuali [Tipe] bekerja.
        return obj[indeks]

    elif isinstance(node, Daftar):
        return [evaluate(el, env) for el in node.elemen]
    elif isinstance(node, Balik):
        nilai = evaluate(node.ekspresi, env) if node.ekspresi else None
        raise ReturnException(nilai)
    elif isinstance(node, Henti):
        raise BreakException()
    elif isinstance(node, Lanjut):
        raise ContinueException()
    elif isinstance(node, Impor):
        return aksara_impor(node.nama_modul, node.alias, env)
    elif isinstance(node, Assign):
        nilai = evaluate(node.nilai, env)
        _tetapkan(node.target, nilai, env)
        return nilai
        
    elif isinstance(node, AssignOp):
        kiri = evaluate(node.target, env)
        kanan = evaluate(node.nilai, env)
        hasil = _nilai_biner(node.op, kiri, kanan)
        _tetapkan(node.target, hasil, env)
        return hasil

    elif isinstance(node, Coba):
        try:
            return evaluate(node.blok_coba, env)
        except (ReturnException, BreakException, ContinueException):
            # balik/henti/lanjut bukan error: lewati handling kecuali.
            raise
        except Exception as e:
            for cabang in node.kecuali_list:
                # Jika cabang punya tipe error spesifik
                if cabang.tipe_error:
                    tipe_target = None
                    try:
                        tipe_target = env.get(cabang.tipe_error)
                    except NameError:
                        tipe_target = getattr(py_builtins, cabang.tipe_error, None)
                    
                    # Jika tipe cocok, eksekusi blok ini
                    if tipe_target and isinstance(e, tipe_target):
                        if cabang.var_error:
                            env.define(cabang.var_error, str(e))
                        return evaluate(cabang.blok, env)
                    # Jika tidak cocok, lanjut ke cabang berikutnya
                    else:
                        continue
                else:
                    # kecuali tanpa tipe: tangkap semua error
                    if cabang.var_error:
                        env.define(cabang.var_error, str(e))
                    return evaluate(cabang.blok, env)
            # Jika tidak ada cabang yang cocok, lempar ulang error
            raise e
        finally:
            if node.akhirnya:
                evaluate(node.akhirnya, env)

    elif isinstance(node,Galat):
        pesan = evaluate(node.pesan,env)
        raise RuntimeError(str(pesan))
            
    elif isinstance(node,Slice):
        obj = evaluate(node.objek,env)
        mulai = evaluate(node.mulai,env) if node.mulai is not None else None
        # Inklusif: a..b mencakup b, jadi geser ujung slice Python +1
        akhir = evaluate(node.akhir,env) + 1 if node.akhir is not None else None
        try:
            return obj[mulai:akhir]
        except (TypeError,IndexError) as e:
            raise RuntimeError(f"Tidak dapat melakukan slice pada {obj}: {e}")
    elif isinstance(node,Kamus):
        hasil = {}
        for kunci,nilai in node.pasangan:
            k = evaluate(kunci,env)
            v = evaluate(nilai,env)
            hasil[k] = v
        return hasil
        
    elif isinstance(node, ImporLokal):
        file_path = _cari_modul_aksara(node.nama_file)
        if file_path is None:
            raise ImportError(f"Tidak dapat menemukan '{node.nama_file}'")

        from aksara.lexer.tokenizer import tokenize
        from aksara.parser.parser import Parser

        with open(file_path, encoding="utf-8") as f:
            kode = f.read()

        tokens = tokenize(kode)
        ast = Parser(tokens).parse_program()

        modul_env = Environment(parent=env)
        for stmt in ast:
            evaluate(stmt, modul_env)

        env.define(node.alias, modul_env)
        return modul_env



    # --- Blok (list of statements) ---
    elif isinstance(node, list):
        result = None
        try:
            for stmt in node:
                result = evaluate(stmt, env)
        except ReturnException:
            raise
        except BreakException:
            # Henti di dalam blok: hentikan sisa statement blok ini,
            # lalu teruskan ke konstruksi perulangan terdekat.
            raise
        except ContinueException:
            raise
        return result
    else:
        raise NotImplementedError(f"Evaluasi belum diimplementasi untuk {type(node)}")
        # ERROR
    
    
                    
# --- Fungsi bantu evaluasi ---
def eval_biner(node, env):
    kiri = evaluate(node.kiri, env)
    kanan = evaluate(node.kanan, env)
    op = node.op

    if op == '+':
        # Jika salah satu string, gabung jadi string
        if isinstance(kiri, str) or isinstance(kanan, str):
            return str(kiri) + str(kanan)
        return kiri + kanan

    elif op == '-':
        return kiri - kanan

    elif op == '*':
        # Jika string * int (atau int * string), ulangi string
        if isinstance(kiri, str) and isinstance(kanan, int):
            return kiri * kanan
        if isinstance(kanan, str) and isinstance(kiri, int):
            return kanan * kiri
        return kiri * kanan

    elif op == '/':
        if kanan == 0:
            raise ZeroDivisionError("Pembagian dengan nol")
        return kiri / kanan

    elif op == '%':
        if kanan == 0:
            raise ZeroDivisionError("Modulo dengan nol")
        return kiri % kanan

    elif op == '**':
        return kiri ** kanan

    elif op == '==':
        return kiri == kanan
    elif op == '!=':
        return kiri != kanan
    elif op == '<':
        return kiri < kanan
    elif op == '>':
        return kiri > kanan
    elif op == '<=':
        return kiri <= kanan
    elif op == '>=':
        return kiri >= kanan

    # Operator logika
    elif op == 'dan':
        return kiri and kanan
    elif op == 'atau':
        return kiri or kanan
    #Null Coalescing
    elif op == '??':
        return kiri if kiri is not None else kanan

    else:
        raise SyntaxError(f"Operator '{op}' tidak dikenal")

def eval_unary(node, env):
    nilai = evaluate(node.ekspresi, env)
    if node.op == '-': 
        return -nilai
    elif node.op == 'bukan': 
        return not nilai
    else:
        raise SyntaxError(f"Operator unary '{node.op}' tidak dikenal")

def eval_panggil_fungsi(node, env):
    # Dapatkan objek fungsi
    if isinstance(node.fungsi, NamaVariabel):
        nama_fungsi = node.fungsi.nama
        # Fungsi buatan user (di env) lebih dulu; builtin jadi cadangan.
        try:
            fungsi_obj = env.get(nama_fungsi)
        except NameError:
            fungsi_obj = BUILTINS.get(nama_fungsi)
        if fungsi_obj is None:
            raise NameError(f"Fungsi '{nama_fungsi}' tidak ditemukan")
    else:
        fungsi_obj = evaluate(node.fungsi, env)

    arg_values = [evaluate(arg, env) for arg in node.argumen]
    arg_kunci = {nama: evaluate(val, env) for nama, val in node.argumen_kunci}

    if isinstance(fungsi_obj, Fungsi):
        return panggil_fungsi_aksara(fungsi_obj, arg_values, arg_kunci)
    if callable(fungsi_obj):
        if arg_kunci:
            return fungsi_obj(*arg_values, **arg_kunci)
        return fungsi_obj(*arg_values)
    raise TypeError(f"'{node.fungsi}' bukan fungsi")

def eval_akses_atribut(node, env):
    obj = evaluate(node.objek, env)
    # Akses anggota modul Aksara (hasil impor .ak disimpan sebagai Environment)
    if isinstance(obj, Environment):
        try:
            return obj.get(node.atribut)
        except NameError:
            raise AttributeError(f"Modul tidak memiliki '{node.atribut}'")
    try:
        return getattr(obj, node.atribut)
    except AttributeError:
        raise AttributeError(f"Objek '{obj}' tidak memiliki atribut '{node.atribut}'")

def eval_ulangi(node, env):
    jumlah = int(evaluate(node.jumlah, env))
    result = None
    for _ in range(jumlah):
        try:
            result = evaluate(node.blok, env)
        except BreakException:
            break
        except ContinueException:
            continue
    return result

def eval_untuk(node, env):
    mulai = evaluate(node.mulai, env)
    akhir = node.akhir
    result = None
    if akhir is None:
        for item in mulai:
            env.define(node.var,item)
            try:
                result = evaluate(node.blok,env)
            except BreakException:
                break
            except ContinueException:
                continue
    else:
         akhir_var = evaluate(akhir,env)
         for i in range (int(mulai),int(akhir_var) + 1):
            env.define(node.var, i)
            try:
                result = evaluate(node.blok, env)
            except BreakException:
                break
            except ContinueException:
                continue
    return result

def eval_selama(node, env):
    result = None
    while evaluate(node.kondisi, env):
        try:
            result = evaluate(node.blok, env)
        except BreakException:
            break
        except ContinueException:
            continue
    return result

def eval_jika(node, env):
    if evaluate(node.kondisi, env):
        return evaluate(node.blok_jika, env)
    else:
        for cabang in node.cabang_lain:
            if isinstance(cabang, Jika):
                if evaluate(cabang.kondisi, env):
                    return evaluate(cabang.blok_jika, env)
            else:
                return evaluate(cabang, env)
        return None

# --- Definisi Fungsi Kustom ---
class Fungsi:
    def __init__(self, nama, parameter, blok, closure, parameter_default=None):
        self.nama = nama
        self.parameter = parameter
        self.blok = blok
        self.closure = closure  # environment tempat fungsi didefinisikan (closure)
        self.parameter_default = parameter_default or [None] * len(parameter)

    def __call__(self, *argumen):
        """Agar Fungsi bisa dipanggil langsung dari Python luar (interop)."""
        return panggil_fungsi_aksara(self, list(argumen))

def panggil_metode(fungsi, ini_obj, arg_values, closure, kelas_asal=None, arg_kunci=None):
    """Menjalankan metode Aksara: `ini` diikat ke objek pemanggil.

    `kelas_asal` adalah kelas tempat metode didefinisikan; `induk` (super)
    dibangun dari induk kelas itu, bukan kelas objek, agar override bertingkat
    tidak berulang tak hingga.
    """
    env_fungsi = Environment(parent=closure)
    env_fungsi.define("ini", ini_obj)
    # Kelas sumber untuk super: kelas_asal bila diketahui, else kelas objek.
    if kelas_asal is not None:
        kelas_super = kelas_asal.induk
    else:
        kelas_obj = getattr(ini_obj, "kelas", None)
        kelas_super = kelas_obj.induk if kelas_obj else None
    env_fungsi.define("induk", _PranalaInduk(ini_obj, kelas_super))
    nilai = urai_argumen(
        fungsi.nama, fungsi.parameter, fungsi.parameter_default,
        arg_values, arg_kunci or {}, closure,
    )
    for param, arg in zip(fungsi.parameter, nilai):
        env_fungsi.define(param, arg)
    try:
        return evaluate(fungsi.blok, env_fungsi)
    except ReturnException as ret:
        return ret.value


def urai_argumen(nama_fungsi, parameter, parameter_default, pos, kunci, env_default):
    """Menyatukan argumen posisional + keyword + nilai default ke urutan parameter."""
    if len(pos) > len(parameter):
        raise TypeError(
            f"Fungsi '{nama_fungsi}' menerima {len(parameter)} argumen, tetapi "
            f"diberikan {len(pos)} posisional"
        )
    peta = {}
    for i, nilai in enumerate(pos):
        peta[parameter[i]] = nilai
    for nama, nilai in kunci.items():
        if nama not in parameter:
            raise TypeError(f"Fungsi '{nama_fungsi}' tidak mengenal argumen '{nama}'")
        if nama in peta:
            raise TypeError(f"Fungsi '{nama_fungsi}': argumen '{nama}' diisi dua kali")
        peta[nama] = nilai
    for i, nama in enumerate(parameter):
        if nama not in peta:
            default = (parameter_default or [None] * len(parameter))[i]
            if default is None:
                raise TypeError(f"Fungsi '{nama_fungsi}' butuh argumen '{nama}'")
            peta[nama] = evaluate(default, env_default)
    return [peta[nama] for nama in parameter]


def panggil_fungsi_aksara(fungsi, arg_values, arg_kunci=None):
    """Mengeksekusi fungsi yang didefinisikan dalam Aksara."""
    nilai = urai_argumen(
        fungsi.nama, fungsi.parameter, fungsi.parameter_default,
        arg_values, arg_kunci or {}, fungsi.closure,
    )
    env_fungsi = Environment(parent=fungsi.closure)
    for param, arg in zip(fungsi.parameter, nilai):
        env_fungsi.define(param, arg)
    try:
        return evaluate(fungsi.blok, env_fungsi)
    except ReturnException as ret:
        return ret.value

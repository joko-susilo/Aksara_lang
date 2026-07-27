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



from aksara.ast.nodes import *
from aksara.interpreter.environment import Environment
from aksara.interpreter.builtins import BUILTINS, aksara_impor
import builtins as py_builtins

# Exception untuk alur kontrol
class ReturnException(Exception):
    def __init__(self, value=None):
        self.value = value

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

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

    # --- Pemanggilan Fungsi & Atribut ---
    elif isinstance(node, PanggilFungsi):
        return eval_panggil_fungsi(node, env)
    elif isinstance(node, AksesAtribut):
        return eval_akses_atribut(node, env)

    # --- Statement ---
    elif isinstance(node, Cetak):
        nilai = evaluate(node.ekspresi, env)
        print(nilai)
        return nilai
    elif isinstance(node, Ulangi):
        return eval_ulangi(node, env)
    elif isinstance(node, Untuk):
        return eval_untuk(node, env)
    elif isinstance(node, Selama):
        return eval_selama(node, env)
    elif isinstance(node, Jika):
        return eval_jika(node, env)
    elif isinstance(node, DefinisiFungsi):
        fungsi = Fungsi(node.nama, node.parameter, node.blok, env)
        env.define(node.nama, fungsi)
        return fungsi
    elif isinstance(node, AksesIndeks):
        obj = evaluate(node.objek, env)
        indeks = evaluate(node.indeks, env)
        try:
            return obj[indeks]
        except (IndexError, TypeError, KeyError) as e:
            raise RuntimeError(f"Tidak dapat mengakses indeks {indeks} pada {obj}: {e}")

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
        target = node.target
        if isinstance (target,NamaVariabel):
           try:
               env.assign(target.nama,nilai)
           except NameError:
               env.define(target.nama,nilai)
        elif isinstance (target,AksesIndeks):
            obj = evaluate(target.objek,env)
            indeks =evaluate(target.indeks,env)
            obj[indeks]=nilai
        elif isinstance (target,AksesAtribut):
            obj = evalutate(target.objek,env)
            setattr(obj,atribut,nilai)
        else:
            raise RuntimeError(f"target assigment tidak di dukung:{type(target)}")
        return nilai
        
    elif isinstance(node, Coba):
        try:
            return evaluate(node.blok_coba, env)
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
        obj = evaluate(node,Objek,env)
        mulai = evaluate(node,mulai,env) if node.mulai is not None else None
        akhir = evaluate(node,akhir,env) if node.akhir is not None else None
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
        
        

    # --- Blok (list of statements) ---
    elif isinstance(node, list):
        result = None
        for stmt in node:
            try:
                result = evaluate(stmt, env)
            except ReturnException as e:
                raise e
            except BreakException:
                break
            except ContinueException:
                continue
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
        # Builtins
        if nama_fungsi in BUILTINS:
            fungsi_obj = BUILTINS[nama_fungsi]
        else:
            fungsi_obj = env.get(nama_fungsi)
    else:      
        fungsi_obj = evaluate(node.fungsi, env)
        
    arg_values = [evaluate(arg, env) for arg in node.argumen]
    
    if callable(fungsi_obj):
        return fungsi_obj(*arg_values)
    elif isinstance(fungsi_obj, Fungsi):
        return panggil_fungsi_aksara(fungsi_obj, arg_values)
    else:
        raise TypeError(f"'{node.fungsi}' bukan fungsi")

def eval_akses_atribut(node, env):
    obj = evaluate(node.objek, env)
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
         for i in range (int(mulai),int(akhir_var)):
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
    def __init__(self, nama, parameter, blok, closure):
        self.nama = nama
        self.parameter = parameter
        self.blok = blok
        self.closure = closure  # environment tempat fungsi didefinisikan (closure)

def panggil_fungsi_aksara(fungsi, arg_values):
    """Mengeksekusi fungsi yang didefinisikan dalam Aksara."""
    if len(arg_values) != len(fungsi.parameter):
        raise TypeError(f"Fungsi '{fungsi.nama}' membutuhkan {len(fungsi.parameter)} argumen, tetapi diberikan {len(arg_values)}")
    
    env_fungsi = Environment(parent=fungsi.closure)
    for param, arg in zip(fungsi.parameter, arg_values):
        env_fungsi.define(param, arg)
    try:
        return evaluate(fungsi.blok, env_fungsi)
    except ReturnException as ret:
        return ret.value

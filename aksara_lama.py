#!/usr/bin/env python3
import sys
import re

# ==========================================
# 1. KAMUS AKSARA (Terintegrasi)
# ==========================================
KAMUS_AKSARA = {
    "atau_jika": "elif",
    "jika": "if",
    "selain_itu": "else",
    "untuk": "for",
    "selama": "while",
    "di_dalam": "in",
    "hentikan": "break",
    "lanjutkan": "continue",
    "fungsi": "def",
    "kembalikan": "return",
    "impor": "import",
    "dari": "from",
    "sebagai": "as",
    "kelas": "class",
    "coba": "try",
    "kecuali": "except",
    "akhirnya": "finally",
    "bangkitkan": "raise",
    "benar": "True",
    "salah": "False",
    "kosong": "None",
    "dan": "and",
    "atau": "or",
    "bukan": "not",
    "cetak": "print",
    "masukan": "input",
    "panjang": "len",
    "rentang": "range",
    "tipe": "type",
    "bulat": "int",
    "desimal": "float",
    "teks": "str",
    "daftar": "list",
    "kamus_data": "dict",
    "urutkan": "sorted"
}

# ==========================================
# 2. MESIN TRANSPILER
# ==========================================
def transpile_aksara(kode_aksara):
    # Urutkan kata kunci dari terpanjang agar frasa seperti 'atau_jika' tidak terpotong
    kata_kunci = sorted(KAMUS_AKSARA.keys(), key=len, reverse=True)
    kode_python = kode_aksara
    
    for kata in kata_kunci:
        padanan = KAMUS_AKSARA[kata]
        # Menggunakan regex dengan \b (word boundary) agar variabel aman
        pola = r'\b' + re.escape(kata) + r'\b'
        kode_python = re.sub(pola, padanan, kode_python)
        
    return kode_python

# ==========================================
# 3. MESIN EKSEKUSI & ERROR HANDLING
# ==========================================
def main():
    # Memastikan pengguna memasukkan nama file sebagai argumen
    if len(sys.argv) < 2:
        print("Penggunaan: aksara <nama_file.ak>")
        sys.exit(1)
    
    # DIPERBAIKI: Mengambil argumen pertama setelah nama skrip (indeks 1)
    nama_file = sys.argv[1]
    
    try:
        # Membaca file sumber Aksara
        with open(nama_file, 'r', encoding='utf-8') as f:
            kode_aksara = f.read()
            
        # Proses penerjemahan ke Python
        kode_python = transpile_aksara(kode_aksara)
        
        # Menjalankan kode Python hasil transpilasi
        exec(kode_python, globals())
        
    except FileNotFoundError:
        print(f"[Aksara Error] Berkas '{nama_file}' tidak ditemukan.")
    except SyntaxError as e:
        pesan = "Terdapat tanda kutip yang belum ditutup" if "unterminated string literal" in str(e) else e.msg
        print(f"[Kesalahan Sintaks] Baris {e.lineno}: {pesan}")
    except NameError as e:
        print(f"[Variabel Tidak Dikenal] Periksa kembali penamaan Anda: {e}")
    except IndentationError:
        print("[Kesalahan Indentasi] Periksa spasi/tab. Gunakan 4 spasi secara konsisten.")
    except ZeroDivisionError:
        print("[Kesalahan Logika] Terjadi pembagian dengan angka nol.")
    except Exception as e:
        print(f"[Error Tak Terduga] Terjadi masalah: {e}")

if __name__ == '__main__':
    main()

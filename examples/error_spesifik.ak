# Uji Error Handling Kompleks
cetak "=== UJI COBA-KECUALI-AKHIRNYA ==="

# 1. Menangkap error spesifik dengan variabel
coba {
    cetak "1. Mencoba membagi dengan nol..."
    x = 10 / 0
} kecuali [ZeroDivisionError] sebagai e {
    cetak "   Tertangkap: " + e
} akhirnya {
    cetak "   Selesai blok 1"
}

# 2. Error tidak cocok dengan tipe yang ditentukan
coba {
    cetak "2. Mencoba mengakses variabel tak dikenal..."
    y = variabel_tidak_ada + 5
} kecuali [ZeroDivisionError] sebagai e {
    cetak "   Ini tidak akan tercetak"
} kecuali sebagai e {
    cetak "   Tertangkap error lain: " + e
}

# 3. Blok tanpa error
coba {
    cetak "3. Operasi normal..."
    z = 10 + 20
    cetak "   Hasil: " + z
} kecuali sebagai e {
    cetak "   Tidak akan tercetak"
} akhirnya {
    cetak "   Selesai blok 3"
}

# 4. Error bersarang (nested)
coba {
    cetak "4. Error bersarang..."
    coba {
        a = [1, 2, 3]
        b = a[10]  # indeks di luar jangkauan
    } kecuali [IndexError] sebagai e {
        cetak "   Error dalam: " + e
        # lempar error baru
        x = "string" / 2
    }
} kecuali sebagai e {
    cetak "   Error luar: " + e
}

# 5. Menggunakan fungsi dengan error handling
fun bagi(a, b) {
    coba {
        jika b == 0 {
            bangkitkan "Pembagi tidak boleh nol!"
        }
        balik a / b
    } kecuali sebagai e {
        cetak "   Error di fungsi: " + e
        balik 0
    }
}

cetak "5. Memanggil fungsi dengan error handling..."
hasil = bagi(10, 0)
cetak "   Hasil: " + hasil
hasil = bagi(10, 2)
cetak "   Hasil: " + hasil

cetak "=== SELESAI ==="

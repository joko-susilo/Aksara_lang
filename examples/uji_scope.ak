cetak "=== Uji Cakupan Variabel (Scope) ==="

# 1. Uji variabel di dalam blok 'jika'
jika benar {
    pesan_rahasia = "Halo dari dalam blok jika!"
    cetak pesan_rahasia
}

# 2. Coba akses variabel tersebut di luar blok
# Bahasa pemrograman yang aman seharusnya memunculkan error (variabel tidak dikenal) 
# karena 'pesan_rahasia' seharusnya hanya hidup di dalam blok di atas.
cetak "Mencoba akses variabel dari luar blok:"
cetak pesan_rahasia

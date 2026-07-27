def kelompok(data, jumlah=2):
    """Kelompokkan data angka menjadi beberapa kelompok (k-means sederhana)"""
    if len(data) < jumlah:
        return data
    
    # Inisialisasi pusat (ambil nilai pertama dan terakhir)
    pusat = [data[0], data[-1]] if jumlah == 2 else data[:jumlah]
    
    for _ in range(10):  # iterasi
        kelompok_list = [[] for _ in range(jumlah)]
        
        # Masukkan setiap data ke kelompok terdekat
        for nilai in data:
            jarak = [abs(nilai - p) for p in pusat]
            idx = jarak.index(min(jarak))
            kelompok_list[idx].append(nilai)
        
        # Update pusat
        for i in range(jumlah):
            if kelompok_list[i]:
                pusat[i] = sum(kelompok_list[i]) / len(kelompok_list[i])
    
    return kelompok_list

def normalisasi(data):
    """Skala data ke rentang 0 sampai 1"""
    if len(data) == 0:
        return []
    
    nilai_min = data[0]
    nilai_max = data[0]
    
    # Cari min & max
    for x in data:
        if x < nilai_min:
            nilai_min = x
        if x > nilai_max:
            nilai_max = x
    
    # Kalau semua nilai sama
    if nilai_max == nilai_min:
        return [0.5 for _ in data]
    
    # Normalisasi
    hasil = []
    for x in data:
        hasil.append(round((x - nilai_min) / (nilai_max - nilai_min), 2))
    
    return hasil

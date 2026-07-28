def cari_mirip(target, data):
    """Cari item paling mirip dengan target"""
    if not data:
        return None
    
    # Untuk string
    if isinstance(target, str):
        terbaik = data[0]
        skor_terbaik = 0
        for item in data:
            # Hitung kemiripan sederhana
            skor = 0
            for c in target:
                if c in item:
                    skor = skor + 1
            if skor > skor_terbaik:
                skor_terbaik = skor
                terbaik = item
        return terbaik
    
    # Untuk angka
    terdekat = data[0]
    jarak_terkecil = abs(target - data[0])
    for item in data:
        jarak = abs(target - item)
        if jarak < jarak_terkecil:
            jarak_terkecil = jarak
            terdekat = item
    return terdekat

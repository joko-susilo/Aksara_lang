def jenis(teks):
    """Klasifikasi sentimen sederhana"""
    positif = ["bagus", "keren", "mantap", "suka", "hebat", "baik", "senang", "indah", "cantik", "luar biasa", "oke", "recommended"]
    negatif = ["jelek", "buruk", "kecewa", "sedih", "marah", "payah", "bosen", "bosan", "rugi", "sampah", "tolol", "gagal"]
    
    teks = teks.lower()
    skor = 0
    
    for kata in positif:
        if kata in teks:
            skor = skor + 1
    
    for kata in negatif:
        if kata in teks:
            skor = skor - 1
    
    if skor > 0:
        return "positif"
    elif skor < 0:
        return "negatif"
    else:
        return "netral"

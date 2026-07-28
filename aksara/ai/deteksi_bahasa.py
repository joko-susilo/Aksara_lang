def deteksi_bahasa(teks):
    """Deteksi bahasa dari teks (Indonesia, Sunda, Jawa, Inggris)"""
    kamus = {
        "sunda": ["kumaha", "damang", "teh", "mah", "ieu", "eta"],
        "jawa": ["piye", "kabare", "iki", "iku", "tenan"],
        "indonesia": ["yang", "dan", "di", "ini", "itu", "adalah"],
        "inggris": ["the", "is", "are", "and", "you", "this"]
    }
    
    teks = teks.lower()
    skor = {}
    
    for bahasa, kata_list in kamus.items():
        skor[bahasa] = 0
        for kata in kata_list:
            if kata in teks:
                skor[bahasa] = skor[bahasa] + 1
    
    terbaik = "indonesia"
    skor_terbaik = 0
    for bahasa, s in skor.items():
        if s > skor_terbaik:
            skor_terbaik = s
            terbaik = bahasa
    
    return terbaik

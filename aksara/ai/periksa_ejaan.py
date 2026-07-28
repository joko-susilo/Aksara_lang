def periksa_ejaan(teks):
    """Koreksi ejaan sederhana (kamus terbatas)"""
    koreksi = {
        "aq": "aku",
        "loe": "kamu",
        "gk": "tidak",
        "ga": "tidak",
        "yg": "yang",
        "dg": "dengan",
        "tp": "tetapi",
        "tdk": "tidak",
        "blm": "belum",
        "sdh": "sudah"
    }
    
    kata_list = teks.split(" ")
    hasil = []
    
    for kata in kata_list:
        if kata.lower() in koreksi:
            hasil.append(koreksi[kata.lower()])
        else:
            hasil.append(kata)
    
    return " ".join(hasil)

def ubah_gaya(teks, gaya):
    """Ubah gaya bahasa (santai, formal, gaul)"""
    kamus = {
        "santai": {"tidak": "gak", "saya": "gue", "kamu": "lo"},
        "formal": {"gak": "tidak", "gue": "saya", "lo": "Anda"},
        "gaul": {"tidak": "gak", "saya": "gw", "kamu": "lu", "bagus": "kece"}
    }
    
    if gaya not in kamus:
        return teks
    
    hasil = teks
    for lama, baru in kamus[gaya].items():
        hasil = hasil.replace(lama, baru)
    
    return hasil

def ekstrak_entitas(teks):
    """Ekstrak entitas (nama, tempat, angka) dari teks"""
    import re
    
    hasil = {
        "angka": [],
        "tempat": ["Jakarta", "Bandung", "Surabaya", "Medan", "Bali"],
        "nama": []
    }
    
    # Ekstrak angka
    angka_list = re.findall(r'\d+', teks)
    hasil["angka"] = [int(a) for a in angka_list]
    
    # Ekstrak tempat
    for tempat in hasil["tempat"]:
        if tempat.lower() in teks.lower():
            hasil["tempat"] = [tempat]
            break
    
    return hasil

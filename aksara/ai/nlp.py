def ringkas(teks, maks_kalimat=3):
    """Ringkasan teks sederhana berdasarkan kalimat terpenting"""
    # Pecah ke kalimat
    kalimat = teks.replace("!", ".").replace("?", ".").split(". ")
    kalimat = [k.strip() for k in kalimat if len(k.strip()) > 10]
    
    if len(kalimat) <= maks_kalimat:
        return teks
    
    # Hitung skor tiap kalimat (berdasarkan kata kunci)
    kata_penting = ["penting", "utama", "kunci", "hasil", "kesimpulan", "adalah", "yaitu", "dengan", "ini", "itu"]
    
    skor = []
    for k in kalimat:
        s = len(k)  # kalimat panjang = penting
        for kata in kata_penting:
            if kata in k.lower():
                s += 10  # bonus kata penting
        skor.append(s)
    
    # Ambil kalimat dengan skor tertinggi
    indeks_terbaik = sorted(range(len(skor)), key=lambda i: skor[i], reverse=True)[:maks_kalimat]
    indeks_terbaik.sort()
    
    hasil = ". ".join([kalimat[i] for i in indeks_terbaik]) + "."
    return hasil

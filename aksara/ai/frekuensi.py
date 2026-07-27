def frekuensi(data):
    """Hitung kemunculan setiap elemen dalam data"""
    hasil = {}
    for item in data:
        if item in hasil:
            hasil[item] = hasil[item] + 1
        else:
            hasil[item] = 1
    return hasil

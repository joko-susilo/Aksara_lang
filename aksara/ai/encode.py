def encode(data):
    """One-hot encoding sederhana"""
    # Ambil semua kategori unik
    kategori = []
    for item in data:
        if item not in kategori:
            kategori.append(item)
    
    # Encode setiap item
    hasil = []
    for item in data:
        encoded = []
        for k in kategori:
            if item == k:
                encoded.append(1)
            else:
                encoded.append(0)
        hasil.append(encoded)
    
    return {"kategori": kategori, "encoded": hasil}

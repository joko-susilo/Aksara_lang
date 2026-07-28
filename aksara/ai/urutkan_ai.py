def urutkan_ai(data):
    """Sorting cerdas (pilih metode terbaik)"""
    n = len(data)
    
    # Data kecil → bubble sort
    if n <= 10:
        for i in range(n):
            for j in range(n-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data
    
    # Data besar → quick sort sederhana
    if n <= 1:
        return data
    
    pivot = data[n//2]
    kiri = [x for x in data if x < pivot]
    tengah = [x for x in data if x == pivot]
    kanan = [x for x in data if x > pivot]
    
    return urutkan_ai(kiri) + tengah + urutkan_ai(kanan)

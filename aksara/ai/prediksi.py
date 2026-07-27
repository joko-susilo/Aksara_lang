def tebak(data_list):
    """Prediksi 2 angka selanjutnya dari deret (regresi linear sederhana)"""
    n = len(data_list)
    if n < 2:
        return data_list
    
    # Hitung rata-rata x dan y
    x_mean = sum(range(n)) / n
    y_mean = sum(data_list) / n
    
    # Hitung slope (w) dan intercept (b)
    num = sum((i - x_mean) * (data_list[i] - y_mean) for i in range(n))
    den = sum((i - x_mean) ** 2 for i in range(n))
    
    if den == 0:
        return [data_list[-1], data_list[-1]]
    
    w = num / den
    b = y_mean - w * x_mean
    
    # Prediksi 2 langkah ke depan
    hasil = [w * (n + i) + b for i in range(1, 3)]
    return [round(x, 2) for x in hasil]
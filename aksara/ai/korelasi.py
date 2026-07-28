import numpy as np

def korelasi(x, y):
    """Hitung korelasi Pearson antara dua variabel"""
    if len(x) != len(y) or len(x) < 2:
        return 0
    
    x = np.array(x)
    y = np.array(y)
    
    # Rumus Pearson
    n = len(x)
    atas = n * np.sum(x * y) - np.sum(x) * np.sum(y)
    bawah = np.sqrt((n * np.sum(x**2) - np.sum(x)**2) * (n * np.sum(y**2) - np.sum(y)**2))
    
    if bawah == 0:
        return 0
    
    return round(atas / bawah, 4)

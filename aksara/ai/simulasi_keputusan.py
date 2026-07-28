def simulasi_keputusan(kondisi, riwayat):
    """Simulasi keputusan berdasarkan riwayat"""
    if not riwayat:
        return "Tidak ada data"
    
    # Hitung probabilitas transisi sederhana
    transisi = {}
    for i in range(len(riwayat)-1):
        key = riwayat[i]
        if key not in transisi:
            transisi[key] = []
        transisi[key].append(riwayat[i+1])
    
    if kondisi in transisi:
        # Return opsi paling sering
        opsi = transisi[kondisi]
        return max(set(opsi), key=opsi.count)
    
    return "Tidak diketahui"

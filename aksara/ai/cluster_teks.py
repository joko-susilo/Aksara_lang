def cluster_teks(teks_list, jumlah):
    """Cluster teks berdasarkan kemiripan kata"""
    if len(teks_list) <= jumlah:
        return [[t] for t in teks_list]
    
    # Hitung skor kemiripan sederhana
    skor = {}
    for i, t1 in enumerate(teks_list):
        for j, t2 in enumerate(teks_list):
            if i < j:
                kata1 = set(t1.lower().split())
                kata2 = set(t2.lower().split())
                sama = len(kata1 & kata2)
                skor[(i, j)] = sama
    
    # Cluster sederhana
    clusters = []
    sudah = set()
    
    for i in range(len(teks_list)):
        if i not in sudah:
            cluster = [teks_list[i]]
            sudah.add(i)
            for j in range(i+1, len(teks_list)):
                if j not in sudah and skor.get((i, j), 0) > 0:
                    cluster.append(teks_list[j])
                    sudah.add(j)
            clusters.append(cluster)
    
    return clusters[:jumlah]

import math

def rangking_tfidf(dokumen, kueri):
    """TF-IDF ranking sederhana"""
    # Tokenisasi sederhana
    docs_token = [d.lower().split() for d in dokumen]
    kueri_token = kueri.lower().split()
    
    # Hitung TF
    skor = []
    for doc in docs_token:
        s = 0
        for kata in kueri_token:
            tf = doc.count(kata) / len(doc) if len(doc) > 0 else 0
            
            # IDF sederhana
            df = sum(1 for d in docs_token if kata in d)
            idf = math.log(len(docs_token) / (df + 1)) + 1
            
            s += tf * idf
        skor.append(round(s, 4))
    
    return skor

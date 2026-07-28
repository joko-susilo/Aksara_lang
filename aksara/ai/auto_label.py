def auto_label(data):
    """Auto labeling berdasarkan kata kunci"""
    label = []
    
    for teks in data:
        teks_lower = teks.lower()
        
        if "rusak" in teks_lower or "jelek" in teks_lower or "kecewa" in teks_lower:
            label.append("negatif")
        elif "bagus" in teks_lower or "keren" in teks_lower or "puas" in teks_lower:
            label.append("positif")
        else:
            label.append("netral")
    
    return label

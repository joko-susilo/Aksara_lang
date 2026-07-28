def rekomendasi(user_item, semua_data):
    """Rekomendasi item berdasarkan kemiripan user"""
    if user_item not in semua_data:
        return []
    
    user_items = semua_data[user_item]
    rekomendasi_list = []
    
    for user_lain, items in semua_data.items():
        if user_lain != user_item:
            for item in items:
                if item not in user_items and item not in rekomendasi_list:
                    rekomendasi_list.append(item)
    
    return rekomendasi_list[:5]

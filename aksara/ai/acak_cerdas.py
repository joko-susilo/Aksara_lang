import random

def acak_cerdas(data, bobot=None):
    """Random berbobot"""
    if bobot is None:
        return random.choice(data)
    
    total = sum(bobot)
    r = random.random() * total
    akumulasi = 0
    
    for i, item in enumerate(data):
        akumulasi = akumulasi + bobot[i]
        if r <= akumulasi:
            return item
    
    return data[-1]

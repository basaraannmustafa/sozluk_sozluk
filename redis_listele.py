from redis_baglanti import redis_baglan

def tum_kelimeleri_getir():
    r = redis_baglan()
    kelimeler = {}
    for key in r.keys('*'):
        kelimeler[key] = r.get(key)
    return kelimeler
    

from redis_baglanti import redis_baglan

def tum_kelimeleri_getir():
    r = redis_baglan()
    kelimeler = {}
    for key in r.keys('*'):
        kelimeler[key] = r.get(key)
    
    sirali_kelimeler = dict(sorted(kelimeler.items()))

    return sirali_kelimeler
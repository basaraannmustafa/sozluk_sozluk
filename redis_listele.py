from redis_baglanti import redis_baglan

def tum_kelimeleri_getir():
    r = redis_baglan()
    keys = r.keys('*')
    sozluk = {}
    for key in keys:
        sozluk[key] = r.get(key)
    return dict(sorted(sozluk.items()))

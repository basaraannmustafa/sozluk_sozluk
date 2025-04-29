from redis_baglanti import redis_baglan 

def tum_kelimeleri_getir():
    r = redis_baglan()
    kelimeler = {}

    for key in r.keys('*'):
        veri = r.hgetall(key)
        # Redis'ten gelen veriler bytes türündedir, decode edelim
        anlam = veri.get(b'anlam', b'').decode('utf-8')
        es_anlam = veri.get(b'es_anlamlar', b'').decode('utf-8')
        kelimeler[key.decode('utf-8')] = {
            "anlam": anlam,
            "es_anlamlar": es_anlam
        }

    sirali_kelimeler = dict(sorted(kelimeler.items()))
    return sirali_kelimeler

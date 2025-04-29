from redis_baglanti import redis_baglan

def tum_kelimeleri_getir():
    r = redis_baglan()
    kelimeler = {}

    for key in r.keys('*'):
        if r.type(key) != b'hash':  # 👈 sadece hash türünde olanları al
            continue
            
        veri = r.hgetall(key)
        anlam = veri.get(b'anlam', b'').decode('utf-8')
        es_anlam = veri.get(b'es_anlamlar', b'').decode('utf-8')
        orijinal = veri.get(b'orijinal', key).decode('utf-8')

        kelimeler[orijinal] = {
            "anlam": anlam,
            "es_anlamlar": es_anlam
        }


    sirali_kelimeler = dict(sorted(kelimeler.items()))
    return sirali_kelimeler

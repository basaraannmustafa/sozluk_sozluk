from redis_baglanti import redis_baglan

def kelime_sil(kelime):
    r = redis_baglan()
    return r.delete(kelime.strip().lower())  # Tüm keyler küçük harfle tutuluyor


from redis_baglanti import redis_baglan

def kelime_ekle(kelime, anlam):
    r = redis_baglan()
    r.set(kelime.capitalize(),
anlam.capitalize())
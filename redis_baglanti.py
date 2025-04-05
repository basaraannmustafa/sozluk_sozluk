import redis

def redis_baglan():
    r = redis.Redis(
        host="redis-13967.c300.eu-central-1-1.ec2.redislabs.cloud.com",
        port=13967,
        username="default",
        password="he7hSzA089lNcWBFRv4B62EY0S9rmOP2",
        decode_responses=True
    )
    return r

# redis_ekle.py
from redis_baglanti import redis_baglan

def kelime_ekle(kelime, anlam):
    r = redis_baglan()
    r.set(kelime.capitalize(), anlam.capitalize())

# redis_sil.py
from redis_baglanti import redis_baglan

def kelime_sil(kelime):
    r = redis_baglan()
    return r.delete(kelime.capitalize())  # Silerse 1 döner, bulamazsa 0

# redis_listele.py
from redis_baglanti import redis_baglan

def tum_kelimeleri_getir():
    r = redis_baglan()
    keys = r.keys('*')
    sozluk = {}
    for key in keys:
        sozluk[key] = r.get(key)
    return dict(sorted(sozluk.items()))

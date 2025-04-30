from redis_baglanti import redis_baglan

def kelime_ekle(kelime, anlam, es_anlamlar=None):
    r = redis_baglan()
    kelime_key = kelime.strip().lower()
    veri = {
        "orijinal": kelime.strip(),
        "anlam": anlam.strip().capitalize(),
        "es_anlamlar": ", ".join(es_anlamlar or [])
    }
    r.hset(kelime_key, mapping=veri)

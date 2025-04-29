from redis_baglanti import redis_baglan

def kelime_ekle(kelime, anlam, es_anlamlar=None):
    r = redis_baglan()
    kelime_key = kelime.lower()
    veri = {
        "anlam": anlam.capitalize()
    }

    if es_anlamlar:
        veri["es_anlamlar"] = ", ".join(es_anlamlar)

    r.hset(kelime_key, mapping=veri)

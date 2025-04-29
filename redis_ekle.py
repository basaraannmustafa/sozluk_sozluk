def kelime_ekle(kelime, anlam, es_anlamlar=None):
    r = redis_baglan()
    kelime_key = kelime.lower()  # Anahtar her zaman küçük
    veri = {
        "orijinal": kelime,  # Kullanıcının girdiği gibi sakla
        "anlam": anlam.capitalize()
    }
    if es_anlamlar:
        veri["es_anlamlar"] = ", ".join(es_anlamlar)
    r.hset(kelime_key, mapping=veri)

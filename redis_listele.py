from redis_baglanti import redis_baglan

def tum_kelimeleri_getir():
    r = redis_baglan()
    kelimeler = {}

    for key in r.keys('*'):
        try:
            if r.type(key) != b'hash':
                continue

            # Veri alınıyor
            veri = r.hgetall(key)
            anlam = veri.get(b'anlam', b'').decode('utf-8').strip()
            es_anlam = veri.get(b'es_anlamlar', b'').decode('utf-8').strip()
            orijinal = veri.get(b'orijinal', key).decode('utf-8').strip()

            # Önemli nokta burası: Hem küçük hem orijinal kelimeler eşleniyor
            kelimeler[orijinal.lower()] = {
                "anlam": anlam,
                "es_anlamlar": es_anlam,
                "orijinal": orijinal
            }

        except Exception as e:
            print(f"Hata ({key}): {e}")
            continue

    # Alfabetik olarak orijinal değerleri sıralayıp döndürelim
    sirali_kelimeler = dict(sorted(kelimeler.items(), key=lambda x: x[1]['orijinal'].lower()))
    return sirali_kelimeler

from redis_baglanti import redis_baglan

def eski_verileri_donustur():
    r = redis_baglan()
    donusen = 0
    atlanan = 0

    for key in r.keys('*'):
        key_type = r.type(key)
        
        if key_type == b'string':
            try:
                anlam = r.get(key).decode('utf-8')
                key_str = key.decode('utf-8')

                # Eğer bu key zaten hash'e dönüştürülmüşse atla
                if r.exists(key_str) and r.type(key_str) == b'hash':
                    atlanan += 1
                    continue

                # Yeni formatta hash olarak ekle
                r.hset(key_str, mapping={
                    "orijinal": key_str.capitalize(),
                    "anlam": anlam,
                    "es_anlamlar": ""
                })

                # Eski string veriyi sil
                r.delete(key_str)

                donusen += 1
            except Exception as e:
                print(f"Hata ({key}):", e)
                continue

    print(f"✅ {donusen} kelime dönüştürüldü.")
    print(f"⚠️ {atlanan} kelime zaten hash formatında olduğu için atlandı.")

if __name__ == "__main__":
    eski_verileri_donustur()

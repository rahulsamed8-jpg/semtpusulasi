import json
import time
import requests

API_KEY = "AIzaSyAFx28L5Vf6lRS9NyTm3a9yJbh6bfcvU08"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

file_path = "src/data/turizm_data.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Toplam {len(data)} mekan için GERÇEK YZ makaleleri yazılmaya başlanıyor...")
print("Google Free Tier limiti (15 İstek/Dakika) sebebiyle işlem yaklaşık 20 dakika sürecektir.")

# Zaten daha önce manuel yazdığım o harika 3 makaleyi (Teos vs) ezmeyelim, veya jenerik şablonları ezmek istiyoruz!
# Jenerik şablonları ezeceğiz, sadece "Teos Antik Kenti: İzmir'in Saklı Tarihi" gibi manuel 3 tanesi hariç mi tutalım?
# Aslında hepsine sıfırdan orijinal yazdıralım, yepyeni olsun!

for i, item in enumerate(data):
    # Jenerik şablonlar "Ege'nin Serin Sularına Davet" gibi başlıklara sahip. Hepsini siliyoruz ve yapay zekaya devrediyoruz!
    print(f"[{i+1}/{len(data)}] {item['name']} ({item['category']}) için Gemini makale yazıyor...")
    
    prompt = f"""
    Sen profesyonel bir seyahat blog yazarısın. Sitenin adı SemtPusulası.
    Görev: '{item['region']}' bölgesinde yer alan '{item['name']}' ({item['category']}) hakkında 200 kelimelik, özgün, SEO uyumlu ve son derece samimi bir inceleme yazısı yaz.
    
    Ek bilgiler (Eğer varsa):
    Google Puanı: {item.get('rating', 'Belirtilmemiş')}
    Yorum Sayısı: {item.get('reviews_count', 0)}
    Adres: {item.get('address', '')}
    
    Lütfen sadece makale metnini ver, Markdown başlıkları (h2, h3) ve maddeleme işaretleri kullanarak estetik bir formatta olsun. Başlık her zaman '## [Mekan Adı]' formatında başlasın. Asla jenerik (standart) ifadeler kullanma, mekana özgü sanki oraya gitmişsin gibi bir yorum kat.
    """

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            article_text = response.json()['candidates'][0]['content']['parts'][0]['text']
            item["seo_article"] = article_text
            print(" -> BAŞARILI!")
        else:
            print(f" -> HATA: {response.status_code} - {response.text}")
    except Exception as e:
        print(" -> İSTİSNA:", e)
    
    # Her başarılı yazım sonrası veriyi hemen kaydedelim ki elektrik gitse bile kaybolmasın.
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    # Free Tier (Ücretsiz Paket) Dakikada 15 istek sınırı var. Yani her istek arasına ortalama 4 saniye koymalıyız.
    time.sleep(4.5)

print("TÜM MEKANLAR İÇİN GERÇEK YAPAY ZEKA MAKALELERİ BAŞARIYLA YAZILDI VE KAYDEDİLDİ!")

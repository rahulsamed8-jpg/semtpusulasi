import json
import time
from google import genai
import os

API_KEY = "AQ.Ab8RN6JYv4NGTmFA59aHiWlY4hrAtXR0pYIUG_SJsop0977gzQ"
client = genai.Client(api_key=API_KEY)

file_path = "turizm_data.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Toplam {len(data)} mekan için SEO makaleleri yazılıyor...")

for i, item in enumerate(data):
    if "seo_article" in item and item["seo_article"]:
        print(f"[{i+1}/{len(data)}] {item['name']} zaten yazılmış, atlanıyor.")
        continue

    print(f"[{i+1}/{len(data)}] {item['name']} için Gemini makale yazıyor...")
    
    prompt = f"""
    Sen profesyonel bir seyahat blog yazarısın. 
    Bana {item['region']} bölgesindeki {item['name']} ({item['category']}) hakkında SEO uyumlu, 
    okuyucuyu içine çeken, çok samimi bir dille yaklaşık 300 kelimelik bir rehber yaz.
    
    Mekanın Google puanı: {item['rating']}. 
    
    Makalede sadece metin olsun, Markdown formatında başlıklar (h2, h3) kullanabilirsin. 
    Sitenin adı 'SemtPusulası'. 
    """

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        item["seo_article"] = response.text
        print(" -> Başarılı!")
    except Exception as e:
        print(" -> HATA:", e)
    
    # API limitine takılmamak için kısa bir bekleme
    time.sleep(2)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Tüm SEO makaleleri turizm_data.json dosyasına başarıyla kaydedildi!")

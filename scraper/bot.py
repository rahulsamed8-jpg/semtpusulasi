import os
import json
import requests
import time
from dotenv import load_dotenv

# .env dosyasından API anahtarını yükle
load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

# Hedef bölgeler ve nişler
REGIONS = ["Seferihisar Merkez", "Sığacık", "Ürkmez", "Akarca", "Doğanbey", "Özdere", "Gümüldür"]
CATEGORIES = ["Gezilecek Yerler", "Plajlar", "Mekanlar", "Oteller", "Pansiyonlar"]

def search_places(query):
    """Google Places API Text Search kullanarak mekanları bulur."""
    print(f"[{query}] aranıyor...")
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": API_KEY,
        "language": "tr"
    }
    
    places = []
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("status") == "OK":
            places.extend(data.get("results", []))
            # Sadece ilk sayfayı alıyoruz şimdilik (test için)
        else:
            print(f"Hata: {data.get('status')} - {data.get('error_message', '')}")
            
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        
    return places

def get_place_details(place_id):
    """Mekanın detaylarını (fotoğraflar, yorumlar, adres) çeker."""
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,geometry,rating,user_ratings_total,photos,reviews,website,formatted_phone_number,url",
        "key": API_KEY,
        "language": "tr"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("status") == "OK":
            return data.get("result", {})
    except Exception as e:
        print(f"Detay çekme hatası: {e}")
        
    return None

def get_photo_url(photo_reference, max_width=800):
    """Fotoğraf referansından gerçek resim URL'si oluşturur."""
    if not photo_reference:
        return None
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photo_reference={photo_reference}&key={API_KEY}"

def generate_slug(text, location):
    """SEO uyumlu URL (slug) üretir."""
    import re
    import unicodedata
    
    # Türkçe karakterleri dönüştür
    text = text.replace('ı', 'i').replace('I', 'i')
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    location = location.replace('ı', 'i').replace('I', 'i')
    location = unicodedata.normalize('NFKD', location).encode('ascii', 'ignore').decode('utf-8')
    
    combined = f"{text} {location}"
    combined = combined.lower()
    combined = re.sub(r'[^a-z0-9\s-]', '', combined)
    combined = re.sub(r'[\s-]+', '-', combined).strip('-')
    return combined

def main():
    if not API_KEY:
        print("HATA: .env dosyasında GOOGLE_PLACES_API_KEY bulunamadı!")
        return

    print("--- Python Turizm Botu Başlıyor (TAM SÜRÜM) ---")
    all_data = []
    
    # Tüm bölge ve kategorilerde dönelim
    for region in REGIONS:
        for category in CATEGORIES:
            query = f"{region} {category}"
            results = search_places(query)
            
            print(f"{query} için {len(results)} mekan bulundu. Detaylar çekiliyor...")
            
            # Her kategori/bölge için en popüler 10 mekanı alalım (Çok fazla API harcamamak için)
            for place in results[:10]:
                place_id = place.get("place_id")
                name = place.get("name")
                
                details = get_place_details(place_id)
                if not details:
                    continue
                    
                # Fotoğraf URL'lerini oluştur
                photos = []
                for photo in details.get("photos", [])[:3]: # İlk 3 fotoğraf
                    photo_url = get_photo_url(photo.get("photo_reference"))
                    if photo_url:
                        photos.append(photo_url)
                        
                # Veriyi hazırla
                item = {
                    "slug": generate_slug(name, region),
                    "name": name,
                    "region": region,
                    "category": category,
                    "address": details.get("formatted_address", ""),
                    "rating": details.get("rating", 0),
                    "reviews_count": details.get("user_ratings_total", 0),
                    "phone": details.get("formatted_phone_number", ""),
                    "website": details.get("website", ""),
                    "google_maps_url": details.get("url", ""),
                    "photos": photos,
                    # Koordinatlar
                    "location": {
                        "lat": details.get("geometry", {}).get("location", {}).get("lat"),
                        "lng": details.get("geometry", {}).get("location", {}).get("lng")
                    }
                }
                
                all_data.append(item)
                print(f"Başarıyla Çekildi: {name} ({category})")
                time.sleep(0.5) # API'yi çok yormamak için bekleme
                
    # Doğrudan Astro'nun data klasörüne kaydet
    output_file = "../frontend/src/data/turizm_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)
        
    print(f"--- İşlem Tamamlandı! Toplam {len(all_data)} mekan {output_file} dosyasına kaydedildi ---")

if __name__ == "__main__":
    main()

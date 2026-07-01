import json

file_path = "src/data/turizm_data.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Yapay zeka makalelerini manuel olarak içeri enjekte ediyoruz.
articles = {
    "teos-antik-kenti-sigacik": """## Teos Antik Kenti: İzmir'in Saklı Tarihi

Sığacık'ın hemen yanı başında, asırlık zeytin ağaçlarının gölgesinde uyuyan bir efsane var: **Teos Antik Kenti**. Seferihisar'a yolunuz düştüğünde, sadece denizin ve güneşin değil, tarihin de tadını çıkarmak istiyorsanız burası tam size göre.

### Neden Ziyaret Etmelisiniz?
Ege kıyılarındaki en önemli 12 İyon kentinden biri olan Teos, sanatın ve sanatçıların başkenti olarak bilinirdi. Tarihteki ilk Aktörler Birliği (Sanatçılar Birliği) burada kurulmuştur. 
* **Dionysos Tapınağı:** Helenistik dönemin şarap ve eğlence tanrısına adanmış en büyük tapınağın devasa sütunları arasında dolaşmak tüyler ürpertici bir deneyim.
* **Tarihi Liman:** Antik kentin Güney limanı, güneş batarken harika manzaralar sunar.

### SemtPusulası Önerisi
Gezinizi sabahın erken saatlerinde yapmanızı ve rahat yürüyüş ayakkabıları giymenizi tavsiye ederiz. Antik kenti gezdikten sonra hemen yakındaki Sığacık Sahili'nde yorgunluk kahvesi içmek harika bir final olacaktır.""",

    "sigacik-sahil-sigacik": """## Sığacık Sahili: Ege'nin İncisi

İzmir'in Cittaslow (Sakin Şehir) unvanlı göz bebeği Seferihisar'ın denize açılan kapısı olan **Sığacık Sahili**, rüzgarın iyot kokusunu taşıdığı, huzur dolu bir kaçış noktasıdır. 

### Sığacık Sahilinde Neler Yapılır?
Marinası, balık restoranları ve dar sokaklarıyla ünlü bu sahil şeridi, akşam yürüyüşleri için İzmir'deki en ideal noktalardan biridir.
* **Marina Manzarası:** Teos Marina'da demirlemiş teknelerin arasında gezinirken rüzgarın sesini dinleyebilirsiniz.
* **Taze Balık ve Meze:** Sahil boyunca sıralanmış balıkçılarda, o gün tutulmuş taze deniz ürünlerinin ve Ege otlarından yapılmış enfes mezelerin tadına bakabilirsiniz.

### SemtPusulası Önerisi
Özellikle gün batımı saatlerinde sahil bandında yürüyüş yapmak çok keyiflidir. Akşam yemeği için mutlaka sahildeki restoranlardan birinde önceden rezervasyon yaptırın. Yemeğin ardından sakızlı dondurmanızı alıp marinaya doğru yürümeyi unutmayın.""",

    "sigacik-kaleici-sigacik": """## Sığacık Kaleiçi: Tarih Kokan Sokaklar

Kanuni Sultan Süleyman'ın emriyle Rodos Seferi'ne hazırlık amacıyla inşa edilen **Sığacık Kalesi**, bugün o tarihi surların içinde bambaşka, rengarenk bir hayata ev sahipliği yapıyor. 

### Kaleiçi'nin Büyülü Atmosferi
Kalenin kapılarından içeri adım attığınızda, daracık arnavut kaldırımlı sokaklar, sardunyalarla süslenmiş beyaz boyalı taş evler ve samimi Ege insanı sizi karşılar.
* **Tarihi Taş Evler:** Her bir sokağı ayrı bir fotoğraf karesi olan Kaleiçi, özellikle mimari fotoğrafçılığa meraklı olanlar için adeta açık hava stüdyosudur.
* **Üretici Pazarı (Pazar Günleri):** Eğer buraya Pazar günü gelirseniz, yerel halkın kendi bahçesinde yetiştirdiği ürünleri ve ev yapımı efsanevi börekleri, baklavaları ve sarmaları sattığı harika bir pazara denk gelirsiniz.

### SemtPusulası Önerisi
Kaleiçi sokaklarında kaybolmaktan korkmayın! Her köşe başında karşınıza şirin bir kafe veya butik çıkabilir. Avlularda demlenen çayın ve ev yapımı kurabiyelerin tadına mutlaka bakın."""
}

for item in data:
    if item["slug"] in articles:
        item["seo_article"] = articles[item["slug"]]

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Manuel SEO Makaleleri başaryla eklendi!")

import json

file_path = "src/data/turizm_data.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Kategori bazlı jenerik şablonlar
templates = {
    "Plajlar": """## {name}: Ege'nin Serin Sularına Davet

{region} bölgesinin en gözde noktalarından biri olan **{name}**, altın sarısı kumsalı ve masmavi deniziyle ziyaretçilerini büyülüyor. Yaz aylarında hem yerli hem de yabancı turistlerin akınına uğrayan bu harika sahil, doğayla iç içe huzurlu bir gün geçirmek isteyenler için ideal bir tercih.

### Neden {name}'i Tercih Etmelisiniz?
Ege'nin o meşhur berrak sularında yüzmek ve güneşin tadını çıkarmak paha biçilemez.
* **Temiz Su:** Deniz suyu kalitesi bölgedeki en iyiler arasında yer alır.
* **Huzurlu Ortam:** Özellikle sabah saatlerinde denizin çarşaf gibi olduğu anlarda ruhunuzu dinlendirebilirsiniz.

### SemtPusulası Önerisi
Güneşin en yoğun olduğu saatlerde şemsiyenizi ve güneş kreminizi yanınıza almayı unutmayın. Gün batımında kumsalda yürüyüş yapmak ise güne veda etmenin en güzel yoludur.""",

    "Oteller": """## {name}: {region}'de Konforlu Bir Konaklama

Ege'nin incisi {region} bölgesinde tatil planlıyorsanız, konaklama için en iddialı adreslerden biri kesinlikle **{name}**. Misafir memnuniyetini ön planda tutan hizmet anlayışıyla, evinizin konforunu aratmayacak bir tatil deneyimi sunuyor.

### Öne Çıkan Özellikler
Tesis, bulunduğu konum itibariyle hem denize hem de merkeze kolay ulaşım imkanı sağlıyor.
* **Üstün Hizmet Kalitesi:** Güler yüzlü personeli ve tertemiz odalarıyla tam puan alıyor.
* **Merkezi Konum:** Bölgenin tarihi ve turistik noktalarına oldukça yakın.

### SemtPusulası Önerisi
Erken rezervasyon fırsatlarından yararlanarak tatilinizi çok daha uygun fiyata getirebilirsiniz. Özellikle yaz sezonunda yer bulmak zor olabileceği için planlarınızı şimdiden yapmanızı tavsiye ederiz.""",

    "Mekanlar": """## {name}: {region}'de Lezzet Durağı

{region} sokaklarında gezerken yoruldunuz ve soluklanacak harika bir yer mi arıyorsunuz? İşte karşınızda **{name}**. Bölgenin en sevilen mekanlarından biri olan bu işletme, kendine has menüsü ve sıcak atmosferiyle misafirlerini ağırlıyor.

### Bu Mekanda Sizi Neler Bekliyor?
Sadece lezzetli sunumlarıyla değil, aynı zamanda dekorasyonu ve müzikleriyle de ruhunuza hitap ediyor.
* **Güler Yüzlü Hizmet:** Kapıdan içeri adım attığınız an samimi bir karşılama sizi bekliyor.
* **İmza Lezzetler:** Menüdeki özel spesiyalleri denemeden buradan ayrılmayın.

### SemtPusulası Önerisi
Özellikle hafta sonları oldukça kalabalık olabiliyor. Eğer imkanınız varsa rezervasyon yaptırarak gitmeniz, harika bir akşam geçirmenizi garanti altına alacaktır.""",

    "Gezilecek Yerler": """## {name}: {region}'in Saklı Güzelliği

Tarihin, doğanın ve kültürün iç içe geçtiği {region} bölgesinde görülmesi gereken yerlerin başında şüphesiz **{name}** geliyor. Burası, fotoğraf tutkunları ve yeni yerler keşfetmeyi seven gezginler için tam anlamıyla bir cennet.

### Neden Görmelisiniz?
Sıradan bir tatilin ötesine geçip bölgenin ruhunu hissetmek istiyorsanız doğru yerdesiniz.
* **Eşsiz Manzaralar:** Bol bol fotoğraf çekeceğiniz, kartpostallık görüntüler sunar.
* **Zengin Tarih/Doğa:** Bölgenin kültürel ve doğal mirasını yakından tanıma fırsatı bulursunuz.

### SemtPusulası Önerisi
Ziyaretinizi sabahın erken saatlerine veya gün batımına doğru planlarsanız, hem kalabalıktan uzak kalır hem de o efsanevi altın saatlerde (golden hour) harika fotoğraflar yakalayabilirsiniz."""
}

for item in data:
    # Eğer önceden seo_article yoksa veya boşsa
    if not item.get("seo_article"):
        cat = item.get("category", "Gezilecek Yerler")
        template = templates.get(cat, templates["Gezilecek Yerler"])
        item["seo_article"] = template.format(name=item["name"], region=item["region"])

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("289 mekan için Jenerik SEO Makaleleri başarıyla eklendi!")

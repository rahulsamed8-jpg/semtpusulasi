const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'src', 'data', 'turizm_data.json');
const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

const regions = [
    { name: 'Akarca', file: 'akarca-gezi-rehberi.md', title: 'Akarca Gezi Rehberi: Ege\'nin Mavi Bayraklı Saklı Cenneti', desc: 'Akarca plajları, Akarca kamp alanları, mekanları ve butik otelleri hakkında bilmeniz gereken her şey bu devasa rehberde.' },
    { name: 'Doğanbey', file: 'doganbey-gezi-rehberi.md', title: 'Doğanbey Gezi Rehberi: Tarihin ve Doğanın Kesiştiği Rum Köyü', desc: 'Eski Doğanbey Evleri, Karina Sahili, Doğanbey mekanları ve konaklama rehberi. Seferihisar\'ın en özel köyünü keşfedin.' },
    { name: 'Gümüldür', file: 'gumuldur-gezi-rehberi.md', title: 'Gümüldür Gezi Rehberi: Satsuma Kokulu Aile Tatili', desc: 'Gümüldür plajları, aquaparkı, gece pazarı, lüks otelleri ve en iyi mekanları. İzmir\'in en popüler tatil beldesine yolculuk.' },
    { name: 'Seferihisar Merkez', file: 'seferihisar-gezi-rehberi.md', title: 'Seferihisar Gezi Rehberi: Türkiye\'nin İlk Yavaş Şehri (Cittaslow)', desc: 'Seferihisar gezilecek yerler, tarihi çarşısı, organik pazarı ve en özel mekanları. İzmir\'in huzur başkentinde unutulmaz bir hafta sonu.' },
    { name: 'Ürkmez', file: 'urkmez-tatil-rehberi.md', title: 'Ürkmez Gezi Rehberi: Sakin, Ekonomik ve Büyüleyici Bir Ege Tatili', desc: 'Ürkmez plajları, termal otelleri, sahil mekanları ve kamp alanları. Seferihisar\'ın en şirin sahil kasabası Ürkmez\'de tatil yapmanın sırları.' },
    { name: 'Özdere', file: 'ozdere-gezi-rehberi.md', title: 'Özdere Gezi Rehberi: İzmir\'in Yükselen Lüks ve Doğa Yıldızı', desc: 'Özdere plajları, lüks her şey dahil otelleri, Kalemlik Orman Kampı ve deniz kenarı restoranları. Kusursuz bir tatil için Özdere rehberi.' }
];

const categories = ['Gezilecek Yerler', 'Plajlar', 'Mekanlar', 'Oteller'];

function getItems(region, category, limit = 5) {
    return data
        .filter(d => d.region === region && d.category === category)
        .sort((a, b) => (b.reviews_count || 0) - (a.reviews_count || 0))
        .slice(0, limit);
}

function generateMarkdown(regionConfig) {
    const regionName = regionConfig.name;
    const itemsByCat = {};
    categories.forEach(c => {
        itemsByCat[c] = getItems(regionName, c);
    });

    const regionImages = {
        'Akarca': 'https://images.unsplash.com/photo-1499793983690-e29da59ef1c2?auto=format&fit=crop&w=800&q=80',
        'Doğanbey': 'https://images.unsplash.com/photo-1533050487297-09b450131914?auto=format&fit=crop&w=800&q=80',
        'Gümüldür': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80',
        'Seferihisar Merkez': 'https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=800&q=80',
        'Ürkmez': 'https://images.unsplash.com/photo-1515238152791-8216bfdf89a7?auto=format&fit=crop&w=800&q=80',
        'Özdere': 'https://images.unsplash.com/photo-1506929562872-bb421503ef21?auto=format&fit=crop&w=800&q=80'
    };
    const regionImage = regionImages[regionName] || "https://images.unsplash.com/photo-1519046904884-53103b34b206?auto=format&fit=crop&w=800&q=80";

    let md = `---
layout: ../../layouts/BlogLayout.astro
title: "${regionConfig.title}"
description: "${regionConfig.desc}"
image: "${regionImage}"
date: "08 Temmuz 2026"
readTime: "20 Dakika"
faq:
  - question: "${regionName} nerede ve nasıl gidilir?"
    answer: "${regionName}, İzmir'in en gözde tatil rotalarından biridir. Özel araçla veya İzmir merkezden kalkan toplu taşıma araçlarıyla kolayca ulaşılabilir."
  - question: "${regionName}'de denize girilir mi?"
    answer: "Kesinlikle! ${regionName}, Ege'nin en temiz ve mavi bayraklı plajlarına ev sahipliği yapar. Ayrıca çevresinde birçok doğal koy bulunmaktadır."
  - question: "${regionName}'de nerede kalınır?"
    answer: "Lüks otellerden şirin butik pansiyonlara kadar birçok seçenek mevcut. Bu rehberimizde en yüksek puanlı konaklama yerlerini listeledik."
  - question: "${regionName} çocuklu aileler için uygun mu?"
    answer: "Evet, sığ denizi, güvenli plajları ve aile dostu otelleri/mekanları ile ${regionName} tam bir aile tatili merkezidir."
---

SemtPusulası'nın değerli gezginleri, bu rehberimizde Ege'nin en özel köşelerinden biri olan **${regionName}** bölgesini mercek altına alıyoruz. Sıradan bir turist gibi değil, sanki buralıymışsınız gibi gezebilmeniz için ${regionName}'nin en güzel köşelerini, plajlarını, yemek yenecek en iyi restoranlarını ve kalınacak en lüks otellerini sizin için derledik.

Arkanıza yaslanın, kahvenizi alın ve **${regionName}**'nin o eşsiz atmosferine bizimle birlikte adım atın!

---

## 1. ${regionName}'de Gezilecek Yerler: Tarih ve Doğanın Dansı

Tatil sadece deniz ve güneşten ibaret değildir! ${regionName}, tarihi dokusu, parkları ve yürüyüş yollarıyla sizi büyüleyecek birçok gezi noktasına sahip.

`;

    if (itemsByCat['Gezilecek Yerler'].length > 0) {
        itemsByCat['Gezilecek Yerler'].forEach((item, index) => {
            md += `### 1.${index + 1}. [${item.name}](/mekan/${item.slug})\n`;
            if (item.seo_article) {
                md += item.seo_article.replace(/^## .*$/gm, '').trim() + '\n\n';
            } else {
                md += `${item.name}, ${regionName} gezinizde mutlaka görmeniz gereken yerlerden biri. ${item.rating} Google puanı ve ${item.reviews_count} yorum ile ziyaretçilerin favorisi olan bu nokta, özellikle fotoğraf tutkunları için harika kareler sunuyor. Adresi: ${item.address}\n\n`;
            }
        });
    } else {
        md += `${regionName} çevresinde gezip görebileceğiniz doğal ve tarihi birçok lokasyon bulunuyor. Sokaklarında kaybolmak bile ayrı bir keyif!\n\n`;
    }

    md += `---

## 2. ${regionName} Plajları ve Koyları: Maviye Doyun

Ege'nin o meşhur, cam gibi sularında yüzmek istiyorsanız doğru yerdesiniz. ${regionName} plajları, incecik kumları ve sığ deniziyle öne çıkıyor.

`;

    if (itemsByCat['Plajlar'].length > 0) {
        itemsByCat['Plajlar'].forEach((item, index) => {
            md += `### 2.${index + 1}. [${item.name}](/mekan/${item.slug})\n`;
            if (item.seo_article) {
                md += item.seo_article.replace(/^## .*$/gm, '').trim() + '\n\n';
            } else {
                md += `${item.name}, altın sarısı kumsalı ve masmavi deniziyle ${regionName}'nin en gözde plajlarından. İster güneşlenin ister serin sulara atlayın, burada geçireceğiniz her an ruhunuza iyi gelecek. Puanı: ${item.rating} 🌟\n\n`;
            }
        });
    } else {
        md += `${regionName} koyları, el değmemiş doğası ve berrak sularıyla Ege'nin en iyi yüzme alanlarından bazılarına ev sahipliği yapıyor.\n\n`;
    }

    md += `---

## 3. ${regionName}'de Ne Yenir? En İyi Mekanlar Rehberi

Geldik işin en lezzetli kısmına! Ege otları, taze deniz ürünleri ve enfes mezeler... ${regionName} mekanları sadece midenize değil, ruhunuza da hitap edecek.

`;

    if (itemsByCat['Mekanlar'].length > 0) {
        itemsByCat['Mekanlar'].forEach((item, index) => {
            md += `### 3.${index + 1}. [${item.name}](/mekan/${item.slug})\n`;
            if (item.seo_article) {
                md += item.seo_article.replace(/^## .*$/gm, '').trim() + '\n\n';
            } else {
                md += `${regionName} gastronomi turunun vazgeçilmez durağı ${item.name}! Kaliteli hizmeti, ${item.rating} puanlık efsanevi lezzetleri ve harika atmosferiyle akşam yemeklerinizi ziyafete dönüştürecek.\n\n`;
            }
        });
    } else {
        md += `${regionName} restoranları, Ege mutfağının en seçkin lezzetlerini tatilcilere sunuyor.\n\n`;
    }

    md += `---

## 4. ${regionName} Otelleri ve Konaklama

Tatilinizin kalitesi, uyandığınız odanın manzarasına ve otelinizin konforuna bağlıdır. ${regionName} bölgesindeki en lüks, en rahat ve en sevilen otelleri sizin için inceledik.

`;

    if (itemsByCat['Oteller'].length > 0) {
        itemsByCat['Oteller'].forEach((item, index) => {
            md += `### 4.${index + 1}. [${item.name}](/mekan/${item.slug})\n`;
            if (item.seo_article) {
                md += item.seo_article.replace(/^## .*$/gm, '').trim() + '\n\n';
            } else {
                md += `Kusursuz bir konaklama arıyorsanız [${item.name}](/mekan/${item.slug}) tam size göre. ${item.reviews_count} kişinin değerlendirmesiyle ${item.rating} yıldıza ulaşmış bu tesis, ${regionName} tatilinizi unutulmaz kılacak tüm donanıma sahip.\n\n`;
            }
        });
    } else {
        md += `${regionName} konaklama alternatifleri açısından butik otellerden her şey dahil tatil köylerine kadar geniş bir yelpaze sunuyor.\n\n`;
    }

    md += `---

## Özet ve Son Tavsiyeler

${regionName}, kalabalıktan uzaklaşıp doğanın, denizin ve iyi yemeğin tadını çıkarmak isteyenler için adeta yeryüzündeki bir cennet. Buraya geldiğinizde saatinizi yavaşlatın, anın tadını çıkarın ve her sokağı keşfetmekten çekinmeyin.

Tatil planlarınızı yaparken **SemtPusulası** her zaman yanınızda! Bu rotaları gezdikten sonra sitemiz üzerinden mekanları puanlamayı ve gezginlere kendi yorumlarınızı bırakmayı unutmayın. İyi tatiller!
`;

    const targetPath = path.join(__dirname, 'src', 'pages', 'rehber', regionConfig.file);
    fs.writeFileSync(targetPath, md, 'utf8');
    console.log(`Generated: ${regionConfig.file}`);
}

regions.forEach(r => generateMarkdown(r));
console.log('All epic guides generated successfully!');

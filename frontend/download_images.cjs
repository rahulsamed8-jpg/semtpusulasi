const fs = require('fs');
const path = require('path');
const axios = require('axios');
const sharp = require('sharp');

const DATA_FILE = path.join(__dirname, 'src', 'data', 'turizm_data.json');
const IMAGES_DIR = path.join(__dirname, 'public', 'images', 'places');

// Klasör yoksa oluştur
if (!fs.existsSync(IMAGES_DIR)) {
    fs.mkdirSync(IMAGES_DIR, { recursive: true });
}

async function downloadAndConvert() {
    console.log('Başlıyor... Veri okunuyor...');
    let data = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    let downloadedCount = 0;
    let failedCount = 0;

    for (let i = 0; i < data.length; i++) {
        const place = data[i];
        if (!place.photos || place.photos.length === 0) continue;

        const newPhotos = [];
        
        for (let j = 0; j < place.photos.length; j++) {
            const photoUrl = place.photos[j];
            
            // Zaten indirilmiş lokal bir resimse geç
            if (!photoUrl.includes('googleapis.com')) {
                newPhotos.push(photoUrl);
                continue;
            }

            const fileName = `${place.slug || 'place-' + i}-${j}.webp`;
            const filePath = path.join(IMAGES_DIR, fileName);
            const publicPath = `/images/places/${fileName}`;

            try {
                // Önceden indirilmişse atla
                if (fs.existsSync(filePath)) {
                    newPhotos.push(publicPath);
                    continue;
                }

                console.log(`İndiriliyor [${i}/${data.length}]: ${place.name} - Fotoğraf ${j+1}`);
                
                const response = await axios({
                    url: photoUrl,
                    method: 'GET',
                    responseType: 'arraybuffer',
                    timeout: 10000 // 10 saniye zaman aşımı
                });

                await sharp(response.data)
                    .webp({ quality: 80 })
                    .toFile(filePath);

                newPhotos.push(publicPath);
                downloadedCount++;
            } catch (error) {
                console.error(`❌ Hata: ${place.name} fotoğrafı indirilemedi. Sebep: ${error.message}`);
                failedCount++;
                // Hata alırsak orijinal URL'yi tutup devam edebiliriz veya kırık resmi silebiliriz.
                // Kotalardan vs. patlarsa diye orijinal URL'yi bırakalım şimdilik.
                newPhotos.push(photoUrl); 
            }
            
            // Google API'ye art arda hızlı istek atıp banlanmamak için küçük bir bekleme
            await new Promise(resolve => setTimeout(resolve, 300));
        }

        // Güncellenmiş fotoğraf dizisini kaydet
        data[i].photos = newPhotos;
    }

    // Veritabanını güncelle
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
    console.log(`\n✅ İşlem Tamamlandı!`);
    console.log(`📥 İndirilen ve dönüştürülen: ${downloadedCount}`);
    console.log(`❌ Hata alınan: ${failedCount}`);
}

downloadAndConvert().catch(console.error);

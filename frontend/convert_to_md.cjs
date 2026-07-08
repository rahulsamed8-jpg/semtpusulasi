const fs = require('fs');
const path = require('path');

const dataFile = path.join(__dirname, 'src/data/turizm_data.json');
const contentDir = path.join(__dirname, 'src/content/mekanlar');

// Koleksiyon dizinini oluştur (yoksa)
if (!fs.existsSync(contentDir)) {
    fs.mkdirSync(contentDir, { recursive: true });
}

// JSON verisini oku
const rawData = fs.readFileSync(dataFile, 'utf8');
const jsonData = JSON.parse(rawData);

const places = jsonData.places || [];

places.forEach(place => {
    const { seo_article, slug, ...frontmatter } = place;

    // Frontmatter'ı YAML formatına çevir
    let yamlFrontmatter = `---\n`;
    yamlFrontmatter += `title: "${frontmatter.name.replace(/"/g, '\\"')}"\n`;
    yamlFrontmatter += `region: "${frontmatter.region}"\n`;
    yamlFrontmatter += `category: "${frontmatter.category}"\n`;
    yamlFrontmatter += `address: "${frontmatter.address ? frontmatter.address.replace(/"/g, '\\"') : ''}"\n`;
    yamlFrontmatter += `rating: ${frontmatter.rating || 0}\n`;
    yamlFrontmatter += `reviews_count: ${frontmatter.reviews_count || 0}\n`;
    yamlFrontmatter += `phone: "${frontmatter.phone || ''}"\n`;
    yamlFrontmatter += `website: "${frontmatter.website || ''}"\n`;
    yamlFrontmatter += `google_maps_url: "${frontmatter.google_maps_url || ''}"\n`;
    
    // Fotoğraflar array'i
    if (frontmatter.photos && frontmatter.photos.length > 0) {
        yamlFrontmatter += `photos:\n`;
        frontmatter.photos.forEach(photo => {
            yamlFrontmatter += `  - "${photo}"\n`;
        });
    } else {
        yamlFrontmatter += `photos: []\n`;
    }

    // Lokasyon objesi
    if (frontmatter.location) {
        yamlFrontmatter += `location:\n`;
        yamlFrontmatter += `  lat: ${frontmatter.location.lat}\n`;
        yamlFrontmatter += `  lng: ${frontmatter.location.lng}\n`;
    }

    yamlFrontmatter += `---\n\n`;

    // İçeriği ekle (Eğer seo_article yoksa boş string)
    const content = seo_article || '';

    // Dosyayı kaydet
    const filePath = path.join(contentDir, `${slug}.md`);
    fs.writeFileSync(filePath, yamlFrontmatter + content, 'utf8');
});

console.log(`${places.length} mekan başarıyla Markdown dosyalarına dönüştürüldü!`);

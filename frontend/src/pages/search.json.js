import { getCollection } from 'astro:content';

export async function GET() {
    const mekanlar = await getCollection('mekanlar');
    const data = mekanlar.map(m => ({ slug: m.slug, ...m.data }));
    const searchData = data.map(item => ({
        name: item.name,
        slug: item.slug,
        region: item.region,
        category: item.category,
        rating: item.rating || 0,
        reviews_count: item.reviews_count || 0,
        photos: item.photos || []
    }));

    return new Response(JSON.stringify(searchData), {
        headers: {
            'Content-Type': 'application/json'
        }
    });
}

import { z, defineCollection } from 'astro:content';

const mekanlarCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    region: z.string(),
    category: z.string(),
    address: z.string().optional(),
    rating: z.number().optional(),
    reviews_count: z.number().optional(),
    phone: z.string().optional(),
    website: z.string().optional(),
    google_maps_url: z.string().optional(),
    photos: z.array(z.string()).optional(),
    location: z.object({
      lat: z.number(),
      lng: z.number(),
    }).optional(),
  }),
});

export const collections = {
  'mekanlar': mekanlarCollection,
};

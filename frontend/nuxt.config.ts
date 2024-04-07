// https://nuxt.com/docs/api/configuration/nuxt-config
if (!process.env.NITRO_PRESET) throw new Error('NITRO_PRESET not found');
export default defineNuxtConfig({
  app: {
    head: {
      title: 'Junkyard of Shangri-La',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1.0' },
        {
          name: 'description',
          content:
            'Junkyard of Shangri-La is a price comparison website for the online bookstore, "Books to Scrape": (https://books.toscrape.com/). ' +
            'Search for books by title, filter search results by one or more genre categories, and compare their prices.'
        }
      ]
    }
  },
  devtools: { enabled: false },
  modules: ['@nuxt/image'],
  imports: {
    autoImport: false
  },
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {}
    }
  },
  ssr: true,
  nitro: {
    preset: process.env.NITRO_PRESET,
    compressPublicAssets: {
      brotli: true
    }
  }
});

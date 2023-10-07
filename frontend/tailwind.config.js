/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      backgroundImage: {
        'search-light': "url('~/assets/svg/search-light.svg')",
        'search-dark': "url('~/assets/svg/search-dark.svg')",
      },
      animation: {
        'float-up': 'float-up .55s cubic-bezier(.38,0,.64,1) both',

        twinkle: 'twinkle 2s ease-in-out infinite both',

        'rotate-cw': 'rotate-cw .2s cubic-bezier(0,0.7,1,1) both',
        'rotate-ccw': 'rotate-ccw .2s cubic-bezier(0,0.7,1,1) both',

        'fade-in-out': 'fade-in-out 5s cubic-bezier(.38,0,.64,1) infinite both',
      },

      keyframes: {
        'float-up': {
          '0%': { opacity: 1, transform: 'translateY(-75%)' },
          '100%': { opacity: 0, transform: 'translateY(-225%)' },
        },

        twinkle: {
          '0%': { filter: 'saturate(0.5)' },
          '100%': { filter: 'saturate(2)' },
        },

        'rotate-cw': {
          '0%': {
            transform: 'rotate3d(0, 0, 1, 0deg)',
          },
          '100%': {
            transform: 'rotate3d(0, 0, 1, 45deg)',
          },
        },

        'rotate-ccw': {
          '0%': {
            transform: 'rotate3d(0, 0, 1, 0deg)',
          },
          '100%': {
            transform: 'rotate3d(0, 0, 1, -45deg)',
          },
        },

        'fall-down': {
          '0%': { transform: 'translateY(-200%)' },
          '100%': { transform: 'translateY(100vh)' },
        },

        'fade-in-out': {
          '0%': { opacity: 0 },
          '51%': {
            opacity: 1,
          },
          '100%': {
            opacity: 0,
          },
        },
      },

      transitionTimingFunction: {
        'custom-ease-in-out': 'cubic-bezier(.38,0,.64,1)',
        'custom-ease-out': 'cubic-bezier(0,.7,1,1)',
      },
    },
  },
  plugins: [],
};

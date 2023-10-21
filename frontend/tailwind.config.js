/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      animation: {
        'hue-rotate': 'hue-rotate 5s cubic-bezier(.38,0,.64,1) infinite both'
      },

      keyframes: {
        'hue-rotate': {
          '0%': { filter: 'hue-rotate(0deg)' },
          '25%': { filter: 'hue-rotate(90deg)' },
          '50%': { filter: 'hue-rotate(180deg)' },
          '75%': { filter: 'hue-rotate(270deg)' },
          '100%': { filter: 'hue-rotate(360deg)' }
        }
      },

      transitionTimingFunction: {
        'custom-ease-in-out': 'cubic-bezier(.38,0,.64,1)',
        'custom-ease-out': 'cubic-bezier(0,.7,1,1)'
      }
    }
  },
  plugins: []
};

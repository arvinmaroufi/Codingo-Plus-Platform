import type { Config } from 'tailwindcss'


const svgToDataUri = require("mini-svg-data-uri");

const colors = require("tailwindcss/colors");
const {
  default: flattenColorPalette,
} = require("tailwindcss/lib/util/flattenColorPalette");


const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
 
    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        custom: ['Gandom', 'sans-serif'],
      },
      colors: {
        // Dark theme colors
        'base-dark': '#031525',
        'primary-dark': '#0794B0',
        'secondary-dark': '#20CCC7',
        'main-text-dark': '#DAEBE7',
        'highlight-text-dark': '#E1F0F7',
        'success-dark': '#16610E',
        'success-text-dark': '#B0DB9C',
        'error-dark': '#8E1616',
        'error-text-dark': '#F7374F',

        // Light theme colors
        'base-light': '#EAF1F0',
        'primary-light': '#63C9DD',
        'secondary-light': '#AAE4E2',
        'main-text-light': '#04364C',
        'highlight-text-light': '#DAEBE7',
        'success-light': '#1DCD9F',
        'success-text-light': '#169976',
        'error-light': '#F15A59',
        'error-text-light': '#8E1616',
      },
      animation: {
        spotlight: "spotlight 2s ease .75s 1 forwards",
      },
      keyframes: {
        spotlight: {
          "0%": {
            opacity: 0,
            transform: "translate(-72%, -62%) scale(0.5)",
          },
          "100%": {
            opacity: 1,
            transform: "translate(-50%,-40%) scale(1)",
          },
        },
      },
      boxShadow: {
        input: `0px 2px 3px -1px rgba(0,0,0,0.1), 0px 1px 0px 0px rgba(25,28,33,0.02), 0px 0px 0px 1px rgba(25,28,33,0.08)`,
      },
    },
  },
  plugins: [],
  'darkMode': 'class',
}

export default config
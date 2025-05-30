import type { Config } from 'tailwindcss'



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
      colors: {
        // Dark theme colors
        'base-dark': '#031525',
        'primary-dark': '#0794B0',
        'secondary-dark': '#20CCC7',
        'main-text-dark': '#DAEBE7',
        'highlight-text-dark': '#E1F0F7',
        // Light theme colors
        'base-light': '#EAF1F0',
        'primary-light': '#63C9DD',
        'secondary-light': '#AAE4E2',
        'main-text-light': '#04364C',
        'highlight-text-light': '#DAEBE7',

      },
    },
  },
  plugins: [],
}

export default config
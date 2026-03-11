/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4338ca', // Indigo 700 - A modern primary color
        secondary: '#64748b', // Slate 500
        accent: '#8b5cf6', // Violet 500
        dark: '#1e293b', // Slate 800
        positive: '#10b981', // Emerald 500
        negative: '#ef4444', // Red 500
        info: '#3b82f6', // Blue 500
        warning: '#f59e0b', // Amber 500
        background: '#f8fafc', // Slate 50
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
}

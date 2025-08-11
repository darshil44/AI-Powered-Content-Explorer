/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4f46e5',    // Indigo-ish
        secondary: '#ec4899',  // Pink-ish
        accent: '#10b981',     // Emerald-ish
        darkbg: '#1f2937',     // Dark gray background
        lightbg: '#f3f4f6',    // Light gray background
      },
      fontFamily: {
        sans: ['"Poppins"', 'ui-sans-serif', 'system-ui'],
      },
    },
  },
  plugins: [],
}

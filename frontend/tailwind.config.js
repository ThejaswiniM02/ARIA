/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        coral: "#FF6B5B",
        violet: "#7C5CFF",
        yellow: "#FFC94A",
        ink: "#1A1B2E",
        paper: "#FBF9F6",
        mint: "#3DD9B3",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
      },
      boxShadow: {
        hard: "6px 6px 0 #1A1B2E",
        "hard-sm": "4px 4px 0 #1A1B2E",
      },
    },
  },
  plugins: [require('@tailwindcss/typography')],
};
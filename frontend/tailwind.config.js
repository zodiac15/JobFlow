/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                heading: ['Outfit', 'sans-serif'],
            },
            colors: {
                primary: {
                    light: '#8b5cf6', // Violet 500
                    DEFAULT: '#7c3aed', // Violet 600
                    dark: '#6d28d9', // Violet 700
                },
                secondary: {
                    light: '#f0abfc', // Fuchsia 300
                    DEFAULT: '#d946ef', // Fuchsia 500
                    dark: '#c026d3', // Fuchsia 600
                },
                surface: '#ffffff',
                background: '#f8fafc', // Slate 50
            },
            boxShadow: {
                'material-1': '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)',
                'material-2': '0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)',
                'material-3': '0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23)',
            },
            keyframes: {
                'fade-in-up': {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
                'fade-out-down': {
                    '0%': { opacity: '1', transform: 'translateY(0)' },
                    '100%': { opacity: '0', transform: 'translateY(10px)' },
                },
                'wiggle': {
                    '0%, 100%': { transform: 'rotate(-3deg)' },
                    '50%': { transform: 'rotate(3deg)' },
                }
            },
            animation: {
                'fade-in-up': 'fade-in-up 0.5s ease-out forwards',
                'fade-out-down': 'fade-out-down 0.5s ease-in forwards',
                'wiggle': 'wiggle 1s ease-in-out infinite',
            }
        },
    },
    plugins: [],
}

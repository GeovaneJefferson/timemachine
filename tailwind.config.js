/**
 * Tailwind configuration using Apple Human Interface Guidelines color tokens
 * and semantic naming. This file drives the local build pipeline; remove all
 * inline CDN config from HTML once the build is working.
 */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './js/**/*.js',
    './css/**/*.css',
    './py/**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        // Apple HIG system colors (light-mode values; Tailwind will invert
        // them automatically under the "dark" utility via the color
        // function when the dark class is present)
        'system-background': '#FFFFFF',
        'system-secondary-background': '#F2F2F7',
        'system-tertiary-background': '#FFFFFF',
        'system-grouped-background': '#F2F2F7',

        'label': '#000000',
        'secondary-label': '#3C3C4399',
        'tertiary-label': '#3C3C434D',
        'quaternary-label': '#3C3C432E',
        'placeholder-text': '#3C3C434D',
        'separator': '#3C3C434D',
        'opaque-separator': '#C6C6C8',
        'link': '#007AFF',

        'system-fill': '#78788033',
        'secondary-system-fill': '#78788028',
        'tertiary-system-fill': '#7676801E',
        'quaternary-system-fill': '#74748014',

        'accent': '#007AFF',
        'system-blue': '#007AFF',
        'system-green': '#34C759',
        'system-indigo': '#5856D6',
        'system-orange': '#FF9500',
        'system-pink': '#FF2D55',
        'system-purple': '#AF52DE',
        'system-red': '#FF3B30',
        'system-teal': '#5AC8FA',
        'system-yellow': '#FFCC00',

        // backwards compatibility
        'primary': '#007AFF',
        'background-light': '#f5f5f7',
        'background-dark': '#1e1e1e',
        'surface-light': '#ffffff',
        'surface-dark': '#2c2c2e',
        'border-light': '#e5e5e5',
        'border-dark': '#3a3a3c',
        'text-secondary-light': '#6e6e73',
        'text-secondary-dark': '#98989d',
        'surface-highlight': '#f2f2f7',
      },
      borderRadius: {
        DEFAULT: '12px',      // more macOS-like radius
        lg: '16px',
        xl: '20px',
      },
      boxShadow: {
        soft: '0 4px 20px -2px rgba(0, 0, 0, 0.1)',
        'inner-light': 'inset 0 1px 2px rgba(0,0,0,0.05)',
        menu: '0 10px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1)',
        glow: '0 0 15px rgba(0, 122, 255, 0.3)',
      },
      fontFamily: {
        display: ['Inter', 'sans-serif'],
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/container-queries'),
  ],
};

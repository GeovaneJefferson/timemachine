/**
 * CENTRALIZED COLOR PALETTE
 * 
 * Edit colors here and they'll apply everywhere!
 * Import this into both index.html and style.css
 */

const APP_COLORS = {
    brand: {
        50: '#EFF6FF',      // Lightest background
        100: '#DBEAFE',     // Light background
        500: '#0052CC',     // Main blue - matching mockup button ⭐
        600: '#0047B2',     // Hover state
        700: '#003A99'      // Active/pressed state
    },
    
    // Override Tailwind's default slate palette
    slate: {
        50: '#FFFFFF',      // Pure white - light mode background
        100: '#F5F5F5',     // Very light gray
        200: '#E5E5E5',     // Light gray
        300: '#D0D0D0',     // Medium-light gray
        400: '#A0A0A0',     // Medium gray
        500: '#707070',     // Medium dark gray
        600: '#505050',     // Dark gray
        700: '#303030',     // Very dark gray
        750: '#252525',     // Extra dark
        800: '#1A1A1A',     // Dark mode card background (matching mockup)
        850: '#0F0F0F',     // Dark mode secondary
        900: '#000000',     // Pure black (matching mockup)
        950: '#000000'      // Darkest
    },
    
    // Status colors
    success: '#28A745',    // Green
    warning: '#FFC107',    // Amber
    error: '#DC3545',      // Red
    
    // Dark mode - matching left mockup
    dark: {
        bg: '#000000',      // Pure black background
        card: '#1A1A1A',    // Dark card
        border: '#303030'   // Dark border
    }
};

// Export for both Node.js and browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APP_COLORS;
}

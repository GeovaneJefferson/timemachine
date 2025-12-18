/**
 * Manages dark/light theme
 */

export class ThemeManager {
    init() {
        const savedTheme = localStorage.getItem('theme');
        const isDark = savedTheme === 'dark';

        this.setTheme(isDark);

        // Update toggle switch
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.checked = isDark;
            themeToggle.addEventListener('change', (e) => this.toggle(e.target.checked));
        }

        // Update theme icon
        this.updateThemeIcon(isDark);
    }

    toggle(isDark) {
        this.setTheme(isDark);
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        this.updateThemeIcon(isDark);
    }

    setTheme(isDark) {
        if (isDark) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }

    updateThemeIcon(isDark) {
        const icon = document.getElementById('theme-icon');
        if (icon) {
            if (isDark) {
                icon.className = 'bi bi-sun-fill text-yellow-400';
            } else {
                icon.className = 'bi bi-moon-stars-fill text-brand-500';
            }
        }
    }
}

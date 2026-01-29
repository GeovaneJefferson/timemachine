// src/js/router.js - Updated with settings routes

class Router {
    constructor() {
        this.routes = {
            '/': 'dashboard',
            '/dashboard': 'dashboard',
            '/applications': 'applications',
            '/dev-packages': 'devPackages',
            '/folders': 'folders',
            '/locations': 'locations',
            '/settings': 'settings',
            '/help': 'help',
            '/about': 'about'
        };
        
        this.currentPage = null;
        this.init();
    }

    init() {
        // Handle browser back/forward
        window.addEventListener('popstate', () => {
            this.handleRoute(window.location.pathname);
        });

        // Handle initial route
        this.handleRoute(window.location.pathname);
    }

    async navigate(path) {
        window.history.pushState({}, '', path);
        await this.handleRoute(path);
    }

    async handleRoute(path) {
        const routeName = this.routes[path] || 'dashboard';
        
        // Dispatch event for app to handle
        const event = new CustomEvent('route-change', {
            detail: { route: routeName, path: path }
        });
        window.dispatchEvent(event);
    }

    getCurrentRoute() {
        const path = window.location.pathname;
        return this.routes[path] || 'dashboard';
    }
}

export default new Router();
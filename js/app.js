// js/app.js

// Import js/utils/notifications.js
// import { NotificationSystem } from './utils/notifications.js';
import './utils/notifications.js';

// Application State Manager
class AppState {
    constructor() {
        this.currentPage = null;
        this.header = null;
        this.pages = {};
        this.searchHistory = [];
        
        // Initialize global state
        window.currentPage = null;
        window.pendingSearchQuery = null;
        window.appState = this;
        window.foldersPage = null;
        window.appHeader = null;
    }
    
    setCurrentPage(page) {
        console.log('AppState: Setting current page to', page);
        this.currentPage = page;
        window.currentPage = page;
        
        // Notify header of page change
        if (window.appHeader && window.appHeader.setCurrentPage) {
            window.appHeader.setCurrentPage(page);
        }
    }
    
    registerPage(name, pageInstance) {
        this.pages[name] = pageInstance;
    }
    
    setHeader(headerInstance) {
        this.header = headerInstance;
        window.appHeader = headerInstance;
    }
    
    addToSearchHistory(query) {
        if (query && query.trim()) {
            this.searchHistory.unshift(query.trim());
            
            // Keep only last 10 searches
            if (this.searchHistory.length > 10) {
                this.searchHistory = this.searchHistory.slice(0, 10);
            }
            
            // Save to localStorage
            try {
                localStorage.setItem('searchHistory', JSON.stringify(this.searchHistory));
            } catch (e) {
                console.warn('Could not save search history:', e);
            }
        }
    }
    
    loadSearchHistory() {
        try {
            const history = localStorage.getItem('searchHistory');
            if (history) {
                this.searchHistory = JSON.parse(history);
            }
        } catch (e) {
            console.warn('Could not load search history:', e);
        }
        return this.searchHistory;
    }
    
    clearSearchHistory() {
        this.searchHistory = [];
        try {
            localStorage.removeItem('searchHistory');
        } catch (e) {
            console.warn('Could not clear search history:', e);
        }
    }
}

// Initialize app state
const appState = new AppState();

// Wait for DOM
document.addEventListener('DOMContentLoaded', async () => {
    console.log('DOM loaded, initializing app...');
    
    try {
        // Load header
        await loadHeader();
        
        // Load sidebar
        await loadSidebar();
        
        // Load dashboard
        await loadDashboard();

        console.log('App initialized successfully');
    } catch (error) {
        console.error('Failed to initialize app:', error);
        document.getElementById('page-content').innerHTML = `
            <div class="p-8 text-center">
                <div class="text-red-500 text-5xl mb-4">⚠️</div>
                <h2 class="text-xl font-bold mb-2">Initialization Error</h2>
                <p class="text-gray-600">${error.message}</p>
                <button onclick="location.reload()" class="mt-4 px-4 py-2 bg-primary text-white rounded">
                    Reload Page
                </button>
            </div>
        `;
    }
});

// Load header
async function loadHeader() {
    console.log('Loading header...');
    
    try {
        // Import header module
        const HeaderModule = await import('./components/header.js');
        const Header = HeaderModule.default;
        
        // Create header instance
        const header = new Header();
        
        // Render header
        const headerContainer = document.getElementById('header-container');
        if (headerContainer) {
            headerContainer.innerHTML = await header.render();
            header.afterRender();
            
            // Set header in app state
            appState.setHeader(header);
        }
        
        console.log('Header loaded successfully');
    } catch (error) {
        console.error('Failed to load header:', error);
        // Fallback header
        document.getElementById('header-container').innerHTML = `
            <div class="flex items-center justify-between px-6 py-3 bg-gray-50 border-b">
                <div class="text-lg font-bold">TimeMachine Backup</div>
                <button onclick="loadPage('dashboard')" class="px-4 py-2 bg-blue-500 text-white rounded">
                    Dashboard
                </button>
            </div>
        `;
    }
}

// Load sidebar
// Load sidebar
async function loadSidebar() {
    console.log('Loading sidebar...');

    try {
        // Import sidebar module using destructuring
        const { default: Sidebar } = await import('./components/sidebar.js');

        // Create sidebar instance
        const sidebar = new Sidebar();

        // Render sidebar
        const sidebarContainer = document.getElementById('sidebar');
        if (sidebarContainer) {
            sidebarContainer.innerHTML = await sidebar.render();
            sidebar.init();

            // Add click handler for navigation
            sidebarContainer.addEventListener('click', (e) => {
                const link = e.target.closest('[data-route]');
                if (link) {
                    e.preventDefault();
                    const route = link.getAttribute('data-route');
                    console.log('Navigating to:', route);
                    loadPage(route);
                }
            });
        }

        console.log('Sidebar loaded successfully');
    } catch (error) {
        console.error('Failed to load sidebar:', error);
        // Fallback sidebar
        document.getElementById('sidebar').innerHTML = `
        <div class="p-4">
        <h3 class="font-bold mb-4">Navigation</h3>
        <button onclick="loadPage('dashboard')" class="block w-full text-left p-2 bg-blue-100 rounded mb-2">
        Dashboard
        </button>
        <button onclick="loadPage('folders')" class="block w-full text-left p-2 hover:bg-gray-100 rounded mb-2">
        Backup Files
        </button>
        <button onclick="loadPage('locations')" class="block w-full text-left p-2 hover:bg-gray-100 rounded">
        Locations
        </button>
        </div>
        `;
    }
}

// Load dashboard
async function loadDashboard() {
    console.log('Loading dashboard...');
    await loadPage('dashboard');
}

// Load any page
async function loadPage(pageName, params = {}) {
    console.log(`Loading page: ${pageName}`, params);
    
    const pageContent = document.getElementById('page-content');
    const loading = document.getElementById('loading');
    
    // Update app state
    appState.setCurrentPage(pageName);
    
    // Check for pending search query
    if (params.searchQuery) {
        window.pendingSearchQuery = params.searchQuery;
    }
    
    if (loading) loading.classList.remove('hidden');
    
    try {
        // Clean up current page if exists
        if (window.currentPageInstance && window.currentPageInstance.destroy) {
            window.currentPageInstance.destroy();
        }
        
        if (pageName === 'dashboard') {
            // Import dashboard module
            const DashboardModule = await import('./pages/dashboard.js');
            const DashboardPage = DashboardModule.default;
            const page = new DashboardPage();
            
            // Render page
            pageContent.innerHTML = await page.render();
            
            // Initialize page
            if (page.afterRender) {
                page.afterRender();
            }
            
            window.currentPageInstance = page;
            appState.registerPage(pageName, page);
            
        } else if (pageName === 'applications') {
            // Import applications module
            const ApplicationsModule = await import('./pages/applications.js');
            const ApplicationsPage = ApplicationsModule.default;
            const page = new ApplicationsPage();
            
            // Render page
            pageContent.innerHTML = await page.render();
            
            // Initialize page
            if (page.afterRender) {
                page.afterRender();
            }
            
            window.currentPageInstance = page;
            appState.registerPage(pageName, page);
            
        } else if (pageName === 'dev-packages') {
            // Import dev-packages module
            const DevPackagesModule = await import('./pages/dev-packages.js');
            const DevPackagesPage = DevPackagesModule.default;
            const page = new DevPackagesPage();

            // Render page
            pageContent.innerHTML = await page.render();

            // Initialize page
            if (page.afterRender) {
                page.afterRender();
            }
            
            window.currentPageInstance = page;
            appState.registerPage(pageName, page);
            
        } else if (pageName === 'folders') {
            // Import folders module
            const FoldersModule = await import('./pages/folders.js');
            const FoldersPage = FoldersModule.default;
            const page = new FoldersPage();
            
            // Store reference globally for search access
            window.foldersPage = page;
            
            // Render page
            pageContent.innerHTML = await page.render();
            
            // Initialize page
            if (page.afterRender) {
                page.afterRender();
            }
            
            window.currentPageInstance = page;
            appState.registerPage(pageName, page);
            
        } else if (pageName === 'locations') {
            // Import locations module
            const LocationsModule = await import('./pages/locations.js');
            const LocationsPage = LocationsModule.default;
            const page = new LocationsPage();
            
            // Render page
            pageContent.innerHTML = await page.render();
            
            // Initialize page
            if (page.afterRender) {
                page.afterRender();
            }
            
            window.currentPageInstance = page;
            appState.registerPage(pageName, page);
            
        } else if (pageName === 'settings') {
            // Import settings module
            const SettingsModule = await import('./pages/settings.js');
            const SettingsPage = SettingsModule.default;
            const page = new SettingsPage();

            // Render page
            pageContent.innerHTML = await page.render();

            // Initialize page
            if (page.afterRender) {
                page.afterRender();
            }
            
            window.currentPageInstance = page;
            appState.registerPage(pageName, page);
            
        } else if (pageName === 'help') {
            // Import help module
            const HelpModule = await import('./pages/help.js');
            const HelpPage = HelpModule.default;
            const page = new HelpPage();

            // Render page
            pageContent.innerHTML = await page.render();

            // Initialize page
            if (page.afterRender) {
                page.afterRender();
            }
            
            window.currentPageInstance = page;
            appState.registerPage(pageName, page);
            
        } else if (pageName === 'about') {
            // Import about module
            const AboutModule = await import('./pages/about.js');
            const AboutPage = AboutModule.default;
            const page = new AboutPage();

            // Render page
            pageContent.innerHTML = await page.render();

            // Initialize page
            if (page.afterRender) {
                page.afterRender();
            }
            
            window.currentPageInstance = page;
            appState.registerPage(pageName, page);
            
        } else {
            // Default/fallback
            pageContent.innerHTML = `
                <div class="p-8">
                    <h1 class="text-2xl font-bold mb-4">${pageName.charAt(0).toUpperCase() + pageName.slice(1)}</h1>
                    <p>This page is under construction.</p>
                </div>
            `;
        }
    } catch (error) {
        console.error(`Failed to load page ${pageName}:`, error);
        pageContent.innerHTML = `
            <div class="p-8 text-red-600">
                <h2 class="text-xl font-bold">Error loading ${pageName}</h2>
                <p>${error.message}</p>
            </div>
        `;
    } finally {
        if (loading) loading.classList.add('hidden');
    }
}

// Global search function for header integration
function performGlobalSearch(query) {
    if (!query || query.trim() === '') return;
    
    const currentPage = window.currentPage || 'dashboard';
    
    if (currentPage === 'folders') {
        // If already on folders page, trigger search directly
        if (window.foldersPage && window.foldersPage.handleHeaderSearch) {
            window.foldersPage.handleHeaderSearch(query.trim());
        }
    } else {
        // Navigate to folders page with search query
        loadPage('folders', { searchQuery: query.trim() });
    }
}

// Make functions globally available
window.loadPage = loadPage;
window.performGlobalSearch = performGlobalSearch;

// Initialize app state globally
window.appState = appState;

console.log('App.js loaded with search integration');

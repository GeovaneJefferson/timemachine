// src/js/pages/about.js - FIXED

export default class AboutPage {
    constructor() {
        this.name = 'about';
    }

    async render() {
        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">About Backup Dashboard</h1>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Information about your application version and resources.</p>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark">
                <div class="max-w-3xl mx-auto p-8">
                    <div class="text-center mb-8">
                        <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center mx-auto mb-4">
                            <span class="material-icons-round text-white text-4xl">backup</span>
                        </div>
                        <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Backup Dashboard</h2>
                        <p class="text-gray-600 dark:text-gray-400 mt-2">Version 0.1 • Build 2023.12.29</p>
                    </div>
                    
                    <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 mb-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Application Information</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between">
                                <span class="text-gray-600 dark:text-gray-400">Version</span>
                                <span class="font-medium text-gray-900 dark:text-white">0.1</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600 dark:text-gray-400">Build Date</span>
                                <span class="font-medium text-gray-900 dark:text-white">December 29, 2023</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600 dark:text-gray-400">License</span>
                                <span class="font-medium text-gray-900 dark:text-white">GNU General Public License v3.0</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-gray-600 dark:text-gray-400">Developer</span>
                                <span class="font-medium text-gray-900 dark:text-white">Geovane J.</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 mb-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">System Resources</h3>
                        <div class="space-y-4">
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-gray-600 dark:text-gray-400">Memory Usage</span>
                                    <span class="font-medium text-gray-900 dark:text-white">45%</span>
                                </div>
                                <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                    <div class="h-full bg-green-500 w-2/5 rounded-full"></div>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-gray-600 dark:text-gray-400">Storage Used</span>
                                    <span class="font-medium text-gray-900 dark:text-white">128 GB / 512 GB</span>
                                </div>
                                <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                    <div class="h-full bg-blue-500 w-1/4 rounded-full"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="flex justify-center gap-4">
                        <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors" id="check-updates-btn">
                            Check for Updates
                        </button>
                        <button class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-blue-600 transition-colors" id="view-license-btn">
                            View License
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    afterRender() {
        console.log('About page initialized');
        
        // Add event listeners
        const checkUpdatesBtn = document.getElementById('check-updates-btn');
        if (checkUpdatesBtn) {
            checkUpdatesBtn.addEventListener('click', () => {
                this.checkForUpdates();
            });
        }
        
        const viewLicenseBtn = document.getElementById('view-license-btn');
        if (viewLicenseBtn) {
            viewLicenseBtn.addEventListener('click', () => {
                this.viewLicense();
            });
        }
    }

    checkForUpdates() {
        console.log('Checking for updates...');
        
        // Simulate checking for updates
        const updateBtn = document.getElementById('check-updates-btn');
        if (updateBtn) {
            const originalText = updateBtn.textContent;
            updateBtn.textContent = 'Checking...';
            updateBtn.disabled = true;
            
            setTimeout(() => {
                updateBtn.textContent = originalText;
                updateBtn.disabled = false;
                alert('You are running the latest version of Backup Dashboard.');
            }, 1500);
        }
    }

    viewLicense() {
        console.log('Viewing license...');
        window.open('https://opensource.org/license/gpl-3-0', '_blank');
    }

    destroy() {
        console.log('Cleaning up About page');
    }
}
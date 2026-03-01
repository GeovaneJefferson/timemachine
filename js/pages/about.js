// src/js/pages/about.js - FIXED

import { electronAPI } from '../utils/electron-adapter.js';

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
                        <p class="text-gray-600 dark:text-gray-400 mt-2" id="app-version-info">Version 0.1 • Build 2023.12.29</p>
                    </div>
                    
                    <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 mb-6">
                        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Application Information</h3>
                        <div class="space-y-3">
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
                                    <span id="memory-usage-percent" class="font-medium text-gray-900 dark:text-white">...</span>
                                </div>
                                <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                    <div id="memory-usage-bar" class="h-full bg-green-500 rounded-full" style="width: 0%"></div>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-gray-600 dark:text-gray-400">Storage Used</span>
                                    <span id="storage-usage-text" class="font-medium text-gray-900 dark:text-white">...</span>
                                </div>
                                <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                    <div id="storage-usage-bar" class="h-full bg-blue-500 rounded-full" style="width: 0%"></div>
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

    // async render() {
    //     return `
    //         <div class="px-8 py-6 flex items-end justify-between border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark">
    //             <div>
    //                 <h1 class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">About Backup Dashboard</h1>
    //                 <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Information about your application version and resources.</p>
    //             </div>
    //         </div>
    //         <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark">
    //             <div class="max-w-3xl mx-auto p-8">
    //                 <div class="text-center mb-8">
    //                     <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center mx-auto mb-4">
    //                         <span class="material-icons-round text-white text-4xl">backup</span>
    //                     </div>
    //                     <h2 class="text-2xl font-bold text-gray-900 dark:text-white">Backup Dashboard</h2>
    //                     <p class="text-gray-600 dark:text-gray-400 mt-2" id="app-version-info">Version 0.1 • Build 2023.12.29</p>
    //                 </div>
                    
    //                 <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 mb-6">
    //                     <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Application Information</h3>
    //                     <div class="space-y-3">
    //                         <div class="flex justify-between">
    //                             <span class="text-gray-600 dark:text-gray-400">Version</span>
    //                             <span class="font-medium text-gray-900 dark:text-white" id="app-version">0.1</span>
    //                         </div>
    //                         <div class="flex justify-between">
    //                             <span class="text-gray-600 dark:text-gray-400">Build Date</span>
    //                             <span class="font-medium text-gray-900 dark:text-white">December 29, 2023</span>
    //                         </div>
    //                         <div class="flex justify-between">
    //                             <span class="text-gray-600 dark:text-gray-400">License</span>
    //                             <span class="font-medium text-gray-900 dark:text-white">GNU General Public License v3.0</span>
    //                         </div>
    //                         <div class="flex justify-between">
    //                             <span class="text-gray-600 dark:text-gray-400">Developer</span>
    //                             <span class="font-medium text-gray-900 dark:text-white">Geovane J.</span>
    //                         </div>
    //                     </div>
    //                 </div>
                    
    //                 <div class="bg-gray-50 dark:bg-gray-800 rounded-xl p-6 mb-6">
    //                     <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">System Resources</h3>
    //                     <div class="space-y-4">
    //                         <div>
    //                             <div class="flex justify-between text-sm mb-1">
    //                                 <span class="text-gray-600 dark:text-gray-400">Memory Usage</span>
    //                                 <span class="font-medium text-gray-900 dark:text-white">45%</span>
    //                             </div>
    //                             <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
    //                                 <div class="h-full bg-green-500 w-2/5 rounded-full"></div>
    //                             </div>
    //                         </div>
    //                         <div>
    //                             <div class="flex justify-between text-sm mb-1">
    //                                 <span class="text-gray-600 dark:text-gray-400">Storage Used</span>
    //                                 <span class="font-medium text-gray-900 dark:text-white">128 GB / 512 GB</span>
    //                             </div>
    //                             <div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
    //                                 <div class="h-full bg-blue-500 w-1/4 rounded-full"></div>
    //                             </div>
    //                         </div>
    //                     </div>
    //                 </div>
                    
    //                 <div class="flex justify-center gap-4">
    //                     <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors" id="check-updates-btn">
    //                         Check for Updates
    //                     </button>
    //                     <button class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-blue-600 transition-colors" id="view-license-btn">
    //                         View License
    //                     </button>
    //                 </div>
    //             </div>
    //         </div>
    //     `;
    // }

    afterRender() {
        console.log('About page initialized');
        this.loadVersionInfo();
        this.loadSystemResources();
        
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

    async loadSystemResources() {
        try {
            const memResponse = await fetch('/api/system-memory');
            const memData = await memResponse.json();
            if (memData.success) {
                const memPercent = memData.memory_percent;
                document.getElementById('memory-usage-percent').textContent = `${memPercent}%`;
                document.getElementById('memory-usage-bar').style.width = `${memPercent}%`;
            }

            const storageResponse = await fetch('/api/backup/usage');
            const storageData = await storageResponse.json();
            if (storageData.success) {
                const storagePercent = storageData.home_percent_used;
                document.getElementById('storage-usage-text').textContent = `${storageData.home_human_used} / ${storageData.home_human_total}`;
                document.getElementById('storage-usage-bar').style.width = `${storagePercent}%`;
            }
        } catch (error) {
            console.error('Error loading system resources:', error);
        }
    }

    async loadVersionInfo() {
        try {
            // Change window.apiAdapter.get to fetch
            const response = await fetch('/api/check-for-updates');
            const info = await response.json();
            
            const versionElement = document.getElementById('app-version-info');
            if (versionElement && info.success) {
                versionElement.textContent = `Version: ${info.current_version} • Build: 2026`;
            }
        } catch (error) {
            console.error('Error loading version info:', error);
        }
    }

    async checkForUpdates() {
        // Instead of handling everything here, just send the user to the update
        // page which will reload the information and allow them to trigger an
        // update explicitly.
        if (window.apiAdapter && window.apiAdapter.isRunningInElectron && window.apiAdapter.isRunningInElectron()) {
            if (window.apiAdapter.openUpdateWindow) {
                window.apiAdapter.openUpdateWindow();
                return;
            }
        }

        if (typeof window.loadPage === 'function') {
            window.loadPage('update');
        } else {
            // fallback to existing behaviour if router isn't available
            try {
                const response = await fetch('/api/check-for-updates');
                const info = await response.json();
                if (info.success) {
                    if (info.update_available) {
                        this.showNotification(`A new version (${info.latest_version}) is available.`, 'info');
                    } else {
                        this.showNotification('You are using the latest version.', 'success');
                    }
                } else {
                    this.showNotification(`Update check failed: ${info.error}`, 'error');
                }
            } catch (error) {
                this.showNotification('Failed to check for updates.', 'error');
                console.error('Error checking for updates:', error);
            }
        }
    }

    viewLicense() {
        console.log('Viewing license...');
        window.open('https://opensource.org/license/gpl-3-0', '_blank');
    }

    destroy() {
        console.log('Cleaning up About page');
    }

    showNotification(message, type = 'info') {
        // basic notification implementation same as sidebar
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2 ${
            type === 'success' ? 'bg-green-100 text-green-800 border border-green-200 dark:bg-green-900/30 dark:text-green-300 dark:border-green-800' :
            type === 'error' ? 'bg-red-100 text-red-800 border border-red-200 dark:bg-red-900/30 dark:text-red-300 dark:border-red-800' :
            'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800'
        }`;

        notification.innerHTML = `
        <span class="material-icons-round text-sm">
        ${type === 'success' ? 'check_circle' :
            type === 'error' ? 'error' :
            'info'}
            </span>
            <span>${message}</span>
            `;

        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }
}
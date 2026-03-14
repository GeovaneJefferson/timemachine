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
                    <h1 class="text-2xl font-bold text-[var(--color-text-primary)] dark:text-white leading-tight">About Backup Dashboard</h1>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Information about your application version and resources.</p>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark">
                <div class="max-w-3xl mx-auto p-8">
                    <div class="text-center mb-8">
                        <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-[var(--color-accent)] to-[var(--color-accent)] flex items-center justify-center mx-auto mb-4">
                            <span class="material-icons-round text-white text-4xl">backup</span>
                        </div>
                        <h2 class="text-2xl font-bold text-[var(--color-text-primary)] dark:text-white">Backup Dashboard</h2>
                        <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mt-2" id="app-version-info">Version 0.1 • Build 2023.12.29</p>
                    </div>
                    
                    <div class="bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] rounded-xl p-6 mb-6">
                        <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-4">Application Information</h3>
                        <div class="space-y-3">
                            <div class="flex justify-between">
                                <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">License</span>
                                <span class="font-medium text-[var(--color-text-primary)] dark:text-white">GNU General Public License v3.0</span>
                            </div>
                            <div class="flex justify-between">
                                <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Developer</span>
                                <span class="font-medium text-[var(--color-text-primary)] dark:text-white">Geovane J.</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] rounded-xl p-6 mb-6">
                        <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-4">System Resources</h3>
                        <div class="space-y-4">
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Memory Usage</span>
                                    <span id="memory-usage-percent" class="font-medium text-[var(--color-text-primary)] dark:text-white">...</span>
                                </div>
                                <div class="w-full h-2 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded-full overflow-hidden">
                                    <div id="memory-usage-bar" class="h-full bg-[var(--color-status-success)] rounded-full" style="width: 0%"></div>
                                </div>
                            </div>
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Storage Used</span>
                                    <span id="storage-usage-text" class="font-medium text-[var(--color-text-primary)] dark:text-white">...</span>
                                </div>
                                <div class="w-full h-2 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded-full overflow-hidden">
                                    <div id="storage-usage-bar" class="h-full bg-[var(--color-accent)] rounded-full" style="width: 0%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="flex justify-center gap-4">
                        <button class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-[var(--color-accent)] transition-colors" id="view-license-btn">
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
    //                 <h1 class="text-2xl font-bold text-[var(--color-text-primary)] dark:text-white leading-tight">About Backup Dashboard</h1>
    //                 <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Information about your application version and resources.</p>
    //             </div>
    //         </div>
    //         <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark">
    //             <div class="max-w-3xl mx-auto p-8">
    //                 <div class="text-center mb-8">
    //                     <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-[var(--color-accent)] to-[var(--color-accent)] flex items-center justify-center mx-auto mb-4">
    //                         <span class="material-icons-round text-white text-4xl">backup</span>
    //                     </div>
    //                     <h2 class="text-2xl font-bold text-[var(--color-text-primary)] dark:text-white">Backup Dashboard</h2>
    //                     <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mt-2" id="app-version-info">Version 0.1 • Build 2023.12.29</p>
    //                 </div>
                    
    //                 <div class="bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] rounded-xl p-6 mb-6">
    //                     <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-4">Application Information</h3>
    //                     <div class="space-y-3">
    //                         <div class="flex justify-between">
    //                             <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Version</span>
    //                             <span class="font-medium text-[var(--color-text-primary)] dark:text-white" id="app-version">0.1</span>
    //                         </div>
    //                         <div class="flex justify-between">
    //                             <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Build Date</span>
    //                             <span class="font-medium text-[var(--color-text-primary)] dark:text-white">December 29, 2023</span>
    //                         </div>
    //                         <div class="flex justify-between">
    //                             <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">License</span>
    //                             <span class="font-medium text-[var(--color-text-primary)] dark:text-white">GNU General Public License v3.0</span>
    //                         </div>
    //                         <div class="flex justify-between">
    //                             <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Developer</span>
    //                             <span class="font-medium text-[var(--color-text-primary)] dark:text-white">Geovane J.</span>
    //                         </div>
    //                     </div>
    //                 </div>
                    
    //                 <div class="bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] rounded-xl p-6 mb-6">
    //                     <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-4">System Resources</h3>
    //                     <div class="space-y-4">
    //                         <div>
    //                             <div class="flex justify-between text-sm mb-1">
    //                                 <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Memory Usage</span>
    //                                 <span class="font-medium text-[var(--color-text-primary)] dark:text-white">45%</span>
    //                             </div>
    //                             <div class="w-full h-2 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded-full overflow-hidden">
    //                                 <div class="h-full bg-[var(--color-status-success)] w-2/5 rounded-full"></div>
    //                             </div>
    //                         </div>
    //                         <div>
    //                             <div class="flex justify-between text-sm mb-1">
    //                                 <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Storage Used</span>
    //                                 <span class="font-medium text-[var(--color-text-primary)] dark:text-white">128 GB / 512 GB</span>
    //                             </div>
    //                             <div class="w-full h-2 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded-full overflow-hidden">
    //                                 <div class="h-full bg-[var(--color-accent)] w-1/4 rounded-full"></div>
    //                             </div>
    //                         </div>
    //                     </div>
    //                 </div>
                    
    //                 <div class="flex justify-center gap-4">
    //                     <button class="px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] bg-[var(--color-gray-100)] dark:bg-[var(--color-gray-700)] rounded-lg hover:bg-[var(--color-gray-200)] dark:hover:bg-[var(--color-gray-600)] transition-colors" id="check-updates-btn">
    //                         Check for Updates
    //                     </button>
    //                     <button class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-[var(--color-accent)] transition-colors" id="view-license-btn">
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


    viewLicense() {
        console.log('Viewing license...');
        window.open('https://opensource.org/license/gpl-3-0', '_blank');
    }

    destroy() {
        console.log('Cleaning up About page');
    }

}
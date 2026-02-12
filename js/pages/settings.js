// src/js/pages/settings.js

import { createLoadingSkeleton } from '../utils/loading-skeleton.js';

export default class SettingsPage {
    constructor() {
        this.name = 'settings';
        this.preferences = {};
    }

    async loadPreferences() {
        try {
            // Use the new endpoint
            const response = await window.electron.api('GET', '/api/settings/preferences');
            if (response.success) {
                this.preferences = response.preferences;
            } else {
                console.error('Failed to load preferences:', response.error);
            }
        } catch (error) {
            console.error('Error loading preferences:', error);
        }
    }

    async render() {
        await this.loadPreferences();
        
        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">Settings</h1>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Configure your backup preferences and application settings.</p>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark p-8">
                <div class="max-w-3xl mx-auto">
                    <div class="space-y-6">
                        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Backup Settings</h2>
                            <div class="space-y-4">
                                <!-- Automatic Backups -->
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-gray-900 dark:text-white">Automatic Backups</p>
                                        <p class="text-sm text-gray-500 dark:text-gray-400">Enable or disable automatic backups when file changes are detected.</p>
                                    </div>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" ${this.preferences.automatic_backups ? 'checked' : ''} id="auto-backup-toggle">
                                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                                    </label>
                                </div>
                                
                                <!-- Launch at Startup -->
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-gray-900 dark:text-white">Launch at Startup</p>
                                        <p class="text-sm text-gray-500 dark:text-gray-400">Automatically start the application when you log in.</p>
                                    </div>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" ${this.preferences.launch_at_startup ? 'checked' : ''} id="launch-startup-toggle">
                                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                                    </label>
                                </div>
                                
                                <!-- Cloud Sync -->
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-gray-900 dark:text-white">Cloud Sync</p>
                                        <p class="text-sm text-gray-500 dark:text-gray-400">Sync backups to cloud storage (feature not implemented).</p>
                                    </div>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" ${this.preferences.cloud_sync ? 'checked' : ''} id="cloud-sync-toggle" disabled>
                                        <div class="w-11 h-6 bg-gray-200 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary opacity-50 cursor-not-allowed"></div>
                                    </label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="flex justify-end gap-3">
                            <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600" id="cancel-settings">
                                Cancel
                            </button>
                            <button class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-blue-600" id="save-settings">
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    afterRender() {
        const saveButton = document.getElementById('save-settings');
        if (saveButton) {
            saveButton.addEventListener('click', () => this.saveSettings());
        }

        const cancelButton = document.getElementById('cancel-settings');
        if (cancelButton) {
            cancelButton.addEventListener('click', () => window.history.back());
        }
    }

    async saveSettings() {
        const settings = {
            automatic_backups: document.getElementById('auto-backup-toggle')?.checked || false,
            launch_at_startup: document.getElementById('launch-startup-toggle')?.checked || false,
            cloud_sync: document.getElementById('cloud-sync-toggle')?.checked || false,
        };
        
        try {
            // Use the new endpoint
            const result = await window.electron.api('POST', '/api/settings/preferences', settings);
            
            if (result.success) {
                this.showNotification('Settings saved successfully!', 'success');
                setTimeout(() => window.history.back(), 1500);
            } else {
                this.showNotification(`Failed to save settings: ${result.error}`, 'error');
            }
        } catch (error) {
            this.showNotification(`Error saving settings: ${error.message}`, 'error');
        }
    }

    showNotification(message, type = 'info') {
        // Your existing notification code
    }

    destroy() {
        // Cleanup if needed
    }
}

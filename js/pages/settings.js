// src/js/pages/settings.js - FIXED

import { createLoadingSkeleton } from '../utils/loading-skeleton.js';

export default class SettingsPage {
    constructor() {
        this.name = 'settings';
        this.preferences = {};
    }

    async loadPreferences() {
        try {
            const response = await fetch('/api/settings/preferences');
            const result = await response.json();
            if (result.success) {
                this.preferences = result.preferences;
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
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-gray-900 dark:text-white">Automatic Backups</p>
                                        <p class="text-sm text-gray-500 dark:text-gray-400">Backup files automatically when changes are detected and launch at startup</p>
                                    </div>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" ${this.preferences.automatic_backups ? 'checked' : ''} id="auto-backup-toggle">
                                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary"></div>
                                    </label>
                                </div>
                                
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-gray-900 dark:text-white">Cloud Sync</p>
                                        <p class="text-sm text-gray-500 dark:text-gray-400">Sync backups to cloud storage</p>
                                    </div>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" ${this.preferences.cloud_sync ? 'checked' : ''} id="cloud-sync-toggle">
                                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary"></div>
                                    </label>
                                </div>
                                
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-gray-900 dark:text-white">Encryption</p>
                                        <p class="text-sm text-gray-500 dark:text-gray-400">Encrypt backup files for security</p>
                                    </div>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" ${this.preferences.encryption ? 'checked' : ''} id="encryption-toggle">
                                        <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary"></div>
                                    </label>
                                </div>
                            </div>
                        </div>
                        
                        <div class="flex justify-end gap-3">
                            <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors" id="cancel-settings">
                                Cancel
                            </button>
                            <button class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-blue-600 transition-colors" id="save-settings">
                                Save Changes
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    afterRender() {
        console.log('Settings page initialized');
        
        // Add event listeners for toggle switches
        const toggles = document.querySelectorAll('input[type="checkbox"]');
        toggles.forEach(toggle => {
            toggle.addEventListener('change', (e) => {
                console.log(`Toggle changed: ${e.target.id} = ${e.target.checked}`);
            });
        });
        
        // Cancel button
        const cancelButton = document.getElementById('cancel-settings');
        if (cancelButton) {
            cancelButton.addEventListener('click', () => {
                console.log('Cancelling settings changes');
                window.history.back();
            });
        }
        
        // Save button
        const saveButton = document.getElementById('save-settings');
        if (saveButton) {
            saveButton.addEventListener('click', () => {
                this.saveSettings();
            });
        }
    }

    async saveSettings() {
        console.log('Saving settings...');
        
        // Get all toggle values
        const settings = {
            automatic_backups: document.getElementById('auto-backup-toggle')?.checked || false,
            cloud_sync: document.getElementById('cloud-sync-toggle')?.checked || false,
            encryption: document.getElementById('encryption-toggle')?.checked || false
        };
        
        console.log('Settings to save:', settings);
        
        try {
            const response = await fetch('/api/settings/preferences', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(settings)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showNotification('Settings saved successfully!', 'success');
                setTimeout(() => {
                    window.history.back();
                }, 1500);
            } else {
                this.showNotification('Failed to save settings: ' + result.error, 'error');
            }
        } catch (error) {
            console.error('Error saving settings:', error);
            this.showNotification('Error saving settings: ' + error.message, 'error');
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-4 py-2 rounded-md shadow-lg z-50 flex items-center gap-2 ${
            type === 'info' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300' :
            type === 'success' ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300' :
            'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
        }`;
        
        notification.innerHTML = `
            <span class="material-icons-round text-sm">
                ${type === 'success' ? 'check_circle' : type === 'info' ? 'info' : 'error'}
            </span>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    destroy() {
        console.log('Cleaning up Settings page');
    }
}
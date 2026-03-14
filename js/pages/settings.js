// src/js/pages/settings.js

import { createLoadingSkeleton } from '../utils/loading-skeleton.js';
import { electronAPI } from '../utils/electron-adapter.js';

export default class SettingsPage {
    constructor() {
        this.name = 'settings';
        this.preferences = {};
    }

    async loadPreferences() {
        try {
            // Use the new endpoint through the adapter so we don't depend on the
            // old `window.electron` global which was never exposed.  The adapter will
            // fall back to fetch when running in a browser.
            const response = await electronAPI.get('/api/settings/preferences');
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
        
        // ensure theme default
        if (!this.preferences.theme) {
            this.preferences.theme = 'system';
        }

        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark">
                <div>
                    <h1 class="text-2xl font-bold text-[var(--color-text-primary)] dark:text-white leading-tight">Settings</h1>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Configure your backup preferences and application settings.</p>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark p-8">
                <div class="max-w-3xl mx-auto">
                    <div class="space-y-6">
                        <div class="bg-[var(--color-system-background)] dark:bg-[var(--color-gray-800)] rounded-xl shadow-sm border border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] p-6">
                            <h2 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-4">Backup Settings</h2>
                            <div class="space-y-4">
                                <!-- Automatic Backups -->
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-[var(--color-text-primary)] dark:text-white">Automatic Backups</p>
                                        <p class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Enable or disable automatic backups when file changes are detected.</p>
                                    </div>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" ${this.preferences.automatic_backups ? 'checked' : ''} id="auto-backup-toggle">
                                        <div class="w-11 h-6 bg-[var(--color-gray-200)] peer-focus:outline-none rounded-full peer dark:bg-[var(--color-gray-700)] peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-[var(--color-system-background)] after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                                    </label>
                                </div>
                                
                                <!-- Theme selection -->
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-[var(--color-text-primary)] dark:text-white">Theme</p>
                                        <p class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Choose light mode, dark mode, or follow your system.</p>
                                    </div>
                                    <div class="flex items-center gap-2 text-sm">
                                        <label class="inline-flex items-center">
                                            <input type="radio" name="theme" value="light" ${this.preferences.theme === 'light' ? 'checked' : ''} class="mr-1">
                                            Light
                                        </label>
                                        <label class="inline-flex items-center">
                                            <input type="radio" name="theme" value="dark" ${this.preferences.theme === 'dark' ? 'checked' : ''} class="mr-1">
                                            Dark
                                        </label>
                                        <label class="inline-flex items-center">
                                            <input type="radio" name="theme" value="system" ${this.preferences.theme === 'system' ? 'checked' : ''} class="mr-1">
                                            System
                                        </label>
                                    </div>
                                </div>

                                <!-- Cloud Sync -->
                                <div class="flex items-center justify-between">
                                    <div>
                                        <p class="font-medium text-[var(--color-text-primary)] dark:text-white">Cloud Sync</p>
                                        <p class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Sync backups to cloud storage (feature not implemented).</p>
                                    </div>
                                    <label class="relative inline-flex items-center cursor-pointer">
                                        <input type="checkbox" class="sr-only peer" ${this.preferences.cloud_sync ? 'checked' : ''} id="cloud-sync-toggle" disabled>
                                        <div class="w-11 h-6 bg-[var(--color-gray-200)] rounded-full peer dark:bg-[var(--color-gray-700)] peer-checked:after:translate-x-full after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-[var(--color-system-background)] after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary opacity-50 cursor-not-allowed"></div>
                                    </label>
                                </div>
                            </div>
                        </div>
                        

                        <div class="flex justify-end gap-3">
                            <button class="px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] bg-[var(--color-gray-100)] dark:bg-[var(--color-gray-700)] rounded-lg hover:bg-[var(--color-gray-200)] dark:hover:bg-[var(--color-gray-600)]" id="cancel-settings">
                                Cancel
                            </button>
                            <button class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-[var(--color-accent)]" id="save-settings">
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
// backend expects the following keys; autostart is handled in tandem with
        // automatic_backups and no longer has its own toggle.
            const settings = {
            automatic_backups: document.getElementById('auto-backup-toggle')?.checked || false,
            cloud_sync: document.getElementById('cloud-sync-toggle')?.checked || false,
            theme: document.querySelector('input[name="theme"]:checked')?.value || 'system'
        };
        
        try {
            // Use the new endpoint
            const result = await electronAPI.post('/api/settings/preferences', settings);
            if (result && result.success) {
                // update local preferences and notify user
                    this.preferences = result.preferences || {};
                    // apply theme immediately if changed
                    if (this.preferences.theme && window.applyTheme) {
                        window.applyTheme(this.preferences.theme);
                    }
                    if (window && typeof window.showToast === 'function') {
                        window.showToast(result.message || 'Settings saved', 'success', 3000);
                    }
            } else {
                const errMsg = result && result.error ? result.error : 'Unknown error';
                    if (window && typeof window.showToast === 'function') {
                        window.showToast(`Error saving settings: ${errMsg}`, 'error', 4000);
                    }
            }
        } catch (error) {
            this.showNotification(`Error saving settings: ${error.message}`, 'error');
        }
    }

    showNotification(message, type = 'info') {
        // copied from sidebar.js for consistency
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2 ${
            type === 'success' ? 'bg-[var(--color-status-success-bg)] text-[var(--color-status-success)] border border-[var(--color-status-success-bg)] dark:bg-[var(--color-status-success-bg-dark)]/30 dark:text-[var(--color-status-success-dark)] dark:border-[var(--color-status-success-dark)]' :
            type === 'error' ? 'bg-[var(--color-status-error-bg)] text-[var(--color-status-error)] border border-[var(--color-status-error)] dark:bg-[var(--color-status-error-bg-dark)] dark:text-[var(--color-status-error-dark)] dark:border-[var(--color-status-error-dark)]' :
            'bg-[var(--color-accent-light)] text-[var(--color-accent)] border border-[var(--color-accent)] dark:bg-[var(--color-accent-light)] dark:text-[var(--color-accent)] dark:border-[var(--color-accent)]'
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
        // Use global notification system (window.showToast) which renders top-center

    destroy() {
        // Cleanup if needed
    }
}

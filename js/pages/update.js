// src/js/pages/update.js

import { electronAPI } from '../utils/electron-adapter.js';

export default class UpdatePage {
    constructor() {
        this.name = 'update';
        this.info = null;
    }

    async loadUpdateInfo() {
        try {
            const resp = await fetch('/api/check-for-updates');
            const data = await resp.json();
            if (data.success) {
                this.info = data;
            } else {
                console.error('Failed to fetch update info:', data.error);
            }
        } catch (err) {
            console.error('Error loading update info:', err);
        }
    }

    async render() {
        await this.loadUpdateInfo();

        const info = this.info || {};
        const hasUpdate = info.update_available;
        const notes = info.release_notes || '';
        const releaseUrl = info.release_url || '#';
        let noUpdateMsg = '';
        let errorMsg = '';
        if (!info.success) {
            errorMsg = `<div class="text-center text-red-600 dark:text-red-400">Error: ${info.error}</div>`;
        } else if (!hasUpdate) {
            noUpdateMsg = '<div class="text-center text-gray-600 dark:text-gray-400">You are already running the latest version.</div>';
        }

        return `
            <div class="px-8 py-6 flex items-end justify-between border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">Application Update</h1>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Manage update to the latest version.</p>
                </div>
            </div>
            <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark p-8">
                <div class="max-w-3xl mx-auto space-y-6">
                    <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                        <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Version Information</h2>
                        <div class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                            <div>Current version: <span class="font-medium text-gray-900 dark:text-white">${info.current_version || 'unknown'}</span></div>
                            <div>Latest version: <span class="font-medium text-gray-900 dark:text-white">${info.latest_version || 'unknown'}</span></div>
                            ${hasUpdate ? `<div><a href="${releaseUrl}" target="_blank" id="release-link" class="text-blue-600 dark:text-blue-400 underline">View release notes</a></div>` : ''}
                        </div>
                    </div>

                    ${hasUpdate ? `
                        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Release Notes</h2>
                            <div class="prose dark:prose-invert text-gray-700 dark:text-gray-300 max-w-none">
                                ${notes.replace(/\n/g, '<br>')}
                            </div>
                        </div>
                    ` : ''}

                    ${errorMsg || noUpdateMsg}
                    <div class="flex justify-end gap-3">
                        <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600" id="back-btn">
                            Back
                        </button>
                        ${hasUpdate ? `<button class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-lg hover:bg-blue-600" id="update-now-btn">Update Now</button>` : ''}
                    </div>
                </div>
            </div>
        `;
    }

    afterRender() {
        const backBtn = document.getElementById('back-btn');
        if (backBtn) backBtn.addEventListener('click', () => window.history.back());

        const updateBtn = document.getElementById('update-now-btn');
        if (updateBtn) {
            updateBtn.addEventListener('click', () => this.performUpdate());
        }
    }

    async performUpdate() {
        try {
            const response = await fetch('/api/update/perform', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const result = await response.json();
            if (result.success) {
                window.showToast('Update applied successfully, restarting...', 'success', 5000);
                setTimeout(() => {
                    // quit whole app (closes main + update window)
                    electronAPI.quit();
                }, 3000);
            } else {
                window.showToast(`Update failed: ${result.error}`, 'error');
            }
        } catch (err) {
            window.showToast('Error during update.', 'error');
            console.error('performUpdate error', err);
        }
    }

    destroy() {
        // nothing special yet
    }
}

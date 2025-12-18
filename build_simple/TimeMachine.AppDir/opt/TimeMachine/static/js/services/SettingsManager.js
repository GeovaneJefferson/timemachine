/**
 * Manages application settings
 */

export class SettingsManager {
    constructor(state, api, eventBus) {
        this.state = state;
        this.api = api;
        this.eventBus = eventBus;
    }

    async loadSettings() {
        try {
            const data = await this.api.getBackupFolders();

            if (data.success) {
                this.state.settings.watchedFolders = data.folders;
                this.state.settings.homeFolders = data.folders.map(folder => ({
                    ...folder,
                    selected: folder.selected || false
                }));

                this.renderFolderList();
                this.updateSummaryText();
            }
        } catch (error) {
            console.error('[SettingsManager] Failed to load settings:', error);
        }
    }

    renderFolderList() {
        const container = document.getElementById('folder-selection-list');
        if (!container) return;

        container.innerHTML = '';

        this.state.settings.homeFolders.forEach((folder, index) => {
            const folderElement = this.createFolderElement(folder, index);
            container.appendChild(folderElement);
        });
    }

    createFolderElement(folder, index) {
        const element = document.createElement('div');
        element.className = 'flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors';

        element.innerHTML = `
        <div class="flex items-center gap-4">
        <div class="w-10 h-10 rounded-lg bg-gray-100 dark:bg-white/10 text-main flex items-center justify-center">
        <i class="bi ${folder.icon || 'bi-folder'}"></i>
        </div>
        <div>
        <h5 class="text-sm font-bold text-main">${folder.name}</h5>
        <p class="text-xs text-muted font-mono">${folder.path}</p>
        </div>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
        <input type="checkbox" class="sr-only peer folder-toggle"
        data-index="${index}" ${folder.selected ? 'checked' : ''}>
        <div class="checkbox-normal"></div>
        </label>
        `;

        return element;
    }

    toggleFolder(index) {
        if (this.state.settings.homeFolders[index]) {
            this.state.settings.homeFolders[index].selected =
            !this.state.settings.homeFolders[index].selected;

            this.renderFolderList();
            this.updateSummaryText();
        }
    }

    toggleAllFolders(selected) {
        this.state.settings.homeFolders.forEach(folder => {
            folder.selected = selected;
        });

        this.renderFolderList();
        this.updateSummaryText();
    }

    updateSummaryText() {
        const selectedCount = this.state.settings.homeFolders.filter(f => f.selected).length;
        const element = document.getElementById('backup-summary-text');

        if (element) {
            element.textContent = `${selectedCount} folders selected for monitoring`;
        }
    }

    async saveSettings() {
        const selectedPaths = this.state.settings.homeFolders
        .filter(f => f.selected)
        .map(f => f.path);

        try {
            const result = await this.api.saveBackupFolders(selectedPaths);

            if (result.success) {
                this.eventBus.emit('notification:show', {
                    type: 'success',
                    title: 'Settings Saved',
                    message: 'Backup configuration updated successfully.'
                });
            } else {
                throw new Error(result.error || 'Save failed');
            }
        } catch (error) {
            console.error('[SettingsManager] Failed to save settings:', error);
            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Save Failed',
                message: error.message
            });
        }
    }

    toggleGeneralSetting(key) {
        switch (key) {
            case 'updates':
                this.state.settings.general.autoUpdates =
                document.getElementById('chk-auto-updates')?.checked || false;
                break;
            case 'notifications':
                this.state.settings.general.showNotifications =
                document.getElementById('chk-show-notifications')?.checked || false;
                break;
            case 'startup':
                this.state.settings.general.autoStartup =
                document.getElementById('chk-auto-startup')?.checked || false;
                break;
        }

        this.saveGeneralSettings();
    }

    saveGeneralSettings() {
        try {
            localStorage.setItem('timeMachine_generalSettings',
                                 JSON.stringify(this.state.settings.general));

            console.log('[SettingsManager] General settings saved:', this.state.settings.general);
        } catch (error) {
            console.error('[SettingsManager] Failed to save general settings:', error);
        }
    }

    loadGeneralSettings() {
        try {
            const saved = localStorage.getItem('timeMachine_generalSettings');
            if (saved) {
                const parsed = JSON.parse(saved);
                this.state.settings.general = { ...this.state.settings.general, ...parsed };

                // Update checkboxes
                const startupCheckbox = document.getElementById('chk-auto-startup');
                const updatesCheckbox = document.getElementById('chk-auto-updates');
                const notificationsCheckbox = document.getElementById('chk-show-notifications');

                if (startupCheckbox) startupCheckbox.checked = this.state.settings.general.autoStartup;
                if (updatesCheckbox) updatesCheckbox.checked = this.state.settings.general.autoUpdates;
                if (notificationsCheckbox) notificationsCheckbox.checked = this.state.settings.general.showNotifications;
            }
        } catch (error) {
            console.log('[SettingsManager] No saved general settings found');
        }
    }

    switchSettingsTab(tabName) {
        this.state.navigation.activeSettingsTab = tabName;

        ['folders', 'general'].forEach(t => {
            const btn = document.getElementById(`sub-tab-btn-${t}`);
            const content = document.getElementById(`settings-tab-${t}`);

            if (!btn || !content) return;

            if (t === tabName) {
                btn.className = "px-4 py-2 text-sm font-bold text-hyperlink border-b-2 cursor-pointer border-hyperlink";
                content.classList.remove('hidden');
            } else {
                btn.className = "px-4 py-2 text-sm font-bold text-secondary border-b-2 border-transparent hover:text-secondary cursor-pointer";
                content.classList.add('hidden');
            }
        });
    }

    setupEventListeners() {
        // Folder toggles
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('folder-toggle')) {
                const index = parseInt(e.target.dataset.index);
                this.toggleFolder(index);
            }
        });

        // Select all/none buttons
        document.addEventListener('click', (e) => {
            if (e.target.id === 'select-all-btn') {
                this.toggleAllFolders(true);
            } else if (e.target.id === 'select-none-btn') {
                this.toggleAllFolders(false);
            }
        });

        // Save settings button
        document.addEventListener('click', (e) => {
            if (e.target.id === 'save-settings-btn') {
                this.initiateSave();
            }
        });

        // General settings toggles
        document.addEventListener('change', (e) => {
            if (e.target.id === 'chk-auto-updates') {
                this.toggleGeneralSetting('updates');
            } else if (e.target.id === 'chk-show-notifications') {
                this.toggleGeneralSetting('notifications');
            } else if (e.target.id === 'chk-auto-startup') {
                this.toggleGeneralSetting('startup');
            }
        });

        // Settings tab navigation
        document.addEventListener('click', (e) => {
            const tabButton = e.target.closest('[data-settings-tab]');
            if (tabButton) {
                const tabName = tabButton.dataset.settingsTab;
                this.switchSettingsTab(tabName);
            }
        });
    }

    initiateSave() {
        const selectedCount = this.state.settings.homeFolders.filter(f => f.selected).length;

        this.eventBus.emit('modal:confirmation:show', {
            title: 'Update Watched Folders?',
            message: `You are about to set <span class="font-bold text-slate-800">${selectedCount} folder${selectedCount !== 1 ? 's' : ''}</span> for continuous, real-time backup. Are you sure?`,
            onConfirm: () => this.saveSettings(),
                           confirmText: 'Save Settings',
                           cancelText: 'Cancel'
        });
    }
}

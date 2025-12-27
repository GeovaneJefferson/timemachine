/**
 * Settings Module
 */

import { state } from './globals.js';
import { showSystemNotification } from './ui-helpers.js';

function renderSettings() {
    const container = document.getElementById('folder-selection-list');
    if (!container) return;

    container.innerHTML = '<div class="p-4 text-center text-slate-500">Scanning home folders...</div>';

    fetch('/api/backup-folders')
    .then(res => res.json())
    .then(data => {
        if (!data.success) {
            container.innerHTML = `<div class="p-4 text-red-500">${data.error}</div>`;
            return;
        }

        state.homeFolders = data.folders;
        renderFolderList();
        updateSummaryText();
        loadGeneralSettings();
    })
    .catch(err => {
        container.innerHTML = '<div class="p-4 text-red-500">Failed to load folders from server.</div>';
    });
}

function renderFolderList() {
    const container = document.getElementById('folder-selection-list');
    if (!container) return;
    container.innerHTML = '';

    if (state.homeFolders.length === 0) {
        return;
    }

    state.homeFolders.forEach((folder, idx) => {
        container.innerHTML += `
        <div class="flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
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
        <input type="checkbox" class="sr-only peer" ${folder.selected ? 'checked' : ''} onchange="toggleFolder(${idx})">
        <div class="checkbox-normal"></div>
        </label>
        </div>
        `;
    });
    updateSummaryText();
}

function toggleFolder(index) {
    if (state.homeFolders[index]) {
        state.homeFolders[index].selected = !state.homeFolders[index].selected;
        updateSummaryText();
    }
}

function updateSummaryText() {
    const count = state.homeFolders.filter(f => f.selected).length;
    const el = document.getElementById('backup-summary-text');
    if(el) el.innerText = `${count} folders selected for monitoring`;
}

function loadGeneralSettings() {
    try {
        const saved = localStorage.getItem('timeMachine_generalSettings');
        if (saved) {
            const parsed = JSON.parse(saved);
            state.generalSettings = { ...state.generalSettings, ...parsed };

            const startupCheckbox = document.getElementById('chk-auto-startup');
            const updatesCheckbox = document.getElementById('chk-auto-updates');
            const notificationsCheckbox = document.getElementById('chk-show-notifications');

            if (startupCheckbox) startupCheckbox.checked = state.generalSettings.autoStartup;
            if (updatesCheckbox) updatesCheckbox.checked = state.generalSettings.autoUpdates;
            if (notificationsCheckbox) notificationsCheckbox.checked = state.generalSettings.showNotifications;
        }
    } catch (error) {
        console.log('No saved general settings found, using defaults.');
    }
}

function toggleGeneralSetting(settingKey) {
    switch(settingKey) {
        case 'updates':
            state.generalSettings.autoUpdates = document.getElementById('chk-auto-updates').checked;
            break;
        case 'notifications':
            state.generalSettings.showNotifications = document.getElementById('chk-show-notifications').checked;
            break;
    }
    console.log('General settings updated:', state.generalSettings);
}

function saveGeneralSettings() {
    const saveBtn = document.querySelector('button[onclick="saveGeneralSettings()"]');
    if (!saveBtn) return;

    const originalText = saveBtn.innerHTML;
    saveBtn.innerHTML = '<i class="bi bi-arrow-clockwise animate-spin"></i> Saving...';
    saveBtn.disabled = true;

    setTimeout(() => {
        try {
            localStorage.setItem('timeMachine_generalSettings', JSON.stringify(state.generalSettings));
            showSystemNotification('success', 'Settings Saved', 'General preferences have been saved successfully.');
        } catch (error) {
            showSystemNotification('error', 'Save Failed', 'Could not save settings. Please try again.');
        } finally {
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
        }
    }, 800);
}

function switchSettingsTab(tabName) {
    state.activeSettingsTab = tabName;
    ['folders', 'general'].forEach(t => {
        const btn = document.getElementById(`sub-tab-btn-${t}`);
        const content = document.getElementById(`settings-tab-${t}`);
        if (t === tabName) {
            btn.className = "px-4 py-2 text-sm font-bold text-sm font-bold text-hyperlink border-b-2 cursor-pointer border-hyperlink";
            content.classList.remove('hidden');
        } else {
            btn.className = "px-4 py-2 text-sm font-bold text-secondary border-b-2 border-transparent hover:text-secondary hover:text-secondary cursor-pointer";
            content.classList.add('hidden');
        }
    });
}

export { renderSettings, toggleFolder, updateSummaryText, loadGeneralSettings, toggleGeneralSetting, saveGeneralSettings, switchSettingsTab };

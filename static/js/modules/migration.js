/**
 * Migration Assistant Module
 */

import { state } from './globals.js';
import { migrationData } from './globals.js';
import { showSystemNotification } from './ui-helpers.js';

let selectedSource = null;

function initMigrationView() {
    document.getElementById('mig-step-1-source').classList.remove('hidden');
    document.getElementById('mig-step-2-content').classList.add('hidden');
    document.getElementById('mig-step-3-progress').classList.add('hidden');
    document.getElementById('mig-step-desc').innerText = "Select a source to start the restoration process.";
    renderSourceList();
}

function renderSourceList() {
    const container = document.getElementById('mig-source-list');
    if (!container) return;

    container.innerHTML = `
    <div class="text-center py-10 text-muted">
    <i class="bi bi-arrow-clockwise animate-spin text-2xl mb-2"></i>
    <p class="text-sm">Scanning for backup sources...</p>
    </div>
    `;

    fetch('/api/migration/sources')
    .then(res => res.json())
    .then(data => {
        container.innerHTML = '';
        if (!data.success || !data.sources || data.sources.length === 0) {
            container.innerHTML = `
            <div class="text-center p-10 border-2 border-dashed border-main rounded-2xl text-muted">
            <i class="bi bi-hdd-network-off text-4xl mb-3"></i>
            <h4 class="font-bold text-main">No Backup Sources Found</h4>
            <p class="text-sm mt-1">Connect a drive with a Time Machine backup and try again.</p>
            </div>`;
            return;
        }

        data.sources.forEach(device => {
            const device_name = device.mount_point.split('/').pop();
            const totalGB = Math.round((device.total || 0) / (1024**3));
            const card = `
            <div onclick='selectSource(${JSON.stringify(device).replace(/'/g, "\\'")})' class="bg-card border border-main rounded-2xl p-5 flex items-center gap-5 hover:border-brand-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer transition-all group">
            <div class="w-16 h-16 rounded-xl bg-blue-50 dark:bg-blue-900/20 text-blue-500 flex items-center justify-center text-3xl border border-main">
            <i class="bi bi-usb-drive-fill"></i>
            </div>
            <div class="flex-1">
            <h4 class="font-bold text-main text-lg">${device_name}</h4>
            <p class="text-xs text-muted">${device.filesystem} • ${totalGB} GB</p>
            </div>
            <i class="bi bi-chevron-right text-muted text-xl opacity-0 group-hover:opacity-100 transition-opacity"></i>
            </div>
            `;
            container.innerHTML += card;
        });
    });
}

function selectSource(device) {
    if (!device) return;
    selectedSource = device;

    document.getElementById('mig-step-1-source').classList.add('hidden');
    document.getElementById('mig-step-2-content').classList.remove('hidden');
    document.getElementById('mig-step-desc').innerText = "Step 2 of 3: Choose what to restore from the backup.";

    state.migSelectionState.home = false;
    state.migSelectionState.flatpaks = false;
    state.migSelectionState.installers = false;

    document.getElementById('desc-flatpaks').innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-1"></i> Scanning...';
    document.getElementById('desc-installers').innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-1"></i> Scanning...';

    setTimeout(() => {
        state.migSelectionState.home = true;
        state.migSelectionState.flatpaks = true;
        state.migSelectionState.installers = true;
    }, 800);
}

function toggleMigrationItem(key) {
    state.migSelectionState[key] = !state.migSelectionState[key];
    updateMigrationsContentUI();
}

function updateMigrationsContentUI() {
    ['home', 'flatpaks', 'installers'].forEach(key => {
        const card = document.getElementById(`mig-card-${key}`);
        const check = document.getElementById(`check-${key}`);
        const desc = document.getElementById(`desc-${key}`);
        const isActive = state.migSelectionState[key];
        const list = migrationData[key];
        const selectedCount = list.filter(i => i.selected).length;

        if (key === 'home' && isActive && desc) desc.innerText = "Calculated: 142 GB";
        else if (key === 'flatpaks' && desc) desc.innerText = `${selectedCount}/${list.length} Apps selected`;
        else if (key === 'installers' && desc) desc.innerText = `${selectedCount}/${list.length} Files selected`;

        if (isActive) {
            card.classList.add('bg-blue-50', 'dark:bg-blue-900/20', 'border-blue-500', 'dark:border-blue-400', 'shadow-md');
            card.classList.remove('bg-card', 'border', 'border-main');
            if (check) check.classList.remove('opacity-0', 'scale-75');
        } else {
            card.classList.remove('bg-blue-50', 'dark:bg-blue-900/20', 'border-blue-500', 'dark:border-blue-400', 'shadow-md');
            card.classList.add('bg-card', 'border', 'border-main');
            if (check) check.classList.add('opacity-0', 'scale-75');
        }
    });
    updateRestoreButton();
}

export { initMigrationView, renderSourceList, selectSource, toggleMigrationItem, updateMigrationsContentUI };

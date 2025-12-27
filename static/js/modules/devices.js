/**
 * @file devices.js
 * @description Device management - scanning, selection, and rendering
 */

import { state } from './globals.js';
import { Utils } from './utils.js';
import { showSystemNotification } from './ui-helpers.js';
import { BackupManager } from './dashboard.js';
import { openConfirmationModal } from './modals.js';

// =====================================================================
// --- DEVICE MANAGER ---
// =====================================================================

export const DeviceManager = {
    load: () => {
        const container = document.getElementById('device-list-container');
        if (!container) return;

        container.innerHTML = `
        <div class="col-span-full flex flex-col items-center justify-center py-12 text-muted">
        <i class="bi bi-arrow-clockwise animate-spin text-2xl mb-2"></i>
        <p>Scanning sources...</p>
        </div>`;

        Promise.all([
            fetch('/api/storage/devices').then(res => res.json()),
                    fetch('/api/config').then(res => res.json())
        ])
        .then(([devicesData, configData]) => {
            if (!devicesData.success || !devicesData.devices || devicesData.devices.length === 0) {
                DeviceManager.render([]);
                return;
            }

            const activePath = configData?.DEVICE_INFO?.path;

            const updatedDevices = devicesData.devices.map(device => {
                return {
                    ...device,
                    isActive: device.mount_point === activePath
                }
            });

            DeviceManager.render(updatedDevices);
        })
        .catch(error => {
            console.error("Failed to load devices or config:", error);
            DeviceManager.render([]);
        });
    },

    render: (devices) => {
        const container = document.getElementById('device-list-container');
        if (!container) return;
        container.innerHTML = '';

        if (devices.length === 0) {
            container.innerHTML = `
            <div class="col-span-full border-2 border-dashed border-main rounded-2xl p-10 text-center">
            <i class="bi bi-hdd text-4xl text-muted mb-3 block"></i>
            <h4 class="font-bold text-main">No Devices Found</h4>
            <p class="text-sm text-muted">Connect a USB drive to get started.</p>
            </div>`;
            return;
        }

        devices.forEach(device => {
            const usedGB = Math.round((device.used || 0) / (1024**3));
            const totalGB = Math.round((device.total || 0) / (1024**3));
            const percent = totalGB > 0 ? Math.round((usedGB / totalGB) * 100) : 0;
            const isSSD = device.is_ssd;

            const isActive = device.isActive;
            const statusColor = isActive ? 'text-emerald-500' : 'text-muted';
            const statusText = isActive ? 'Active' : 'Ready';
            const borderClass = isActive ? 'border-emerald-500 ring-1 ring-emerald-500' : 'border-main hover:border-brand-300';

            const deviceId = device.id || Math.random().toString(36).substr(2, 9);

            const card = `
            <div class="bg-card p-6 rounded-2xl border ${borderClass} group cursor-pointer transition-all duration-200" data-device-id="${deviceId}">
            <div class="flex items-start justify-between mb-4">
            <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-xl bg-gray-50 dark:bg-white/5 flex items-center justify-center text-xl text-main">
            ${isSSD
                ? '<i class="bi bi-device-ssd-fill"></i>'
                : '<i class="bi bi-hdd-fill"></i>'
            }
            </div>
            <div>
            <h4 class="font-bold text-main text-base">${device.label || device.name || 'Unnamed Drive'}</h4>
            <div class="flex items-center gap-1.5 mt-0.5">
            <span class="w-1.5 h-1.5 rounded-full ${isActive ? 'bg-emerald-500' : 'bg-gray-400'}"></span>
            <span class="text-xs font-medium ${statusColor}">${statusText}</span>
            </div>
            </div>
            </div>
            </div>

            <div class="mb-4">
            <div class="flex justify-between text-xs font-medium text-secondary mb-2">
            <span>${usedGB} GB Used</span>
            <span>${totalGB} GB Total</span>
            </div>
            <div class="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-2 overflow-hidden">
            <div class="h-full bg-brand-500 rounded-full" style="width: ${percent}%"></div>
            </div>
            </div>

            ${isActive
                ? `<button disabled class="w-full py-2 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center justify-center gap-2"><i class="bi bi-check-circle-fill"></i> Backup Location</button>`
                : `<button onclick="handleDeviceSelection('${deviceId}')" class="w-full py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main text-xs font-bold transition cursor-pointer">Set as Backup</button>`
            }
            </div>`;
            container.innerHTML += card;

            if (!window.deviceMap) window.deviceMap = {};
            window.deviceMap[deviceId] = device;
        });
    },

    selectDevice: async (device) => {
        console.log("Selecting device:", device);

        try {
            const response = await fetch('/api/backup/select-device', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    device_info: device
                })
            });

            const result = await response.json();

            if (result.success) {
                console.log('Device configured successfully:', result.path);
                showSystemNotification('success', 'Device Configured', `${device.name} is now your backup device.`);

                DeviceManager.load();
                BackupManager.updateUsage();
            } else {
                throw new Error(result.error || 'Server rejected the selection.');
            }

        } catch (error) {
            console.error('Network error during device selection:', error);
            showSystemNotification('error', 'Configuration Failed', error.message || 'Could not connect to server.');
        }
    }
};

// =====================================================================
// --- DEVICE SELECTION HANDLER ---
// =====================================================================

export function handleDeviceSelection(deviceId) {
    if (!window.deviceMap || !window.deviceMap[deviceId]) {
        console.error('Device not found:', deviceId);
        showSystemNotification('error', 'Device Error', 'Could not find device information.');
        return;
    }

    const device = window.deviceMap[deviceId];
    useThisBackupDevice(device);
}

export function useThisBackupDevice(device) {
    console.log("Device object for selection:", device);

    if (!device || !device.mount_point) {
        showSystemNotification('error', 'Invalid Device', 'Device information is incomplete.');
        return;
    }

    const deviceInfo = {
        ...device,
        total: parseInt(device.total || device.total_size || 0),
        used: parseInt(device.used || 0),
        free: parseInt(device.free || 0),
        is_ssd: Boolean(device.is_ssd)
    };

    openConfirmationModal(
        "Set Backup Device?",
        `Are you sure you want to set <span class="font-bold text-main">${device.label || device.name || 'this device'}</span> as your backup destination?`,
        async () => {
            try {
                const response = await fetch('/api/backup/select-device', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        device_info: deviceInfo
                    })
                });

                const result = await response.json();

                if (result.success) {
                    DeviceManager.load();
                    BackupManager.updateUsage();

                    showSystemNotification('success', 'Device Configured',
                                           `${device.label || device.name} is now your backup device.`);

                    try {
                        const creationResponse = await fetch('/api/base-folders-creation', {
                            method: 'GET'
                        });

                        const creation = await creationResponse.json();
                        if (!creation.success) {
                            showSystemNotification('error', 'Error', `Failed to create base folders: ${creation.error || 'Unknown error'}`);
                        }
                    } catch (error) {
                        console.error('Error during folder creation fetch:', error);
                    }

                } else {
                    throw new Error(result.error || 'Server rejected the selection.');
                }

            } catch (error) {
                console.error('Network error during device selection:', error);
                showSystemNotification('error', 'Configuration Failed',
                                       error.message || 'Could not connect to server.');
            }
        }
    );
}

export function refreshDevices() {
    const container = document.getElementById('device-list-container');
    if(container) {
        container.innerHTML = `
        <div class="col-span-3 bg-white p-10 rounded-xl border border-gray-200 shadow-sm flex flex-col items-center justify-center text-center">
        <i class="bi bi-arrow-clockwise animate-spin text-2xl text-brand-500 mb-3"></i>
        <p class="text-sm text-brand-600 font-medium">Scanning for new devices...</p>
        </div>`;
        DeviceManager.load();
    }
}

// Make functions globally available
window.handleDeviceSelection = handleDeviceSelection;
window.useThisBackupDevice = useThisBackupDevice;
window.refreshDevices = refreshDevices;

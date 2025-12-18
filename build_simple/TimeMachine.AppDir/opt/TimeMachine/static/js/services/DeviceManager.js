/**
 * Manages device operations and device listing
 */

export class DeviceManager {
    constructor(state, api, eventBus) {
        this.state = state;
        this.api = api;
        this.eventBus = eventBus;
    }

    async loadDevices() {
        try {
            const [devicesData, configData] = await Promise.all([
                this.api.getDevices(),
                                                                this.api.getConfig()
            ]);

            if (!devicesData.success || !devicesData.devices?.length) {
                this.renderNoDevices();
                return;
            }

            const activePath = configData?.DEVICE_INFO?.path;
            const updatedDevices = devicesData.devices.map(device => ({
                ...device,
                isActive: device.mount_point === activePath
            }));

            this.state.devices.list = updatedDevices;
            this.renderDevices(updatedDevices);
        } catch (error) {
            console.error('[DeviceManager] Failed to load devices:', error);
            this.renderError(error);
        }
    }

    renderDevices(devices) {
        const container = document.getElementById('device-list-container');
        if (!container) return;

        container.innerHTML = '';

        devices.forEach(device => {
            const card = this.createDeviceCard(device);
            container.appendChild(card);
        });
    }

    createDeviceCard(device) {
        const usedGB = Math.round((device.used || 0) / (1024 ** 3));
        const totalGB = Math.round((device.total || 0) / (1024 ** 3));
        const percent = totalGB > 0 ? Math.round((usedGB / totalGB) * 100) : 0;
        const isActive = device.isActive;
        const isSSD = device.is_ssd;

        const card = document.createElement('div');
        card.className = `bg-card p-6 rounded-2xl border ${
            isActive ? 'border-emerald-500 ring-1 ring-emerald-500' : 'border-main hover:border-brand-300'
        } group cursor-pointer transition-all duration-200`;
        card.dataset.deviceId = device.id || Math.random().toString(36).substr(2, 9);

        card.innerHTML = `
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
        <span class="text-xs font-medium ${isActive ? 'text-emerald-500' : 'text-muted'}">
        ${isActive ? 'Active' : 'Ready'}
        </span>
        </div>
        </div>
        </div>
        </div>
        <div class="mb-4">
        <div class="flex justify-between text-xs font-medium text-muted mb-2">
        <span>${usedGB} GB Used</span>
        <span>${totalGB} GB Total</span>
        </div>
        <div class="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-2 overflow-hidden">
        <div class="h-full bg-brand-500 rounded-full" style="width: ${percent}%"></div>
        </div>
        </div>
        ${
            isActive
            ? `<button disabled class="w-full py-2 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center justify-center gap-2">
            <i class="bi bi-check-circle-fill"></i> Backup Location
            </button>`
            : `<button class="device-select-btn w-full py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main text-xs font-bold transition cursor-pointer"
            data-device-id="${card.dataset.deviceId}">
            Set as Backup
            </button>`
        }
        `;

        return card;
    }

    async selectDevice(device) {
        try {
            const result = await this.api.selectDevice(device);

            if (result.success) {
                this.eventBus.emit('notification:show', {
                    type: 'success',
                    title: 'Device Configured',
                    message: `${device.label || device.name} is now your backup device`
                });

                // Refresh devices list
                await this.loadDevices();

                // Refresh backup usage
                this.eventBus.emit('backup:refreshUsage');

                // Create base folders
                await this.createBaseFolders();
            } else {
                throw new Error(result.error || 'Server rejected the selection');
            }
        } catch (error) {
            console.error('[DeviceManager] Device selection failed:', error);
            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Configuration Failed',
                message: error.message
            });
        }
    }

    async createBaseFolders() {
        try {
            const response = await fetch('/api/base-folders-creation');
            const data = await response.json();

            if (data.success) {
                console.log('[DeviceManager] Base folders created successfully');
            } else {
                console.warn('[DeviceManager] Failed to create base folders:', data.error);
            }
        } catch (error) {
            console.error('[DeviceManager] Folder creation error:', error);
        }
    }

    renderNoDevices() {
        const container = document.getElementById('device-list-container');
        if (container) {
            container.innerHTML = `
            <div class="col-span-full border-2 border-dashed border-main rounded-2xl p-10 text-center">
            <i class="bi bi-hdd text-4xl text-muted mb-3 block"></i>
            <h4 class="font-bold text-main">No Devices Found</h4>
            <p class="text-sm text-muted">Connect a USB drive to get started.</p>
            </div>`;
        }
    }

    renderError(error) {
        const container = document.getElementById('device-list-container');
        if (container) {
            container.innerHTML = `
            <div class="col-span-3 text-center py-10 border-2 border-red-100 dark:border-red-900/30 bg-red-50 dark:bg-red-900/10 rounded-xl">
            <i class="bi bi-exclamation-triangle text-red-400 text-3xl mb-2 block"></i>
            <div class="text-red-600 dark:text-red-400 font-bold">Error loading devices</div>
            <div class="text-sm text-red-500 dark:text-red-300 mt-1">${error.message || 'Connection failed'}</div>
            </div>`;
        }
    }

    setupEventListeners() {
        // Device selection
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('device-select-btn')) {
                const deviceId = e.target.dataset.deviceId;
                const device = this.state.devices.list.find(d =>
                d.id === deviceId ||
                d.id === e.target.closest('[data-device-id]')?.dataset.deviceId
                );

                if (device) {
                    this.eventBus.emit('device:selected', device);
                }
            }
        });
    }
}

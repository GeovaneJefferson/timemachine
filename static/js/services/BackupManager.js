/**
 * Manages backup operations and status
 */

import { FileUtils } from '../utils/FileUtils.js';

export class BackupManager {
    constructor(state, api, eventBus) {
        this.state = state;
        this.api = api;
        this.eventBus = eventBus;
    }

    async checkConnection() {
        try {
            const data = await this.api.checkConnection();
            const wasConnected = this.state.connection.isDeviceConnected;
            const isConnectedNow = data.connected;

            this.state.updateConnectionStatus(isConnectedNow);

            // Update UI indicators
            this.updateConnectionUI(isConnectedNow);

            // Handle state transitions
            if (this.state.navigation.currentTab === 'files') {
                if (wasConnected !== isConnectedNow) {
                    this.eventBus.emit('files:connectionChanged', {
                        wasConnected,
                        isConnected: isConnectedNow
                    });
                }
            }
        } catch (error) {
            console.error('[BackupManager] Connection check failed:', error);
            this.state.updateConnectionStatus(false);
            this.updateConnectionUI(false);
        }
    }

    updateConnectionUI(isConnected) {
        const staticDot = document.getElementById('devices-connection-ping');
        const pingAnimation = document.getElementById('devices-connection-ping-animation');

        if (!staticDot || !pingAnimation) return;

        if (isConnected) {
            staticDot.classList.replace('status-dot-disconnected', 'status-dot-connected');
            pingAnimation.classList.replace('animate-ping-disconnected', 'animate-ping-connected');
        } else {
            staticDot.classList.replace('status-dot-connected', 'status-dot-disconnected');
            pingAnimation.classList.replace('animate-ping-connected', 'animate-ping-disconnected');
        }
    }

    async updateUsage() {
        try {
            const data = await this.api.getBackupUsage();

            if (data.success) {
                this.updateUsageUI(data);

                // Update file counts if available
                if (data.summary?.categories) {
                    this.updateFileCounts(data.summary.categories);
                }
            }
        } catch (error) {
            console.error('[BackupManager] Failed to update usage:', error);
        }
    }

    updateUsageUI(data) {
        // Update backup usage text
        const usageElement = document.getElementById('backup-usage');
        const usagePercentElement = document.getElementById('backup-usage-percent');
        const locationElement = document.getElementById('backup-location-path');

        if (usageElement) {
            usageElement.textContent =
            `${data.human_used} Used / ${data.human_total} (${data.percent_used}% used)`;
        }

        if (usagePercentElement) {
            usagePercentElement.textContent = `${data.percent_used}%`;
        }

        if (locationElement) {
            locationElement.textContent = data.location || '';
        }
    }

    updateFileCounts(categories) {
        const imageCount = document.getElementById('files-images-count');
        const videoCount = document.getElementById('files-videos-count');
        const documentCount = document.getElementById('files-documents-count');
        const otherCount = document.getElementById('files-others-count');

        const imageSize = document.getElementById('files-images-size');
        const videoSize = document.getElementById('files-videos-size');
        const documentSize = document.getElementById('files-documents-size');
        const otherSize = document.getElementById('files-others-size');

        categories.forEach(category => {
            switch (category.name.toLowerCase()) {
                case 'image':
                    if (imageCount) imageCount.textContent = `${category.count.toLocaleString()} files`;
                    if (imageSize) imageSize.textContent = category.size_str;
                    break;
                case 'video':
                    if (videoCount) videoCount.textContent = `${category.count.toLocaleString()} files`;
                    if (videoSize) videoSize.textContent = category.size_str;
                    break;
                case 'document':
                    if (documentCount) documentCount.textContent = `${category.count.toLocaleString()} files`;
                    if (documentSize) documentSize.textContent = category.size_str;
                    break;
                case 'others':
                    if (otherCount) otherCount.textContent = `${category.count.toLocaleString()} files`;
                    if (otherSize) otherSize.textContent = category.size_str;
                    break;
            }
        });
    }

    toggleRealtimeBackup() {
        const checkbox = document.getElementById('realTimeCheckbox');
        if (!checkbox) return;

        const isChecked = checkbox.checked;
        checkbox.disabled = true;

        // Optimistic UI update
        this.updateRealtimeStatusUI(isChecked);

        // Send request to backend
        this.updateRealtimeBackupState(isChecked)
        .finally(() => {
            checkbox.disabled = false;
        });
    }

    updateRealtimeStatusUI(isActive) {
        const statusLabel = document.getElementById('realTimeStatusLabel');

        if (statusLabel) {
            if (isActive) {
                statusLabel.classList.replace('text-red-500', 'text-green-500');
                statusLabel.classList.replace('far', 'fas');
                statusLabel.title = "Real-time backup active";
            } else {
                statusLabel.classList.replace('text-green-500', 'text-red-500');
                statusLabel.classList.replace('fas', 'far');
                statusLabel.title = "Real-time backup inactive";
            }
        }
    }

    async updateRealtimeBackupState(isActive) {
        try {
            const response = await fetch('/api/realtime-backup/daemon', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ is_active: isActive })
            });

            const data = await response.json();

            if (data.error) {
                console.error('[BackupManager] Failed to toggle daemon:', data.error);
                this.eventBus.emit('notification:show', {
                    type: 'error',
                    title: 'Daemon Error',
                    message: data.error
                });

                // Revert checkbox
                const checkbox = document.getElementById('realTimeCheckbox');
                if (checkbox) {
                    checkbox.checked = !isActive;
                    this.updateRealtimeStatusUI(!isActive);
                }
            }
        } catch (error) {
            console.error('[BackupManager] Network error:', error);
            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Network Error',
                message: 'Failed to connect to server'
            });

            // Revert checkbox
            const checkbox = document.getElementById('realTimeCheckbox');
            if (checkbox) {
                checkbox.checked = !isActive;
                this.updateRealtimeStatusUI(!isActive);
            }
        }
    }

    setupEventListeners() {
        // Realtime backup toggle
        const realtimeCheckbox = document.getElementById('realTimeCheckbox');
        if (realtimeCheckbox) {
            realtimeCheckbox.addEventListener('change', () => this.toggleRealtimeBackup());
        }

        // Refresh devices button
        const refreshButton = document.getElementById('refresh-devices-btn');
        if (refreshButton) {
            refreshButton.addEventListener('click', () => {
                this.eventBus.emit('devices:refresh');
            });
        }
    }
}

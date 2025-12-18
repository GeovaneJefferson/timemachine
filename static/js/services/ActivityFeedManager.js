/**
 * Manages the activity feed and WebSocket updates
 */

import { FileUtils } from '../utils/FileUtils.js';

export class ActivityFeedManager {
    constructor(state, eventBus) {
        this.state = state;
        this.eventBus = eventBus;
        this.feedContainer = null;
        this.storageKey = 'timemachine_activity_feed';
        this.maxStoredItems = 50;
    }

    init() {
        this.feedContainer = document.querySelector('#live-activities-feed');
        if (!this.feedContainer) {
            console.error('[ActivityFeed] Container not found');
            return;
        }

        this.loadFromStorage();
        this.setupEventListeners();
    }

    loadFromStorage() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                const activities = JSON.parse(stored);
                activities.forEach(activity => {
                    this.addToFeed(activity);
                });
            }
        } catch (error) {
            console.warn('[ActivityFeed] Could not load from storage:', error);
        }
    }

    saveToStorage(activities) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(activities));
        } catch (error) {
            console.warn('[ActivityFeed] Could not save to storage:', error);
        }
    }

    addToFeed(activity) {
        if (!this.feedContainer) return;

        const row = this.createActivityRow(activity);
        this.feedContainer.insertAdjacentHTML('afterbegin', row);

        // Trim old entries
        while (this.feedContainer.children.length > this.state.constants.MAX_TRANSFER_ITEMS) {
            this.feedContainer.removeChild(this.feedContainer.lastChild);
        }

        // Update storage
        this.updateStorage(activity);
    }

    createActivityRow(activity) {
        const { title, description, size, timestamp } = activity;
        const safeDescription = description || "";
        const safeTitle = title || "";

        const fileName = safeDescription.split('/').pop();
        const fileData = FileUtils.getFileIconDetails(fileName);

        // Determine action and color
        let actionLabel = "Processing";
        let actionColorClass = "bg-slate-100 text-slate-700 dark:bg-slate-700/50 text-main";

        if (safeTitle.includes('Backed Up') || safeTitle.includes('Hardlinked')) {
            actionLabel = 'Backed Up';
            actionColorClass = "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400";
        } else if (safeTitle.includes('Modified') || safeTitle.includes('Restoring')) {
            actionLabel = 'Modified';
            actionColorClass = "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400";
        } else if (safeTitle.includes('Moving') || safeTitle.includes('Renamed')) {
            actionLabel = 'Moved';
            actionColorClass = "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400";
        } else if (safeTitle.includes('Deleted')) {
            actionLabel = 'Deleted';
            actionColorClass = "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400";
        }

        const formattedSize = FileUtils.humanFileSize(size || 0);
        const formattedTime = FileUtils.timeSince(timestamp);

        return `
        <tr class="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition">
        <td class="px-6 py-3 flex items-center gap-3">
        <i class="bi ${fileData.iconClass} ${fileData.iconColor} text-main"></i>
        ${fileName}
        </td>
        <td class="px-6 py-3">
        <span class="px-2 py-0.5 ${actionColorClass} rounded text-xs font-bold">${actionLabel}</span>
        </td>
        <td class="px-6 py-3 text-muted">${formattedSize}</td>
        <td class="px-6 py-3">
        <button class="activity-view-snapshots text-hyperlink hover:text-hyperlink dark:hover:text-blue-300 text-xs font-medium transition hover:underline cursor-pointer"
        data-file-name="${fileName}">
        View Snapshots
        </button>
        </td>
        <td class="px-6 py-3 text-right text-muted font-medium text-xs">${formattedTime}</td>
        </tr>
        `;
    }

    updateStorage(newActivity) {
        try {
            const stored = localStorage.getItem(this.storageKey);
            let activities = stored ? JSON.parse(stored) : [];

            activities.unshift(newActivity);
            activities = activities.slice(0, this.maxStoredItems);

            this.saveToStorage(activities);
        } catch (error) {
            console.warn('[ActivityFeed] Could not update storage:', error);
        }
    }

    clearFeed() {
        if (!this.feedContainer) return;

        this.feedContainer.innerHTML = '';

        try {
            localStorage.removeItem(this.storageKey);
        } catch (error) {
            // Ignore
        }

        this.eventBus.emit('notification:show', {
            type: 'info',
            title: 'Feed Cleared',
            message: 'Transfers feed has been cleared.'
        });
    }

    handleMessage(message) {
        if (message.type === 'backup_progress') {
            this.handleBackupProgress(message);
        } else {
            this.addToFeed(message);
        }
    }

    handleBackupProgress(message) {
        const { progress, status, current_file, files_completed, total_files, bytes_processed, total_bytes } = message;

        // Find or create progress container
        let progressContainer = document.getElementById('backup-progress-container');
        if (!progressContainer) {
            progressContainer = this.createProgressContainer();

            // Insert into the overview view
            const firstGrid = document.querySelector('#view-overview .grid-cols-1.lg\\:grid-cols-3');
            if (firstGrid) {
                firstGrid.insertBefore(progressContainer, firstGrid.firstChild);
            }
        }

        // Update progress container
        this.updateProgressContainer(progressContainer, message);

        // Add current file to feed if exists
        if (current_file) {
            const activity = {
                title: this.getActivityTitle(status),
                description: current_file,
                size: bytes_processed || 0,
                timestamp: Date.now()
            };

            this.addToFeed(activity);
        }
    }

    createProgressContainer() {
        const container = document.createElement('div');
        container.id = 'backup-progress-container';
        container.className = 'lg:col-span-2 bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-800 dark:to-slate-800/50 rounded-2xl border border-slate-200 hover:shadow-md transition duration-200 dark:border-slate-700 shadow-sm p-6 relative overflow-hidden';

        container.innerHTML = `
        <div class="absolute top-0 right-0 w-32 h-32 bg-brand-500/5 rounded-full blur-3xl -z-0"></div>
        <div class="relative z-10 space-y-5">
        <div class="flex items-center justify-between">
        <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-blue-50 dark:bg-blue-900/20 rounded-lg flex items-center justify-center flex-shrink-0">
        <i class="bi bi-cloud-check-fill text-blue-600 dark:text-blue-400"></i>
        </div>
        <div>
        <h3 class="font-bold text-main text-lg">Backup Progress</h3>
        <p class="text-xs text-muted capitalize" id="backup-status-label">In Progress</p>
        </div>
        </div>
        <div class="text-right">
        <span class="text-2xl font-bold text-main" id="backup-progress-percent">0%</span>
        <p class="text-xs text-muted">Complete</p>
        </div>
        </div>
        <div>
        <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-4 overflow-hidden shadow-inner">
        <div class="bg-gradient-to-r from-brand-500 via-brand-600 to-brand-700 h-full transition-all duration-500 ease-out rounded-full shadow-lg"
        id="backup-progress-bar" style="width: 0%">
        <div class="h-full bg-white/20 animate-pulse"></div>
        </div>
        </div>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3" id="backup-stats-grid"></div>
        <div id="current-file-container" class="hidden"></div>
        </div>
        `;

        return container;
    }

    updateProgressContainer(container, message) {
        const { progress, status, eta, current_file, files_completed, total_files, bytes_processed, total_bytes } = message;

        const progressPercent = Math.round((progress || 0) * 100);
        const processedMB = (bytes_processed / (1024 * 1024)).toFixed(1);
        const totalMB = (total_bytes / (1024 * 1024)).toFixed(1);

        // Update status label
        const statusLabel = container.querySelector('#backup-status-label');
        if (statusLabel) {
            statusLabel.textContent = status || 'In Progress';
            statusLabel.className = `text-xs ${this.getStatusColorClass(status)} capitalize`;
        }

        // Update progress percentage
        const progressPercentElement = container.querySelector('#backup-progress-percent');
        if (progressPercentElement) {
            progressPercentElement.textContent = `${progressPercent}%`;
        }

        // Update progress bar
        const progressBar = container.querySelector('#backup-progress-bar');
        if (progressBar) {
            progressBar.style.width = `${progressPercent}%`;
        }

        // Update stats grid
        const statsGrid = container.querySelector('#backup-stats-grid');
        if (statsGrid) {
            const speed = bytes_processed > 0 ? (bytes_processed / (1024 * 1024 * 10)).toFixed(1) : '0';

            statsGrid.innerHTML = `
            <div class="bg-white dark:bg-slate-700/50 rounded-lg p-3 border border-slate-200 dark:border-slate-600">
            <p class="text-secondary text-main text-xs font-medium mb-1">Files</p>
            <p class="text-main font-bold text-lg">${files_completed}<span class="text-slate-500 text-sm">/${total_files}</span></p>
            </div>
            <div class="bg-white dark:bg-slate-700/50 rounded-lg p-3 border border-slate-200 dark:border-slate-600">
            <p class="text-secondary text-main text-xs font-medium mb-1">Data</p>
            <p class="text-main font-bold text-lg">${processedMB}<span class="text-slate-500 text-sm">/${totalMB} MB</span></p>
            </div>
            <div class="bg-white dark:bg-slate-700/50 rounded-lg p-3 border border-slate-200 dark:border-slate-600">
            <p class="text-secondary text-main text-xs font-medium mb-1">Speed</p>
            <p class="text-main font-bold text-lg">${speed}<span class="text-slate-500 text-sm"> MB/s</span></p>
            </div>
            <div class="bg-white dark:bg-slate-700/50 rounded-lg p-3 border border-slate-200 dark:border-slate-600">
            <p class="text-secondary text-main text-xs font-medium mb-1">ETA</p>
            <p class="text-main font-bold text-lg">${eta || '--'}</p>
            </div>
            `;
        }

        // Update current file
        const currentFileContainer = container.querySelector('#current-file-container');
        if (currentFileContainer) {
            if (current_file) {
                currentFileContainer.classList.remove('hidden');
                currentFileContainer.innerHTML = `
                <div class="bg-white dark:bg-slate-700/50 rounded-lg p-3 border border-slate-200 dark:border-slate-600">
                <p class="text-secondary text-main text-xs font-medium mb-1">
                <i class="bi bi-file-earmark mr-1"></i>Current File
                </p>
                <p class="text-sm dark:text-slate-300 truncate font-medium">${current_file}</p>
                </div>
                `;
            } else {
                currentFileContainer.classList.add('hidden');
            }
        }
    }

    getStatusColorClass(status) {
        switch (status) {
            case 'completed':
                return 'text-emerald-600 dark:text-emerald-400';
            case 'failed':
            case 'error':
                return 'text-red-600 dark:text-red-400';
            default:
                return 'text-blue-600 dark:text-blue-400';
        }
    }

    getActivityTitle(status) {
        switch (status) {
            case 'failed':
            case 'error':
                return 'Error';
            case 'completed':
                return 'Backed Up';
            default:
                return 'Backed Up';
        }
    }

    viewSnapshots(fileName) {
        if (!this.state.connection.isDeviceConnected) {
            this.eventBus.emit('notification:show', {
                type: 'warning',
                title: 'Device Required',
                message: 'Please connect backup device to view snapshots'
            });
            return;
        }

        // Switch to files view
        this.eventBus.emit('navigation:change', { tab: 'files' });

        // Set search query
        this.eventBus.emit('files:search', { query: fileName });
    }

    setupEventListeners() {
        // View snapshots buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('activity-view-snapshots')) {
                const fileName = e.target.dataset.fileName;
                this.viewSnapshots(fileName);
            }
        });

        // Clear feed button
        const clearButton = document.getElementById('clear-activity-feed');
        if (clearButton) {
            clearButton.addEventListener('click', () => this.clearFeed());
        }
    }
}

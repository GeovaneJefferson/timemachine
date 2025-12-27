/**
 * Dashboard & Activity Feed Module
 */

import { MAX_TRANSFER_ITEMS, elements } from './globals.js';
import { humanFileSize, timeSince } from './utils.js';

// Define appState if not already defined
if (typeof window.appState === 'undefined') {
    window.appState = {
        backup: { running: false }
    };
}
const appState = window.appState;

const BackupManager = {
    updateUsage: () => {
        fetch('/api/backup/usage')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                BackupManager.updateUI(data);
            }
        })
        .catch(error => {
            console.error('Backup usage check failed:', error);
        });
    },

    updateUI: (data) => {
        if (data.success) {
            // Safely update elements if they exist
            if (elements.backupUsage) {
                elements.backupUsage.textContent =
                `${data.human_used} Used / ${data.human_total} (${data.percent_used}% used)`;
            }
            if (elements.backupUsagePercent) {
                elements.backupUsagePercent.textContent = `${data.percent_used}%`;
            }
            if (elements.backupLocationPath) {
                elements.backupLocationPath.textContent = `${data.location}`;
            }

            // Update the usage circle if it exists
            const usageCircle = document.querySelector('svg .text-blue-500');
            if (usageCircle) {
                const percent = data.percent_used;
                const CIRCUMFERENCE = 251.2;
                const offset = CIRCUMFERENCE - (percent / 100) * CIRCUMFERENCE;
                usageCircle.style.strokeDashoffset = offset;
            }
        }
    },

    checkDaemonStatus: () => {
        // First check WebSocket connection
        let wsConnected = false;
        if (window.backupStatusClient && window.backupStatusClient.ws) {
            wsConnected = window.backupStatusClient.ws.readyState === WebSocket.OPEN;
        }

        // Then check daemon status via API
        fetch('/api/backup/daemon-status')
        .then(response => response.json())
        .then(data => {
            const isRunning = data.running || false;
            const realTimeStatusLabel = document.getElementById('realTimeStatusLabel');

            if (realTimeStatusLabel) {
                if (isRunning && wsConnected) {
                    realTimeStatusLabel.className = 'bi bi-circle-fill text-green-500 mr-1 text-xs';
                    realTimeStatusLabel.title = 'Real-time backup active';
                    appState.backup.running = true;
                } else {
                    realTimeStatusLabel.className = 'bi bi-circle-fill text-red-500 mr-1 text-xs';
                    realTimeStatusLabel.title = 'Real-time backup inactive';
                    appState.backup.running = false;
                }
            }
        })
        .catch(error => {
            console.error('Failed to check daemon status:', error);
            // Fallback to WebSocket status only
            const realTimeStatusLabel = document.getElementById('realTimeStatusLabel');
            if (realTimeStatusLabel) {
                if (wsConnected) {
                    realTimeStatusLabel.className = 'bi bi-circle-fill text-green-500 mr-1 text-xs';
                    realTimeStatusLabel.title = 'Real-time backup active (WS only)';
                } else {
                    realTimeStatusLabel.className = 'bi bi-circle-fill text-red-500 mr-1 text-xs';
                    realTimeStatusLabel.title = 'Real-time backup inactive';
                }
            }
        });
    },

    toggle: () => {
        const realTimeCheckbox = document.getElementById('realTimeCheckbox');
        if (!realTimeCheckbox) return;

        realTimeCheckbox.disabled = true;
        const isChecked = realTimeCheckbox.checked;

        BackupManager.updateVisualStatus(isChecked);

        BackupManager.updateRealTimeBackupState(isChecked)
        .finally(() => {
            realTimeCheckbox.disabled = false;
        });
    },

    updateVisualStatus: (isActive) => {
        appState.backup.running = isActive;
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
    },

    updateRealTimeBackupState: (isChecked) => {
        return fetch('/api/realtime-backup/daemon', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_active: isChecked }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error toggling daemon:", data.error);
                alert("Failed to toggle backup: " + data.error);
                const checkbox = document.getElementById('realTimeCheckbox');
                if (checkbox) {
                    checkbox.checked = !isChecked;
                }
                BackupManager.updateVisualStatus(!isChecked);
            }
        })
        .catch(err => {
            console.error("Network error:", err);
            const checkbox = document.getElementById('realTimeCheckbox');
            if (checkbox) {
                checkbox.checked = !isChecked;
            }
            BackupManager.updateVisualStatus(!isChecked);
        });
    }
};

// Alias for backward compatibility
const DaemonControlManager = BackupManager;

const ActivityFeedManager = {
    init() {
        this.feedContainer = document.querySelector('#live-activities-feed');
        if (!this.feedContainer) {
            console.error("Activity feed container not found (#live-activities-feed).");
            return;
        }
        this.loadFromStorage();
        this._sortRowsByTimestamp();
    },

    loadFromStorage() {
        try {
            const stored = localStorage.getItem('timemachine_activity_feed');
            if (stored) {
                const activities = JSON.parse(stored);
                activities.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));

                this.feedContainer.innerHTML = '';

                const latestActivities = {};
                activities.forEach(activity => {
                    const fileName = (activity.description || "").split('/').pop();
                    if (!latestActivities[fileName] ||
                        (activity.timestamp || 0) > (latestActivities[fileName].timestamp || 0)) {
                        latestActivities[fileName] = activity;
                        }
                });

                const uniqueActivities = Object.values(latestActivities);
                uniqueActivities.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));

                const activitiesToShow = Math.min(uniqueActivities.length, MAX_TRANSFER_ITEMS);

                for (let i = 0; i < activitiesToShow; i++) {
                    this._addRowToFeed(uniqueActivities[i]);
                }
            }
        } catch (e) {
            console.warn('[ActivityFeed] Could not load from localStorage:', e);
        }
    },

    _addRowToFeed(activity) {
        if (!this.feedContainer) return;

        const { description, title, timestamp } = activity;
        const filePath = description || "";
        const fileName = filePath.split('/').pop();

        const newRowId = `activity-${fileName.replace(/[^a-zA-Z0-9]/g, '')}-${Date.now()}`;
        const newRowHtml = this._createRowHtml(activity, newRowId);
        this.feedContainer.insertAdjacentHTML('afterbegin', newRowHtml);
        this._trimToMax();
        this._sortRowsByTimestamp();
    },

    _createRowHtml(activity, rowId) {
        if (!activity) return '';

        const { title, description, size, timestamp } = activity;
        const safeDescription = description || "";
        const safeTitle = title || "";
        const fileName = safeDescription.split('/').pop();

        let actionLabel = "Processing";
        let actionColorClass = "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400";

        if (safeTitle.includes('Backed Up') || safeTitle.includes('Hardlinked')) {
            actionLabel = 'Backed Up';
            actionColorClass = "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400";
        } else if (safeTitle.includes('Modified')) {
            actionLabel = 'Modified';
            actionColorClass = "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400";
        }

        const formattedTime = timeSince(timestamp);
        const finalRowId = rowId;

        return `
        <tr id="${finalRowId}"
        class="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition activity-row"
        data-timestamp="${timestamp}">
        <td class="px-6 py-3 flex items-center gap-3 file-name-cell">
        ${fileName}
        ${safeTitle === 'Processing' ? '<i class="bi bi-arrow-clockwise animate-spin text-blue-500 text-xs ml-2"></i>' : ''}
        </td>
        <td class="px-6 py-3 status-cell">
        <span class="px-2 py-0.5 ${actionColorClass} rounded text-xs font-bold">${actionLabel}</span>
        </td>
        <td class="px-6 py-3 text-muted size-cell">${humanFileSize(size)}</td>
        <td class="px-6 py-3 action-cell">
        <button class="text-hyperlink hover:text-hyperlink dark:hover:text-blue-300 text-xs font-medium transition hover:underline cursor-pointer"
        onclick="if (window.isDeviceConnected) { window.ActivityFeedManager.viewSnapshots('${fileName.replace(/'/g, "\\'")}') }">
        View Snapshots
        </button>
        </td>
        <td class="px-6 py-3 text-right text-muted font-medium text-xs time-ago-cell">${formattedTime}</td>
        </tr>
        `;
    },

    _trimToMax() {
        if (!this.feedContainer) return;

        const rows = Array.from(this.feedContainer.children);
        if (rows.length <= MAX_TRANSFER_ITEMS) return;

        while (rows.length > MAX_TRANSFER_ITEMS) {
            const row = rows.pop();
            row.remove();
        }
    },

    _sortRowsByTimestamp() {
        if (!this.feedContainer) return;

        const rows = Array.from(this.feedContainer.querySelectorAll('.activity-row'));
        rows.sort((a, b) => {
            const tsA = parseInt(a.getAttribute('data-timestamp') || '0', 10);
            const tsB = parseInt(b.getAttribute('data-timestamp') || '0', 10);
            const timeA = isNaN(tsA) ? 0 : tsA;
            const timeB = isNaN(tsB) ? 0 : tsB;
            return timeB - timeA;
        });

        rows.forEach(row => {
            this.feedContainer.appendChild(row);
        });
    },

    updateTimeAgo() {
        if (!this.feedContainer) return;

        const rows = this.feedContainer.querySelectorAll('tr[data-timestamp]');
        rows.forEach(row => {
            const timestamp = parseInt(row.dataset.timestamp, 10);
            const timeCell = row.querySelector('.time-ago-cell');

            if (timeCell && !isNaN(timestamp)) {
                timeCell.textContent = timeSince(timestamp);
            }
        });
    },

    handleMessage(message) {
        if (!this.feedContainer) return;

        if (message.type === 'backup_progress') {
            this._handleBackupProgress(message);
            return;
        }

        if (!message.timestamp) {
            message.timestamp = Date.now();
        }

        this._addRowToFeed(message);

        if (message.title && message.title !== 'Processing') {
            this._persistToStorage(message);
        }

        this._sortRowsByTimestamp();
    },

    _persistToStorage(message) {
        try {
            let allActivities = [];
            const stored = localStorage.getItem('timemachine_activity_feed');
            if (stored) {
                allActivities = JSON.parse(stored);
            }

            if (!message.timestamp) {
                message.timestamp = Date.now();
            }

            allActivities = allActivities.filter(activity =>
            activity.description !== message.description
            );

            allActivities.push(message);
            allActivities.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
            allActivities = allActivities.slice(0, 20);

            localStorage.setItem('timemachine_activity_feed', JSON.stringify(allActivities));
        } catch (e) {
            console.warn('[ActivityFeed] Could not persist activity:', e);
        }
    },

    _handleBackupProgress(message) {
        const { progress, status, current_file, bytes_processed } = message;

        if (current_file) {
            let activityTitle = 'Processing';
            if (status === 'completed') {
                activityTitle = 'Backed Up';
            } else if (status === 'failed' || status === 'error') {
                activityTitle = 'Error';
            }

            const activity = {
                title: activityTitle,
                description: current_file,
                size: bytes_processed || 0,
                timestamp: Date.now()
            };

            this._addRowToFeed(activity);
        }
    },

    viewSnapshots(fileName) {
        if (window.nav) {
            window.nav('files');
        }
        const searchInput = document.getElementById('file-search-input');
        if (searchInput) {
            searchInput.value = fileName;
            searchInput.dispatchEvent(new Event('keyup'));
        }
    }
};

// Make sure appState is defined globally
if (typeof appState === 'undefined') {
    window.appState = { backup: { running: false } };
}

export { BackupManager, ActivityFeedManager, DaemonControlManager };

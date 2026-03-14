// src/js/pages/locations.js - WITH MULTI-COLOR STORAGE BREAKDOWN

import { createLoadingSkeleton, createCardLoadingSkeleton } from '../utils/loading-skeleton.js';

export default class LocationsPage {
    constructor() {
        this.name = 'locations';
        this.showGetVersionsModal = false;
        this.loading = true;
        this.error = null;
        this.currentView = 'list';
        
        // Initialize with empty data
        this.data = {
            deviceInfo: null, // Will be populated from real device
            currentPath: ['Home'],
            folders: [],
            versionPoints: [
                { id: 'today', name: 'Today', time: '10:42 AM (Latest)', icon: 'schedule', selected: true },
                { id: 'yesterday', name: 'Yesterday', time: '4:20 PM', icon: 'history' },
                { id: 'last-week', name: 'Last Week', time: 'Oct 15 - Oct 21', icon: 'date_range' },
                { id: 'custom', name: 'Custom Date', time: 'Choose from calendar', icon: 'edit_calendar' }
            ]
        };
        
        this.selectedDevice = null;
        this.currentBackupDevice = null;
        this.isDeviceActive = false;
        
        // Fake storage breakdown data (sizes filled later based on real usage)
        this.storageBreakdown = [
            { category: 'System', percentage: 45, color: 'bg-primary' },
            { category: 'Documents', percentage: 20, color: 'bg-[var(--color-gray-50)]0' },
            { category: 'Media', percentage: 10, color: 'bg-[var(--color-gray-50)]0' },
            { category: 'Applications', percentage: 7.5, color: 'bg-indigo-500' },
            { category: 'Other', percentage: 17.5, color: 'bg-[var(--color-gray-400)]' }
        ];
    }

    async loadHomeFolders() {
        try {
            this.loading = true;
            this.error = null;
            
            const response = await fetch('/api/home/folders');
            const data = await response.json();
            
            if (data.success && data.folders) {
                // Sort folders alphabetically (case-insensitive)
                data.folders.sort((a, b) => (a.name || '').localeCompare(b.name || '', undefined, { sensitivity: 'base' }));
                console.log(`Loaded ${data.folders.length} home folders`);

                // Map API data to UI format
                this.data.folders = data.folders.map(folder => ({
                    name: folder.name,
                    type: 'folder',
                    icon: this.getFolderIcon(folder.name),
                    date: this.formatDate(folder.lastModified),
                    size: this.formatSize(folder.size),
                    kind: 'Folder',
                    included: false,
                    selected: false,
                    canExclude: true,
                    protected: false,
                    path: folder.path
                }));
                
                // Update current path
                if (data.homePath) {
                    const pathParts = data.homePath.split('/').filter(p => p);
                    this.data.currentPath = ['Home', ...pathParts.slice(-1)];
                }
            } else {
                throw new Error(data.error || 'Failed to load folders');
            }
            
        } catch (error) {
            console.error('Error loading home folders:', error);
            this.error = error.message;
        } finally {
            this.loading = false;
        }
    }

    async loadDeviceInfo() {
        try {
            // Check if we have a selected device
            if (this.selectedDevice) {
                // Use the selected device's real data
                this.data.deviceInfo = {
                    name: this.selectedDevice.name || 'Unknown Device',
                    type: this.selectedDevice.filesystem || 'Storage Device',
                    status: this.selectedDevice.status || 'Connected',
                    statusColor: this.selectedDevice.status_color || 'green',
                    totalStorage: this.selectedDevice.total_human || '0 B',
                    usedStorage: this.selectedDevice.used_human || '0 B',
                    freeStorage: this.selectedDevice.free_human || '0 B',
                    percentUsed: this.selectedDevice.percent_used || 0,
                    mountpoint: this.selectedDevice.mountpoint || '',
                    device: this.selectedDevice.device || '',
                    is_removable: this.selectedDevice.is_removable || false,
                    is_media: this.selectedDevice.is_media || false
                };
                console.log('Loaded device info from selected device:', this.data.deviceInfo);
            } 
            // Otherwise check if there's a configured backup device
            else {
                const response = await fetch('/api/locations/current-backup');
                const data = await response.json();
                
                if (data.success && data.has_backup && data.device) {
                    this.currentBackupDevice = data.device;
                    this.data.deviceInfo = {
                        name: data.device.name || 'Backup Device',
                        type: data.device.filesystem || 'Storage Device',
                        status: 'Configured as Backup',
                        statusColor: 'green',
                        totalStorage: data.device.total_human || '0 B',
                        usedStorage: data.device.used_human || '0 B',
                        freeStorage: data.device.free_human || '0 B',
                        percentUsed: data.device.percent_used || 0,
                        mountpoint: data.device.mountpoint || '',
                        device: data.device.device || '',
                        is_removable: data.device.is_removable || false,
                        is_media: data.device.is_media || false
                    };
                    console.log('Loaded device info from backup device:', this.data.deviceInfo);
                } else {
                    // No device selected or configured
                    this.data.deviceInfo = {
                        name: 'No Device Selected',
                        type: 'Select a device to view details',
                        status: 'Not Connected',
                        statusColor: 'gray',
                        totalStorage: '0 B',
                        usedStorage: '0 B',
                        freeStorage: '0 B',
                        percentUsed: 0,
                        mountpoint: '',
                        device: '',
                        is_removable: false,
                        is_media: false
                    };
                    console.log('No device info available');
                }
            }
        } catch (error) {
            console.error('Error loading device info:', error);
            this.data.deviceInfo = {
                name: 'Error Loading Device',
                type: 'Could not load device information',
                status: 'Error',
                statusColor: 'red',
                totalStorage: '0 B',
                usedStorage: '0 B',
                freeStorage: '0 B',
                percentUsed: 0,
                mountpoint: '',
                device: '',
                is_removable: false,
                is_media: false
            };
        }
    }

    getFolderIcon(folderName) {
        const icons = {
            'Desktop': 'desktop_windows',
            'Documents': 'description',
            'Downloads': 'download',
            'Music': 'music_note',
            'Pictures': 'photo_library',
            'Videos': 'video_library',
            'Movies': 'video_library',
            'Public': 'public',
            'Library': 'folder_shared'
        };
        return icons[folderName] || 'folder';
    }

    formatDate(isoDate) {
        if (!isoDate) return '--';
        
        const date = new Date(isoDate);
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);
        
        if (date >= today) {
            return `Today at ${date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`;
        } else if (date >= yesterday) {
            return `Yesterday at ${date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })}`;
        } else {
            return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }
    }

    formatSize(bytes) {
        if (!bytes || bytes === 0) return '--';
        
        const units = ['B', 'KB', 'MB', 'GB', 'TB'];
        let size = bytes;
        let unitIndex = 0;
        
        while (size >= 1024 && unitIndex < units.length - 1) {
            size /= 1024;
            unitIndex++;
        }
        
        return `${size.toFixed(1)} ${units[unitIndex]}`;
    }

    getCategoryIcon(category) {
        const icons = {
            'System': 'computer',
            'Documents': 'description',
            'Media': 'video_library',
            'Applications': 'apps',
            'Other': 'folder'
        };
        return icons[category] || 'folder';
    }

    getCategoryIconColor(category) {
        const colors = {
            'System': 'text-[var(--color-accent)]',
            'Documents': 'text-purple-600',
            'Media': 'text-yellow-500',
            'Applications': 'text-indigo-500',
            'Other': 'text-[var(--color-text-secondary)]'
        };
        return colors[category] || 'text-[var(--color-text-secondary)]';
    }

    getDeviceIconColor(percentUsed, isDeviceActive) {
        if (percentUsed > 90) return 'text-[var(--color-status-error)] dark:text-[var(--color-status-error)]';
        if (percentUsed > 75) return 'text-yellow-500 dark:text-yellow-400';
        if (isDeviceActive) return 'text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)]';
        return 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]';
    }

    getUsageBarColor(percentUsed, isDeviceActive) {
        if (percentUsed > 90) return 'bg-[var(--color-status-error-bg)]';
        if (percentUsed > 75) return 'bg-[var(--color-gray-50)]0';
        if (isDeviceActive) return 'bg-[var(--color-status-success)]';
        return 'bg-[var(--color-accent)]';
    }

    // Convert a human-readable size string (eg. "12.3 GB") into bytes
    parseSize(str) {
        if (!str || typeof str !== 'string') return 0;
        const m = str.match(/([\d\.]+)\s*([KMGT]?B)/i);
        if (!m) return 0;
        const value = parseFloat(m[1]);
        const unit = m[2].toUpperCase();
        const units = { B: 1, KB: 1024, MB: 1024 ** 2, GB: 1024 ** 3, TB: 1024 ** 4 };
        return value * (units[unit] || 1);
    }

    // Generate fake storage breakdown based on real usage and used bytes
    getStorageBreakdown(realPercentUsed, usedHuman) {
        // default base items (sum to 100%)
        const base = [
            { category: 'System', percentage: 45, color: 'bg-primary' },
            { category: 'Documents', percentage: 20, color: 'bg-[var(--color-gray-50)]0' },
            { category: 'Media', percentage: 10, color: 'bg-[var(--color-gray-50)]0' },
            { category: 'Applications', percentage: 7.5, color: 'bg-indigo-500' },
            { category: 'Other', percentage: 17.5, color: 'bg-[var(--color-gray-400)]' }
        ];
        
        if (realPercentUsed > 0) {
            const scaleFactor = realPercentUsed / 100;
            const usedBytes = this.parseSize(usedHuman);
            // apply rounding but keep track of total so we can adjust last element
            let acc = 0;
            const result = base.map((item, idx) => {
                let pct = Math.round(item.percentage * scaleFactor);
                if (idx === base.length - 1) {
                    // adjust for rounding error
                    const target = Math.round(realPercentUsed);
                    pct = target - acc;
                }
                acc += pct;

                let sizeStr = '';
                if (usedBytes && pct > 0) {
                    const bytes = Math.round((usedBytes * pct) / 100);
                    sizeStr = this.formatSize(bytes);
                }
                return {
                    category: item.category,
                    percentage: pct,
                    color: item.color,
                    size: sizeStr
                };
            });
            return result;
        }

        // no real data; return base with static size labels if present
        return base.map(item => ({ ...item, size: item.size || '' }));
    }

    async render() {
        if (this.loading) {
            return `
                <div class="px-8 py-6 bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark">
                    <div class="h-8 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-64 animate-pulse mb-2"></div>
                    <div class="h-4 bg-[var(--color-gray-100)] dark:bg-[var(--color-gray-800)] rounded w-96 animate-pulse"></div>
                </div>
                <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark p-8">
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        ${createCardLoadingSkeleton(3)}
                    </div>
                </div>
            `;
        }

        if (this.error) {
            return `
                <div class="flex flex-col items-center justify-center h-full p-8">
                    <div class="w-16 h-16 rounded-full bg-[var(--color-status-error-bg)] dark:bg-red-900 flex items-center justify-center mb-4">
                        <span class="material-icons-round text-[var(--color-status-error)] dark:text-[var(--color-status-error)] text-2xl">error</span>
                    </div>
                    <h3 class="text-lg font-medium text-[var(--color-text-primary)] dark:text-white mb-2">Error Loading Folders</h3>
                    <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] text-center mb-6">${this.error}</p>
                    <button onclick="window.location.reload()" class="px-4 py-2 bg-[var(--color-accent)] text-white rounded hover:bg-[var(--color-accent)]">
                        Try Again
                    </button>
                </div>
            `;
        }

        // Get real device info or use defaults
        const device = this.data.deviceInfo || {};
        const deviceName = device.name || 'No Device Selected';
        const deviceType = device.type || 'Select a device to view details';
        const deviceStatus = device.status || 'Not Connected';
        const statusColor = device.statusColor || 'gray';
        const totalStorage = device.totalStorage || '0 B';
        const usedStorage = device.usedStorage || '0 B';
        const freeStorage = device.freeStorage || '0 B';
        const percentUsed = device.percentUsed || 0;
        const mountpoint = device.mountpoint || '';
        const devicePath = device.device || '';
        const isRemovable = device.is_removable || false;

        // Determine status display
        const isDeviceActive = this.isDeviceActive;
        const statusText = isDeviceActive ? 'Configured as Backup' : deviceStatus;
        const statusDotColor = isDeviceActive ? 'bg-[var(--color-status-success)]' : 
                              statusColor === 'green' ? 'bg-[var(--color-status-success)]' :
                              statusColor === 'yellow' ? 'bg-[var(--color-gray-50)]0' :
                              statusColor === 'red' ? 'bg-[var(--color-status-error-bg)]' : 'bg-[var(--color-gray-50)]0';
        const statusBgColor = isDeviceActive ? 'bg-[var(--color-gray-50)] dark:bg-[var(--color-status-success-bg-dark)]/20 border border-[var(--color-status-success-bg)] dark:border-[var(--color-status-success-dark)]' :
                             statusColor === 'green' ? 'bg-[var(--color-gray-50)] dark:bg-[var(--color-status-success-bg-dark)]/20 border border-[var(--color-status-success-bg)] dark:border-[var(--color-status-success-dark)]' :
                             statusColor === 'yellow' ? 'bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)]/20 border border-[var(--color-gray-100)] dark:border-[var(--color-gray-700)]' :
                             statusColor === 'red' ? 'bg-[var(--color-status-error-bg)] dark:bg-[var(--color-status-error-bg-dark)]/20 border border-[var(--color-status-error)] dark:border-[var(--color-status-error-dark)]' :
                             'bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)]/20 border border-[var(--color-gray-100)] dark:border-[var(--color-gray-700)]';
        const statusTextColor = isDeviceActive ? 'text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)]' :
                               statusColor === 'green' ? 'text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)]' :
                               statusColor === 'yellow' ? 'text-yellow-500 dark:text-yellow-300' :
                               statusColor === 'red' ? 'text-[var(--color-status-error)] dark:text-[var(--color-status-error-dark)]' :
                               'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]';

        // Get storage breakdown (fake categories for now). Pass usedStorage so sizes can be computed.
        const storageBreakdown = this.getStorageBreakdown(percentUsed, usedStorage);
        const totalBreakdownPercent = storageBreakdown.reduce((sum, item) => sum + item.percentage, 0);
        
        // Calculate free space percentage
        const freePercent = Math.max(0, 100 - totalBreakdownPercent);

        return `
            <div class="flex flex-col h-full overflow-hidden">
                <div class="px-8 py-6 bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark flex-shrink-0">
                    <div class="flex gap-8 items-start">
                        <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center shadow-soft border border-[var(--color-gray-200)] dark:border-[var(--color-gray-600)] flex-shrink-0">
                            <span class="material-symbols-outlined text-5xl ${this.getDeviceIconColor(percentUsed, isDeviceActive)}">hard_drive</span>
                        </div>
                        <div class="flex-1">
                            <div class="flex justify-between items-center mb-2">
                                <div>
                                    <h1 class="text-2xl font-bold text-[var(--color-text-primary)] dark:text-white leading-tight">${deviceName}</h1>
                                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">
                                        ${deviceType} ${devicePath ? `• ${devicePath}` : ''}
                                    </p>
                                </div>
                                <div class="flex items-center gap-2">
                                    <div class="flex items-center gap-2 px-3 py-1 rounded-full ${statusBgColor}">
                                        <span class="w-2 h-2 rounded-full ${statusDotColor} animate-pulse"></span>
                                        <span class="text-xs font-medium ${statusTextColor}">${statusText}</span>
                                    </div>
                                    ${this.selectedDevice ? `
                                        <div class="flex items-center gap-2">
                                            ${isDeviceActive ? `
                                                <button class="px-3 py-1 rounded bg-green-600 text-white text-sm" disabled>Configured</button>
                                            ` : `
                                                <button id="use-device-btn" class="px-3 py-1 rounded bg-[var(--color-accent)] text-white text-sm hover:bg-[var(--color-accent-hover)]">Use As Backup Device</button>
                                            `}
                                        </div>
                                    ` : ''}
                                </div>
                            </div>
                            <div class="mb-4">
                                <div class="flex justify-between text-xs font-medium mb-1.5">
                                    <span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Storage Used</span>
                                    <span class="text-text-secondary-light dark:text-text-secondary-dark">${usedStorage} of ${totalStorage} (${percentUsed}%)</span>
                                </div>
                                <div class="w-full h-3 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded-full overflow-hidden flex">
                                    ${storageBreakdown.map(item => `
                                        <div class="h-full ${item.color}" style="width: ${item.percentage}%" title="${item.category} (${item.size})"></div>
                                    `).join('')}
                                    ${freePercent > 0 ? `<div class="h-full bg-transparent" style="width: ${freePercent}%" title="Free (${freeStorage})"></div>` : ''}
                                </div>
                                
                                <!-- Compact horizontal breakdown with icons -->
                                <div class="mt-3 pt-3 border-t border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)]">
                                    <div class="flex flex-wrap items-center gap-2 mb-1">
                                        ${storageBreakdown.map(item => {
                                            // Get icon for each category
                                            const icon = this.getCategoryIcon(item.category);
                                            return `
                                            <div class="group relative">
                                                <div class="flex items-center gap-1 px-2 py-1 bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] rounded-lg cursor-help hover:bg-[var(--color-gray-100)] dark:hover:bg-[var(--color-gray-700)] transition-colors">
                                                    <span class="material-icons-round text-sm ${this.getCategoryIconColor(item.category)}">${icon}</span>
                                                    <span class="text-xs font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">${item.category}</span>
                                                    <span class="text-xs text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">${item.percentage}%</span>
                                                </div>
                                                <!-- Tooltip -->
                                                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 px-2 py-1 bg-[var(--color-gray-900)] text-white text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-10">
                                                    ${item.category}: ${item.size}
                                                    <div class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-900"></div>
                                                </div>
                                            </div>
                                            `;
                                        }).join('')}
                                        
                                        <div class="group relative">
                                            <div class="flex items-center gap-1 px-2 py-1 bg-[var(--color-gray-50)] dark:bg-[var(--color-status-success-bg-dark)]/20 rounded-lg cursor-help hover:bg-[var(--color-status-success-bg)] dark:hover:bg-green-900/30 transition-colors">
                                                <span class="material-icons-round text-sm text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)]">check_circle</span>
                                                <span class="text-xs font-medium text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)]">Free</span>
                                                <span class="text-xs text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)]">${freePercent}%</span>
                                            </div>
                                            <!-- Tooltip -->
                                            <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 px-2 py-1 bg-[var(--color-gray-900)] text-white text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-10">
                                                Free Space: ${freeStorage}
                                                <div class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-900"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="px-6 py-2 bg-[var(--color-gray-50)]/50 dark:bg-[var(--color-gray-800)]/30 border-b border-border-light dark:border-border-dark flex items-center justify-between flex-shrink-0">
                    <div class="flex items-center gap-2">
                        <div class="flex items-center text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] bg-[var(--color-system-background)] dark:bg-[var(--color-gray-700)] border border-border-light dark:border-border-dark rounded px-2 py-1 shadow-sm" id="breadcrumbs">
                            ${this.renderBreadcrumbs()}
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <div class="flex bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded-lg p-0.5" id="view-toggle">
                            <button class="p-1 rounded-md ${this.currentView === 'list' ? 'bg-[var(--color-system-background)] dark:bg-[var(--color-gray-600)] shadow-sm text-[var(--color-text-secondary)] dark:text-white' : 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] hover:text-[var(--color-text-secondary)] dark:hover:text-white'}" data-view="list">
                                <span class="material-icons-round text-lg">list</span>
                            </button>
                            <button class="p-1 rounded-md ${this.currentView === 'grid' ? 'bg-[var(--color-system-background)] dark:bg-[var(--color-gray-600)] shadow-sm text-[var(--color-text-secondary)] dark:text-white' : 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] hover:text-[var(--color-text-secondary)] dark:hover:text-white'}" data-view="grid">
                                <span class="material-icons-round text-lg">grid_view</span>
                            </button>
                        </div>
                        <button class="flex items-center gap-1.5 px-3 py-1.5 ${isDeviceActive ? 'bg-[var(--color-accent)] hover:bg-[var(--color-accent)] text-white' : 'bg-[var(--color-gray-300)] text-[var(--color-text-secondary)] cursor-not-allowed'} rounded-md shadow-sm transition-colors text-xs font-medium" id="save-changes-btn" ${isDeviceActive ? '' : 'disabled'}>
                            <span class="material-icons-round text-sm">save</span>
                            Save Changes
                        </button>
                    </div>
                </div>
                <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark ${!isDeviceActive ? 'pointer-events-none opacity-60' : ''}">
                    ${this.data.folders.length > 0 ? (this.currentView === 'list' ? `
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] sticky top-0 z-0">
                                <tr>
                                    <th class="w-12 px-4 py-2 border-b border-[var(--color-gray-200)] dark:border-border-dark">
                                        <input class="rounded border-[var(--color-gray-300)] text-primary focus:ring-primary h-4 w-4" type="checkbox" id="select-all" />
                                    </th>
                                    <th class="px-4 py-2 text-xs font-semibold text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] dark:border-border-dark w-1/3">Name</th>
                                    <th class="px-4 py-2 text-xs font-semibold text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] dark:border-border-dark">Date Modified</th>
                                    <th class="px-4 py-2 text-xs font-semibold text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] dark:border-border-dark">Kind</th>
                                    <th class="px-4 py-2 text-xs font-semibold text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] dark:border-border-dark">Size</th>
                                    <th class="px-4 py-2 text-xs font-semibold text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] border-b border-[var(--color-gray-200)] dark:border-border-dark text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-100 dark:divide-gray-800 text-sm" id="folders-list">
                                ${this.renderFoldersList()}
                            </tbody>
                        </table>
                    ` : `
                        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4" id="folders-grid">
                            ${this.data.folders.map(folder => `
                                <div class="p-4 rounded-lg border border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] flex items-center justify-between" data-folder="${folder.name}" data-type="${folder.type}">
                                    <div class="flex items-center gap-3">
                                        <input class="rounded border-[var(--color-gray-300)] text-primary focus:ring-primary h-4 w-4 ${folder.protected ? 'opacity-50 cursor-not-allowed' : ''}" 
                                            type="checkbox" 
                                            ${folder.selected ? 'checked' : ''}
                                            ${folder.protected || !isDeviceActive ? 'disabled' : ''}
                                            data-folder="${folder.name}" />
                                        <span class="material-icons-round ${folder.protected ? 'text-[var(--color-text-secondary)]' : 'text-[var(--color-accent)]'} text-3xl">${folder.icon}</span>
                                        <div>
                                            <div class="font-medium ${folder.protected ? 'text-[var(--color-text-secondary)]' : 'text-[var(--color-text-primary)] dark:text-[var(--color-text-secondary)]'}">${folder.name}</div>
                                            <div class="text-xs text-text-secondary-light dark:text-text-secondary-dark">${folder.date} • ${folder.size}</div>
                                        </div>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        ${folder.protected ? '<span class="text-xs font-medium text-[var(--color-text-secondary)] px-2 py-1">Protected</span>' : `<span class="text-xs font-medium ${folder.selected ? 'text-[var(--color-status-success)]' : 'text-text-secondary-light'} px-2 py-1 rounded">${folder.selected ? 'Included' : 'Excluded'}</span>`}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `) : `
                        <div class="flex flex-col items-center justify-center h-full p-8">
                            <div class="w-16 h-16 rounded-full bg-[var(--color-gray-100)] dark:bg-[var(--color-gray-800)] flex items-center justify-center mb-4">
                                <span class="material-icons-round text-[var(--color-text-secondary)] text-2xl">folder_open</span>
                            </div>
                            <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">No folders found in home directory</p>
                        </div>
                    `}
                </div>
                <div class="px-6 py-2 bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] border-t border-border-light dark:border-border-dark text-xs text-text-secondary-light dark:text-text-secondary-dark flex justify-between items-center flex-shrink-0">
                    <span id="folder-summary">${this.data.folders.length} items, ${freeStorage} available${deviceName !== 'No Device Selected' ? ` on ${deviceName}` : ''}</span>
                    <div class="flex gap-4">
                        ${mountpoint ? `<span class="text-text-secondary-light dark:text-text-secondary-dark">Mount: ${mountpoint}</span>` : ''}
                        ${isRemovable ? `<span class="text-text-secondary-light dark:text-text-secondary-dark">Removable Storage</span>` : ''}
                    </div>
                </div>
            </div>
            ${this.showGetVersionsModal ? this.renderGetVersionsModal() : ''}
        `;
    }

    renderBreadcrumbs() {
        return this.data.currentPath.map((segment, index) => {
            const isLast = index === this.data.currentPath.length - 1;
            return `
                ${index > 0 ? '<span class="material-icons-round text-base text-[var(--color-text-secondary)] mx-1">chevron_right</span>' : ''}
                ${isLast ? 
                    `<span class="font-medium">${segment}</span>` :
                    `<span class="text-text-secondary-light">${segment}</span>`
                }
            `;
        }).join('');
    }

    renderFoldersList() {
        const isDeviceActive = this.isDeviceActive;
        return this.data.folders.map(folder => `
            <tr class="hover:bg-[var(--color-gray-50)] dark:hover:bg-[var(--color-accent-light)]/20 group cursor-default transition-colors ${folder.protected ? 'bg-[var(--color-gray-50)]/50 dark:bg-[var(--color-gray-800)]/30 cursor-not-allowed' : ''}" 
                data-folder="${folder.name}"
                data-type="${folder.type}">
                <td class="px-4 py-3">
                    <input class="rounded border-[var(--color-gray-300)] text-primary focus:ring-primary h-4 w-4 ${folder.protected ? 'opacity-50 cursor-not-allowed' : ''}" 
                           type="checkbox" 
                           ${folder.selected ? 'checked' : ''}
                           ${folder.protected || !isDeviceActive ? 'disabled' : ''}
                           data-folder="${folder.name}" />
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                    <div class="flex items-center gap-3">
                        <span class="material-icons-round ${folder.protected ? 'text-[var(--color-text-secondary)]' : 'text-[var(--color-accent)]'} text-xl">${folder.icon}</span>
                        <span class="font-medium ${folder.protected ? 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]' : 'text-[var(--color-text-primary)] dark:text-[var(--color-text-secondary)]'}">${folder.name}</span>
                    </div>
                </td>
                <td class="px-4 py-3 ${folder.protected ? 'text-[var(--color-text-secondary)]' : 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]'} whitespace-nowrap">${folder.date}</td>
                <td class="px-4 py-3 ${folder.protected ? 'text-[var(--color-text-secondary)]' : 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]'} whitespace-nowrap">${folder.kind}</td>
                <td class="px-4 py-3 ${folder.protected ? 'text-[var(--color-text-secondary)]' : 'text-gray500 dark:text-[var(--color-text-secondary)]'} whitespace-nowrap">${folder.size}</td>
                <td class="px-4 py-3 whitespace-nowrap text-right">
                    ${folder.protected ? 
                        `<span class="text-xs font-medium text-[var(--color-text-secondary)] px-2 py-1">Protected</span>` :
                        `<span class="text-xs font-medium ${folder.selected ? 'text-[var(--color-status-success)]' : 'text-text-secondary-light'} px-2 py-1 rounded">${folder.selected ? 'Included' : 'Excluded'}</span>`
                    }
                </td>
            </tr>
        `).join('');
    }

    renderGetVersionsModal() {
        const selectedFolders = this.data.folders.filter(f => f.selected);
        const selectedCount = selectedFolders.length;
        const selectedVersionPoint = this.data.versionPoints.find(rp => rp.selected);
        const device = this.data.deviceInfo || {};

        return `
            <div class="fixed inset-0 bg-black/80 backdrop-blur-md transition-opacity z-50" id="get-versions-modal-backdrop"></div>
            <div class="fixed inset-0 z-50 w-screen overflow-y-auto" id="get-versions-modal-container">
                <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
                    <div class="relative transform overflow-hidden rounded-2xl bg-system-background text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-3xl border border-separator">
                        <div class="px-6 py-5 border-b border-separator flex justify-between items-center bg-secondary-background">
                            <div>
                                <h3 class="text-xl font-semibold leading-6 text-white" id="modal-title">Get File Versions</h3>
                                <p class="mt-1 text-sm text-[var(--color-text-secondary)]">Choose a recovery point for your files.</p>
                            </div>
                            <button class="text-[var(--color-text-secondary)] hover:text-white transition-colors" id="close-get-versions-modal">
                                <span class="material-icons-round">close</span>
                            </button>
                        </div>
                        <div class="px-6 py-8 bg-system-background">
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="version-points">
                                ${this.data.versionPoints.map(point => `
                                    <div class="relative flex cursor-pointer rounded-xl ${point.selected ? 'border-2 border-accent bg-accent-light' : 'border border-separator hover:border-secondary-label bg-secondary-background hover:bg-tertiary-background'} p-4 shadow-sm focus:outline-none ring-offset-2 ring-offset-system-background ring-accent transition-all" 
                                         data-version-point="${point.id}">
                                        <div class="flex w-full items-center justify-between">
                                            <div class="flex items-center gap-4">
                                                <div class="flex h-12 w-12 items-center justify-center rounded-full ${point.selected ? 'bg-primary/20 text-[var(--color-accent)]' : 'bg-[var(--color-gray-700)] text-[var(--color-text-secondary)]'}">
                                                    <span class="material-icons-round text-2xl">${point.icon}</span>
                                                </div>
                                                <div>
                                                    <p class="font-semibold ${point.selected ? 'text-white' : 'text-[var(--color-text-secondary)]'}">${point.name}</p>
                                                    <p class="text-sm ${point.selected ? 'text-[var(--color-text-secondary)]' : 'text-[var(--color-text-secondary)]'}">${point.time}</p>
                                                </div>
                                            </div>
                                            ${point.selected ? '<span class="material-icons-round text-primary text-xl">check_circle</span>' : ''}
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                            <div class="mt-6 flex items-start gap-3 p-4 rounded-lg bg-secondary-background border border-separator">
                                <span class="material-icons-round text-[var(--color-accent)] mt-0.5">info</span>
                                <div class="text-sm text-[var(--color-text-secondary)]">
                                    <p class="font-medium text-white mb-0.5">Get Versions Summary</p>
                                    <p>You are about to get versions for <span class="font-semibold text-white">${selectedCount} items</span> from <span class="font-semibold text-white">${device.name || 'Device'}</span> to their state on <span class="font-semibold text-white">${selectedVersionPoint?.name || ''} at ${selectedVersionPoint?.time || ''}</span>.</p>
                                </div>
                            </div>
                        </div>
                        <div class="bg-secondary-background px-6 py-4 sm:flex sm:flex-row-reverse sm:px-6 gap-3 border-t border-separator">
                            <button class="inline-flex w-full justify-center rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white shadow-glow hover:bg-[var(--color-accent)] sm:w-auto transition-colors items-center gap-2" id="confirm-get-versions" type="button">
                                <span class="material-icons-round text-lg">history</span>
                                Get Versions
                            </button>
                            <button class="mt-3 inline-flex w-full justify-center rounded-lg bg-tertiary-background px-4 py-2.5 text-sm font-semibold text-secondary-label shadow-sm ring-1 ring-inset ring-separator hover:bg-system-fill sm:mt-0 sm:w-auto transition-colors" id="cancel-get-versions" type="button">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    async afterRender() {
        console.log('Locations page initialized');
        
        // Load selected device from sessionStorage (if any)
        try {
            const stored = sessionStorage.getItem('selectedDevice');
            if (stored) {
                this.selectedDevice = JSON.parse(stored);
                console.log('Loaded selected device from session:', this.selectedDevice);
            }
        } catch (e) {
            this.selectedDevice = null;
            console.log('No selected device in session');
        }

        // Load device information
        await this.loadDeviceInfo();
        
        // Load home folders from API
        await this.loadHomeFolders();

        // Load current backup device info and check if it's active
        try {
            const resp = await fetch('/api/locations/current-backup');
            const data = await resp.json();
            if (data.success && data.has_backup && data.device) {
                this.currentBackupDevice = data.device;
                // Check if selected device is the current backup device
                if (this.selectedDevice && this.currentBackupDevice) {
                    this.isDeviceActive = this.selectedDevice.mountpoint === this.currentBackupDevice.mountpoint;
                    console.log('Device active status:', this.isDeviceActive);
                }
            } else {
                this.currentBackupDevice = null;
                this.isDeviceActive = false;
            }
        } catch (e) {
            console.error('Error loading current backup:', e);
            this.currentBackupDevice = null;
            this.isDeviceActive = false;
        }

        // Load saved backup folders
        try {
            const respFolders = await fetch('/api/locations/backup-folders');
            const bf = await respFolders.json();
            if (bf && bf.success && Array.isArray(bf.folders)) {
                const saved = bf.folders;
                this.data.folders.forEach(f => {
                    if (saved.includes(f.path)) {
                        f.selected = true;
                        f.included = true;
                    }
                });
                console.log('Loaded saved backup folders:', saved.length);
            }
        } catch (e) {
            console.warn('Could not load saved backup folders:', e);
        }

        // Re-render with loaded data
        const pageContent = document.getElementById('page-content');
        if (pageContent) {
            pageContent.innerHTML = await this.render();
        }

        // Re-render the page
        this.setupEventListeners();
        this.setupSelection();
        this.updateSelectAllState();
        this.updateFolderSummary();
        this.updateViewButtonsState();
        this.setupEjectButton();

        // Re-attach the use button listener
        const useBtn = document.getElementById('use-device-btn');
        if (useBtn && this.selectedDevice) {
            useBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.useSelectedDevice(this.selectedDevice.mountpoint);
            });
        }
        
        // Listen for device ejection events from sidebar
        this.handleDeviceEjected = async (event) => {
            console.log('Device ejected event received:', event.detail);
            
            const ejectedMountpoint = event.detail?.mountpoint;
            
            // Check if the ejected device is the one we're currently displaying
            if (this.selectedDevice && ejectedMountpoint === this.selectedDevice.mountpoint) {
                console.log('Current device was ejected, updating page...');
                
                // DON'T clear the selectedDevice - keep it so we can still show it
                // Just mark it as not active anymore
                this.isDeviceActive = false;
                
                // Update the device status in deviceInfo (if it exists)
                if (this.data.deviceInfo) {
                    this.data.deviceInfo.status = 'Not Connected';
                    this.data.deviceInfo.statusColor = 'gray';
                }
                
                // Re-render the page
                const pageContent = document.getElementById('page-content');
                if (pageContent) {
                    pageContent.innerHTML = await this.render();
                    this.setupEventListeners();
                    this.setupSelection();
                    this.updateSelectAllState();
                    this.updateFolderSummary();
                    this.updateViewButtonsState();
                    
                    // Re-attach the use button listener
                    const useBtn = document.getElementById('use-device-btn');
                    if (useBtn && this.selectedDevice) {
                        useBtn.addEventListener('click', (e) => {
                            e.preventDefault();
                            this.useSelectedDevice(this.selectedDevice.mountpoint);
                        });
                    }
                }
            }
        };
        
        document.addEventListener('device-ejected', this.handleDeviceEjected);
    }

    async useSelectedDevice(mountpoint) {
        try {
            // send selected device metadata when available to ensure full config is saved
            const payload = { mountpoint };
            if (this.selectedDevice && typeof this.selectedDevice === 'object') {
                payload.device_info = this.selectedDevice;
            }

            const resp = await fetch('/api/locations/select-device', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();
            if (data.success) {
                showToast(data.message || 'Backup device configured', 'success');
                // Update device active status
                this.isDeviceActive = true;
                // Refresh sidebar and page state
                document.dispatchEvent(new CustomEvent('devices-updated'));
                
                // Reload current backup info without re-rendering yet
                await this.loadDeviceInfo();
                await this.loadHomeFolders();

                // Update header device connection status to green
                if (window.appHeader && typeof window.appHeader.checkBackupDevice === 'function') {
                    try {
                        await window.appHeader.checkBackupDevice();
                        window.appHeader.updateDeviceStatus();
                        console.log('Updated header device status to connected');
                    } catch (e) {
                        console.error('Error updating header device status:', e);
                    }
                }

                // Auto-select default folders (Desktop, Documents, Music, Pictures, Videos)
                const defaultFolders = ['Desktop', 'Documents', 'Music', 'Pictures', 'Videos'];
                let autoSelectedCount = 0;
                this.data.folders.forEach(folder => {
                    if (defaultFolders.includes(folder.name)) {
                        folder.selected = true;
                        folder.included = true;
                        autoSelectedCount++;
                        console.log(`Auto-selected default folder: ${folder.name}`);
                    }
                });
                
                if (autoSelectedCount > 0) {
                    // Auto-save selected folders
                    const selectedPaths = this.data.folders.filter(f => f.selected).map(f => f.path);
                    console.log(`Auto-saving ${autoSelectedCount} default folders: ${selectedPaths.join(', ')}`);
                    try {
                        const saveResp = await fetch('/api/locations/save-folders', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ folders: selectedPaths })
                        });
                        const saveData = await saveResp.json();
                        if (saveData && saveData.success) {
                            console.log('Auto-saved default folders successfully');
                        } else {
                            console.warn('Failed to auto-save folders:', saveData?.error);
                        }
                    } catch (e) {
                        console.error('Error auto-saving folders:', e);
                    }
                }
                
                // Now re-render the page with auto-selected folders checked
                const pageContent = document.getElementById('page-content');
                if (pageContent) {
                    pageContent.innerHTML = await this.render();
                    // Setup event listeners for the newly rendered page
                    this.setupEventListeners();
                    this.setupSelection();
                }

                // Programmatically click the refresh button in the sidebar as requested
                const refreshBtn = document.querySelector('.refresh-backup-folders-btn');
                if (refreshBtn) {
                    console.log('Automatically refreshing backup folders list by clicking refresh button.');
                    refreshBtn.click();
                } else {
                    console.error('Could not find .refresh-backup-folders-btn to click.');
                }
            } else {
                showError(data.error || 'Failed to set backup device', 'error');
            }
        } catch (e) {
            showError(e.message || 'Error setting device', 'error');
        }
    }

    setupEventListeners() {        
        const viewButtons = document.querySelectorAll('#view-toggle button');
        viewButtons.forEach(button => {
            button.addEventListener('click', () => this.toggleView(button.getAttribute('data-view')));
        });
        
        document.getElementById('save-changes-btn')?.addEventListener('click', () => this.saveChanges());
        
        const selectAllCheckbox = document.getElementById('select-all');
        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', (e) => this.toggleSelectAll(e.target.checked));
        }
        
        const folderRows = document.querySelectorAll('#folders-list tr:not(.cursor-not-allowed)');
        folderRows.forEach(row => {
            row.addEventListener('click', (e) => {
                if (!e.target.matches('input[type="checkbox"], button')) {
                    const checkbox = row.querySelector('input[type="checkbox"]');
                    if (checkbox && !checkbox.disabled) {
                        checkbox.checked = !checkbox.checked;
                        this.updateFolderSelection(checkbox);
                    }
                }
            });
        });

        const gridCards = document.querySelectorAll('#folders-grid [data-folder]:not(.cursor-not-allowed)');
        gridCards.forEach(card => {
            card.addEventListener('click', (e) => {
                if (!e.target.matches('input[type="checkbox"], button')) {
                    const checkbox = card.querySelector('input[type="checkbox"]');
                    if (checkbox && !checkbox.disabled) {
                        checkbox.checked = !checkbox.checked;
                        this.updateFolderSelection(checkbox);
                    }
                }
            });
        });
    }

    setupSelection() {
        document.querySelectorAll('#folders-list input[type="checkbox"], #folders-grid input[type="checkbox"]').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => this.updateFolderSelection(e.target));
        });
    }

    setupEjectButton() {
        // This is handled in the sidebar
    }

    async toggleView(viewType) {
        this.currentView = viewType;
        this.updateViewButtonsState();

        const pageContent = document.getElementById('page-content');
        if (pageContent) {
            pageContent.innerHTML = await this.render();
        }

        this.setupEventListeners();
        this.setupSelection();
        console.log('Switched to', viewType, 'view');
    }

    updateViewButtonsState() {
        const viewButtons = document.querySelectorAll('#view-toggle button');
        viewButtons.forEach(btn => {
            if (btn.getAttribute('data-view') === this.currentView) {
                btn.classList.add('bg-[var(--color-system-background)]', 'dark:bg-[var(--color-gray-600)]', 'shadow-sm', 'text-[var(--color-text-secondary)]', 'dark:text-white');
                btn.classList.remove('text-[var(--color-text-secondary)]', 'dark:text-[var(--color-text-secondary)]', 'hover:text-[var(--color-text-secondary)]', 'dark:hover:text-white');
            } else {
                btn.classList.remove('bg-[var(--color-system-background)]', 'dark:bg-[var(--color-gray-600)]', 'shadow-sm', 'text-[var(--color-text-secondary)]', 'dark:text-white');
                btn.classList.add('text-[var(--color-text-secondary)]', 'dark:text-[var(--color-text-secondary)]', 'hover:text-[var(--color-text-secondary)]', 'dark:hover:text-white');
            }
        });
    }

    saveChanges() {
        if (!this.isDeviceActive) {
            showInfo('Please set the selected device as backup first', 'warning');
            return;
        }

        // Persist selected folders to backend config
        const selectedFolders = this.data.folders.filter(f => f.selected).map(f => f.path);

        fetch('/api/locations/save-folders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ folders: selectedFolders })
        }).then(resp => resp.json())
        .then(data => {
            if (data && data.success) {
                showToast('Changes saved', 'success');
            } else {
                showError(data && data.error ? data.error : 'Failed to save changes', 'error');
            }
        }).catch(err => {
            console.error('Error saving folders:', err);
            showError('Error saving changes', 'error');
        });
    }

    toggleSelectAll(checked) {
        const checkboxes = document.querySelectorAll('#folders-list input[type="checkbox"]:not(:disabled), #folders-grid input[type="checkbox"]:not(:disabled)');
        checkboxes.forEach(checkbox => {
            checkbox.checked = checked;
            const folderName = checkbox.getAttribute('data-folder');
            const folder = this.data.folders.find(f => f.name === folderName);
            if (folder) {
                folder.selected = checked;
                folder.included = checked;
            }
            // update badge in DOM
            const escaped = (window.CSS && CSS.escape) ? CSS.escape(folderName) : folderName.replace(/(["\\])/g, '\\$1');
            const row = document.querySelector(`[data-folder="${escaped}"]`);
            if (row) {
                const badge = row.querySelector('.text-xs.font-medium');
                if (badge) {
                    badge.textContent = checked ? 'Included' : 'Excluded';
                    badge.classList.toggle('text-[var(--color-status-success)]', checked);
                    badge.classList.toggle('text-text-secondary-light', !checked);
                }
            }
        });
        this.updateFolderSummary();
    }

    updateFolderSelection(checkbox) {
        const folderName = checkbox.getAttribute('data-folder');
        const folder = this.data.folders.find(f => f.name === folderName);
        if (folder) {
            folder.selected = checkbox.checked;
            folder.included = checkbox.checked;
        }
        this.updateSelectAllState();
        this.updateFolderSummary();
        
        // update badge for this folder in DOM (table row or grid card)
        const escaped = (window.CSS && CSS.escape) ? CSS.escape(folderName) : folderName.replace(/(["\\])/g, '\\$1');
        const row = document.querySelector(`[data-folder="${escaped}"]`);
        if (row) {
            const badge = row.querySelector('.text-xs.font-medium');
            if (badge) {
                badge.textContent = folder.selected ? 'Included' : 'Excluded';
                badge.classList.toggle('text-[var(--color-status-success)]', folder.selected);
                badge.classList.toggle('text-text-secondary-light', !folder.selected);
            }
        }
    }

    updateSelectAllState() {
        const selectAllCheckbox = document.getElementById('select-all');
        if (!selectAllCheckbox) return;
        
        const checkboxes = document.querySelectorAll('#folders-list input[type="checkbox"]:not(:disabled), #folders-grid input[type="checkbox"]:not(:disabled)');
        const checkedCount = Array.from(checkboxes).filter(cb => cb.checked).length;

        if (checkedCount === 0) {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = false;
        } else if (checkedCount === checkboxes.length) {
            selectAllCheckbox.checked = true;
            selectAllCheckbox.indeterminate = false;
        } else {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = true;
        }
    }

    updateFolderSummary() {
        const selectedCount = this.data.folders.filter(f => f.selected).length;
        const device = this.data.deviceInfo || {};
        const summary = document.getElementById('folder-summary');
        if (summary) {
            if (selectedCount > 0) {
                summary.textContent = `${selectedCount} selected, ${this.data.folders.length} items, ${device.freeStorage || '0 B'} available on ${device.name || 'Device'}`;
            } else {
                summary.textContent = `${this.data.folders.length} items, ${device.freeStorage || '0 B'} available${device.name ? ` on ${device.name}` : ''}`;
            }
        }
    }

    async ejectDevice() {
        if (!this.selectedDevice) {
            showError('No device selected', 'error');
            return;
        }
        
        if (!confirm(`Eject "${this.selectedDevice.name}" from ${this.selectedDevice.mountpoint}?\n\nMake sure no files are being accessed from this device.`)) {
            return;
        }
        
        try {
            showInfo(`Ejecting ${this.selectedDevice.name}...`, 'info');
            
            const response = await fetch('/api/locations/eject-device', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mountpoint: this.selectedDevice.mountpoint })
            });
            
            const data = await response.json();
            
            if (data.success) {
                showToast(`${this.selectedDevice.name} ejected successfully`, 'success');
                
                this.selectedDevice = null;
                sessionStorage.removeItem('selectedDevice');
                
                document.dispatchEvent(new CustomEvent('devices-updated'));
                
                // Disable options on the current locations page
                this.isDeviceActive = false;
                await this.afterRender(); // Re-render the page to reflect the disabled state
            } else {
                showError(`❌ Failed to eject: ${data.error || 'Unknown error'}`, 'error');
            }
            
        } catch (error) {
            showError(`❌ Error: ${error.message}`, 'error');
        }
    }

    destroy() {
        console.log('Cleaning up Locations page');
        
        // Remove event listener
        if (this.handleDeviceEjected) {
            document.removeEventListener('device-ejected', this.handleDeviceEjected);
        }
    }
}
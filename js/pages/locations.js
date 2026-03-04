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
            { category: 'Documents', percentage: 20, color: 'bg-purple-500' },
            { category: 'Media', percentage: 10, color: 'bg-yellow-500' },
            { category: 'Applications', percentage: 7.5, color: 'bg-indigo-500' },
            { category: 'Other', percentage: 17.5, color: 'bg-gray-400' }
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
            'System': 'text-blue-500',
            'Documents': 'text-purple-500',
            'Media': 'text-yellow-500',
            'Applications': 'text-indigo-500',
            'Other': 'text-gray-500'
        };
        return colors[category] || 'text-gray-500';
    }

    getDeviceIconColor(percentUsed, isDeviceActive) {
        if (percentUsed > 90) return 'text-red-500 dark:text-red-400';
        if (percentUsed > 75) return 'text-yellow-500 dark:text-yellow-400';
        if (isDeviceActive) return 'text-green-500 dark:text-green-400';
        return 'text-gray-500 dark:text-gray-400';
    }

    getUsageBarColor(percentUsed, isDeviceActive) {
        if (percentUsed > 90) return 'bg-red-500';
        if (percentUsed > 75) return 'bg-yellow-500';
        if (isDeviceActive) return 'bg-green-500';
        return 'bg-blue-500';
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
            { category: 'Documents', percentage: 20, color: 'bg-purple-500' },
            { category: 'Media', percentage: 10, color: 'bg-yellow-500' },
            { category: 'Applications', percentage: 7.5, color: 'bg-indigo-500' },
            { category: 'Other', percentage: 17.5, color: 'bg-gray-400' }
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
                    <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-64 animate-pulse mb-2"></div>
                    <div class="h-4 bg-gray-100 dark:bg-gray-800 rounded w-96 animate-pulse"></div>
                </div>
                <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark p-8">
                    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        ${createCardLoadingSkeleton(3)}
                    </div>
                </div>
            `;
        }

        if (this.error) {
            return `
                <div class="flex flex-col items-center justify-center h-full p-8">
                    <div class="w-16 h-16 rounded-full bg-red-100 dark:bg-red-900 flex items-center justify-center mb-4">
                        <span class="material-icons-round text-red-600 dark:text-red-400 text-2xl">error</span>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Error Loading Folders</h3>
                    <p class="text-gray-500 dark:text-gray-400 text-center mb-6">${this.error}</p>
                    <button onclick="window.location.reload()" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
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
        const statusDotColor = isDeviceActive ? 'bg-green-500' : 
                              statusColor === 'green' ? 'bg-green-500' :
                              statusColor === 'yellow' ? 'bg-yellow-500' :
                              statusColor === 'red' ? 'bg-red-500' : 'bg-gray-500';
        const statusBgColor = isDeviceActive ? 'bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-800' :
                             statusColor === 'green' ? 'bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-800' :
                             statusColor === 'yellow' ? 'bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-100 dark:border-yellow-800' :
                             statusColor === 'red' ? 'bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-800' :
                             'bg-gray-50 dark:bg-gray-800/20 border border-gray-100 dark:border-gray-700';
        const statusTextColor = isDeviceActive ? 'text-green-700 dark:text-green-300' :
                               statusColor === 'green' ? 'text-green-700 dark:text-green-300' :
                               statusColor === 'yellow' ? 'text-yellow-700 dark:text-yellow-300' :
                               statusColor === 'red' ? 'text-red-700 dark:text-red-300' :
                               'text-gray-700 dark:text-gray-300';

        // Get storage breakdown (fake categories for now). Pass usedStorage so sizes can be computed.
        const storageBreakdown = this.getStorageBreakdown(percentUsed, usedStorage);
        const totalBreakdownPercent = storageBreakdown.reduce((sum, item) => sum + item.percentage, 0);
        
        // Calculate free space percentage
        const freePercent = Math.max(0, 100 - totalBreakdownPercent);

        return `
            <div class="flex flex-col h-full overflow-hidden">
                <div class="px-8 py-6 bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark flex-shrink-0">
                    <div class="flex gap-8 items-start">
                        <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center shadow-soft border border-gray-200 dark:border-gray-600 flex-shrink-0">
                            <span class="material-symbols-outlined text-5xl ${this.getDeviceIconColor(percentUsed, isDeviceActive)}">hard_drive</span>
                        </div>
                        <div class="flex-1">
                            <div class="flex justify-between items-center mb-2">
                                <div>
                                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">${deviceName}</h1>
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
                                                <button id="use-device-btn" class="px-3 py-1 rounded bg-blue-600 text-white text-sm hover:bg-blue-700">Use As Backup Device</button>
                                            `}
                                        </div>
                                    ` : ''}
                                </div>
                            </div>
                            <div class="mb-4">
                                <div class="flex justify-between text-xs font-medium mb-1.5">
                                    <span class="text-gray-700 dark:text-gray-300">Storage Used</span>
                                    <span class="text-text-secondary-light dark:text-text-secondary-dark">${usedStorage} of ${totalStorage} (${percentUsed}%)</span>
                                </div>
                                <div class="w-full h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden flex">
                                    ${storageBreakdown.map(item => `
                                        <div class="h-full ${item.color}" style="width: ${item.percentage}%" title="${item.category} (${item.size})"></div>
                                    `).join('')}
                                    ${freePercent > 0 ? `<div class="h-full bg-transparent" style="width: ${freePercent}%" title="Free (${freeStorage})"></div>` : ''}
                                </div>
                                
                                <!-- Compact horizontal breakdown with icons -->
                                <div class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
                                    <div class="flex flex-wrap items-center gap-2 mb-1">
                                        ${storageBreakdown.map(item => {
                                            // Get icon for each category
                                            const icon = this.getCategoryIcon(item.category);
                                            return `
                                            <div class="group relative">
                                                <div class="flex items-center gap-1 px-2 py-1 bg-gray-50 dark:bg-gray-800 rounded-lg cursor-help hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                                                    <span class="material-icons-round text-sm ${this.getCategoryIconColor(item.category)}">${icon}</span>
                                                    <span class="text-xs font-medium text-gray-700 dark:text-gray-200">${item.category}</span>
                                                    <span class="text-xs text-gray-500 dark:text-gray-400">${item.percentage}%</span>
                                                </div>
                                                <!-- Tooltip -->
                                                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-10">
                                                    ${item.category}: ${item.size}
                                                    <div class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-gray-900"></div>
                                                </div>
                                            </div>
                                            `;
                                        }).join('')}
                                        
                                        <div class="group relative">
                                            <div class="flex items-center gap-1 px-2 py-1 bg-green-50 dark:bg-green-900/20 rounded-lg cursor-help hover:bg-green-100 dark:hover:bg-green-900/30 transition-colors">
                                                <span class="material-icons-round text-sm text-green-600 dark:text-green-400">check_circle</span>
                                                <span class="text-xs font-medium text-green-700 dark:text-green-300">Free</span>
                                                <span class="text-xs text-green-600 dark:text-green-400">${freePercent}%</span>
                                            </div>
                                            <!-- Tooltip -->
                                            <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity whitespace-nowrap z-10">
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
                <div class="px-6 py-2 bg-gray-50/50 dark:bg-gray-800/30 border-b border-border-light dark:border-border-dark flex items-center justify-between flex-shrink-0">
                    <div class="flex items-center gap-2">
                        <div class="flex items-center text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-border-light dark:border-border-dark rounded px-2 py-1 shadow-sm" id="breadcrumbs">
                            ${this.renderBreadcrumbs()}
                        </div>
                    </div>
                    <div class="flex items-center gap-2">
                        <div class="flex bg-gray-200 dark:bg-gray-700 rounded-lg p-0.5" id="view-toggle">
                            <button class="p-1 rounded-md ${this.currentView === 'list' ? 'bg-white dark:bg-gray-600 shadow-sm text-gray-800 dark:text-white' : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white'}" data-view="list">
                                <span class="material-icons-round text-lg">list</span>
                            </button>
                            <button class="p-1 rounded-md ${this.currentView === 'grid' ? 'bg-white dark:bg-gray-600 shadow-sm text-gray-800 dark:text-white' : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white'}" data-view="grid">
                                <span class="material-icons-round text-lg">grid_view</span>
                            </button>
                        </div>
                        <button class="flex items-center gap-1.5 px-3 py-1.5 ${isDeviceActive ? 'bg-blue-500 hover:bg-blue-600 text-white' : 'bg-gray-300 text-gray-600 cursor-not-allowed'} rounded-md shadow-sm transition-colors text-xs font-medium" id="save-changes-btn" ${isDeviceActive ? '' : 'disabled'}>
                            <span class="material-icons-round text-sm">save</span>
                            Save Changes
                        </button>
                    </div>
                </div>
                <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark ${!isDeviceActive ? 'pointer-events-none opacity-60' : ''}">
                    ${this.data.folders.length > 0 ? (this.currentView === 'list' ? `
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-gray-50 dark:bg-gray-800 sticky top-0 z-0">
                                <tr>
                                    <th class="w-12 px-4 py-2 border-b border-gray-200 dark:border-border-dark">
                                        <input class="rounded border-gray-300 text-primary focus:ring-primary h-4 w-4" type="checkbox" id="select-all" />
                                    </th>
                                    <th class="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-border-dark w-1/3">Name</th>
                                    <th class="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-border-dark">Date Modified</th>
                                    <th class="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-border-dark">Kind</th>
                                    <th class="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-border-dark">Size</th>
                                    <th class="px-4 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-border-dark text-right">Action</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-100 dark:divide-gray-800 text-sm" id="folders-list">
                                ${this.renderFoldersList()}
                            </tbody>
                        </table>
                    ` : `
                        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4" id="folders-grid">
                            ${this.data.folders.map(folder => `
                                <div class="p-4 rounded-lg border border-gray-200 dark:border-gray-700 flex items-center justify-between" data-folder="${folder.name}" data-type="${folder.type}">
                                    <div class="flex items-center gap-3">
                                        <input class="rounded border-gray-300 text-primary focus:ring-primary h-4 w-4 ${folder.protected ? 'opacity-50 cursor-not-allowed' : ''}" 
                                            type="checkbox" 
                                            ${folder.selected ? 'checked' : ''}
                                            ${folder.protected || !isDeviceActive ? 'disabled' : ''}
                                            data-folder="${folder.name}" />
                                        <span class="material-icons-round ${folder.protected ? 'text-gray-400' : 'text-blue-400'} text-3xl">${folder.icon}</span>
                                        <div>
                                            <div class="font-medium ${folder.protected ? 'text-gray-500' : 'text-gray-900 dark:text-gray-200'}">${folder.name}</div>
                                            <div class="text-xs text-text-secondary-light dark:text-text-secondary-dark">${folder.date} • ${folder.size}</div>
                                        </div>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        ${folder.protected ? '<span class="text-xs font-medium text-gray-400 px-2 py-1">Protected</span>' : `<span class="text-xs font-medium ${folder.selected ? 'text-green-600' : 'text-text-secondary-light'} px-2 py-1 rounded">${folder.selected ? 'Included' : 'Excluded'}</span>`}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    `) : `
                        <div class="flex flex-col items-center justify-center h-full p-8">
                            <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
                                <span class="material-icons-round text-gray-400 text-2xl">folder_open</span>
                            </div>
                            <p class="text-gray-500 dark:text-gray-400">No folders found in home directory</p>
                        </div>
                    `}
                </div>
                <div class="px-6 py-2 bg-gray-50 dark:bg-gray-800 border-t border-border-light dark:border-border-dark text-xs text-text-secondary-light dark:text-text-secondary-dark flex justify-between items-center flex-shrink-0">
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
                ${index > 0 ? '<span class="material-icons-round text-base text-gray-400 mx-1">chevron_right</span>' : ''}
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
            <tr class="hover:bg-blue-50 dark:hover:bg-blue-900/20 group cursor-default transition-colors ${folder.protected ? 'bg-gray-50/50 dark:bg-gray-800/30 cursor-not-allowed' : ''}" 
                data-folder="${folder.name}"
                data-type="${folder.type}">
                <td class="px-4 py-3">
                    <input class="rounded border-gray-300 text-primary focus:ring-primary h-4 w-4 ${folder.protected ? 'opacity-50 cursor-not-allowed' : ''}" 
                           type="checkbox" 
                           ${folder.selected ? 'checked' : ''}
                           ${folder.protected || !isDeviceActive ? 'disabled' : ''}
                           data-folder="${folder.name}" />
                </td>
                <td class="px-4 py-3 whitespace-nowrap">
                    <div class="flex items-center gap-3">
                        <span class="material-icons-round ${folder.protected ? 'text-gray-400' : 'text-blue-400'} text-xl">${folder.icon}</span>
                        <span class="font-medium ${folder.protected ? 'text-gray-500 dark:text-gray-500' : 'text-gray-900 dark:text-gray-200'}">${folder.name}</span>
                    </div>
                </td>
                <td class="px-4 py-3 ${folder.protected ? 'text-gray-400' : 'text-gray-500 dark:text-gray-400'} whitespace-nowrap">${folder.date}</td>
                <td class="px-4 py-3 ${folder.protected ? 'text-gray-400' : 'text-gray-500 dark:text-gray-400'} whitespace-nowrap">${folder.kind}</td>
                <td class="px-4 py-3 ${folder.protected ? 'text-gray-400' : 'text-gray500 dark:text-gray-400'} whitespace-nowrap">${folder.size}</td>
                <td class="px-4 py-3 whitespace-nowrap text-right">
                    ${folder.protected ? 
                        `<span class="text-xs font-medium text-gray-400 px-2 py-1">Protected</span>` :
                        `<span class="text-xs font-medium ${folder.selected ? 'text-green-600' : 'text-text-secondary-light'} px-2 py-1 rounded">${folder.selected ? 'Included' : 'Excluded'}</span>`
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
                    <div class="relative transform overflow-hidden rounded-2xl bg-[#1c1c1e] text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-3xl border border-gray-700">
                        <div class="px-6 py-5 border-b border-gray-700 flex justify-between items-center bg-[#2c2c2e]">
                            <div>
                                <h3 class="text-xl font-semibold leading-6 text-white" id="modal-title">Get File Versions</h3>
                                <p class="mt-1 text-sm text-gray-400">Choose a recovery point for your files.</p>
                            </div>
                            <button class="text-gray-400 hover:text-white transition-colors" id="close-get-versions-modal">
                                <span class="material-icons-round">close</span>
                            </button>
                        </div>
                        <div class="px-6 py-8 bg-[#1c1c1e]">
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4" id="version-points">
                                ${this.data.versionPoints.map(point => `
                                    <div class="relative flex cursor-pointer rounded-xl ${point.selected ? 'border-2 border-primary bg-primary/10' : 'border border-gray-700 hover:border-gray-500 bg-[#2c2c2e] hover:bg-[#3a3a3c]'} p-4 shadow-sm focus:outline-none ring-offset-2 ring-offset-[#1c1c1e] ring-primary transition-all" 
                                         data-version-point="${point.id}">
                                        <div class="flex w-full items-center justify-between">
                                            <div class="flex items-center gap-4">
                                                <div class="flex h-12 w-12 items-center justify-center rounded-full ${point.selected ? 'bg-primary/20 text-blue-400' : 'bg-gray-700 text-gray-300'}">
                                                    <span class="material-icons-round text-2xl">${point.icon}</span>
                                                </div>
                                                <div>
                                                    <p class="font-semibold ${point.selected ? 'text-white' : 'text-gray-200'}">${point.name}</p>
                                                    <p class="text-sm ${point.selected ? 'text-gray-400' : 'text-gray-500'}">${point.time}</p>
                                                </div>
                                            </div>
                                            ${point.selected ? '<span class="material-icons-round text-primary text-xl">check_circle</span>' : ''}
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                            <div class="mt-6 flex items-start gap-3 p-4 rounded-lg bg-[#2c2c2e] border border-gray-700">
                                <span class="material-icons-round text-blue-400 mt-0.5">info</span>
                                <div class="text-sm text-gray-300">
                                    <p class="font-medium text-white mb-0.5">Get Versions Summary</p>
                                    <p>You are about to get versions for <span class="font-semibold text-white">${selectedCount} items</span> from <span class="font-semibold text-white">${device.name || 'Device'}</span> to their state on <span class="font-semibold text-white">${selectedVersionPoint?.name || ''} at ${selectedVersionPoint?.time || ''}</span>.</p>
                                </div>
                            </div>
                        </div>
                        <div class="bg-[#2c2c2e] px-6 py-4 sm:flex sm:flex-row-reverse sm:px-6 gap-3 border-t border-gray-700">
                            <button class="inline-flex w-full justify-center rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white shadow-glow hover:bg-blue-600 sm:w-auto transition-colors items-center gap-2" id="confirm-get-versions" type="button">
                                <span class="material-icons-round text-lg">history</span>
                                Get Versions
                            </button>
                            <button class="mt-3 inline-flex w-full justify-center rounded-lg bg-[#3a3a3c] px-4 py-2.5 text-sm font-semibold text-gray-200 shadow-sm ring-1 ring-inset ring-gray-600 hover:bg-[#48484a] sm:mt-0 sm:w-auto transition-colors" id="cancel-get-versions" type="button">Cancel</button>
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
                btn.classList.add('bg-white', 'dark:bg-gray-600', 'shadow-sm', 'text-gray-800', 'dark:text-white');
                btn.classList.remove('text-gray-500', 'dark:text-gray-400', 'hover:text-gray-800', 'dark:hover:text-white');
            } else {
                btn.classList.remove('bg-white', 'dark:bg-gray-600', 'shadow-sm', 'text-gray-800', 'dark:text-white');
                btn.classList.add('text-gray-500', 'dark:text-gray-400', 'hover:text-gray-800', 'dark:hover:text-white');
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
                    badge.classList.toggle('text-green-600', checked);
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
                badge.classList.toggle('text-green-600', folder.selected);
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
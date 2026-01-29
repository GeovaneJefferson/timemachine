// dashboard.js - Dashboard Page Module

import { createTableLoadingSkeleton } from '../utils/loading-skeleton.js';

export default class DashboardPage {
    constructor() {
        this.name = 'dashboard';
        this.data = {
            systemInfo: {
                name: 'Loading...',
                memory: 'Loading...',
                storage: 'Loading...',
                os: 'Loading...'
            },
            backupInfo: {
                lastBackup: 'Loading...',
                nextScheduled: 'Not configured',
                diskUsage: 0
            },
            // Backup summary data
            summary: {
                categories: [],
                totalFiles: 0,
                totalSize: '0 B',
                mostFrequent: []
            },
            files: [] // Initialize empty array - will be populated from API
        };
        
        // Fetch real data immediately
        this.loadRealData();
    }

    // Load real system data from backend
    async loadRealData() {
        try {
            const [sysRes, backupRes, summaryRes, recentFilesRes] = await Promise.all([
                fetch('/api/system-info'),
                fetch('/api/backup/usage'),
                fetch('/api/backup-summary'), // New endpoint for backup summary
                fetch('/api/backup/recent-files') // Fetch recent backup files
            ]);
            
            const sysData = await sysRes.json();
            const backupData = await backupRes.json();
            
            if (sysData.success) {
                this.data.systemInfo.name = `${sysData.username || 'User'}'s Computer`;
                this.data.systemInfo.os = sysData.platform || 'Unknown';
            }
            
            if (backupData.success) {
                // Get memory info from psutil
                const memResponse = await fetch('/api/system-memory');
                const memData = await memResponse.json();
                
                this.data.systemInfo.memory = memData.success ? memData.memory_total : 'N/A';
                this.data.systemInfo.storage = backupData.home_human_total || 'N/A';
                
                if (backupData.connected && backupData.has_backup) {
                    this.data.backupInfo.diskUsage = backupData.percent_used || 0;
                } else {
                    this.data.backupInfo.diskUsage = 0;
                }
                
                // Always hide last backup
                this.data.backupInfo.lastBackup = '';
            }
            
            // Load backup summary
            if (summaryRes.ok) {
                const summaryData = await summaryRes.json();
                if (summaryData.success) {
                    this.data.summary = {
                        categories: summaryData.categories || [],
                        totalFiles: summaryData.total_files || 0,
                        totalSize: summaryData.total_size_str || '0 B',
                        mostFrequent: summaryData.most_frequent_recent_backups || [],
                        generatedAt: summaryData.generated_at || ''
                    };
                }
            } else {
                // Fallback to default categories if API fails
                this.data.summary.categories = [
                    { name: 'Images', count: 0, size_str: '0 B', icon: 'image' },
                    { name: 'Videos', count: 0, size_str: '0 B', icon: 'video_library' },
                    { name: 'Music', count: 0, size_str: '0 B', icon: 'music_note' },
                    { name: 'Documents', count: 0, size_str: '0 B', icon: 'description' }
                ];
            }
            
            // NEW: Load recent backup files
            if (recentFilesRes.ok) {
                const recentFilesData = await recentFilesRes.json();
                if (recentFilesData.success) {
                    this.data.files = recentFilesData.files || [];
                } else {
                    // Fallback to default files if API fails
                    this.data.files = this.getDefaultFilesData();
                }
            } else {
                // Fallback to default files if API fails
                this.data.files = this.getDefaultFilesData();
            }
            
            // Mark files as loaded
            window.dashboardFilesLoaded = true;
            
            // Re-render after data is loaded
            this.updateDisplay();
            
        } catch (error) {
            console.error('Error fetching system data:', error);
            // Set default categories on error
            this.data.summary.categories = [
                { name: 'Images', count: 0, size_str: '0 B', icon: 'image' },
                { name: 'Videos', count: 0, size_str: '0 B', icon: 'video_library' },
                { name: 'Music', count: 0, size_str: '0 B', icon: 'music_note' },
                { name: 'Documents', count: 0, size_str: '0 B', icon: 'description' }
            ];
            // Fallback to default files
            this.data.files = this.getDefaultFilesData();
            window.dashboardFilesLoaded = true;
            this.updateDisplay();
        }
    }

    // Default fallback files data
    getDefaultFilesData() {
        return [];
    }

    // Update the display with new data
    updateDisplay() {
        const headerEl = document.querySelector('.px-8.pt-8.pb-6');
        if (headerEl) {
            headerEl.outerHTML = this.renderHeader();
        }
        
        const deviceInfoEl = document.querySelector('.px-8.py-6.border-b');
        if (deviceInfoEl) {
            deviceInfoEl.outerHTML = this.renderDeviceInfo();
        }
        
        // Update files table if it exists
        const filesTableContainer = document.querySelector('.flex-1.overflow-y-auto.bg-white.dark\\:bg-surface-dark');
        if (filesTableContainer) {
            filesTableContainer.outerHTML = this.renderFilesTable();
        }
        
        // Re-attach event listeners after DOM update
        setTimeout(() => this.attachEventListeners(), 100);
    }

    // Render the entire dashboard page
    async render() {
        return `
            <!-- Header Section -->
            ${this.renderHeader()}
            
            <!-- Device Info Section -->
            ${this.renderDeviceInfo()}
            
            <!-- Files Table -->
            ${this.renderFilesTable()}
        `;
    }

    // Render the header with device info
    renderHeader() {
        return `
            <div class="px-8 pt-8 pb-6 border-b border-border-light dark:border-border-dark flex gap-6 items-center bg-surface-light dark:bg-surface-dark">
                <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-gray-50 to-gray-200 dark:from-gray-800 dark:to-gray-900 flex items-center justify-center shadow-soft border border-gray-200 dark:border-gray-700 flex-shrink-0">
                    <span class="material-icons-round text-5xl text-gray-600 dark:text-gray-400">laptop_mac</span>
                </div>
                <div class="flex-1">
                    <div class="flex justify-between items-start">
                        <div>
                            <h1 class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">${this.data.systemInfo.name}</h1>
                            <div class="flex items-center gap-4 mt-2 text-sm text-text-secondary-light dark:text-text-secondary-dark">
                                <span class="flex items-center gap-1.5">
                                    <span class="material-icons-round text-base">memory</span>
                                    ${this.data.systemInfo.memory}
                                </span>
                                <span class="flex items-center gap-1.5">
                                    <span class="material-icons-round text-base">storage</span>
                                    ${this.data.systemInfo.storage}
                                </span>
                                <span class="flex items-center gap-1.5">
                                    <span class="material-icons-round text-base">update</span>
                                    ${this.data.systemInfo.os}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4 flex gap-8">
                        <div>
                            <p class="text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wide">Disk Usage</p>
                            <div class="flex items-center gap-2 mt-0.5">
                                <div class="w-24 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                    <div class="h-full bg-primary rounded-full" style="width: ${this.data.backupInfo.diskUsage}%"></div>
                                </div>
                                <span class="text-xs font-medium text-gray-600 dark:text-gray-400">${this.data.backupInfo.diskUsage}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Render the device info section - UPDATED to remove buttons and show category summary
    renderDeviceInfo() {
        // Get categories or use defaults
        const categories = this.data.summary.categories.length > 0 
            ? this.data.summary.categories 
            : [
                { name: 'Images', count: 0, size_str: '0 B', icon: 'image' },
                { name: 'Videos', count: 0, size_str: '0 B', icon: 'video_library' },
                { name: 'Music', count: 0, size_str: '0 B', icon: 'music_note' },
                { name: 'Documents', count: 0, size_str: '0 B', icon: 'description' }
            ];
        
        // Calculate total files and size for summary
        const totalFiles = categories.reduce((sum, cat) => sum + (cat.count || 0), 0);
        const totalSize = this.data.summary.totalSize || categories.reduce((sum, cat) => {
            // Try to extract size from size_str
            const sizeMatch = cat.size_str?.match(/([\d.]+)\s+(\w+)/);
            if (sizeMatch) {
                const value = parseFloat(sizeMatch[1]);
                const unit = sizeMatch[2];
                // Simple conversion for display (not accurate but good for UI)
                return sum + value;
            }
            return sum;
        }, 0).toFixed(1) + ' GB';
        
        return `
            <div class="px-8 py-6 border-b border-border-light dark:border-border-dark bg-surface-light dark:bg-surface-dark">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Backup Summary</h2>
                        <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">
                            ${totalFiles} files • ${totalSize} total
                        </p>
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                    ${categories.map(category => this.renderCategoryCard(category)).join('')}
                </div>
                
                <!-- Most Frequently Modified Files - HORIZONTAL LAYOUT -->
                ${this.renderMostFrequentSection()}
            </div>
        `;
    }

    // Render a single category card
    renderCategoryCard(category) {
        // Map category names to colors and icons
        const categoryConfig = {
            'Images': { color: 'from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/30', border: 'border-blue-100 dark:border-blue-800', icon: 'image', iconColor: 'text-blue-500' },
            'Image': { color: 'from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/30', border: 'border-blue-100 dark:border-blue-800', icon: 'image', iconColor: 'text-blue-500' },
            'Videos': { color: 'from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/30', border: 'border-purple-100 dark:border-purple-800', icon: 'video_library', iconColor: 'text-purple-500' },
            'Video': { color: 'from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/30', border: 'border-purple-100 dark:border-purple-800', icon: 'video_library', iconColor: 'text-purple-500' },
            'Music': { color: 'from-pink-50 to-pink-100 dark:from-pink-900/20 dark:to-pink-800/30', border: 'border-pink-100 dark:border-pink-800', icon: 'music_note', iconColor: 'text-pink-500' },
            'Documents': { color: 'from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/30', border: 'border-green-100 dark:border-green-800', icon: 'description', iconColor: 'text-green-500' },
            'Document': { color: 'from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/30', border: 'border-green-100 dark:border-green-800', icon: 'description', iconColor: 'text-green-500' },
            'Others': { color: 'from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700', border: 'border-gray-200 dark:border-gray-700', icon: 'folder', iconColor: 'text-gray-500' }
        };
        
        const config = categoryConfig[category.name] || {
            color: 'from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700',
            border: 'border-gray-200 dark:border-gray-700',
            icon: category.icon || 'folder',
            iconColor: 'text-gray-500'
        };
        
        return `
            <div class="bg-gradient-to-br ${config.color} p-4 rounded-lg border ${config.border}">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-gray-700 dark:text-gray-300">${category.name}</p>
                        <p class="text-2xl font-bold text-gray-900 dark:text-white mt-1">${category.count || 0}</p>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mt-0.5">${category.size_str || '0 B'}</p>
                    </div>
                    <span class="material-icons-round ${config.iconColor} text-2xl">${config.icon}</span>
                </div>
            </div>
        `;
    }

    // Render most frequently modified files section - HORIZONTAL LAYOUT
    renderMostFrequentSection() {
        const frequentFiles = this.data.summary.mostFrequent || [];
        
        if (frequentFiles.length === 0) {
            return '';
        }
        
        return `
            <div class="mt-6">
                <div class="flex items-center justify-between mb-3">
                    <h3 class="text-sm font-semibold text-gray-900 dark:text-white">Most Frequently Modified Files</h3>
                    ${this.data.summary.generatedAt ? `
                        <p class="text-xs text-gray-400 dark:text-gray-500">
                            Updated: ${new Date(this.data.summary.generatedAt).toLocaleDateString()}
                        </p>
                    ` : ''}
                </div>
                <div class="relative">
                    <div class="flex overflow-x-auto gap-3 pb-4 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600 scrollbar-track-transparent">
                        ${frequentFiles.slice(0, 10).map((file, index) => `
                            <div class="flex-shrink-0 w-64 p-4 bg-gradient-to-br from-gray-50 to-white dark:from-gray-800 dark:to-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-md transition-all duration-200 hover:border-gray-300 dark:hover:border-gray-600 group cursor-pointer">
                                <div class="flex items-start gap-3">
                                    <div class="w-10 h-10 rounded-lg bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                                        <span class="material-icons-round text-blue-500 dark:text-blue-400">insert_drive_file</span>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <div class="flex items-center gap-2 mb-1">
                                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300">
                                                ${index + 1}
                                            </span>
                                            <p class="text-xs text-gray-500 dark:text-gray-400 font-medium">
                                                Modified ${file.count || 0} times
                                            </p>
                                        </div>
                                        <p class="text-sm font-medium text-gray-900 dark:text-gray-200 truncate" title="${file.path}">
                                            ${this.formatFilePath(file.path)}
                                        </p>
                                        <div class="mt-2 pt-2 border-t border-gray-100 dark:border-gray-700">
                                            <p class="text-xs text-gray-500 dark:text-gray-400 truncate" title="${file.path}">
                                                ${this.formatDirectoryPath(file.path)}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-3 flex items-center gap-1 text-xs text-gray-400 dark:text-gray-500">
                                    <span class="material-icons-round text-sm">schedule</span>
                                    <span>Recently active</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    ${frequentFiles.length > 5 ? `
                        <div class="absolute right-0 top-0 bottom-4 w-8 bg-gradient-to-l from-white dark:from-gray-900 to-transparent pointer-events-none"></div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    // Format file path for display
    formatFilePath(path) {
        if (!path) return '';
        // Extract filename from path
        const parts = path.split('/');
        return parts[parts.length - 1] || path;
    }

    // Format directory path (remove filename)
    formatDirectoryPath(path) {
        if (!path) return '';
        const parts = path.split('/');
        if (parts.length > 1) {
            // Remove the filename and join the rest
            const directory = parts.slice(0, -1).join('/');
            // Truncate if too long
            if (directory.length > 40) {
                return '...' + directory.substring(directory.length - 37);
            }
            return directory;
        }
        return '/';
    }

    // Render the files table
    renderFilesTable() {
        if (this.data.files.length === 0) {
            // Show loading skeleton while fetching
            if (!window.dashboardFilesLoaded) {
                return `
                    <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark">
                        <div class="px-8 py-4 border-b border-gray-200 dark:border-gray-700 animate-pulse">
                            <div class="h-6 bg-gray-200 dark:bg-gray-700 rounded w-48 mb-2"></div>
                            <div class="h-4 bg-gray-100 dark:bg-gray-800 rounded w-32"></div>
                        </div>
                        ${createTableLoadingSkeleton(5)}
                    </div>
                `;
            }

            // Show empty state with setup tutorial
            return `
                <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark flex items-center justify-center">
                    <div class="text-center px-8 max-w-md">
                        <div class="mb-6">
                            <span class="material-icons-round text-6xl text-gray-300 dark:text-gray-600">backup</span>
                        </div>
                        <h3 class="text-2xl font-semibold text-gray-900 dark:text-white mb-2">No Backup Files Found</h3>
                        <p class="text-gray-600 dark:text-gray-400 mb-6">Start your first backup to see files here.</p>
                        
                        <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 text-left mb-6">
                            <h4 class="font-semibold text-blue-900 dark:text-blue-200 mb-3">Quick Setup Guide:</h4>
                            <ol class="text-sm text-blue-800 dark:text-blue-300 space-y-2">
                                <li class="flex gap-2">
                                    <span class="font-bold flex-shrink-0">1.</span>
                                    <span>Go to <strong>Locations</strong> (left sidebar) to see available backup devices</span>
                                </li>
                                <li class="flex gap-2">
                                    <span class="font-bold flex-shrink-0">2.</span>
                                    <span>Click on a device you want to use for backups</span>
                                </li>
                                <li class="flex gap-2">
                                    <span class="font-bold flex-shrink-0">3.</span>
                                    <span>Click <strong>"Use As Backup Device"</strong> button (top right)</span>
                                </li>
                                <li class="flex gap-2">
                                    <span class="font-bold flex-shrink-0">4.</span>
                                    <span>Go to <strong>Folders</strong> and select what to backup</span>
                                </li>
                                <li class="flex gap-2">
                                    <span class="font-bold flex-shrink-0">5.</span>
                                    <span>Enable <strong>"Automatic Backups"</strong> in Settings</span>
                                </li>
                            </ol>
                        </div>
                    </div>
                </div>
            `;
        }
        
        return `
            <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark">
                <div class="px-8 py-4 border-b border-gray-200 dark:border-gray-700">
                    <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Recent Backup Files</h2>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">${this.data.files.length} backup files found</p>
                </div>
                <table class="w-full text-left border-collapse">
                    <thead class="bg-gray-50 dark:bg-gray-800 sticky top-0 z-0 shadow-sm">
                        <tr>
                            <th class="px-6 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700 w-1/3">Name</th>
                            <th class="px-6 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">Date Modified</th>
                            <th class="px-6 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">Size</th>
                            <th class="px-6 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">Type</th>
                            <th class="px-6 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">Snapshot</th>
                            <th class="px-6 py-2 text-xs font-semibold text-gray-500 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700">Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 dark:divide-gray-800 text-sm">
                        ${this.data.files.map(file => this.renderFileRow(file)).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    // Render a single file row
    renderFileRow(file) {
        const statusClasses = {
            completed: 'bg-green-100 text-green-800 dark:bg-green-500/20 dark:text-green-300',
            archived: 'bg-gray-100 text-gray-800 dark:bg-gray-600/40 dark:text-gray-300',
            failed: 'bg-red-100 text-red-800 dark:bg-red-500/20 dark:text-red-300',
            in_progress: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-500/20 dark:text-yellow-300',
            pending: 'bg-blue-100 text-blue-800 dark:bg-blue-500/20 dark:text-blue-300'
        };

        const statusText = {
            completed: 'Completed',
            archived: 'Archived',
            failed: 'Failed',
            in_progress: 'In Progress',
            pending: 'Pending'
        };

        // Change type badges (new vs modified)
        const changeTypeClasses = {
            new: 'bg-blue-100 text-blue-800 dark:bg-blue-500/20 dark:text-blue-300',
            modified: 'bg-amber-100 text-amber-800 dark:bg-amber-500/20 dark:text-amber-300'
        };

        const changeTypeText = {
            new: 'New',
            modified: 'Modified'
        };

        // Determine icon based on file type or name
        let icon = file.icon || 'description';
        if (file.type === 'folder') {
            icon = 'folder';
        } else if (file.name.toLowerCase().includes('backup')) {
            icon = 'folder_zip';
        } else if (file.name.toLowerCase().includes('log')) {
            icon = 'description';
        }

        // Determine status if not provided
        const status = file.status || 'completed';
        const changeType = file.change_type || 'new';
        
        // Create snapshot link based on file name
        const snapshotLink = file.snapshotLink || `#${file.name}`;

        return `
            <tr class="hover:bg-blue-50 dark:hover:bg-blue-900/20 group cursor-default transition-colors file-row-hover" 
                data-type="${file.type}" 
                data-name="${file.name}"
                oncontextmenu="window.showContextMenu(event, '${file.type}')">
                <td class="px-6 py-3 whitespace-nowrap">
                    <div class="flex items-center gap-3">
                        <span class="material-icons-round ${icon === 'folder_zip' || icon === 'folder' ? 'text-blue-400' : 'text-gray-400'} text-xl">
                            ${icon}
                        </span>
                        <span class="font-medium text-gray-900 dark:text-gray-200">${file.name}</span>
                    </div>
                </td>
                <td class="px-6 py-3 text-gray-500 dark:text-gray-400 whitespace-nowrap">${file.date}</td>
                <td class="px-6 py-3 text-gray-500 dark:text-gray-400 whitespace-nowrap">${file.size}</td>
                <td class="px-6 py-3 whitespace-nowrap">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${changeTypeClasses[changeType] || ''}">
                        ${changeTypeText[changeType] || changeType}
                    </span>
                </td>
                <td class="px-6 py-3 whitespace-nowrap">
                    <a class="text-primary hover:underline" href="${snapshotLink}">View Snapshot</a>
                </td>
                <td class="px-6 py-3 whitespace-nowrap">
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusClasses[status] || ''}">
                        ${statusText[status] || status}
                    </span>
                </td>
            </tr>
        `;
    }

    // Initialize dashboard-specific functionality
    afterRender() {
        this.attachEventListeners();
        this.updateMonitoringStatus();
        console.log('Dashboard page initialized');
    }

    // Attach event listeners
    attachEventListeners() {
        // Add click handlers for table rows and snapshot links
        const tableRows = document.querySelectorAll('.file-row-hover');
        tableRows.forEach(row => {
            row.addEventListener('click', (e) => {
                // Check if clicking on the "View Snapshot" link
                if (e.target.closest('a') && e.target.textContent === 'View Snapshot') {
                    e.preventDefault();
                    const fileName = row.getAttribute('data-name');
                    this.searchFile(fileName);
                    return;
                }
                
                // Regular row click
                if (!e.target.matches('a')) {
                    const fileName = row.getAttribute('data-name');
                    console.log('Selected file:', fileName);
                    // You could trigger a preview or selection here
                }
            });
        });

        // Add double-click handlers
        tableRows.forEach(row => {
            row.addEventListener('dblclick', (e) => {
                const fileType = row.getAttribute('data-type');
                const fileName = row.getAttribute('data-name');
                this.openFile(fileType, fileName);
            });
        });

        // Add click handlers for frequently modified files
        const frequentFiles = document.querySelectorAll('.cursor-pointer');
        frequentFiles.forEach((card, index) => {
            card.addEventListener('click', () => {
                const files = this.data.summary.mostFrequent || [];
                if (files[index]) {
                    this.openFrequentFile(files[index]);
                }
            });
        });

        // Add refresh button if exists
        const refreshBtn = document.querySelector('#refresh-backup-files');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshBackupFiles();
            });
        }
    }

    // Search for a file
    searchFile(fileName) {
        console.log('Searching for file:', fileName);
        
        // Get the search input from header
        const searchInput = document.getElementById('global-search-input');
        if (!searchInput) {
            console.error('Search input not found');
            return;
        }
        
        // Set the search value
        searchInput.value = fileName;
        
        // Trigger input event to update header state
        const inputEvent = new Event('input', { bubbles: true });
        searchInput.dispatchEvent(inputEvent);
        
        // Perform search via header if available
        if (window.appHeader && window.appHeader.performSearch) {
            window.appHeader.performSearch(fileName);
        } else {
            console.warn('Header not available for search');
        }
        
        // Focus on search input to show user it's active
        searchInput.focus();
    }

    // Open frequently modified file
    openFrequentFile(file) {
        console.log('Opening frequently modified file:', file.path);
        // You could implement navigation to the file preview or location
        // alert(`Would open: ${file.path}\nModified ${file.count} times`);
    }

    // Update monitoring status in header - REMOVED (header handles this now)
    updateMonitoringStatus() {
        // Do nothing - monitoring status is managed by header.js
    }

    // Open file/folder (simulated)
    openFile(type, name) {
        console.log(`Opening ${type}: ${name}`);
        // This would navigate to the appropriate page
        if (type === 'folder') {
            // router.navigate(`/folders/${encodeURIComponent(name)}`);
            alert(`Would open folder: ${name}`);
        } else {
            // router.navigate(`/file/${encodeURIComponent(name)}`);
            alert(`Would open file: ${name}`);
        }
    }

    // Refresh backup files data
    async refreshBackupFiles() {
        try {
            console.log('Refreshing backup files...');
            const response = await fetch('/api/backup/recent-files');
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.data.files = data.files || [];
                    this.updateDisplay();
                    console.log('Backup files refreshed successfully');
                }
            }
        } catch (error) {
            console.error('Error refreshing backup files:', error);
        }
    }

    // Get dashboard data (could be from API)
    async fetchData() {
        // Simulate API call
        return new Promise(resolve => {
            setTimeout(() => {
                resolve(this.data);
            }, 300);
        });
    }

    // Cleanup when leaving page
    destroy() {
        // Clean up any intervals or event listeners
        const monitoringElement = document.querySelector('.monitoring-status');
        if (monitoringElement && monitoringElement.intervalId) {
            clearInterval(monitoringElement.intervalId);
        }
    }
}

// Export a function to create dashboard page (factory pattern)
export function createDashboardPage() {
    return new DashboardPage();
}
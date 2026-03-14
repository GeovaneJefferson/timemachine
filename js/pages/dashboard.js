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
        const filesTableContainer = document.querySelector('.flex-1.overflow-y-auto');
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
                <div class="w-24 h-24 rounded-2xl bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)] flex items-center justify-center shadow-soft border border-[var(--color-separator)] flex-shrink-0">
                    <span class="material-icons-round text-5xl text-[var(--color-text-secondary)]">laptop_mac</span>
                </div>
                <div class="flex-1">
                    <div class="flex justify-between items-start">
                        <div>
                            <h1 class="text-2xl font-bold text-[var(--color-text-primary)] leading-tight">${this.data.systemInfo.name}</h1>
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
                                <div class="w-24 h-2 bg-[var(--color-separator)] dark:bg-[var(--color-tertiary-background)] rounded-full overflow-hidden">
                                    <div class="h-full bg-primary rounded-full" style="width: ${this.data.backupInfo.diskUsage}%"></div>
                                </div>
                                <span class="text-xs font-medium text-[var(--color-text-secondary)]">${this.data.backupInfo.diskUsage}%</span>
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
                        <h2 class="text-lg font-semibold text-[var(--color-text-primary)]">Backup Summary</h2>
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
            'Images': { color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]', border: 'border-[var(--color-separator)]', icon: 'image', iconColor: 'text-[var(--color-accent)]' },
            'Image': { color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]', border: 'border-[var(--color-separator)]', icon: 'image', iconColor: 'text-[var(--color-accent)]' },
            'Videos': { color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]', border: 'border-[var(--color-separator)]', icon: 'video_library', iconColor: 'text-[var(--color-accent)]' },
            'Video': { color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]', border: 'border-[var(--color-separator)]', icon: 'video_library', iconColor: 'text-[var(--color-accent)]' },
            'Music': { color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]', border: 'border-[var(--color-separator)]', icon: 'music_note', iconColor: 'text-[var(--color-accent)]' },
            'Documents': { color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]', border: 'border-[var(--color-separator)]', icon: 'description', iconColor: 'text-[var(--color-accent)]' },
            'Document': { color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]', border: 'border-[var(--color-separator)]', icon: 'description', iconColor: 'text-[var(--color-accent)]' },
            'Others': { color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]', border: 'border-[var(--color-separator)]', icon: 'folder', iconColor: 'text-[var(--color-accent)]' }
        };
        
        const config = categoryConfig[category.name] || {
            color: 'bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)]',
            border: 'border-[var(--color-separator)]',
            icon: category.icon || 'folder',
            iconColor: 'text-[var(--color-accent)]'
        };
        
        return `
            <div class="${config.color} p-4 rounded-lg border ${config.border}">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-[var(--color-text-secondary)]">${category.name}</p>
                        <p class="text-2xl font-bold text-[var(--color-text-primary)] mt-1">${category.count || 0}</p>
                        <p class="text-xs text-[var(--color-text-secondary)] mt-0.5">${category.size_str || '0 B'}</p>
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
                    <h3 class="text-sm font-semibold text-[var(--color-text-primary)]">Most Frequently Modified Files</h3>
                    ${this.data.summary.generatedAt ? `
                        <p class="text-xs text-[var(--color-text-secondary)]">
                            Updated: ${new Date(this.data.summary.generatedAt).toLocaleDateString()}
                        </p>
                    ` : ''}
                </div>
                <div class="relative">
                    <div class="flex overflow-x-auto gap-3 pb-4 scrollbar-thin scrollbar-thumb-[var(--color-separator)] dark:scrollbar-thumb-[var(--color-tertiary-background)] scrollbar-track-transparent">
                        ${frequentFiles.slice(0, 10).map((file, index) => `
                            <div class="frequent-file-card flex-shrink-0 w-64 p-4 bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)] rounded-lg border border-[var(--color-separator)] hover:shadow-md transition-all duration-200 hover:border-[var(--color-accent-lighter)] group cursor-pointer" data-file-path="${file.path}">
                                <div class="flex items-start gap-3">
                                    <div class="w-10 h-10 rounded-lg bg-[var(--color-accent-lighter)] dark:bg-[var(--color-accent-dark)] flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                                        <span class="material-icons-round text-[var(--color-accent)]">insert_drive_file</span>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <div class="flex items-center gap-2 mb-1">
                                            <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-[var(--color-accent-light)] text-[var(--color-accent)] dark:bg-[var(--color-accent-dark)] dark:text-[var(--color-accent-light)]">
                                                ${index + 1}
                                            </span>
                                            <p class="text-xs text-[var(--color-text-secondary)] font-medium">
                                                Modified ${file.count || file.weighted_score || 0} times
                                            </p>
                                        </div>
                                        <p class="text-sm font-medium text-[var(--color-text-primary)] truncate" title="${file.path}">
                                            ${this.formatFilePath(file.path)}
                                        </p>
                                        <div class="mt-2 pt-2 border-t border-[var(--color-separator)]">
                                            <p class="text-xs text-[var(--color-text-secondary)] truncate" title="${file.path}">
                                                ${this.formatDirectoryPath(file.path)}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-3 flex items-center gap-1 text-xs text-[var(--color-text-secondary)]">
                                    <span class="material-icons-round text-sm">schedule</span>
                                    <span>Recently active</span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                    ${frequentFiles.length > 5 ? `
                        <div class="absolute right-0 top-0 bottom-4 w-8 bg-gradient-to-l from-[var(--color-surface-light)] dark:from-[var(--color-surface-dark)] to-transparent pointer-events-none"></div>
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

    // Format date for display
    formatDate(dateString) {
        if (!dateString) {
            return '';
        }

        const date = new Date(dateString);
        const now = new Date();

        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        const dateToCompare = new Date(date.getFullYear(), date.getMonth(), date.getDate());

        const timeOptions = { hour: '2-digit', minute: '2-digit', hour12: false };
        const dateOptions = { month: 'short', day: 'numeric', year: 'numeric' };

        const formattedTime = date.toLocaleTimeString('en-GB', timeOptions);
        const formattedDate = date.toLocaleDateString('en-US', dateOptions);

        if (dateToCompare.getTime() === today.getTime()) {
            return `Today, ${formattedDate} at ${formattedTime}`;
        } else if (dateToCompare.getTime() === yesterday.getTime()) {
            return `Yesterday, ${formattedDate} at ${formattedTime}`;
        } else {
            return `${formattedDate} at ${formattedTime}`;
        }
    }

    // Render the files table
    renderFilesTable() {
        if (this.data.files.length === 0) {
            // Show loading skeleton while fetching
            if (!window.dashboardFilesLoaded) {
                return `
                    <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark">
                        <div class="px-8 py-4 border-b border-[var(--color-separator)] animate-pulse">
                            <div class="h-6 bg-[var(--color-separator)] dark:bg-[var(--color-tertiary-background)] rounded w-48 mb-2"></div>
                            <div class="h-4 bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)] rounded w-32"></div>
                        </div>
                        ${createTableLoadingSkeleton(5)}
                    </div>
                `;
            }

            // Show a neutral loading skeleton instead of the setup tutorial
            return `
                <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark">
                    <div class="px-8 py-6 border-b border-[var(--color-separator)]">
                        <div class="h-6 bg-[var(--color-separator)] dark:bg-[var(--color-tertiary-background)] rounded w-48 mb-2 animate-pulse"></div>
                        <div class="h-4 bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)] rounded w-32 animate-pulse"></div>
                    </div>
                    ${createTableLoadingSkeleton(6)}
                </div>
            `;
        }
        
        return `
            <div class="flex-1 overflow-y-auto bg-[var(--color-system-background)] dark:bg-surface-dark">
                <div class="px-8 py-4 border-b border-[var(--color-separator)]">
                    <h2 class="text-lg font-semibold text-[var(--color-text-primary)]">Recent Backup Files</h2>
                    <p class="text-sm text-[var(--color-text-secondary)] mt-1">${this.data.files.length} backup files found</p>
                </div>
                <table class="w-full text-left border-collapse">
                    <thead class="bg-[var(--color-secondary-background)] dark:bg-[var(--color-tertiary-background)] sticky top-0 z-0 shadow-sm">
                        <tr>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-separator)] w-1/3">Name</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-separator)]">Date Modified</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-separator)]">Size</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-separator)]">Type</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-separator)]">Snapshot</th>
                            <th class="px-6 py-2 text-xs font-semibold text-[var(--color-text-secondary)] border-b border-[var(--color-separator)]">Status</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-[var(--color-separator)] text-sm">
                        ${this.data.files.map(file => this.renderFileRow(file)).join('')}
                    </tbody>
                </table>
            </div>
        `;
    }

    // Render a single file row
    renderFileRow(file) {
        const statusClasses = {
            completed: 'bg-[var(--color-status-success-bg)] text-[var(--color-status-success)]',
            archived: 'bg-[var(--color-status-info-bg)] text-[var(--color-status-info)]',
            failed: 'bg-[var(--color-status-error-bg)] text-[var(--color-status-error)]',
            in_progress: 'bg-[var(--color-status-warning-bg)] text-[var(--color-status-warning)]',
            pending: 'bg-[var(--color-status-info-bg)] text-[var(--color-status-info)]'
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
            new: 'bg-[var(--color-accent-light)] text-[var(--color-accent)]',
            modified: 'bg-[var(--color-status-warning-bg)] text-[var(--color-status-warning)]'
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
            <tr class="hover:bg-[var(--color-accent-lighter)] group cursor-default transition-colors file-row-hover" 
                data-type="${file.type}" 
                data-name="${file.name}"
                oncontextmenu="window.showContextMenu(event, '${file.type}')">
                <td class="px-6 py-3 whitespace-nowrap">
                    <div class="flex items-center gap-3">
                        <span class="material-icons-round ${icon === 'folder_zip' || icon === 'folder' ? 'text-[var(--color-accent)]' : 'text-[var(--color-text-secondary)]'} text-xl">
                            ${icon}
                        </span>
                        <span class="font-medium text-[var(--color-text-primary)]">${file.name}</span>
                    </div>
                </td>
                <td class="px-6 py-3 text-[var(--color-text-secondary)] whitespace-nowrap">${this.formatDate(file.date)}</td>
                <td class="px-6 py-3 text-[var(--color-text-secondary)] whitespace-nowrap">${file.size}</td>
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
        const frequentFileCards = document.querySelectorAll('.frequent-file-card');
        frequentFileCards.forEach((card) => {
            card.addEventListener('click', () => {
                const filePath = card.getAttribute('data-file-path');
                if (filePath) {
                    console.log('Searching for frequently modified file:', filePath);
                    this.searchFile(filePath);
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
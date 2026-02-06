// src/js/pages/folders.js

import RestoreWindow from '../components/restore-window.js';
import { createTableLoadingSkeleton } from '../utils/loading-skeleton.js';

export default class FoldersPage {
    constructor() {
        this.name = 'folders';
        this.currentPath = [];
        this.allFiles = []; 
        this.rawSearchResults = null; 
        this.filteredFiles = []; // This is the single source of truth for the view
        this.viewMode = 'list';
        this.sortColumn = 'name';
        this.sortDirection = 'asc';
        this.searchQuery = '';
        this.isLoading = false;
        this.selectedFiles = new Set();
        this.backupBasePath = '';
        this.lastSelected = null;
        this.activeFilters = {
            showFolders: true,
            showFiles: true,
            sizeFilter: 'all',
            sortBy: 'name'
        };
        
        this.isBackupDeviceConfigured = false;
        this.maximizedPreview = null; // Track maximized preview state
        
        // Bind methods
        this.handleGlobalSearch = this.handleGlobalSearch.bind(this);
        this.handleGlobalSearchClear = this.handleGlobalSearchClear.bind(this);
        this.handleClearSearchClick = this.handleClearSearchClick.bind(this);
        this.handlePreviewMaximize = this.handlePreviewMaximize.bind(this);
        this.handlePreviewAction = this.handlePreviewAction.bind(this);

        // Initialize RestoreWindow component
        this.restoreWindow = new RestoreWindow();
    }

    async render() {
        return `
            <div class="flex flex-col h-full"> <!-- Added flex container -->
                <div class="px-8 py-6 bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark flex-shrink-0">
                    <div class="flex gap-6 items-center">
                        <div class="w-16 h-16 rounded-xl bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/40 dark:to-blue-800/20 flex items-center justify-center shadow-sm border border-blue-100 dark:border-blue-800/50 flex-shrink-0">
                            <span class="material-symbols-outlined text-4xl text-blue-500 dark:text-blue-400">folder_open</span>
                        </div>
                        <div class="flex-1">
                            <div class="flex justify-between items-center mb-1">
                                <div>
                                    <h1 class="text-2xl font-bold text-gray-900 dark:text-white leading-tight">Backup Files</h1>
                                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-0.5" id="folder-stats">
                                        Loading...
                                    </p>
                                    <div id="search-indicator" class="hidden mt-1">
                                        <div class="flex items-center gap-2">
                                            <span class="material-icons-round text-sm text-primary">search</span>
                                            <span class="text-xs text-primary font-medium" id="search-indicator-text"></span>
                                            <button class="text-xs text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 ml-2 px-2 py-0.5 rounded hover:bg-gray-100 dark:hover:bg-gray-700" id="clear-search-btn">
                                                Clear
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2">
                                    <button class="text-sm text-primary hover:text-blue-700 font-medium px-3 py-1.5 rounded-md hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors" id="manage-exclusions">
                                        Manage Exclusions
                                    </button>
                                </div>
                            </div>
                            <div class="flex gap-2 mt-2" id="folder-tags">
                                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                                    Backup
                                </span>
                                <span id="search-tag" class="hidden inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300">
                                    <span class="material-icons-round text-xs mr-1">search</span>
                                    Search
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="px-6 py-3 bg-gray-50/50 dark:bg-gray-800/30 border-b border-border-light dark:border-border-dark flex items-center justify-between flex-shrink-0">
                    <div class="flex items-center gap-2">
                        <button class="p-1.5 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 dark:text-gray-400 disabled:opacity-50 transition-colors" 
                                id="nav-back" 
                                ${this.currentPath.length === 0 || !this.isBackupDeviceConfigured ? 'disabled' : ''}>
                            <span class="material-icons-round text-lg">chevron_left</span>
                        </button>
                        <button class="p-1.5 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 dark:text-gray-400 disabled:opacity-50 transition-colors" id="nav-forward" disabled>
                            <span class="material-icons-round text-lg">chevron_right</span>
                        </button>
                        <div class="h-4 w-px bg-gray-300 dark:bg-gray-600 mx-1"></div>
                        <div class="flex items-center text-sm text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-border-light dark:border-border-dark rounded px-2 py-1.5 shadow-sm min-w-0" id="breadcrumbs-container">
                            <div class="flex items-center overflow-x-auto hide-scrollbar max-w-md" id="breadcrumbs">
                                ${this.renderBreadcrumbs()}
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center gap-3">
                        <div class="flex bg-gray-200 dark:bg-gray-700 rounded-lg p-0.5" id="view-toggle">
                            <button class="p-1.5 rounded-md flex items-center justify-center ${this.viewMode === 'list' ? 'bg-white dark:bg-gray-600 shadow-sm text-gray-800 dark:text-white' : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white transition-colors'} ${!this.isBackupDeviceConfigured ? 'opacity-50 cursor-not-allowed' : ''}" 
                                    data-view="list" 
                                    title="List view" 
                                    ${!this.isBackupDeviceConfigured ? 'disabled' : ''}>
                                <span class="material-icons-round text-lg">list</span>
                            </button>
                            <button class="p-1.5 rounded-md flex items-center justify-center ${this.viewMode === 'grid' ? 'bg-white dark:bg-gray-600 shadow-sm text-gray-800 dark:text-white' : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white transition-colors'} ${!this.isBackupDeviceConfigured ? 'opacity-50 cursor-not-allowed' : ''}" 
                                    data-view="grid" 
                                    title="Grid view" 
                                    ${!this.isBackupDeviceConfigured ? 'disabled' : ''}>
                                <span class="material-icons-round text-lg">grid_view</span>
                            </button>
                        </div>
                        
                        <div class="relative" id="filter-container">
                            <button class="flex items-center gap-2 px-3 py-1.5 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors text-sm font-medium text-gray-700 dark:text-gray-200 ${!this.isBackupDeviceConfigured ? 'opacity-50 cursor-not-allowed' : ''}" 
                                    id="filter-btn" 
                                    ${!this.isBackupDeviceConfigured ? 'disabled' : ''}>
                                <span class="material-icons-round text-base">filter_list</span>
                                Filter
                            </button>
                            
                            <div class="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50 hidden glass-light dark:glass-dark animate-fade-in-down" id="filter-dropdown">
                                <div class="p-3">
                                    <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-3 flex items-center gap-2">
                                        <span class="material-icons-round text-base">filter_alt</span>
                                        Filter Options
                                    </h3>
                                    
                                    <div class="space-y-3">
                                        <div>
                                            <label class="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2 block">File Type</label>
                                            <div class="space-y-2">
                                                <label class="flex items-center gap-2 cursor-pointer">
                                                    <input type="checkbox" class="rounded text-primary focus:ring-primary" data-filter="folder" ${this.activeFilters.showFolders ? 'checked' : ''}>
                                                    <span class="text-sm text-gray-700 dark:text-gray-300">Folders</span>
                                                </label>
                                                <label class="flex items-center gap-2 cursor-pointer">
                                                    <input type="checkbox" class="rounded text-primary focus:ring-primary" data-filter="file" ${this.activeFilters.showFiles ? 'checked' : ''}>
                                                    <span class="text-sm text-gray-700 dark:text-gray-300">Files</span>
                                                </label>
                                            </div>
                                        </div>
                                        
                                        <div class="pt-3 border-t border-gray-200 dark:border-gray-700">
                                            <label class="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2 block">File Size</label>
                                            <select class="w-full text-sm border border-gray-200 dark:border-gray-700 rounded px-3 py-2 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-primary focus:border-primary transition-all dark:text-white" id="size-filter">
                                                <option value="all" ${this.activeFilters.sizeFilter === 'all' ? 'selected' : ''}>All Sizes</option>
                                                <option value="small" ${this.activeFilters.sizeFilter === 'small' ? 'selected' : ''}>Small (&lt; 1 MB)</option>
                                                <option value="medium" ${this.activeFilters.sizeFilter === 'medium' ? 'selected' : ''}>Medium (1-100 MB)</option>
                                                <option value="large" ${this.activeFilters.sizeFilter === 'large' ? 'selected' : ''}>Large (&gt; 100 MB)</option>
                                                <option value="huge" ${this.activeFilters.sizeFilter === 'huge' ? 'selected' : ''}>Huge (&gt; 1 GB)</option>
                                            </select>
                                        </div>
                                        
                                        <div class="pt-3 border-t border-gray-200 dark:border-gray-700">
                                            <label class="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2 block">Sort By</label>
                                            <select class="w-full text-sm border border-gray-200 dark:border-gray-700 rounded px-3 py-2 bg-white dark:bg-gray-700 focus:ring-2 focus:ring-primary focus:border-primary transition-all dark:text-white" id="sort-filter">
                                                <option value="name" ${this.activeFilters.sortBy === 'name' ? 'selected' : ''}>Name (A-Z)</option>
                                                <option value="name-desc" ${this.activeFilters.sortBy === 'name-desc' ? 'selected' : ''}>Name (Z-A)</option>
                                                <option value="date" ${this.activeFilters.sortBy === 'date' ? 'selected' : ''}>Date (Newest)</option>
                                                <option value="date-desc" ${this.activeFilters.sortBy === 'date-desc' ? 'selected' : ''}>Date (Oldest)</option>
                                                <option value="size" ${this.activeFilters.sortBy === 'size' ? 'selected' : ''}>Size (Smallest)</option>
                                                <option value="size-desc" ${this.activeFilters.sortBy === 'size-desc' ? 'selected' : ''}>Size (Largest)</option>
                                                <option value="type" ${this.activeFilters.sortBy === 'type' ? 'selected' : ''}>Type</option>
                                            </select>
                                        </div>
                                    </div>
                                    
                                    <div class="flex gap-2 mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
                                        <button class="flex-1 px-3 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-md transition-colors" id="reset-filter">
                                            Reset
                                        </button>
                                        <button class="flex-1 px-3 py-2 bg-primary hover:bg-blue-600 text-white text-sm font-medium rounded-md transition-colors" id="apply-filter">
                                            Apply
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Changed this to flex-1 to take remaining space -->
                <div class="flex-1 overflow-hidden relative">
                    <div class="h-full flex"> <!-- Added h-full flex -->
                        <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark" id="content-container">
                            ${this.isLoading ? this.renderLoading() : this.renderContent()}
                        </div>
                        
                        <div class="w-80 bg-gray-50 dark:bg-gray-800 border-l border-border-light dark:border-border-dark flex flex-col hidden transition-all duration-300 ease-in-out" id="preview-panel">
                            <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
                                <h3 class="font-semibold text-gray-900 dark:text-white">Preview</h3>
                                <button id="close-preview" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
                                    <span class="material-icons-round text-sm">close</span>
                                </button>
                            </div>
                            <div id="preview-content" class="flex-1 overflow-y-auto p-4 flex flex-col">
                                <p class="text-gray-500 text-center mt-10 text-sm">Select a file to preview</p>
                            </div>
                            <!-- Action buttons for selected file -->
                            <div id="preview-actions" class="p-4 border-t border-gray-200 dark:border-gray-700 hidden">
                                <div class="grid grid-cols-2 gap-2">
                                    <button class="preview-action-btn" data-action="open" data-file="" data-type="">
                                        <span class="material-icons-round text-sm mr-2">visibility</span>
                                        Open
                                    </button>
                                    <button class="preview-action-btn" data-action="open-location" data-file="" data-type="">
                                        <span class="material-icons-round text-sm mr-2">folder_open</span>
                                        Location
                                    </button>
                                    <button class="preview-action-btn" data-action="restore" data-file="" data-type="">
                                        <span class="material-icons-round text-sm mr-2">restore</span>
                                        Restore
                                    </button>
                                    <button class="preview-action-btn" data-action="download" data-file="" data-type="">
                                        <span class="material-icons-round text-sm mr-2">download</span>
                                        Download
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- This container will now stay at the bottom -->
                <div class="px-6 py-3 bg-gray-50 dark:bg-gray-800 border-t border-border-light dark:border-border-dark text-xs text-text-secondary-light dark:text-text-secondary-dark flex justify-between items-center flex-shrink-0" id="file-summary-container">
                    <span id="file-summary">${this.isBackupDeviceConfigured ? 'Loading...' : 'No backup device configured'}</span>
                    <div class="flex gap-4">
                        <span class="hover:text-gray-800 dark:hover:text-gray-200 cursor-pointer ${this.selectedFiles.size === 0 || !this.isBackupDeviceConfigured ? 'opacity-50 cursor-not-allowed' : ''}" id="restore-all">Restore Selected</span>
                        <span class="hover:text-gray-800 dark:hover:text-gray-200 cursor-pointer ${this.selectedFiles.size === 0 || !this.isBackupDeviceConfigured ? 'opacity-50 cursor-not-allowed' : ''}" id="download-selected">Download Selected</span>
                    </div>
                </div>
            </div> <!-- Closing flex container -->
        `;
    }

    renderBreadcrumbs() {
        const breadcrumbs = ['Backup'];
        if (this.currentPath.length > 0) {
            breadcrumbs.push(...this.currentPath);
        }
        
        return breadcrumbs.map((segment, index) => {
            const isLast = index === breadcrumbs.length - 1;
            const displaySegment = segment.length > 15 ? segment.substring(0, 15) + '...' : segment;
            
            return `
                ${index > 0 ? '<span class="material-icons-round text-base text-gray-400 mx-1 flex-shrink-0">chevron_right</span>' : ''}
                ${isLast ? 
                    `<span class="font-medium text-gray-900 dark:text-white flex-shrink-0" title="${segment}">${displaySegment}</span>` :
                    `<button class="flex-shrink-0 text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors truncate max-w-32" data-breadcrumb="${segment}" data-index="${index}" title="${segment}">${displaySegment}</button>`
                }
            `;
        }).join('');
    }

    updateBreadcrumbs() {
        const breadcrumbsContainer = document.getElementById('breadcrumbs');
        if (breadcrumbsContainer) {
            breadcrumbsContainer.innerHTML = this.renderBreadcrumbs();
            
            breadcrumbsContainer.querySelectorAll('[data-breadcrumb]').forEach(button => {
                button.addEventListener('click', (e) => {
                    const index = parseInt(e.target.getAttribute('data-index'));
                    this.navigateToBreadcrumb(index);
                });
            });
        }
        
        const navBack = document.getElementById('nav-back');
        if (navBack) {
            navBack.disabled = this.currentPath.length === 0 || !this.isBackupDeviceConfigured;
            navBack.classList.toggle('opacity-50', this.currentPath.length === 0 || !this.isBackupDeviceConfigured);
        }
    }

    updateViewToggle() {
        const viewToggle = document.getElementById('view-toggle');
        if (viewToggle) {
            const listButton = viewToggle.querySelector('[data-view="list"]');
            const gridButton = viewToggle.querySelector('[data-view="grid"]');
            
            if (listButton) {
                listButton.className = `p-1.5 rounded-md flex items-center justify-center ${this.viewMode === 'list' ? 'bg-white dark:bg-gray-600 shadow-sm text-gray-800 dark:text-white' : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white transition-colors'} ${!this.isBackupDeviceConfigured ? 'opacity-50 cursor-not-allowed' : ''}`;
                listButton.disabled = !this.isBackupDeviceConfigured;
            }
            
            if (gridButton) {
                gridButton.className = `p-1.5 rounded-md flex items-center justify-center ${this.viewMode === 'grid' ? 'bg-white dark:bg-gray-600 shadow-sm text-gray-800 dark:text-white' : 'text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-white transition-colors'} ${!this.isBackupDeviceConfigured ? 'opacity-50 cursor-not-allowed' : ''}`;
                gridButton.disabled = !this.isBackupDeviceConfigured;
            }
        }
    }

    renderLoading() {
        return `
            <div class="flex flex-col items-center justify-center h-full">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
                <p class="text-gray-600 dark:text-gray-400">Loading folder contents...</p>
            </div>
        `;
    }

    renderContent() {
        const noDeviceConfigured = this.allFiles.length === 0 && !this.isLoading && !this.searchQuery;
        
        if (noDeviceConfigured) {
            return this.renderNoDeviceState();
        }
        
        // FIXED: Always use filteredFiles for display. 
        // Previously, the app ignored filters if searchQuery was empty.
        // filteredFiles is initialized as a copy of allFiles and updated by applyCurrentFilters.
        const displayFiles = this.filteredFiles;
        
        if (displayFiles.length === 0) {
            return `
                <div class="flex flex-col items-center justify-center h-full">
                    <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center mb-6 shadow-soft border border-gray-200 dark:border-gray-600">
                        <span class="material-icons-round text-5xl text-gray-400 dark:text-gray-500">${this.searchQuery ? 'search_off' : 'folder_open'}</span>
                    </div>
                    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
                        ${this.searchQuery ? 'No results found' : 'No files found'}
                    </h3>
                    <p class="text-gray-600 dark:text-gray-400 max-w-md text-center mb-4">
                        ${this.searchQuery ? 
                            `No files found matching "${this.searchQuery}" with current filters.` :
                            'No files match the current filters.'
                        }
                    </p>
                    ${this.searchQuery || this.getActiveFilterCount() > 0 ? `
                        <button onclick="window.foldersPage.resetFilters(); window.foldersPage.clearHeaderSearch()" class="mt-2 px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors">
                            Clear Filters & Search
                        </button>
                    ` : ''}
                </div>
            `;
        }

        if (this.viewMode === 'grid') {
            return this.renderGridView(displayFiles);
        }

        return this.renderListView(displayFiles);
    }

    renderNoDeviceState() {
        return `
            <div class="flex flex-col items-center justify-center h-full p-8">
                <div class="w-24 h-24 rounded-2xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center mb-6 shadow-soft border border-gray-200 dark:border-gray-600">
                    <span class="material-symbols-outlined text-5xl text-gray-400 dark:text-gray-500">hard_drive</span>
                </div>
                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
                    No Backup Device Configured
                </h3>
                <p class="text-gray-600 dark:text-gray-400 max-w-md text-center mb-4">
                    You need to set up a backup device before you can view and manage backup files.
                </p>
            </div>
        `;
    }

    renderListView(filesToDisplay) {
        // Use passed files to ensure filters apply
        const files = filesToDisplay || this.filteredFiles;
        const sortIndicator = this.sortDirection === 'asc' ? '↑' : '↓';
        const isEnabled = this.isBackupDeviceConfigured;
        
        return `
            <div class="w-full overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-gray-50 dark:bg-gray-800 sticky top-0 z-10">
                        <tr>
                            <th class="px-6 py-3 pl-8 text-xs font-semibold ${isEnabled ? 'text-gray-500 dark:text-gray-400 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors' : 'text-gray-400 dark:text-gray-500 cursor-default'} ${this.sortColumn === 'name' ? 'text-primary' : ''}" id="sort-name">
                                <div class="flex items-center gap-1">
                                    <span>Name</span>
                                    ${this.sortColumn === 'name' ? `<span class="text-xs">${sortIndicator}</span>` : ''}
                                </div>
                            </th>
                            <th class="px-6 py-3 text-xs font-semibold ${isEnabled ? 'text-gray-500 dark:text-gray-400 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors' : 'text-gray-400 dark:text-gray-500 cursor-default'} ${this.sortColumn === 'path' ? 'text-primary' : ''}" id="sort-path">
                                <div class="flex items-center gap-1">
                                    <span>Location</span>
                                    ${this.sortColumn === 'path' ? `<span class="text-xs">${sortIndicator}</span>` : ''}
                                </div>
                            </th>
                            <th class="px-6 py-3 text-xs font-semibold ${isEnabled ? 'text-gray-500 dark:text-gray-400 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors' : 'text-gray-400 dark:text-gray-500 cursor-default'} ${this.sortColumn === 'type' ? 'text-primary' : ''}" id="sort-type">
                                <div class="flex items-center gap-1">
                                    <span>Type</span>
                                    ${this.sortColumn === 'type' ? `<span class="text-xs">${sortIndicator}</span>` : ''}
                                </div>
                            </th>
                            <th class="px-6 py-3 text-xs font-semibold ${isEnabled ? 'text-gray-500 dark:text-gray-400 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700/50 transition-colors' : 'text-gray-400 dark:text-gray-500 cursor-default'} ${this.sortColumn === 'size' ? 'text-primary' : ''}" id="sort-size">
                                <div class="flex items-center gap-1">
                                    <span>Size</span>
                                    ${this.sortColumn === 'size' ? `<span class="text-xs">${sortIndicator}</span>` : ''}
                                </div>
                            </th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 dark:divide-gray-800 text-sm" id="files-list">
                        ${this.renderFilesList(files)}
                    </tbody>
                </table>
            </div>
        `;
    }

    renderGridView(filesToDisplay) {
        const files = filesToDisplay || this.filteredFiles;
        
        return `
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 p-6" id="files-grid">
                ${files.map(file => {
                    const versionCount = file.versionCount || 0;
                    const hasVersions = versionCount > 0;
                    const ext = file.name.split('.').pop().toLowerCase();
                    const isImage = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext);
                    const previewUrl = isImage ? `/api/stream/file?path=${encodeURIComponent(file.path)}` : null;

                    return `
                        <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 border border-gray-200 dark:border-gray-700 hover:shadow-md transition-all cursor-pointer group relative ${
                            this.selectedFiles.has(file.path) ? 'selected-highlight ring-1 ring-primary' : ''
                        }" data-file="${file.path}" data-type="${file.type}">
                            ${hasVersions ? `
                            <div class="absolute -top-2 -right-2 w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center shadow-lg z-10">
                                <span class="text-xs font-bold text-white">${versionCount}</span>
                            </div>
                            ` : ''}
                            <div class="flex flex-col items-center text-center mb-3">
                                ${previewUrl ? `
                                <div class="w-16 h-16 rounded-lg flex items-center justify-center mb-2 relative overflow-hidden">
                                    <img src="${previewUrl}" class="w-full h-full object-cover" alt="${file.name}" onerror="this.onerror=null; this.parentElement.innerHTML = '<span class=\\'material-icons-round text-3xl text-gray-400\\'>broken_image</span>';">
                                </div>
                                ` : `
                                <div class="w-16 h-16 rounded-lg bg-gradient-to-br ${
                                    file.type === 'folder' ? 
                                        'from-blue-50 to-blue-100 dark:from-blue-900/30 dark:to-blue-800/20' :
                                        'from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700'
                                } flex items-center justify-center mb-2 relative">
                                    <span class="material-icons-round text-3xl ${
                                        file.type === 'folder' ? 
                                            'text-blue-500 dark:text-blue-400' :
                                            this.getFileIconColor(file.name)
                                    }">
                                        ${file.type === 'folder' ? 'folder' : this.getFileIcon(file.name)}
                                    </span>
                                </div>
                                `}
                                <div class="w-full">
                                    <div class="text-sm font-medium text-gray-900 dark:text-white truncate mb-1" title="${file.name}">
                                        ${this.highlightSearchText(file.name)}
                                    </div>
                                    <div class="text-xs text-gray-500 dark:text-gray-400">
                                        ${file.type === 'folder' ? 'Folder' : file.size}
                                    </div>
                                </div>
                            </div>
                            <div class="flex justify-between items-center text-xs text-gray-500 dark:text-gray-400">
                                <span class="truncate max-w-[100px]" title="${file.path}">${this.formatPathLocation(file.path)}</span>
                                <!-- Removed the context menu button -->
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }

    renderFilesList(files) {
        return files.map(file => {
            const isSelected = this.selectedFiles.has(file.path);
            const versionCount = file.versionCount || 0;
            const hasVersions = versionCount > 0;
            
            return `
                <tr class="file-row-hover group cursor-default transition-all ${
                    isSelected ? 'selected-highlight' : ''
                }" data-file="${file.path}" data-type="${file.type}">
                    <td class="px-6 py-3 pl-8 whitespace-nowrap">
                        <div class="flex items-center gap-3">
                            <div class="relative flex items-center">
                                <input type="checkbox" class="absolute opacity-0 w-0 h-0" ${
                                    isSelected ? 'checked' : ''
                                }>
                                <span class="material-icons-round ${
                                    file.type === 'folder' ? 
                                        'text-blue-500 dark:text-blue-400' :
                                        this.getFileIconColor(file.name)
                                } text-xl">
                                    ${file.type === 'folder' ? 'folder' : this.getFileIcon(file.name)}
                                </span>
                                ${hasVersions ? `
                                <div class="absolute -top-1 -right-1 w-5 h-5 bg-blue-500 rounded-full flex items-center justify-center">
                                    <span class="text-[10px] font-bold text-white">${versionCount}</span>
                                </div>
                                ` : ''}
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="font-medium text-gray-900 dark:text-gray-200 truncate max-w-xs" title="${file.name}">
                                    ${this.highlightSearchText(file.name)}
                                </span>
                                ${hasVersions ? `
                                <div class="flex items-center gap-1" title="${versionCount} backup versions available">
                                    <span class="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse"></span>
                                    <span class="text-xs text-blue-600 dark:text-blue-400 font-medium">${versionCount}</span>
                                </div>
                                ` : ''}
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-3 text-gray-500 dark:text-gray-400 whitespace-nowrap text-xs" title="${file.path}">
                        ${this.formatPathLocation(file.path)}
                    </td>
                    <td class="px-6 py-3 text-gray-500 dark:text-gray-400 whitespace-nowrap">${file.type === 'folder' ? 'Folder' : this.getFileType(file.name)}</td>
                    <td class="px-6 py-3 text-gray-500 dark:text-gray-400 whitespace-nowrap">${file.type === 'folder' ? '--' : file.size}</td>
                </tr>
            `;
        }).join('');
    }

    formatPathLocation(path) {
        if (!path) return '';
        const parts = path.split('/').filter(p => p.length > 0);
        if (parts.length <= 3) return path;
        const lastThree = parts.slice(-3);
        return '.../' + lastThree.join('/');
    }

    highlightSearchText(text) {
        if (!this.searchQuery || !text) return text;
        const query = this.searchQuery.toLowerCase();
        const lowerText = text.toLowerCase();
        const index = lowerText.indexOf(query);
        if (index === -1) return text;
        const before = text.substring(0, index);
        const match = text.substring(index, index + query.length);
        const after = text.substring(index + query.length);
        return `${before}<span class="bg-yellow-200 dark:bg-yellow-700 font-semibold">${match}</span>${after}`;
    }

    getFileIcon(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        if (['pdf'].includes(ext)) return 'picture_as_pdf';
        if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext)) return 'image';
        if (['doc', 'docx', 'txt', 'rtf', 'md'].includes(ext)) return 'article';
        if (['xls', 'xlsx', 'csv'].includes(ext)) return 'table_view';
        if (['mp3', 'wav', 'ogg', 'flac', 'm4a'].includes(ext)) return 'music_note';
        if (['mp4', 'avi', 'mov', 'mkv', 'webm'].includes(ext)) return 'movie';
        if (['zip', 'rar', 'tar', 'gz', '7z'].includes(ext)) return 'folder_zip';
        if (['py', 'js', 'java', 'cpp', 'c', 'html', 'css', 'json', 'xml'].includes(ext)) return 'code';
        if (['blend', 'fbx', 'obj', 'glb', 'gltf', 'stl'].includes(ext)) return 'view_in_ar';
        return 'description';
    }

    getFileIconColor(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        if (['pdf'].includes(ext)) return 'text-red-500 dark:text-red-400';
        if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext)) return 'text-green-500 dark:text-green-400';
        if (['doc', 'docx', 'txt', 'rtf', 'md'].includes(ext)) return 'text-blue-500 dark:text-blue-400';
        if (['xls', 'xlsx', 'csv'].includes(ext)) return 'text-green-600 dark:text-green-500';
        if (['zip', 'rar', 'tar', 'gz', '7z'].includes(ext)) return 'text-orange-500 dark:text-orange-400';
        if (['py', 'js', 'java', 'cpp', 'c', 'html', 'css', 'json', 'xml'].includes(ext)) return 'text-purple-500 dark:text-purple-400';
        if (['blend', 'fbx', 'obj', 'glb', 'gltf', 'stl'].includes(ext)) return 'text-orange-600 dark:text-orange-400';
        return 'text-gray-500 dark:text-gray-400';
    }

    getFileType(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const types = {
            pdf: 'PDF Document',
            jpg: 'JPEG Image', jpeg: 'JPEG Image',
            png: 'PNG Image', gif: 'GIF Image', bmp: 'Bitmap Image',
            svg: 'SVG Image', webp: 'WebP Image',
            doc: 'Word Document', docx: 'Word Document',
            txt: 'Text Document', rtf: 'Rich Text', md: 'Markdown',
            xls: 'Excel Spreadsheet', xlsx: 'Excel Spreadsheet', csv: 'CSV File',
            mp3: 'Audio File', wav: 'Audio File', ogg: 'Audio File', flac: 'FLAC Audio',
            mp4: 'Video File', avi: 'Video File', mov: 'Video File', mkv: 'MKV Video',
            zip: 'ZIP Archive', rar: 'RAR Archive', tar: 'TAR Archive', gz: 'GZIP Archive',
            py: 'Python Script', js: 'JavaScript', html: 'HTML File',
            css: 'Stylesheet', json: 'JSON File', xml: 'XML File',
            java: 'Java File', cpp: 'C++ File', c: 'C File',
            blend: 'Blender 3D File', fbx: 'FBX 3D Model', obj: 'OBJ 3D Model',
            glb: 'GLB 3D Model', gltf: 'GLTF 3D Model', stl: 'STL 3D Model'
        };
        return types[ext] || 'File';
    }

    formatDate(timestamp) {
        if (!timestamp) return '--';
        const date = new Date(timestamp * 1000);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 86400000) {
            return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        } else if (diff < 604800000) {
            return date.toLocaleDateString([], { weekday: 'short' });
        } else {
            return date.toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' });
        }
    }

    async afterRender() {
        console.log('Folders page initialized');
        window.foldersPage = this;
        window.currentPage = 'folders';
        
        if (window.appHeader) window.appHeader.setCurrentPage('folders');
        this.setupGlobalEventListeners();
        
        if (window.pendingSearchQuery) {
            this.handleHeaderSearch(window.pendingSearchQuery);
            delete window.pendingSearchQuery;
        }
        
        const hasBackupDevice = await this.checkBackupDeviceConfigured();
        this.isBackupDeviceConfigured = hasBackupDevice;
        
        if (!hasBackupDevice) {
            this.showNoDeviceState();
            this.updateUIControlsState();
            this.setupEventListeners();
            return;
        }
        
        await this.loadFolderContents();
        this.updateUIControlsState();
        this.setupEventListeners();
        
        document.addEventListener('device-configured', () => {
            this.refreshDeviceStatus();
        });
    }
    
    setupGlobalEventListeners() {
        document.addEventListener('global-search', (event) => this.handleGlobalSearch(event));
        document.addEventListener('global-search-clear', (event) => this.handleGlobalSearchClear(event));
    }

    handleGlobalSearch(event) {
        const query = event.detail.query;
        if (!query || query.trim() === '') {
            this.clearHeaderSearch();
            return;
        }
        this.handleHeaderSearch(query.trim());
    }
    
    handleGlobalSearchClear(event) {
        this.clearHeaderSearch();
    }
    
    handleClearSearchClick() {
        this.clearHeaderSearch();
    }
    
    async handleHeaderSearch(query) {
        if (!this.isBackupDeviceConfigured) {
            showInfo('Please configure a backup device first', 'warning');
            return;
        }

        this.searchQuery = query;
        if (window.appHeader) window.appHeader.updateSearchValue(this.searchQuery);
        this.showSearchIndicator();
        this.isLoading = true;
        this.updateContentOnly();

        try {
            const results = await this.performBackendSearch(this.searchQuery);
            if (results.success) {
                this.rawSearchResults = results.results.map(item => ({
                    name: item.name,
                    path: item.path,
                    type: item.type,
                    date: item.date,
                    // Parse integer size for reliable sorting and filtering
                    // rawSize: item.size ? parseInt(item.size, 10) : 0,
                    rawSize: item.rawSize,
                    size: item.type === 'folder' ? '--' : this.formatFileSize(item.size)
                }));
                this.applyCurrentFilters();
                this.applySortingFromFilters();

                // if (this.filteredFiles.length === 0) {
                //     showInfo(`No results found for "${query}"`, 'info');
                // } else {
                //     showInfo(`Found ${this.filteredFiles.length} results`, 'success');
                // }
            } else {
                showInfo('Search failed. Using local search instead.', 'warning');
                this.rawSearchResults = null;
                this.applyCurrentFilters(); 
            }
        } catch (error) {
            console.error('Backend search error:', error);
            showInfo('Search error. Using local search instead.', 'warning');
            this.rawSearchResults = null;
            this.applyCurrentFilters();
        } finally {
            this.isLoading = false;
            this.updateContentOnly();
            this.updateFileSummary();
        }
    }

    async performBackendSearch(query) {
        try {
            const url = `/api/search/files?query=${encodeURIComponent(query)}`;
            const response = await fetch(url);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Search request failed');
            return {
                success: true,
                results: data.results || [],
                total: data.total || 0,
                message: data.message || ''
            };
        } catch (error) {
            return { success: false, error: error.message, results: [] };
        }
    }
    
    showSearchIndicator() {
        const searchIndicator = document.getElementById('search-indicator');
        const searchIndicatorText = document.getElementById('search-indicator-text');
        const searchTag = document.getElementById('search-tag');
        
        if (searchIndicator) {
            searchIndicator.classList.remove('hidden');
            if (searchIndicatorText) searchIndicatorText.textContent = `Searching: "${this.searchQuery}"`;
        }
        
        if (searchTag) searchTag.classList.remove('hidden');
        
        const clearBtn = document.getElementById('clear-search-btn');
        if (clearBtn) {
            clearBtn.replaceWith(clearBtn.cloneNode(true));
            document.getElementById('clear-search-btn').addEventListener('click', this.handleClearSearchClick);
        }
    }
    
    clearHeaderSearch() {
        this.searchQuery = '';
        this.rawSearchResults = null;
        this.filteredFiles = [];
        if (window.appHeader) window.appHeader.clearSearch();

        const searchIndicator = document.getElementById('search-indicator');
        const searchTag = document.getElementById('search-tag');
        if (searchIndicator) searchIndicator.classList.add('hidden');
        if (searchTag) searchTag.classList.add('hidden');

        this.loadFolderContents();
    }

    async getBackupInfo() {
        try {
            const response = await fetch('/api/backup/path');
            const data = await response.json();
            if (data.success && data.device_configured) {
                this.backupBasePath = data.backup_path;
                return true;
            }
            return false;
        } catch (error) {
            return false;
        }
    }
    
    async checkBackupDeviceConfigured() {
        try {
            const response = await fetch('/api/locations/current-backup');
            const data = await response.json();
            return (data.success && data.has_backup);
        } catch (error) {
            return false;
        }
    }
    
    setupEventListeners() {
        setTimeout(() => {
            const navBack = document.getElementById('nav-back');
            const navForward = document.getElementById('nav-forward');
            
            if (navBack) navBack.addEventListener('click', () => this.navigateBack());
            if (navForward) navForward.addEventListener('click', () => this.navigateForward());
            
            const viewToggle = document.getElementById('view-toggle');
            if (viewToggle) {
                viewToggle.querySelectorAll('button').forEach(button => {
                    button.addEventListener('click', (e) => {
                        if (!this.isBackupDeviceConfigured) {
                            showInfo('Please configure a backup device first', 'warning');
                            return;
                        }
                        const view = e.currentTarget.getAttribute('data-view');
                        this.toggleView(view);
                    });
                });
            }
            
            const filterBtn = document.getElementById('filter-btn');
            const filterDropdown = document.getElementById('filter-dropdown');

            if (filterBtn) {
                console.log('Setting up filter button and dropdown');
                
                // Toggle dropdown function
                const toggleDropdown = (e) => {
                    if (e) {
                        e.preventDefault();
                        e.stopPropagation();
                        e.stopImmediatePropagation();
                    }
                    
                    if (!this.isBackupDeviceConfigured) {
                        showInfo('Please configure a backup device first', 'warning');
                        return;
                    }
                    
                    // Make sure dropdown exists
                    if (!filterDropdown) {
                        console.error('Filter dropdown not found in DOM');
                        return;
                    }
                    
                    // Toggle visibility
                    const isHidden = filterDropdown.classList.contains('hidden');
                    console.log('Toggling dropdown, currently hidden:', isHidden);
                    
                    if (isHidden) {
                        filterDropdown.classList.remove('hidden');
                        // Bring to front
                        filterDropdown.style.zIndex = '9999';
                    } else {
                        filterDropdown.classList.add('hidden');
                    }
                };
                
                // Close dropdown function
                const closeDropdown = () => {
                    if (filterDropdown && !filterDropdown.classList.contains('hidden')) {
                        filterDropdown.classList.add('hidden');
                    }
                };
                
                // Handle outside clicks
                const handleOutsideClick = (e) => {
                    if (!filterDropdown || filterDropdown.classList.contains('hidden')) return;
                    
                    // Check if click is outside both button and dropdown
                    const isClickInside = filterDropdown.contains(e.target) || filterBtn.contains(e.target);
                    
                    if (!isClickInside) {
                        console.log('Click outside - closing dropdown');
                        closeDropdown();
                    }
                };
                
                // Attach button click
                filterBtn.addEventListener('click', toggleDropdown);
                
                // Attach document click for outside clicks
                document.addEventListener('click', handleOutsideClick);
                
                // Stop propagation inside dropdown
                if (filterDropdown) {
                    filterDropdown.addEventListener('click', (e) => {
                        e.stopPropagation();
                    });
                    
                    // Apply button
                    const applyFilter = document.getElementById('apply-filter');
                    if (applyFilter) {
                        applyFilter.addEventListener('click', (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log('Apply filter clicked');
                            this.applyFilters();
                            closeDropdown();
                        });
                    }
                    
                    // Reset button
                    const resetFilter = document.getElementById('reset-filter');
                    if (resetFilter) {
                        resetFilter.addEventListener('click', (e) => {
                            e.preventDefault();
                            e.stopPropagation();
                            console.log('Reset filter clicked');
                            this.resetFilters();
                            closeDropdown();
                        });
                    }
                    
                    // Handle escape key
                    document.addEventListener('keydown', (e) => {
                        if (e.key === 'Escape' && filterDropdown && !filterDropdown.classList.contains('hidden')) {
                            closeDropdown();
                        }
                    });
                }
            }

            // Preview Close button
            const closePreviewBtn = document.getElementById('close-preview');
            if (closePreviewBtn) {
                closePreviewBtn.addEventListener('click', () => {
                    const previewPanel = document.getElementById('preview-panel');
                    if (previewPanel) previewPanel.classList.add('hidden');
                });
            }
            
            this.setupFileSelection();
            
            const manageExclusions = document.getElementById('manage-exclusions');
            const restoreAll = document.getElementById('restore-all');
            const downloadSelected = document.getElementById('download-selected');
            
            if (manageExclusions) manageExclusions.addEventListener('click', () => this.manageExclusions());
            
            if (restoreAll) {
                restoreAll.addEventListener('click', () => {
                    if (!this.isBackupDeviceConfigured) {
                        showInfo('Please configure a backup device first', 'warning');
                        return;
                    }
                    this.restoreSelected();
                });
            }
            
            if (downloadSelected) {
                downloadSelected.addEventListener('click', () => {
                    if (!this.isBackupDeviceConfigured) {
                        showInfo('Please configure a backup device first', 'warning');
                        return;
                    }
                    this.downloadSelected();
                });
            }

            // Initial bind of sort listeners
            this.attachDynamicListeners();

        }, 100);
    }

    // Separated dynamic listeners (sorting) to re-attach them after table re-render
    attachDynamicListeners() {
        const sortName = document.getElementById('sort-name');
        const sortPath = document.getElementById('sort-path');
        const sortType = document.getElementById('sort-type');
        const sortSize = document.getElementById('sort-size');
        
        const attach = (element, column) => {
            if (element) {
                // Remove existing listener by cloning (simplest way to wipe anon listeners)
                const newElement = element.cloneNode(true);
                element.parentNode.replaceChild(newElement, element);
                
                newElement.addEventListener('click', () => {
                    if (!this.isBackupDeviceConfigured) {
                        showInfo('Please configure a backup device first', 'warning');
                        return;
                    }
                    this.sortFiles(column);
                });
            }
        };

        attach(sortName, 'name');
        attach(sortPath, 'path');
        attach(sortType, 'type');
        attach(sortSize, 'size');
    }

    updateUIControlsState() {
        const viewToggle = document.getElementById('view-toggle');
        if (viewToggle) {
            const listButton = viewToggle.querySelector('[data-view="list"]');
            const gridButton = viewToggle.querySelector('[data-view="grid"]');
            
            if (listButton) {
                listButton.disabled = !this.isBackupDeviceConfigured;
                listButton.classList.toggle('opacity-50', !this.isBackupDeviceConfigured);
                listButton.classList.toggle('cursor-not-allowed', !this.isBackupDeviceConfigured);
            }
            
            if (gridButton) {
                gridButton.disabled = !this.isBackupDeviceConfigured;
                gridButton.classList.toggle('opacity-50', !this.isBackupDeviceConfigured);
                gridButton.classList.toggle('cursor-not-allowed', !this.isBackupDeviceConfigured);
            }
        }
        
        const filterBtn = document.getElementById('filter-btn');
        if (filterBtn) {
            filterBtn.disabled = !this.isBackupDeviceConfigured;
            filterBtn.classList.toggle('opacity-50', !this.isBackupDeviceConfigured);
            filterBtn.classList.toggle('cursor-not-allowed', !this.isBackupDeviceConfigured);
        }
        
        const navBack = document.getElementById('nav-back');
        if (navBack) {
            navBack.disabled = this.currentPath.length === 0 || !this.isBackupDeviceConfigured;
            navBack.classList.toggle('opacity-50', this.currentPath.length === 0 || !this.isBackupDeviceConfigured);
        }
        
        const restoreBtn = document.getElementById('restore-all');
        const downloadBtn = document.getElementById('download-selected');
        
        if (restoreBtn && downloadBtn) {
            const isDisabled = this.selectedFiles.size === 0 || !this.isBackupDeviceConfigured;
            restoreBtn.classList.toggle('opacity-50', isDisabled);
            restoreBtn.classList.toggle('cursor-not-allowed', isDisabled);
            downloadBtn.classList.toggle('opacity-50', isDisabled);
            downloadBtn.classList.toggle('cursor-not-allowed', isDisabled);
        }
        
        const filterDropdown = document.getElementById('filter-dropdown');
        if (filterDropdown) {
            if (!this.isBackupDeviceConfigured) {
                filterDropdown.classList.add('hidden');
            }
            // Ensure dropdown has proper styling
            filterDropdown.classList.add('z-50');
        }
        
        this.updateSortingHeadersState();
    }
    
    updateSortingHeadersState() {
        const sortName = document.getElementById('sort-name');
        const sortPath = document.getElementById('sort-path');
        const sortType = document.getElementById('sort-type');
        const sortSize = document.getElementById('sort-size');
        
        [sortName, sortPath, sortType, sortSize].forEach(header => {
            if (header) {
                if (this.isBackupDeviceConfigured) {
                    header.classList.remove('text-gray-400', 'dark:text-gray-500', 'cursor-default');
                    header.classList.add('text-gray-500', 'dark:text-gray-400', 'cursor-pointer', 'hover:bg-gray-100', 'dark:hover:bg-gray-700/50');
                } else {
                    header.classList.remove('text-gray-500', 'dark:text-gray-400', 'cursor-pointer', 'hover:bg-gray-100', 'dark:hover:bg-gray-700/50');
                    header.classList.add('text-gray-400', 'dark:text-gray-500', 'cursor-default');
                }
            }
        });
    }
    
    setupFileSelection() {
        const contentContainer = document.getElementById('content-container');
        if (!contentContainer) return;
        
        contentContainer.addEventListener('click', (e) => {
            if (!this.isBackupDeviceConfigured) {
                if (e.target.closest('button') && e.target.closest('button').textContent.includes('Configure Backup Device')) {
                    return; 
                }
                e.preventDefault();
                showInfo('Please configure a backup device first', 'warning');
                return;
            }
            
            const row = e.target.closest('[data-file]');
            if (!row) {
                if (!e.target.closest('thead')) { 
                    // Optional: this.clearSelection();
                }
                return;
            }
            
            const filePath = row.getAttribute('data-file');
            const fileType = row.getAttribute('data-type');
            
            if (e.detail === 2) {
                if (fileType === 'folder') {
                    this.navigateIntoFolder(filePath);
                // } else {
                //     this.openFile(filePath);
                }
                return;
            }
            
            // Remove context menu button handling
            if (!e.target.matches('button, a, input, .material-icons-round, .preview-maximize-overlay, .maximize-preview-btn, .preview-action-btn')) {
                if (e.shiftKey && this.lastSelected) {
                    this.selectRange(this.lastSelected, filePath);
                } else if (e.ctrlKey || e.metaKey) {
                    this.toggleFileSelection(filePath);
                } else {
                    this.selectSingleFile(filePath);
                }
                this.lastSelected = filePath;
            }
        });
        
        // Remove the contextmenu event listener entirely
    }

    renderPreviewMedia(file) {
        if (file.type === 'folder') return null;
        
        const ext = file.name.split('.').pop().toLowerCase();
        const previewUrl = `/api/stream/file?path=${encodeURIComponent(file.path)}`;

        // 3D Models
        if (['glb', 'gltf', 'fbx', 'obj', 'blend', 'stl'].includes(ext)) {
            return this.render3DPreview(file);
        }

        // Images
        if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext)) {
            return `
                <div class="preview-media-container relative group">
                    <img src="${previewUrl}" 
                         class="w-full h-auto max-h-60 object-contain rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 transition-all duration-300 group-hover:blur-sm group-hover:brightness-75" 
                         alt="${file.name}" 
                         onerror="this.onerror=null; this.parentElement.innerHTML='<div class=\\'text-center text-xs text-red-400\\'>Preview unavailable</div>';">
                    <div class="preview-maximize-overlay absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                        <button class="maximize-preview-btn bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2 hover:bg-white dark:hover:bg-gray-700 transition-colors"
                                data-file="${file.path}"
                                data-type="${file.type}"
                                data-name="${file.name}">
                            <span class="material-icons-round">fullscreen</span>
                            Maximize
                        </button>
                    </div>
                </div>
            `;
        }
        
        // Video
        if (['mp4', 'webm', 'mov'].includes(ext)) {
            return `
                <div class="preview-media-container relative group">
                    <video controls class="w-full max-h-60 rounded-lg border border-gray-200 dark:border-gray-700 bg-black transition-all duration-300 group-hover:blur-sm group-hover:brightness-75">
                        <source src="${previewUrl}" type="video/${ext === 'mov' ? 'mp4' : ext}">
                    </video>
                    <div class="preview-maximize-overlay absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                        <button class="maximize-preview-btn bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2 hover:bg-white dark:hover:bg-gray-700 transition-colors"
                                data-file="${file.path}"
                                data-type="${file.type}"
                                data-name="${file.name}">
                            <span class="material-icons-round">fullscreen</span>
                            Maximize
                        </button>
                    </div>
                </div>
            `;
        }
        
        // Audio
        if (['mp3', 'wav', 'ogg', 'm4a'].includes(ext)) {
            return `
                <div class="preview-media-container relative group">
                    <div class="w-full p-4 bg-gray-100 dark:bg-gray-700 rounded-lg transition-all duration-300 group-hover:blur-sm group-hover:brightness-75">
                        <div class="flex items-center justify-center mb-2">
                            <span class="material-icons-round text-4xl text-gray-500">audiotrack</span>
                        </div>
                        <audio controls class="w-full h-8">
                            <source src="${previewUrl}" type="audio/${ext}">
                        </audio>
                    </div>
                    <div class="preview-maximize-overlay absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                        <button class="maximize-preview-btn bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2 hover:bg-white dark:hover:bg-gray-700 transition-colors"
                                data-file="${file.path}"
                                data-type="${file.type}"
                                data-name="${file.name}">
                            <span class="material-icons-round">fullscreen</span>
                            Maximize
                        </button>
                    </div>
                </div>`;
        }

        // PDF
        if (ext === 'pdf') {
            return `
                <div class="preview-media-container relative group">
                    <object data="${previewUrl}" 
                            type="application/pdf" 
                            class="w-full h-64 rounded-lg border border-gray-200 dark:border-gray-700 transition-all duration-300 group-hover:blur-sm group-hover:brightness-75">
                        <div class="flex items-center justify-center h-full text-sm text-gray-500">PDF Preview Unavailable</div>
                    </object>
                    <div class="preview-maximize-overlay absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                        <button class="maximize-preview-btn bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2 hover:bg-white dark:hover:bg-gray-700 transition-colors"
                                data-file="${file.path}"
                                data-type="${file.type}"
                                data-name="${file.name}">
                            <span class="material-icons-round">fullscreen</span>
                            Maximize
                        </button>
                    </div>
                </div>`;
        }

        // Text files
        if (['txt', 'md', 'html', 'css', 'js', 'py', 'json', 'xml', 'csv'].includes(ext)) {
            return `
                <div class="preview-media-container relative group">
                    <div class="w-full h-64 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 overflow-hidden transition-all duration-300 group-hover:blur-sm group-hover:brightness-75">
                        <div class="h-full overflow-auto p-3 text-sm font-mono">
                            <div class="text-preview-content" data-url="${previewUrl}">
                                Loading text preview...
                            </div>
                        </div>
                    </div>
                    <div class="preview-maximize-overlay absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300">
                        <button class="maximize-preview-btn bg-white/90 dark:bg-gray-800/90 text-gray-800 dark:text-white px-4 py-2 rounded-lg shadow-lg flex items-center gap-2 hover:bg-white dark:hover:bg-gray-700 transition-colors"
                                data-file="${file.path}"
                                data-type="${file.type}"
                                data-name="${file.name}">
                            <span class="material-icons-round">fullscreen</span>
                            Maximize
                        </button>
                    </div>
                </div>
            `;
        }
        
        return null;
    }

    render3DPreview(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        
        if (!['glb', 'gltf', 'fbx', 'obj'].includes(ext)) {
            return `
                <div class="flex flex-col items-center justify-center p-6 bg-gray-100 dark:bg-gray-700 rounded-lg">
                    <span class="material-icons-round text-4xl text-gray-400 mb-2">view_in_ar</span>
                    <p class="text-xs text-gray-500 text-center">3D Preview not supported for ${ext.toUpperCase()}</p>
                </div>`;
        }
        
        const previewUrl = `/api/stream/file?path=${encodeURIComponent(file.path)}`;
        const containerId = `model-${Date.now()}`;
        
        // Create container
        setTimeout(() => {
            const container = document.getElementById(containerId);
            if (!container || !window.THREE) return;
            
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x1a1a1a);
            
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / 300, 0.1, 1000);
            camera.position.z = 5;
            
            const renderer = new THREE.WebGLRenderer({ antialias: true });
            renderer.setSize(container.clientWidth, 300);
            container.appendChild(renderer.domElement);
            
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
            scene.add(ambientLight);
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 5, 5);
            scene.add(directionalLight);
            
            // Load model
            if (ext === 'glb' || ext === 'gltf') {
                const loader = new THREE.GLTFLoader();
                loader.load(previewUrl, (gltf) => {
                    scene.add(gltf.scene);
                    
                    // Center and scale
                    const box = new THREE.Box3().setFromObject(gltf.scene);
                    const center = box.getCenter(new THREE.Vector3());
                    gltf.scene.position.sub(center);
                    
                    const size = box.getSize(new THREE.Vector3());
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const scale = 3 / maxDim;
                    gltf.scene.scale.multiplyScalar(scale);
                }, undefined, (error) => {
                    console.error('Error loading model:', error);
                    container.innerHTML = '<div class="text-red-500 text-xs p-4">Failed to load model</div>';
                });
            } else if (ext === 'fbx') {
                const loader = new THREE.FBXLoader();
                loader.load(previewUrl, (fbx) => {
                    scene.add(fbx);
                    const box = new THREE.Box3().setFromObject(fbx);
                    const center = box.getCenter(new THREE.Vector3());
                    fbx.position.sub(center);
                    const size = box.getSize(new THREE.Vector3());
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const scale = 3 / maxDim;
                    fbx.scale.multiplyScalar(scale);
                }, undefined, (error) => {
                    console.error('Error loading FBX:', error);
                    container.innerHTML = '<div class="text-red-500 text-xs p-4">Failed to load FBX</div>';
                });
            }
            
            function animate() {
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            }
            animate();
            
            // Cleanup on panel close
            document.getElementById('close-preview')?.addEventListener('click', () => {
                renderer.dispose();
                controls.dispose();
            }, { once: true });
            
        }, 100);
        
        return `<div id="${containerId}" class="w-full h-[300px] rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-900"></div>`;
    }

    renderPreviewPanel(file) {
        if (!file) {
            return `<p class="text-gray-500 text-center mt-10 text-sm">Select a file to preview</p>`;
        }
        
        const icon = file.type === 'folder' ? 'folder' : this.getFileIcon(file.name);
        const iconColor = file.type === 'folder' ? 'text-blue-500 dark:text-blue-400' : this.getFileIconColor(file.name);
        
        const mediaPreview = this.renderPreviewMedia(file);

        return `
            <div class="flex flex-col items-center">
                <div class="w-full mb-6 flex justify-center">
                    ${mediaPreview ? mediaPreview : `
                    <div class="w-24 h-24 rounded-2xl bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                        <span class="material-icons-round text-6xl ${iconColor}">${icon}</span>
                    </div>
                    `}
                </div>
                
                <h4 class="text-lg font-bold text-gray-900 dark:text-white text-center break-all mb-1">${file.name}</h4>
                <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">${file.type === 'folder' ? 'Folder' : this.getFileType(file.name)}</p>
                
                <div class="w-full space-y-4">
                    <div class="bg-white dark:bg-gray-700/50 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
                        <h5 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">Details</h5>
                        <div class="grid grid-cols-[80px_1fr] gap-2 text-sm">
                            <div class="text-gray-500 dark:text-gray-400">Size</div>
                            <div class="text-gray-900 dark:text-gray-200 font-medium">${file.size}</div>
                            
                            <div class="text-gray-500 dark:text-gray-400">Type</div>
                            <div class="text-gray-900 dark:text-gray-200 font-medium">${file.type === 'folder' ? 'Folder' : file.name.split('.').pop().toUpperCase()}</div>
                            
                            <div class="text-gray-500 dark:text-gray-400">Modified</div>
                            <div class="text-gray-900 dark:text-gray-200 font-medium">${this.formatDate(file.date)}</div>
                        </div>
                    </div>
                    
                    <div class="bg-white dark:bg-gray-700/50 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
                        <h5 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">Location</h5>
                        <p class="text-sm text-gray-700 dark:text-gray-300 break-all font-mono bg-gray-50 dark:bg-gray-800 p-2 rounded border border-gray-100 dark:border-gray-700/50">
                            ${file.path}
                        </p>
                    </div>
                </div>
                
                </div>
        `;
    }
    
    updatePreview() {
        const previewPanel = document.getElementById('preview-panel');
        const previewContent = document.getElementById('preview-content');
        const previewActions = document.getElementById('preview-actions');
        
        if (!previewPanel || !previewContent || !previewActions) return;
        
        if (this.selectedFiles.size === 1) {
            const filePath = Array.from(this.selectedFiles)[0];
            const sourceFiles = this.filteredFiles; // Always use filtered files
            const file = sourceFiles.find(f => f.path === filePath);
            
            if (file) {
                previewContent.innerHTML = this.renderPreviewPanel(file);
                previewActions.classList.remove('hidden');
                
                // Update action buttons with current file data
                previewActions.querySelectorAll('.preview-action-btn').forEach(btn => {
                    btn.setAttribute('data-file', file.path);
                    btn.setAttribute('data-type', file.type);
                    btn.setAttribute('data-name', file.name);
                    
                    // Update button text for restore based on file type
                    if (btn.getAttribute('data-action') === 'restore') {
                        const isFolder = file.type === 'folder';
                        btn.innerHTML = `
                            <span class="material-icons-round text-sm mr-2">restore</span>
                            Restore ${isFolder ? 'Folder' : 'File'}
                        `;
                    }
                });
                
                previewPanel.classList.remove('hidden');
                
                // Load text content for text files
                this.loadTextPreviewContent(file);
                
                // Set up maximize button listeners
                this.setupPreviewMaximizeListeners();
            }
        } else if (this.selectedFiles.size > 1) {
            previewContent.innerHTML = `
                <div class="flex flex-col items-center justify-center h-full">
                    <span class="material-icons-round text-4xl text-gray-400 mb-2">filter_none</span>
                    <p class="text-gray-600 dark:text-gray-300 font-medium">${this.selectedFiles.size} items selected</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Select a single item to view details</p>
                </div>
            `;
            previewActions.classList.add('hidden');
            previewPanel.classList.remove('hidden');
        } else {
            previewPanel.classList.add('hidden');
            previewActions.classList.add('hidden');
        }
    }

    async loadTextPreviewContent(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        if (!['txt', 'md', 'html', 'css', 'js', 'py', 'json', 'xml', 'csv'].includes(ext)) {
            return;
        }

        const previewUrl = `/api/stream/file?path=${encodeURIComponent(file.path)}`;
        const textPreviewEl = document.querySelector('.text-preview-content[data-url="' + previewUrl + '"]');
        
        if (!textPreviewEl) return;

        try {
            const response = await fetch(previewUrl);
            if (response.ok) {
                const text = await response.text();
                // Show first 1000 characters
                const previewText = text.length > 1000 ? text.substring(0, 1000) + '...' : text;
                textPreviewEl.textContent = previewText;
                textPreviewEl.classList.add('whitespace-pre-wrap');
            } else {
                textPreviewEl.textContent = 'Unable to load text content';
            }
        } catch (error) {
            textPreviewEl.textContent = 'Error loading text content';
        }
    }

    setupPreviewMaximizeListeners() {
        // Remove existing listeners
        document.querySelectorAll('.maximize-preview-btn').forEach(btn => {
            btn.replaceWith(btn.cloneNode(true));
        });

        // Add new listeners
        document.querySelectorAll('.maximize-preview-btn').forEach(btn => {
            btn.addEventListener('click', this.handlePreviewMaximize);
        });

        // Add preview action listeners
        document.querySelectorAll('.preview-action-btn').forEach(btn => {
            btn.addEventListener('click', this.handlePreviewAction);
        });
    }

    handlePreviewMaximize(event) {
        event.stopPropagation();
        
        const filePath = event.currentTarget.getAttribute('data-file');
        const fileType = event.currentTarget.getAttribute('data-type');
        const fileName = event.currentTarget.getAttribute('data-name');
        
        if (!filePath || !fileType) return;
        
        const sourceFiles = this.filteredFiles;
        const file = sourceFiles.find(f => f.path === filePath);
        
        if (!file) return;
        
        this.showMaximizedPreview(file);
    }

    showMaximizedPreview(file) {
        // Remove existing maximized preview
        const existingOverlay = document.getElementById('maximized-preview-overlay');
        if (existingOverlay) {
            this.closeMaximizedPreview();
        }

        this.maximizedPreview = file;
        
        const overlay = document.createElement('div');
        overlay.id = 'maximized-preview-overlay';
        overlay.className = 'fixed inset-0 bg-black/90 dark:bg-black/95 z-50 flex items-center justify-center p-4 modal-backdrop';
        
        // Generate a unique container ID for 3D models
        const ext = file.name.split('.').pop().toLowerCase();
        const is3DModel = ['glb', 'gltf', 'fbx', 'obj', 'blend', 'stl'].includes(ext);
        const containerId = is3DModel ? `maximized-3d-${Date.now()}` : null;
        
        overlay.innerHTML = this.renderMaximizedPreview(file, containerId);
        
        document.body.appendChild(overlay);
        
        // Close on click outside
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.closeMaximizedPreview();
            }
        });
        
        // Escape key to close
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                this.closeMaximizedPreview();
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
        
        // Load text content for maximized text preview
        this.loadMaximizedTextPreviewContent(file);
    }

    renderMaximizedPreview(file, containerId = null) {
        const icon = file.type === 'folder' ? 'folder' : this.getFileIcon(file.name);
        const iconColor = file.type === 'folder' ? 'text-blue-500 dark:text-blue-400' : this.getFileIconColor(file.name);
        const ext = file.name.split('.').pop().toLowerCase();
        const previewUrl = `/api/stream/file?path=${encodeURIComponent(file.path)}`;
        
        let content = '';
        
        // 3D Models
        if (['glb', 'gltf', 'fbx', 'obj', 'blend', 'stl'].includes(ext)) {
            const modelContainerId = containerId || `maximized-3d-${Date.now()}`;
            content = `
                <div id="${modelContainerId}" class="w-full h-[85vh] rounded-lg shadow-2xl bg-gray-900"></div>
            `;
            
            // Store the container ID for cleanup
            this.maximized3DContainerId = modelContainerId;
            
            // Load the 3D model after the DOM is ready
            setTimeout(() => {
                this.setupMaximized3DPreview(modelContainerId, previewUrl, ext, file.name);
            }, 100);
            
        } else if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext)) {
            content = `
                <img src="${previewUrl}" 
                    class="max-w-full max-h-[85vh] object-contain rounded-lg shadow-2xl"
                    alt="${file.name}"
                    onerror="this.onerror=null; this.src='';">`;
        } else if (['mp4', 'webm', 'mov'].includes(ext)) {
            content = `
                <video controls autoplay class="max-w-full max-h-[85vh] rounded-lg shadow-2xl bg-black">
                    <source src="${previewUrl}" type="video/${ext === 'mov' ? 'mp4' : ext}">
                </video>`;
        } else if (ext === 'pdf') {
            content = `
                <object data="${previewUrl}" 
                        type="application/pdf" 
                        class="w-full h-[85vh] rounded-lg shadow-2xl bg-white">
                    <div class="flex items-center justify-center h-full text-lg text-gray-500">
                        PDF Preview Unavailable
                    </div>
                </object>`;
        } else if (['txt', 'md', 'html', 'css', 'js', 'py', 'json', 'xml', 'csv'].includes(ext)) {
            content = `
                <div class="w-full h-[85vh] rounded-lg shadow-2xl bg-white dark:bg-gray-900 overflow-hidden">
                    <div class="h-full overflow-auto p-6 text-base font-mono">
                        <div class="text-preview-content-maximized" data-url="${previewUrl}">
                            Loading text content...
                        </div>
                    </div>
                </div>
            `;
        } else {
            content = `
                <div class="w-48 h-48 rounded-2xl bg-gray-100 dark:bg-gray-700 flex items-center justify-center shadow-2xl">
                    <span class="material-icons-round text-8xl ${iconColor}">${icon}</span>
                </div>
            `;
        }
        
        return `
            <div class="relative w-full max-w-7xl animate-fade-in-up flex flex-col items-center">
                <div class="w-full flex justify-center">
                    ${content}
                </div>
                
                <div class="mt-4 bg-white/10 dark:bg-gray-800/50 backdrop-blur-sm rounded-lg p-4 w-full max-w-3xl">
                    <h3 class="text-xl font-bold text-white mb-2">${file.name}</h3>
                    <div class="flex flex-wrap gap-4 text-sm text-gray-300">
                        <span class="flex items-center gap-2">
                            <span class="material-icons-round text-base">description</span>
                            ${file.type === 'folder' ? 'Folder' : this.getFileType(file.name)}
                        </span>
                        <span class="flex items-center gap-2">
                            <span class="material-icons-round text-base">storage</span>
                            ${file.size}
                        </span>
                        <span class="flex items-center gap-2">
                            <span class="material-icons-round text-base">schedule</span>
                            ${this.formatDate(file.date)}
                        </span>
                    </div>
                </div>
            </div>
        `;
    }

    setupMaximized3DPreview(containerId, previewUrl, ext, fileName) {
        const container = document.getElementById(containerId);
        if (!container || !window.THREE) {
            if (!window.THREE) {
                container.innerHTML = `
                    <div class="flex flex-col items-center justify-center h-full">
                        <span class="material-icons-round text-6xl text-gray-400 mb-2">view_in_ar</span>
                        <p class="text-gray-300">3D Preview requires Three.js library</p>
                        <p class="text-gray-400 text-sm mt-1">Please ensure Three.js is loaded</p>
                    </div>
                `;
            }
            return;
        }
        
        try {
            // Clear any existing content
            container.innerHTML = '';
            
            // Create a loading indicator
            const loadingIndicator = document.createElement('div');
            loadingIndicator.className = 'flex flex-col items-center justify-center h-full text-gray-300';
            loadingIndicator.innerHTML = `
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
                <p>Loading 3D model...</p>
                <p class="text-sm text-gray-400 mt-1">${fileName}</p>
            `;
            container.appendChild(loadingIndicator);
            
            // Setup Three.js scene
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x1a1a1a);
            
            // Create camera with aspect ratio based on container
            const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.z = 5;
            
            // Create renderer
            const renderer = new THREE.WebGLRenderer({ 
                antialias: true,
                alpha: true 
            });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            
            // Create controls
            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.screenSpacePanning = false;
            controls.minDistance = 1;
            controls.maxDistance = 50;
            controls.maxPolarAngle = Math.PI;
            
            // Add lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(5, 5, 5);
            scene.add(directionalLight);
            
            // Add a subtle hemisphere light for better lighting
            const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.3);
            scene.add(hemisphereLight);
            
            // Grid helper for reference
            const gridHelper = new THREE.GridHelper(10, 10, 0x444444, 0x222222);
            scene.add(gridHelper);
            
            // Load the model
            const loadModel = () => {
                let loader;
                
                if (ext === 'glb' || ext === 'gltf') {
                    if (!THREE.GLTFLoader) {
                        throw new Error('GLTFLoader not available');
                    }
                    loader = new THREE.GLTFLoader();
                    loader.load(previewUrl, 
                        (gltf) => {
                            container.removeChild(loadingIndicator);
                            container.appendChild(renderer.domElement);
                            
                            const model = gltf.scene;
                            scene.add(model);
                            
                            // Center and scale the model
                            const box = new THREE.Box3().setFromObject(model);
                            const center = box.getCenter(new THREE.Vector3());
                            const size = box.getSize(new THREE.Vector3());
                            
                            model.position.x += (model.position.x - center.x);
                            model.position.y += (model.position.y - center.y);
                            model.position.z += (model.position.z - center.z);
                            
                            const maxDim = Math.max(size.x, size.y, size.z);
                            const scale = 5 / maxDim;
                            model.scale.multiplyScalar(scale);
                            
                            // Update controls target
                            controls.target.copy(center);
                            controls.update();
                            
                            // Start animation loop
                            animate();
                        },
                        (xhr) => {
                            // Progress callback
                            const percent = Math.round((xhr.loaded / xhr.total) * 100);
                            loadingIndicator.innerHTML = `
                                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
                                <p>Loading 3D model...</p>
                                <p class="text-sm text-gray-400 mt-1">${percent}% loaded</p>
                                <div class="w-48 h-2 bg-gray-700 rounded-full mt-2 overflow-hidden">
                                    <div class="h-full bg-blue-500 transition-all duration-300" style="width: ${percent}%"></div>
                                </div>
                            `;
                        },
                        (error) => {
                            console.error('Error loading 3D model:', error);
                            loadingIndicator.innerHTML = `
                                <span class="material-icons-round text-6xl text-red-400 mb-2">error</span>
                                <p class="text-red-300">Failed to load 3D model</p>
                                <p class="text-gray-400 text-sm mt-1">${error.message || 'Unknown error'}</p>
                            `;
                        }
                    );
                } else if (ext === 'fbx') {
                    if (!THREE.FBXLoader) {
                        throw new Error('FBXLoader not available');
                    }
                    loader = new THREE.FBXLoader();
                    loader.load(previewUrl, 
                        (fbx) => {
                            container.removeChild(loadingIndicator);
                            container.appendChild(renderer.domElement);
                            
                            scene.add(fbx);
                            
                            const box = new THREE.Box3().setFromObject(fbx);
                            const center = box.getCenter(new THREE.Vector3());
                            const size = box.getSize(new THREE.Vector3());
                            
                            fbx.position.x += (fbx.position.x - center.x);
                            fbx.position.y += (fbx.position.y - center.y);
                            fbx.position.z += (fbx.position.z - center.z);
                            
                            const maxDim = Math.max(size.x, size.y, size.z);
                            const scale = 5 / maxDim;
                            fbx.scale.multiplyScalar(scale);
                            
                            controls.target.copy(center);
                            controls.update();
                            
                            animate();
                        },
                        (xhr) => {
                            const percent = Math.round((xhr.loaded / xhr.total) * 100);
                            loadingIndicator.innerHTML = `
                                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
                                <p>Loading FBX model...</p>
                                <p class="text-sm text-gray-400 mt-1">${percent}% loaded</p>
                                <div class="w-48 h-2 bg-gray-700 rounded-full mt-2 overflow-hidden">
                                    <div class="h-full bg-blue-500 transition-all duration-300" style="width: ${percent}%"></div>
                                </div>
                            `;
                        },
                        (error) => {
                            console.error('Error loading FBX:', error);
                            loadingIndicator.innerHTML = `
                                <span class="material-icons-round text-6xl text-red-400 mb-2">error</span>
                                <p class="text-red-300">Failed to load FBX model</p>
                                <p class="text-gray-400 text-sm mt-1">${error.message || 'Unknown error'}</p>
                            `;
                        }
                    );
                } else if (ext === 'obj') {
                    if (!THREE.OBJLoader) {
                        throw new Error('OBJLoader not available');
                    }
                    loader = new THREE.OBJLoader();
                    loader.load(previewUrl, 
                        (obj) => {
                            container.removeChild(loadingIndicator);
                            container.appendChild(renderer.domElement);
                            
                            scene.add(obj);
                            
                            const box = new THREE.Box3().setFromObject(obj);
                            const center = box.getCenter(new THREE.Vector3());
                            const size = box.getSize(new THREE.Vector3());
                            
                            obj.position.x += (obj.position.x - center.x);
                            obj.position.y += (obj.position.y - center.y);
                            obj.position.z += (obj.position.z - center.z);
                            
                            const maxDim = Math.max(size.x, size.y, size.z);
                            const scale = 5 / maxDim;
                            obj.scale.multiplyScalar(scale);
                            
                            controls.target.copy(center);
                            controls.update();
                            
                            animate();
                        },
                        (xhr) => {
                            const percent = Math.round((xhr.loaded / xhr.total) * 100);
                            loadingIndicator.innerHTML = `
                                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
                                <p>Loading OBJ model...</p>
                                <p class="text-sm text-gray-400 mt-1">${percent}% loaded</p>
                                <div class="w-48 h-2 bg-gray-700 rounded-full mt-2 overflow-hidden">
                                    <div class="h-full bg-blue-500 transition-all duration-300" style="width: ${percent}%"></div>
                                </div>
                            `;
                        },
                        (error) => {
                            console.error('Error loading OBJ:', error);
                            loadingIndicator.innerHTML = `
                                <span class="material-icons-round text-6xl text-red-400 mb-2">error</span>
                                <p class="text-red-300">Failed to load OBJ model</p>
                                <p class="text-gray-400 text-sm mt-1">${error.message || 'Unknown error'}</p>
                            `;
                        }
                    );
                } else {
                    // Unsupported 3D format
                    loadingIndicator.innerHTML = `
                        <span class="material-icons-round text-6xl text-yellow-400 mb-2">view_in_ar</span>
                        <p class="text-yellow-300">3D Preview not supported</p>
                        <p class="text-gray-400 text-sm mt-1">Format: ${ext.toUpperCase()}</p>
                    `;
                }
            };
            
            // Animation loop
            const animate = () => {
                requestAnimationFrame(animate);
                controls.update();
                renderer.render(scene, camera);
            };
            
            // Handle window resize
            const handleResize = () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            };
            
            window.addEventListener('resize', handleResize);
            
            // Store references for cleanup
            container._threejs = {
                scene,
                camera,
                renderer,
                controls,
                animate,
                handleResize,
                cleanup: () => {
                    window.removeEventListener('resize', handleResize);
                    if (renderer) renderer.dispose();
                    if (controls) controls.dispose();
                    if (scene) {
                        scene.traverse((object) => {
                            if (object.geometry) object.geometry.dispose();
                            if (object.material) {
                                if (Array.isArray(object.material)) {
                                    object.material.forEach(material => material.dispose());
                                } else {
                                    object.material.dispose();
                                }
                            }
                        });
                    }
                }
            };
            
            // Start loading the model
            loadModel();
            
        } catch (error) {
            console.error('Error setting up 3D preview:', error);
            container.innerHTML = `
                <div class="flex flex-col items-center justify-center h-full text-red-300">
                    <span class="material-icons-round text-6xl mb-2">error</span>
                    <p>Failed to initialize 3D preview</p>
                    <p class="text-gray-400 text-sm mt-1">${error.message}</p>
                </div>
            `;
        }
    }

    async loadMaximizedTextPreviewContent(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        if (!['txt', 'md', 'html', 'css', 'js', 'py', 'json', 'xml', 'csv'].includes(ext)) {
            return;
        }

        const previewUrl = `/api/stream/file?path=${encodeURIComponent(file.path)}`;
        const textPreviewEl = document.querySelector('.text-preview-content-maximized[data-url="' + previewUrl + '"]');
        
        if (!textPreviewEl) return;

        try {
            const response = await fetch(previewUrl);
            if (response.ok) {
                const text = await response.text();
                // Show full content in maximized view
                textPreviewEl.textContent = text;
                textPreviewEl.classList.add('whitespace-pre-wrap');
            } else {
                textPreviewEl.textContent = 'Unable to load text content';
            }
        } catch (error) {
            textPreviewEl.textContent = 'Error loading text content';
        }
    }

    closeMaximizedPreview() {
        const overlay = document.getElementById('maximized-preview-overlay');
        
        // Clean up Three.js resources if present
        if (this.maximized3DContainerId) {
            const container = document.getElementById(this.maximized3DContainerId);
            if (container && container._threejs) {
                container._threejs.cleanup();
            }
            this.maximized3DContainerId = null;
        }
        
        if (overlay) {
            overlay.remove();
        }
        this.maximizedPreview = null;
    }

    handlePreviewAction(event) {
        event.preventDefault();
        event.stopPropagation();
        
        const action = event.currentTarget.getAttribute('data-action');
        const filePath = event.currentTarget.getAttribute('data-file');
        const fileType = event.currentTarget.getAttribute('data-type');
        const fileName = event.currentTarget.getAttribute('data-name');
        
        if (!filePath || !fileType) return;
        
        this.handleFileAction(action, filePath, fileType, fileName);
    }

    async loadFolderContents() {
        try {
            this.isLoading = true;
            this.updateContentOnly();
            
            const path = this.currentPath.join('/');
            const response = await fetch(`/api/backup/files?path=${encodeURIComponent(path)}`);
            const data = await response.json();
            
            if (data.success) {
                console.log('API response data:', data); // Added log
                if (data.message) {
                    if (data.message.includes('No backup device configured')) {
                        this.isBackupDeviceConfigured = false;
                        this.showNoDeviceState();
                        return;
                    } else {
                        this.allFiles = [];
                        this.filteredFiles = [];
                    }
                } else {
                    this.allFiles = data.items.map(item => ({
                        name: item.name,
                        path: item.path,
                        type: item.type,
                        date: item.lastModified || Date.now() / 1000,
                        // Fix: Parse to int for strictly correct size comparison
                        rawSize: item.size ? parseInt(item.size, 10) : 0,
                        size: item.size ? this.formatFileSize(item.size) : '--'
                    }));
                    
                    if (data.backup_base) this.backupBasePath = data.backup_base;
                    
                    this.rawSearchResults = null;
                    this.applyCurrentFilters();
                    this.applySortingFromFilters();
                    this.isBackupDeviceConfigured = true;
                }
            } else {
                this.allFiles = [];
                this.filteredFiles = [];
                this.isBackupDeviceConfigured = false;
            }
        } catch (error) {
            this.allFiles = [];
            this.filteredFiles = [];
            console.error('Error loading folder contents:', error); // Added log
            this.isBackupDeviceConfigured = false;
        } finally {
            this.isLoading = false;
            this.updateContentOnly();
            this.updateFileSummary();
            this.updateBreadcrumbs();
            this.updateUIControlsState();
        }
    }
    
    updateContentOnly() {
        const contentContainer = document.getElementById('content-container');
        if (contentContainer) {
            contentContainer.innerHTML = this.isLoading ? this.renderLoading() : this.renderContent();
            
            if (!this.isLoading) {
                this.setupFileSelection();
                this.updatePreview();
                // FIX: Re-attach sort listeners because the header HTML was just replaced
                this.attachDynamicListeners();
            }
        }
    }
    
    updateFileSummary() {
        // Always use filteredFiles for summary stats to match view
        const displayFiles = this.filteredFiles;
        const totalItems = displayFiles.length;
        const selectedCount = this.selectedFiles.size;
        
        const totalSize = displayFiles.reduce((sum, file) => {
            return sum + (file.rawSize !== undefined ? file.rawSize : this.parseFileSize(file.size));
        }, 0);
        
        const summaryElement = document.getElementById('file-summary');
        if (summaryElement) {
            if (!this.isBackupDeviceConfigured) {
                summaryElement.textContent = 'No backup device configured';
                return;
            }
            
            let summaryText = `${totalItems} item${totalItems !== 1 ? 's' : ''}`;
            if (this.searchQuery) summaryText += ` matching "${this.searchQuery}"`;
            else if (this.getActiveFilterCount() > 0) summaryText += ` (filtered)`;
            
            if (selectedCount > 0) summaryText += ` (${selectedCount} selected)`;
            summaryText += `, ${this.formatFileSize(totalSize)} total`;
            summaryElement.textContent = summaryText;
        }
        
        const statsElement = document.getElementById('folder-stats');
        if (statsElement) {
            if (!this.isBackupDeviceConfigured) {
                statsElement.textContent = 'No backup device configured';
            } else if (totalItems === 0) {
                if (this.searchQuery) {
                    statsElement.textContent = `No files found matching "${this.searchQuery}"`;
                } else if (this.getActiveFilterCount() > 0) {
                    statsElement.textContent = 'No files match filters';
                } else {
                    statsElement.textContent = 'No files found';
                }
            } else {
                let statsText = `${totalItems} item${totalItems !== 1 ? 's' : ''}`;
                if (this.searchQuery) statsText += ` matching "${this.searchQuery}"`;
                else if (this.getActiveFilterCount() > 0) statsText += ` (filtered)`;
                
                statsText += ` • ${this.formatFileSize(totalSize)}`;
                statsElement.textContent = statsText;
            }
        }
        
        const restoreBtn = document.getElementById('restore-all');
        const downloadBtn = document.getElementById('download-selected');
        
        if (restoreBtn && downloadBtn) {
            const isDisabled = selectedCount === 0 || !this.isBackupDeviceConfigured;
            restoreBtn.classList.toggle('opacity-50', isDisabled);
            restoreBtn.classList.toggle('cursor-not-allowed', isDisabled);
            downloadBtn.classList.toggle('opacity-50', isDisabled);
            downloadBtn.classList.toggle('cursor-not-allowed', isDisabled);
        }
    }
    
    toggleFileSelection(filePath) {
        if (this.selectedFiles.has(filePath)) {
            this.selectedFiles.delete(filePath);
        } else {
            this.selectedFiles.add(filePath);
        }
        this.updateFileSummary();
        this.updateSelectionUI();
        this.updatePreview();
    }
    
    selectSingleFile(filePath) {
        this.selectedFiles.clear();
        this.selectedFiles.add(filePath);
        this.updateFileSummary();
        this.updateSelectionUI();
        this.updatePreview();
    }
    
    selectRange(startPath, endPath) {
        const files = this.filteredFiles.map(f => f.path);
        const startIndex = files.indexOf(startPath);
        const endIndex = files.indexOf(endPath);
        
        if (startIndex === -1 || endIndex === -1) return;
        
        const [min, max] = [Math.min(startIndex, endIndex), Math.max(startIndex, endIndex)];
        
        for (let i = min; i <= max; i++) {
            this.selectedFiles.add(files[i]);
        }
        
        this.updateFileSummary();
        this.updateSelectionUI();
        this.updatePreview();
    }
    
    updateSelectionUI() {
        const selector = this.viewMode === 'list' ? '#files-list tr' : '#files-grid > div';
        const elements = document.querySelectorAll(selector);
        
        elements.forEach(element => {
            const filePath = element.getAttribute('data-file');
            if (filePath) {
                if (this.selectedFiles.has(filePath)) {
                    element.classList.add('selected-highlight');
                } else {
                    element.classList.remove('selected-highlight');
                }
            }
        });
    }
    
    navigateBack() {
        if (!this.isBackupDeviceConfigured) {
            showInfo('Please configure a backup device first', 'warning');
            return;
        }
        if (this.currentPath.length > 0) {
            this.currentPath.pop();
            this.loadFolderContents();
        }
    }
    
    navigateForward() {
        // Future implementation
    }
    
    navigateToBreadcrumb(index) {
        if (!this.isBackupDeviceConfigured) {
            showInfo('Please configure a backup device first', 'warning');
            return;
        }
        if (index === 0) {
            this.currentPath = [];
        } else {
            this.currentPath = this.currentPath.slice(0, index);
        }
        this.loadFolderContents();
    }
    
    navigateIntoFolder(folderPath) {
        if (!this.isBackupDeviceConfigured) {
            showInfo('Please configure a backup device first', 'warning');
            return;
        }
        
        const pathSegments = folderPath.split('/').filter(segment => segment.length > 0);
        let startIndex = 0;
        for (let i = 0; i < Math.min(this.currentPath.length, pathSegments.length); i++) {
            if (this.currentPath[i] === pathSegments[i]) {
                startIndex = i + 1;
            } else {
                break;
            }
        }
        for (let i = startIndex; i < pathSegments.length; i++) {
            this.currentPath.push(pathSegments[i]);
        }
        this.loadFolderContents();
    }
    
    toggleView(viewType) {
        if (!this.isBackupDeviceConfigured) {
            showInfo('Please configure a backup device first', 'warning');
            return;
        }
        this.viewMode = viewType;
        this.updateViewToggle();
        this.updateContentOnly();
    }
    
    applyCurrentFilters() {
        console.log('Applying current filters:', this.activeFilters);
        
        let source = this.allFiles;
        if (this.searchQuery) {
            if (this.rawSearchResults) {
                source = this.rawSearchResults;
            } else {
                const query = this.searchQuery.toLowerCase();
                source = this.allFiles.filter(file => 
                    file.name.toLowerCase().includes(query) || 
                    (file.path && file.path.toLowerCase().includes(query))
                );
            }
        }
        
        let filtered = [...source];
        
        console.log('Total items before filtering:', filtered.length);
        
        // Apply type filters (Folder vs File)
        if (!this.activeFilters.showFolders || !this.activeFilters.showFiles) {
            filtered = filtered.filter(file => {
                const isFolder = file.type === 'folder';
                // If not showing folders, and this is a folder, filter out
                if (!this.activeFilters.showFolders && isFolder) return false;
                // If not showing files, and this is NOT a folder, filter out
                if (!this.activeFilters.showFiles && !isFolder) return false;
                
                return true;
            });
        }
        
        console.log('Items after type filtering:', filtered.length);
        
        // Apply size filter
        if (this.activeFilters.sizeFilter !== 'all') {
            console.log('Applying size filter:', this.activeFilters.sizeFilter);
            
            filtered = filtered.filter(file => {
                if (file.type === 'folder') return true; // Always show folders regardless of size settings (prevents empty screens)
                
                // Robust size retrieval: check rawSize, then fall back to parsing string
                let size = 0;
                if (file.rawSize !== undefined && file.rawSize !== null) {
                     size = file.rawSize;
                } else {
                     size = this.parseFileSize(file.size);
                }
                
                switch (this.activeFilters.sizeFilter) {
                    case 'small':
                        return size < 1024 * 1024; // < 1 MB
                    case 'medium':
                        return size >= 1024 * 1024 && size <= 100 * 1024 * 1024; // 1-100 MB
                    case 'large':
                        return size > 100 * 1024 * 1024; // > 100 MB
                    case 'huge':
                        return size > 1024 * 1024 * 1024; // > 1 GB
                    default:
                        return true;
                }
            });
        }
        
        this.filteredFiles = filtered;
        
        // Apply sorting
        this.applySorting();
    }
        
    applySortingFromFilters() {
        switch (this.activeFilters.sortBy) {
            case 'name': this.sortColumn = 'name'; this.sortDirection = 'asc'; break;
            case 'name-desc': this.sortColumn = 'name'; this.sortDirection = 'desc'; break;
            case 'date': this.sortColumn = 'date'; this.sortDirection = 'desc'; break;
            case 'date-desc': this.sortColumn = 'date'; this.sortDirection = 'asc'; break;
            case 'size': this.sortColumn = 'size'; this.sortDirection = 'asc'; break;
            case 'size-desc': this.sortColumn = 'size'; this.sortDirection = 'desc'; break;
            case 'type': this.sortColumn = 'type'; this.sortDirection = 'asc'; break;
        }
        this.applySorting();
    }
    
    applyFilters() {
        console.log('Applying filters...');
        
        // Use a scoped query selector to avoid picking up elements from other parts of the app
        const dropdown = document.getElementById('filter-dropdown');
        if (!dropdown) return;
        
        // Get current values from the DOM
        const folderCheckbox = dropdown.querySelector('[data-filter="folder"]');
        const fileCheckbox = dropdown.querySelector('[data-filter="file"]');
        const sizeFilter = document.getElementById('size-filter');
        const sortFilter = document.getElementById('sort-filter');
        
        console.log('Folder checkbox:', folderCheckbox?.checked);
        console.log('File checkbox:', fileCheckbox?.checked);
        console.log('Size filter:', sizeFilter?.value);
        console.log('Sort filter:', sortFilter?.value);
        
        // Update active filters
        this.activeFilters.showFolders = folderCheckbox ? folderCheckbox.checked : true;
        this.activeFilters.showFiles = fileCheckbox ? fileCheckbox.checked : true;
        this.activeFilters.sizeFilter = sizeFilter ? sizeFilter.value : 'all';
        this.activeFilters.sortBy = sortFilter ? sortFilter.value : 'name';
        
        console.log('Active filters after update:', this.activeFilters);
        
        // Apply the filters
        this.applyCurrentFilters();
        this.applySortingFromFilters();
        this.updateContentOnly();
        this.updateFileSummary();
        
        // Show feedback
        const filterCount = this.getActiveFilterCount();
        if (filterCount > 0) {
            showInfo(`Applied ${filterCount} filter${filterCount > 1 ? 's' : ''}`, 'success');
        }
    }

    // Helper method to count active filters
    getActiveFilterCount() {
        let count = 0;
        
        // Check if folders/files are filtered out
        if (!this.activeFilters.showFolders || !this.activeFilters.showFiles) {
            count++;
        }
        
        // Check if size filter is active
        if (this.activeFilters.sizeFilter !== 'all') {
            count++;
        }
        
        // Check if sort is not default
        if (this.activeFilters.sortBy !== 'name') {
            count++;
        }
        
        return count;
    }

    resetFilters() {
        console.log('Resetting filters...');
        
        // Reset to defaults
        this.activeFilters = {
            showFolders: true,
            showFiles: true,
            sizeFilter: 'all',
            sortBy: 'name'
        };
        
        // Update DOM elements
        const folderCheckbox = document.querySelector('[data-filter="folder"]');
        const fileCheckbox = document.querySelector('[data-filter="file"]');
        const sizeFilter = document.getElementById('size-filter');
        const sortFilter = document.getElementById('sort-filter');
        
        if (folderCheckbox) folderCheckbox.checked = true;
        if (fileCheckbox) fileCheckbox.checked = true;
        if (sizeFilter) sizeFilter.value = 'all';
        if (sortFilter) sortFilter.value = 'name';
        
        console.log('Reset to default filters:', this.activeFilters);
        
        // Apply the reset filters
        this.applyCurrentFilters();
        this.applySortingFromFilters();
        this.updateContentOnly();
        this.updateFileSummary();
        
        showInfo('Filters reset to default', 'success');
    }
    
    parseFileSize(sizeStr) {
        if (!sizeStr || sizeStr === '--' || sizeStr === '0 B' || sizeStr === '') return 0;
        
        // Clean the string
        const cleanStr = sizeStr.trim().replace(/,/g, '');
        
        // Extract number and unit
        const match = cleanStr.match(/^([\d.]+)\s*([KMGTP]?B)$/i);
        if (!match) {
            // Try alternative pattern
            const altMatch = cleanStr.match(/^([\d.]+)\s*([a-zA-Z]+)$/);
            if (!altMatch) return 0;
            
            const [, valueStr, unit] = altMatch;
            const value = parseFloat(valueStr);
            if (isNaN(value)) return 0;
            
            const unitUpper = unit.toUpperCase();
            switch (unitUpper) {
                case 'B': return value;
                case 'KB': return value * 1024;
                case 'MB': return value * 1024 * 1024;
                case 'GB': return value * 1024 * 1024 * 1024;
                case 'TB': return value * 1024 * 1024 * 1024 * 1024;
                default: return 0;
            }
        }
        
        const [, valueStr, unit] = match;
        const value = parseFloat(valueStr);
        if (isNaN(value)) return 0;
        
        const unitUpper = unit.toUpperCase();
        switch (unitUpper) {
            case 'B': return value;
            case 'KB': return value * 1024;
            case 'MB': return value * 1024 * 1024;
            case 'GB': return value * 1024 * 1024 * 1024;
            case 'TB': return value * 1024 * 1024 * 1024 * 1024;
            default: return value;
        }
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        if (typeof bytes !== 'number' || isNaN(bytes)) return '--';
        
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        // Handle very small files (less than 1 KB)
        if (i === 0) return bytes + ' B';
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }
        
    sortFiles(column) {
        if (!this.isBackupDeviceConfigured) {
            showInfo('Please configure a backup device first', 'warning');
            return;
        }
        if (this.sortColumn === column) {
            this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
        } else {
            this.sortColumn = column;
            this.sortDirection = 'asc';
        }
        this.applySorting();
        this.updateContentOnly();
    }
    
    applySorting() {
        const filesToSort = this.filteredFiles; // Correctly sort filtered files
        filesToSort.sort((a, b) => {
            let aValue, bValue;
            switch (this.sortColumn) {
                case 'name':
                    aValue = a.name.toLowerCase();
                    bValue = b.name.toLowerCase();
                    break;
                case 'date':
                    aValue = a.date;
                    bValue = b.date;
                    break;
                case 'path':
                    aValue = a.path.toLowerCase();
                    bValue = b.path.toLowerCase();
                    break;
                case 'type':
                    aValue = a.type;
                    bValue = b.type;
                    break;
                case 'size':
                    // Use rawSize if available for better sorting
                    aValue = a.rawSize !== undefined ? a.rawSize : this.parseFileSize(a.size);
                    bValue = b.rawSize !== undefined ? b.rawSize : this.parseFileSize(b.size);
                    break;
                default:
                    return 0;
            }
            const direction = this.sortDirection === 'asc' ? 1 : -1;
            if (aValue < bValue) return -1 * direction;
            if (aValue > bValue) return 1 * direction;
            return 0;
        });
    }
    
    showNoDeviceState() {
        const contentContainer = document.getElementById('content-container');
        if (contentContainer) contentContainer.innerHTML = this.renderNoDeviceState();
        
        const statsElement = document.getElementById('folder-stats');
        if (statsElement) statsElement.textContent = 'No backup device configured';
        
        this.updateUIControlsState();
    }
    
    async refreshDeviceStatus() {
        const hasBackupDevice = await this.checkBackupDeviceConfigured();
        this.isBackupDeviceConfigured = hasBackupDevice;
        
        if (hasBackupDevice && this.allFiles.length === 0) {
            await this.loadFolderContents();
        } else if (!hasBackupDevice) {
            this.showNoDeviceState();
        }
        
        // Re-render the entire page to update the filter dropdown
        const container = document.getElementById('page-container');
        if (container) {
            container.innerHTML = await this.render();
            await this.afterRender();
        }
    }
    
    async handleFileAction(action, filePath, fileType, fileName) {
        if (!this.isBackupDeviceConfigured) {
            showInfo('Please configure a backup device first', 'warning');
            return;
        }
        
        switch(action) {
            case 'open':
                if (fileType === 'folder') {
                    this.navigateIntoFolder(filePath);
                } else {
                    this.openFile(filePath);
                }
                break;
                
            case 'open-location':
                try {
                    const fullPath = this.backupBasePath + '/' + filePath;
                    const response = await fetch('/api/open-location', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ file_path: fullPath })
                    });
                    const data = await response.json();
                    if (data.success) {
                        showInfo('Location opened', 'success');
                    } else {
                        showInfo('Failed to open location', 'error');
                    }
                } catch (error) {
                    showInfo('Failed to open location', 'error');
                }
                break;
                
            case 'restore':
                // Use RestoreWindow instead of direct restore
                this.restoreWindow.open(filePath, fileType, fileName);
                break;
                
            case 'download':
                this.downloadFile(filePath, fileName);
                break;
        }
    }
    
    async openFile(filePath) {
        try {
            const fullPath = this.backupBasePath + '/' + filePath;
            const response = await fetch('/api/open-file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_path: fullPath })
            });
            const data = await response.json();
            if (data.success) {
                showInfo('File opened', 'success');
            } else {
                showInfo('Failed to open file', 'error');
            }
        } catch (error) {
            showInfo('Failed to open file', 'error');
        }
    }
    
    async restoreSelected() {
        if (this.selectedFiles.size === 0) {
            showInfo('No files selected to restore', 'warning');
            return;
        }
        
        try {
            for (const filePath of this.selectedFiles) {
                const fileName = filePath.split('/').pop();
                const response = await fetch('/api/backup/restore', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        file_path: filePath,
                        restore_to: 'original'
                    })
                });
                await response.json();
            }
            
            showInfo(`Restoring ${this.selectedFiles.size} files...`, 'info');
            this.selectedFiles.clear();
            this.updateFileSummary();
            
            setTimeout(() => {
                showInfo('Files restored successfully', 'success');
            }, 2000);
        } catch (error) {
            showInfo('Failed to restore files', 'error');
        }
    }
    
    async downloadFile(filePath, fileName) {
        showInfo(`Downloading ${fileName}...`, 'info');
        setTimeout(() => {
            showInfo(`${fileName} download started`, 'success');
        }, 1000);
    }
    
    async downloadSelected() {
        if (this.selectedFiles.size === 0) {
            showInfo('No files selected to download', 'warning');
            return;
        }
        
        showInfo(`Downloading ${this.selectedFiles.size} files...`, 'info');
        setTimeout(() => {
            showInfo('Downloads started', 'success');
        }, 1000);
    }
    
    manageExclusions() {
        showInfo('Opening exclusions manager...', 'info');
    }
    
    destroy() {
        console.log('Cleaning up Folders page');
        
        document.removeEventListener('global-search', this.handleGlobalSearch);
        document.removeEventListener('global-search-clear', this.handleGlobalSearchClear);
        document.removeEventListener('device-configured', this.refreshDeviceStatus);
        
        // Close maximized preview if open
        this.closeMaximizedPreview();
        
        this.selectedFiles.clear();
        delete window.foldersPage;
        delete window.currentPage;
    }
}

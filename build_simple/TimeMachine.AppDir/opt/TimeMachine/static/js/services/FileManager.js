/**
 * Manages file operations and file system interactions
 */

import { FileUtils } from '../utils/FileUtils.js';
import { RestoreManager } from './RestoreManager.js';

export class FileManager {
    constructor(state, api, eventBus) {
        this.state = state;
        this.api = api;
        this.eventBus = eventBus;
        this.restoreManager = new RestoreManager(state, api, eventBus);

        this.setupEventListeners();
    }

    async initializeFileSystem() {
        try {
            await this.api.initFileSearch();

            this.state.files.fileSystem = {
                name: '.main_backup',
                type: 'folder',
                children: []
            };

            this.state.navigation.breadcrumbStack = [this.state.files.fileSystem];
            this.state.files.currentFolder = this.state.files.fileSystem;

            console.log('[FileManager] File system initialized');
        } catch (error) {
            console.error('[FileManager] Failed to initialize:', error);

            // Fallback empty file system
            this.state.files.fileSystem = {
                name: '.main_backup',
                type: 'folder',
                children: []
            };
            this.state.navigation.breadcrumbStack = [this.state.files.fileSystem];
            this.state.files.currentFolder = this.state.files.fileSystem;
        }
    }

    async loadFolderContents(folderPath = '') {
        if (!this.state.connection.isDeviceConnected) {
            this.showDisconnectedState();
            return;
        }

        try {
            const data = await this.api.getFolderContents(folderPath);

            if (data.success && data.items?.length > 0) {
                const enrichedItems = data.items.map(item => {
                    if (item.type === 'file') {
                        item.icon = FileUtils.getIconForFile(item.name);
                        item.color = FileUtils.getColorForFile(item.name);
                    } else if (item.type === 'folder') {
                        item.icon = 'bi-folder-fill';
                        item.color = 'text-blue-500';
                    }
                    return item;
                });

                this.state.files.currentFolder.children = enrichedItems;
                this.renderExplorer(enrichedItems);
            } else {
                this.renderEmptyState();
            }
        } catch (error) {
            console.error('[FileManager] Failed to load folder contents:', error);
            this.renderErrorState(error);
        }
    }

    renderExplorer(items = null) {
        const container = document.getElementById('file-list-container');
        const breadcrumb = document.getElementById('file-path-breadcrumb');

        if (!container || !breadcrumb) return;

        // Update breadcrumbs
        this.renderBreadcrumbs(breadcrumb);

        const itemsToRender = items || this.state.files.currentFolder?.children || [];
        container.innerHTML = '';

        if (itemsToRender.length === 0) {
            this.renderEmptyState();
            return;
        }

        // Sort: folders first, then files
        const sortedItems = [...itemsToRender].sort((a, b) => {
            if (a.type === 'folder' && b.type !== 'folder') return -1;
            if (a.type !== 'folder' && b.type === 'folder') return 1;
            return a.name.localeCompare(b.name);
        });

        sortedItems.forEach(item => {
            const element = this.createFileElement(item);
            container.appendChild(element);
        });
    }

    createFileElement(item) {
        const isFolder = item.type === 'folder';
        const iconClass = isFolder ? 'bi-folder-fill text-blue-400' : item.icon;
        const iconColor = isFolder ? '' : item.color;
        const displayName = item.name.length > 50
        ? item.name.substring(0, 47) + '...'
        : item.name;

        const element = document.createElement('div');
        element.className = 'flex items-center gap-3 p-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5 cursor-pointer transition-colors group';
        element.dataset.type = item.type;
        element.dataset.name = item.name;
        element.dataset.path = item.path;

        element.innerHTML = `
        <i class="bi ${iconClass} ${iconColor} text-lg flex-shrink-0"></i>
        <span class="text-sm text-main font-medium truncate flex-1" title="${item.name}">${displayName}</span>
        <i class="bi bi-chevron-right text-xs text-muted opacity-0 group-hover:opacity-100 transition-opacity"></i>
        `;

        element.addEventListener('click', () => {
            if (isFolder) {
                this.openFolder(item);
            } else {
                this.selectFile(item);
            }
        });

        return element;
    }

    openFolder(folder) {
        // Clear search
        const searchInput = document.getElementById('file-search-input');
        if (searchInput) searchInput.value = '';

        // Update state
        this.state.navigation.breadcrumbStack.push(folder);
        this.state.files.currentFolder = folder;

        // Load folder contents
        const folderPath = folder.path ? folder.path.replace(/^.*\.main_backup\/?/, '') : folder.name;
        this.loadFolderContents(folderPath);
    }

    async selectFile(file) {
        this.state.files.selectedFile = file;

        if (!this.state.connection.isDeviceConnected) {
            this.showDisconnectedPreview();
            return;
        }

        this.renderFilePreview(file);

        try {
            // Fetch file info and versions in parallel
            const [fileInfo, versions] = await Promise.all([
                this.api.getFileInfo(file.path || file.name),
                                                           this.api.getFileVersions(file.path || file.name)
            ]);

            this.updateFilePreview(file, fileInfo, versions);
        } catch (error) {
            console.error('[FileManager] Failed to load file details:', error);
            this.updateFilePreviewError(error);
        }
    }

    renderFilePreview(file) {
        const preview = document.getElementById('preview-content');
        if (!preview) return;

        preview.innerHTML = `
        <div class="animate-entry h-full flex flex-col">
        <div class="flex items-start gap-4 mb-6 border-b border-main pb-6">
        <div class="w-16 h-16 rounded-2xl bg-gray-50 dark:bg-white/5 flex items-center justify-center text-3xl border border-main shadow-sm">
        <i class="bi ${file.icon || 'bi-file-earmark-text-fill'} ${file.color || 'text-brand-500'}"></i>
        </div>
        <div class="flex-1 min-w-0">
        <h4 class="font-bold text-main text-lg truncate" title="${file.name}">${file.name}</h4>
        <div class="flex items-center gap-2 mt-1">
        <span class="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/20 text-[10px] font-bold text-secondary border border-main uppercase tracking-wider">FILE</span>
        <span id="preview-size" class="text-xs text-secondary">Loading size...</span>
        </div>
        <div class="flex items-center gap-2 mt-1">
        <span class="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/20 text-[10px] font-bold text-secondary border border-main uppercase tracking-wider">LOCATION</span>
        <span id="preview-location" class="text-xs text-secondary">Checking file location...</span>
        </div>
        <div class="flex items-center gap-2 mt-1">
        <span class="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/20 text-[10px] font-bold text-secondary border border-main uppercase tracking-wider">STATUS</span>
        <span id="preview-status" class="text-xs text-secondary">Checking file existence...</span>
        </div>
        </div>
        </div>
        <div class="grid grid-cols-2 gap-3 mb-6" id="preview-action-buttons"></div>
        <div class="flex-1 flex flex-col min-h-0">
        <div class="flex items-center justify-between mb-3">
        <p class="text-xs font-bold text-muted uppercase tracking-wider">Version History</p>
        <span class="text-[10px] text-brand-500 font-medium bg-blue-50 dark:bg-blue-900/20 px-2 py-0.5 rounded-full">Time Machine</span>
        </div>
        <div id="preview-versions-list" class="flex-1 overflow-y-auto space-y-3 pr-1 no-scrollbar pb-4">
        <div class="text-center py-8 text-muted">
        <i class="bi bi-arrow-clockwise animate-spin text-xl"></i>
        <p class="text-xs mt-2">Fetching versions...</p>
        </div>
        </div>
        </div>
        </div>
        `;
    }

    updateFilePreview(file, fileInfo, versions) {
        // Update file info section
        this.updateFileInfoSection(fileInfo);

        // Update version history
        this.updateVersionHistory(versions);

        // Update action buttons
        this.updateActionButtons(file, fileInfo);
    }

    updateFileInfoSection(fileInfo) {
        const sizeEl = document.getElementById('preview-size');
        const locationEl = document.getElementById('preview-location');
        const statusEl = document.getElementById('preview-status');

        if (!sizeEl || !locationEl || !statusEl) return;

        if (fileInfo.success) {
            sizeEl.textContent = fileInfo.size ? FileUtils.formatBytes(fileInfo.size) : 'Size unknown';

            const displayPath = this.getDisplayPath(fileInfo);
            locationEl.innerHTML = `<div class="text-xs text-secondary">${displayPath}</div>`;
            locationEl.title = displayPath;

            statusEl.textContent = this.getStatusText(fileInfo);
            statusEl.className = this.getStatusClass(fileInfo);
        } else {
            sizeEl.textContent = 'Error';
            locationEl.textContent = 'Failed to get location';
            statusEl.textContent = 'ERROR';
            statusEl.className = 'text-xs text-red-500 font-bold';
        }
    }

    getDisplayPath(fileInfo) {
        if (fileInfo.exists) {
            return fileInfo.actual_path || fileInfo.current_location || fileInfo.home_path || 'Path unknown';
        }
        return fileInfo.home_path || 'Path unknown';
    }

    getStatusText(fileInfo) {
        if (!fileInfo.exists) return 'NOT FOUND';

        const isMoved = fileInfo.is_moved ||
        (fileInfo.current_location && fileInfo.current_location !== fileInfo.home_path);

        if (isMoved) {
            const isRenamed = fileInfo.actual_path?.split('/').pop() !== fileInfo.home_path?.split('/').pop();
            return isRenamed ? 'RENAMED' : 'MOVED';
        }

        return 'FOUND';
    }

    getStatusClass(fileInfo) {
        if (!fileInfo.exists) return 'text-xs font-bold text-red-500';

        const isMoved = fileInfo.is_moved ||
        (fileInfo.current_location && fileInfo.current_location !== fileInfo.home_path);

        if (isMoved) {
            return 'text-xs font-bold text-yellow-500';
        }

        return 'text-xs font-bold text-green-500';
    }

    updateActionButtons(file, fileInfo) {
        const container = document.getElementById('preview-action-buttons');
        if (!container) return;

        let buttonsHtml = '';

        if (fileInfo.exists) {
            if (fileInfo.is_moved) {
                buttonsHtml = `
                <button disabled class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 cursor-not-allowed">
                <i class="bi bi-eye-fill"></i> Open
                </button>
                <button disabled class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 cursor-not-allowed">
                <i class="bi bi-folder-fill"></i> Open Location
                </button>
                `;
            } else {
                const actualPath = fileInfo.actual_path || fileInfo.current_location || fileInfo.home_path;
                buttonsHtml = `
                <button onclick="app.fileManager.openFile('${actualPath.replace(/'/g, "\\'")}')"
                class="btn-normal flex items-center justify-center gap-2 py-2 hover:bg-gray-100 dark:hover:bg-white/10 cursor-pointer">
                <i class="bi bi-eye-fill"></i> Open
                </button>
                <button onclick="app.fileManager.openLocation('${actualPath.replace(/'/g, "\\'")}')"
                class="btn-normal flex items-center justify-center gap-2 py-2 hover:bg-gray-100 dark:hover:bg-white/10 cursor-pointer">
                <i class="bi bi-folder-fill"></i> Open Location
                </button>
                `;
            }
        } else {
            buttonsHtml = `
            <button disabled class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 cursor-not-allowed">
            <i class="bi bi-eye-fill"></i> Open
            </button>
            <button disabled class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 cursor-not-allowed">
            <i class="bi bi-folder-fill"></i> Open Location
            </button>
            `;
        }

        container.innerHTML = buttonsHtml;
    }

    updateVersionHistory(versions) {
        const container = document.getElementById('preview-versions-list');
        if (!container) return;

        container.innerHTML = '';

        if (!versions.success || !versions.versions?.length) {
            container.innerHTML = `
            <div class="p-4 rounded-xl border border-dashed border-main text-center bg-gray-50 dark:bg-white/5">
            <p class="text-xs text-muted">No history found for this file.</p>
            </div>`;
            return;
        }

        versions.versions.forEach((version, index) => {
            const card = this.createVersionCard(version, index);
            container.appendChild(card);
        });
    }

    createVersionCard(version, index) {
        const isMain = version.key === 'main';
        const sizeStr = version.size ? FileUtils.formatBytes(version.size) : 'Unknown Size';
        const timeStr = version.time || 'Unknown Date';
        const formattedDate = FileUtils.formatRelativeDate(timeStr);

        const card = document.createElement('div');
        card.className = "bg-card border border-main rounded-xl p-3 hover:border-brand-500 transition-all duration-200 group relative";

        card.innerHTML = `
        <div class="flex justify-between items-start mb-3">
        <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg ${isMain ? 'bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-yellow-500' : 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-500'} flex items-center justify-center text-sm font-bold border border-black/5">
        ${isMain ? '<i class="bi bi-star-fill text-[10px]"></i>' : index + 1}
        </div>
        <div>
        <p class="text-xs font-bold text-main leading-tight">${formattedDate}</p>
        <p class="text-xs text-secondary">${sizeStr}</p>
        <p class="text-xs text-secondary">${version.path ? version.path.split('/').pop() : ''}</p>
        </div>
        </div>
        ${isMain ? '<span class="text-[10px] font-bold text-amber-600 bg-amber-50 dark:bg-amber-900/20 px-2 py-0.5 rounded">ORIGINAL</span>' : ''}
        </div>
        <div class="grid grid-cols-3 gap-2 mt-2 pt-2 border-t border-main">
        <button class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200"
        onclick="app.fileManager.openFile('${version.path.replace(/\\/g, '\\\\')}')">
        <i class="bi bi-eye-fill"></i> Open
        </button>
        <button class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200"
        onclick="app.fileManager.openLocation('${version.path.replace(/\\/g, '\\\\')}')">
        <i class="bi bi-folder-fill"></i> Location
        </button>
        <button class="btn-normal text-brand-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 dark:text-blue-400 cursor-pointer flex items-center justify-center gap-2 py-2"
        onclick="app.restoreManager.showRestoreOptions('${version.path.replace(/\\/g, '\\\\')}', '${version.path.split('/').pop()}')">
        <i class="bi bi-arrow-counterclockwise"></i> Restore
        </button>
        </div>
        `;

        return card;
    }

    async openFile(path) {
        try {
            await this.api.openFile(path);
        } catch (error) {
            console.warn('[FileManager] Failed to open file:', error);
        }
    }

    async openLocation(path) {
        try {
            await this.api.openLocation(path);
        } catch (error) {
            console.warn('[FileManager] Failed to open location:', error);
        }
    }

    async searchFiles(query) {
        if (!query.trim()) {
            this.renderExplorer();
            return;
        }

        try {
            const data = await this.api.searchFiles(query);

            if (data.files?.length > 0) {
                const results = data.files.map(file => ({
                    name: file.name,
                    path: file.path,
                    search_display_path: file.search_display_path,
                    type: 'file',
                    icon: FileUtils.getIconForFile(file.name),
                                                        color: FileUtils.getColorForFile(file.name)
                }));

                this.renderExplorer(results);
            } else {
                this.renderNoResults();
            }
        } catch (error) {
            console.error('[FileManager] Search failed:', error);
            this.renderSearchError(error);
        }
    }

    // Helper methods
    showDisconnectedState() {
        const container = document.getElementById('file-list-container');
        const searchInput = document.getElementById('file-search-input');

        if (searchInput) searchInput.disabled = true;

        if (container) {
            container.innerHTML = `
            <div class="p-8 text-center text-muted">
            <i class="bi bi-exclamation-triangle-fill text-3xl mb-3"></i>
            <h4 class="font-bold text-main">No Backup Device Connected</h4>
            <p class="text-sm mt-1">Please connect your backup device to browse files.</p>
            </div>`;
        }
    }

    renderEmptyState() {
        const container = document.getElementById('file-list-container');
        if (container) {
            container.innerHTML = '<div class="p-8 text-center text-muted text-sm">Folder is empty</div>';
        }
    }

    renderErrorState(error) {
        const container = document.getElementById('file-list-container');
        if (container) {
            container.innerHTML = '<p class="p-4 text-red-500">Failed to load folder contents.</p>';
        }
    }

    renderNoResults() {
        const container = document.getElementById('file-list-container');
        if (container) {
            container.innerHTML = '<p class="p-4 text-gray-400">No files found matching your search.</p>';
        }
    }

    renderSearchError(error) {
        const container = document.getElementById('file-list-container');
        if (container) {
            container.innerHTML = '<p class="p-4 text-red-500">Search failed. Please try again.</p>';
        }
    }

    showDisconnectedPreview() {
        const preview = document.getElementById('preview-content');
        if (preview) {
            preview.innerHTML = `
            <div class="p-8 text-center text-muted">
            <i class="bi bi-file-earmark-bar-graph text-3xl mb-3"></i>
            <h4 class="font-bold text-main">Device Disconnected</h4>
            <p class="text-sm mt-1">File preview unavailable until the backup device reconnects.</p>
            </div>`;
        }
    }

    updateFilePreviewError(error) {
        const statusEl = document.getElementById('preview-status');
        if (statusEl) {
            statusEl.innerText = 'NETWORK ERROR';
            statusEl.className = 'text-xs text-red-500 font-bold';
        }
    }

    renderBreadcrumbs(breadcrumbElement) {
        const breadcrumbs = this.state.navigation.breadcrumbStack.map((folder, index) => {
            const isLast = index === this.state.navigation.breadcrumbStack.length - 1;
            const folderName = folder.name || '/';
            const displayName = folderName.length > 20
            ? folderName.substring(0, 17) + '...'
            : folderName;

            return `
            <div class="flex items-center flex-shrink-0">
            <span class="${isLast ? 'font-bold text-main' : 'text-brand-500 hover:underline cursor-pointer'}"
            title="${folderName}"
            ${!isLast ? `onclick="app.fileManager.navigateToBreadcrumb(${index})"` : ''}>
            ${displayName}
            </span>
            ${!isLast ? '<i class="bi bi-chevron-right text-[10px] mx-2 text-muted"></i>' : ''}
            </div>
            `;
        }).join('');

        breadcrumbElement.innerHTML = breadcrumbs;
    }

    navigateToBreadcrumb(index) {
        this.state.navigation.breadcrumbStack = this.state.navigation.breadcrumbStack.slice(0, index + 1);
        this.state.files.currentFolder = this.state.navigation.breadcrumbStack[index];

        const folderPath = this.state.files.currentFolder.path
        ? this.state.files.currentFolder.path.replace(/^.*\.main_backup\/?/, '')
        : this.state.files.currentFolder.name;

        this.loadFolderContents(folderPath);
    }

    resetExplorer() {
        const searchInput = document.getElementById('file-search-input');
        if (searchInput) searchInput.value = '';

        this.state.navigation.breadcrumbStack = [this.state.files.fileSystem];
        this.state.files.currentFolder = this.state.files.fileSystem;

        this.renderExplorer();
    }

    setupEventListeners() {
        // File search
        const searchInput = document.getElementById('file-search-input');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.searchFiles(e.target.value);
                }, 300);
            });

            searchInput.addEventListener('keyup', (e) => {
                if (e.key === 'Enter') {
                    this.searchFiles(e.target.value);
                }
            });
        }

        // File list container clicks
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-type="folder"]')) {
                const element = e.target.closest('[data-type="folder"]');
                const folder = {
                    name: element.dataset.name,
                    path: element.dataset.path,
                    type: 'folder'
                };
                this.openFolder(folder);
            }

            if (e.target.closest('[data-type="file"]')) {
                const element = e.target.closest('[data-type="file"]');
                const file = {
                    name: element.dataset.name,
                    path: element.dataset.path,
                    type: 'file',
                    icon: FileUtils.getIconForFile(element.dataset.name),
                                  color: FileUtils.getColorForFile(element.dataset.name)
                };
                this.selectFile(file);
            }
        });
    }

    handleRestoreRequest(data) {
        this.restoreManager.handleRestoreRequest(data);
    }
}

// js/components/restore-window.js

export default class VersionsWindow {
    constructor() {
        this.isOpen = false;
        this.currentFile = null;
        this.selectedSnapshot = null;
        this.snapshots = [];
        this.viewMode = 'diff';
        this.isLoading = false;
        this.isLoadingPreview = false;
        this.abortController = null;
        this.activeJobId = null;
    }

    async open(filePath, fileType, fileName) {
        console.log('Opening get versions window for:', fileName);

        this.currentFile = {
            path: filePath,
            type: fileType,
            name: fileName
        };

        this.isOpen = true;
        this.render();
        
        // Load snapshots for this file
        await this.loadSnapshots();
    }

    close() {
        const modal = document.getElementById('versions-modal');
        if (modal) {
            modal.remove();
        }
        this.isOpen = false;
        this.currentFile = null;
        this.selectedSnapshot = null;
        this.snapshots = [];
        this.isLoading = false;
        this.isLoadingPreview = false;
        this.activeJobId = null;
        
        // Restore body overflow
        document.body.style.overflow = '';
    }

    render() {
        // Remove existing modal
        const existing = document.getElementById('versions-modal');
        if (existing) existing.remove();

        // Create modal
        const modal = document.createElement('div');
        modal.id = 'versions-modal';
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 modal-backdrop';
        modal.innerHTML = this.getModalHTML();
        
        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';
        
        // Add event listeners
        this.addEventListeners();
    }

    getModalHTML() {
        return `
        <div class="relative isolation-isolate opacity-100 bg-[var(--color-system-background)] dark:bg-[var(--color-surface-dark)] rounded-lg shadow-xl w-full max-w-6xl max-h-[90vh] overflow-hidden flex flex-col">
            <!-- Header -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)]">
                <div>
                    <h2 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white">Get Versions</h2>
                    <p class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">${this.currentFile.name}</p>
                </div>
                <button class="text-[var(--color-text-secondary)] hover:text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] dark:hover:text-[var(--color-text-secondary)] p-1 rounded hover:bg-[var(--color-gray-100)] dark:hover:bg-[var(--color-gray-700)]" onclick="window.versionsWindow.close()">
                    <span class="material-icons-round">close</span>
                </button>
            </div>
            
            <!-- Content -->
            <div class="flex flex-1 overflow-hidden">
                <!-- Left sidebar - Snapshots -->
                <div class="w-80 border-r border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] overflow-y-auto">
                    <div class="p-4">
                        <h3 class="text-sm font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mb-4">Available Versions (${this.snapshots.length})</h3>
                        
                        ${this.isLoading ? this.renderLoadingSnapshots() : this.renderSnapshots()}
                    </div>
                </div>
                
                <!-- Right panel - Preview -->
                <div class="flex-1 flex flex-col">
                    <!-- Preview header -->
                    <div class="px-4 py-3 border-b border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <span class="material-icons-round text-[var(--color-text-secondary)]">preview</span>
                            <span class="font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Preview</span>
                        </div>
                        ${this.canShowTextPreview() ? `
                        <div class="flex space-x-1 bg-[var(--color-gray-100)] dark:bg-[var(--color-gray-700)] rounded-lg p-1">
                            <button class="px-3 py-1 text-sm rounded ${this.viewMode === 'source' ? 'bg-[var(--color-system-background)] dark:bg-[var(--color-gray-600)] text-[var(--color-accent)] dark:text-[var(--color-accent)] shadow-sm' : 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] hover:text-[var(--color-text-secondary)] dark:hover:text-[var(--color-text-secondary)]'}" data-mode="source">Source</button>
                            <button class="px-3 py-1 text-sm rounded ${this.viewMode === 'diff' ? 'bg-[var(--color-system-background)] dark:bg-[var(--color-gray-600)] text-[var(--color-accent)] dark:text-[var(--color-accent)] shadow-sm' : 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] hover:text-[var(--color-text-secondary)] dark:hover:text-[var(--color-text-secondary)]'}" data-mode="diff">Diff</button>
                        </div>
                        ` : ''}
                    </div>
                    
                    <!-- Preview content -->
                    <div class="flex-1 overflow-auto p-4" id="versions-preview-content">
                        ${this.renderPreview()}
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="px-6 py-4 border-t border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)]">
                <div class="flex justify-between items-center">
                    <div class="flex space-x-3">
                        <button class="px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] bg-[var(--color-system-background)] dark:bg-[var(--color-gray-700)] border border-[var(--color-gray-300)] dark:border-[var(--color-gray-600)] rounded-lg hover:bg-[var(--color-gray-50)] dark:hover:bg-[var(--color-gray-600)] flex items-center" onclick="window.versionsWindow.openBackedUpFile()">
                            <span class="material-icons-round text-sm mr-2">open_in_new</span>
                            Open
                        </button>
                        <button class="px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] bg-[var(--color-system-background)] dark:bg-[var(--color-gray-700)] border border-[var(--color-gray-300)] dark:border-[var(--color-gray-600)] rounded-lg hover:bg-[var(--color-gray-50)] dark:hover:bg-[var(--color-gray-600)] flex items-center" onclick="window.versionsWindow.openBackedUpFileLocation()">
                            <span class="material-icons-round text-sm mr-2">folder_open</span>
                            Open Location
                        </button>
                        <button class="px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] bg-[var(--color-system-background)] dark:bg-[var(--color-gray-700)] border border-[var(--color-gray-300)] dark:border-[var(--color-gray-600)] rounded-lg hover:bg-[var(--color-gray-50)] dark:hover:bg-[var(--color-gray-600)] flex items-center" onclick="window.versionsWindow.downloadBackedUpFile()">
                            <span class="material-icons-round text-sm mr-2">download</span>
                            Download
                        </button>
                    </div>
                    <div class="flex justify-end space-x-3">
                        <button class="px-4 py-2 text-sm font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] bg-[var(--color-system-background)] dark:bg-[var(--color-gray-700)] border border-[var(--color-gray-300)] dark:border-[var(--color-gray-600)] rounded-lg hover:bg-[var(--color-gray-50)] dark:hover:bg-[var(--color-gray-600)]" onclick="window.versionsWindow.close()">
                            Cancel
                        </button>
                        <button class="px-4 py-2 text-sm font-medium text-white bg-[var(--color-accent)] rounded-lg hover:bg-[var(--color-accent-hover)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center" 
                                id="get-version-button"
                                ${!this.selectedSnapshot ? 'disabled' : ''}>
                            <span class="material-icons-round text-sm mr-2">history</span>
                            Get Version
                        </button>
                    </div>
                </div>
            </div>
        </div>
        `;
    }

    renderLoadingSnapshots() {
        return `
        <div class="space-y-3">
            ${[1, 2, 3].map(() => `
            <div class="p-3 border border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] rounded-lg">
                <div class="h-4 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-24 mb-2 animate-pulse"></div>
                <div class="h-3 bg-[var(--color-gray-200)] dark:bg-[var(--color-gray-700)] rounded w-16 animate-pulse"></div>
            </div>
            `).join('')}
        </div>
        `;
    }

    renderSnapshots() {
        if (this.snapshots.length === 0) {
            return `
            <div class="text-center py-8">
                <span class="material-icons-round text-[var(--color-text-secondary)] text-4xl mb-3">history</span>
                <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">No backup versions found</p>
                <p class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mt-1">This file or folder hasn't been backed up yet</p>
            </div>
            `;
        }

        return `
        <div class="space-y-2">
            ${this.snapshots.map((snapshot, index) => {
                const isSelected = this.selectedSnapshot === snapshot.id;
                const isMainBackup = snapshot.is_main_backup || snapshot.type === 'main';
                const isLatest = index === 0 && !isMainBackup;
                const sizeOrCount = snapshot.size !== undefined 
                    ? snapshot.size 
                    : (snapshot.file_count !== undefined ? `${snapshot.file_count} files` : '');

                return `
                <div class="p-3 border rounded-lg cursor-pointer transition-colors ${isSelected ? 'border-[var(--color-accent)] bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)]' : 'border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] hover:bg-[var(--color-surface-light)] dark:hover:bg-[var(--color-surface-dark)]'}"
                     onclick="window.versionsWindow.selectSnapshot('${snapshot.id}')">
                    <div class="flex justify-between items-start mb-1">
                        <div class="flex items-center">
                            <span class="font-medium ${isSelected ? 'text-[var(--color-accent)] dark:text-[var(--color-accent)]' : 'text-[var(--color-text-primary)] dark:text-white'}">${snapshot.time}</span>
                            ${isMainBackup ? '<span class="ml-2 text-xs px-2 py-0.5 bg-[var(--color-gray-100)] text-purple-800 dark:bg-purple-900 dark:text-purple-300 rounded font-medium">Primary</span>' : ''}
                            ${isLatest ? '<span class="ml-2 text-xs px-2 py-0.5 bg-[var(--color-status-success-bg)] text-[var(--color-status-success)] dark:bg-[var(--color-status-success-bg-dark)] dark:text-[var(--color-status-success-dark)] rounded font-medium">Latest</span>' : ''}
                        </div>
                        <span class="text-xs ${isSelected ? 'text-[var(--color-accent)] dark:text-[var(--color-accent)]' : 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]'}">${sizeOrCount}</span>
                    </div>
                    <div class="text-sm ${isSelected ? 'text-[var(--color-accent)] dark:text-[var(--color-accent)]' : 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]'}">
                        ${snapshot.date} • ${snapshot.type}
                    </div>
                </div>
                `;
            }).join('')}
        </div>
        `;
    }

    renderPreview() {
        if (!this.selectedSnapshot) {
            return `
            <div class="flex items-center justify-center h-full">
                <div class="text-center">
                    <span class="material-icons-round text-[var(--color-text-secondary)] text-4xl mb-3">select_all</span>
                    <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Select a version to preview</p>
                </div>
            </div>
            `;
        }

        if (this.isLoadingPreview) {
            return `
            <div class="flex items-center justify-center h-full">
                <div class="text-center">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
                    <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Loading preview...</p>
                </div>
            </div>
            `;
        }

        const snapshot = this.snapshots.find(s => s.id === this.selectedSnapshot);
        const isTextFile = this.canShowTextPreview();

        if (!isTextFile) {
            const isFolder = this.currentFile.type === 'folder';
            const icon = isFolder ? 'folder' : 'insert_drive_file';
            
            return `
            <div class="flex flex-col items-center justify-center h-full p-8">
                <div class="w-16 h-16 bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)] rounded-lg flex items-center justify-center mb-4">
                    <span class="material-icons-round text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] text-3xl">${icon}</span>
                </div>
                <h3 class="text-lg font-medium text-[var(--color-text-primary)] dark:text-white mb-2">${this.currentFile.name}</h3>
                <p class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mb-6">Preview not available for this file type</p>
                <div class="bg-[var(--color-surface-light)] dark:bg-[var(--color-surface-dark)] rounded-lg p-4 w-full max-w-md">
                    <div class="space-y-2">
                        <div class="flex justify-between">
                            <span class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Version:</span>
                            <span class="text-sm font-medium text-[var(--color-text-primary)] dark:text-white">${snapshot.date} ${snapshot.time}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Size:</span>
                            <span class="text-sm font-medium text-[var(--color-text-primary)] dark:text-white">${snapshot.size}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Backup Type:</span>
                            <span class="text-sm font-medium text-[var(--color-text-primary)] dark:text-white">${snapshot.type}</span>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        return `
        <div class="h-full">
            <div class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mb-3">
                Select a view mode above to preview
            </div>
        </div>
        `;
    }

    async loadSnapshots() {
        this.isLoading = true;
        this.updateUI();

        try {
            const endpoint = `/api/backup/snapshots?file_path=${encodeURIComponent(this.currentFile.path)}`;

            const response = await fetch(endpoint);
            const data = await response.json();

            if (data.success) {
                // Sort snapshots: latest first, initial backup last.
                data.snapshots.sort((a, b) => {
                    const isAMain = a.is_main_backup || a.type === 'main';
                    const isBMain = b.is_main_backup || b.type === 'main';

                    if (isAMain) return 1;
                    if (isBMain) return -1;
                    
                    const a_ts = typeof a.timestamp === 'string' ? new Date(a.timestamp).getTime() : a.timestamp * 1000;
                    const b_ts = typeof b.timestamp === 'string' ? new Date(b.timestamp).getTime() : b.timestamp * 1000;

                    return b_ts - a_ts;
                });
                this.snapshots = data.snapshots;
            } else {
                console.error('API Error:', data.error);
                this.snapshots = [];
            }
        } catch (error) {
            console.error('Network Error:', error);
            this.snapshots = []; // Reset on error
        } finally {
            this.isLoading = false;
            this.updateUI();
        }
    }

    async loadPreview() {
        const previewContainer = document.getElementById('versions-preview-content');
        if (!previewContainer || !this.selectedSnapshot || !this.canShowTextPreview()) return;
        
        this.isLoadingPreview = true;
        this.updateUI();
        
        try {
            if (this.viewMode === 'source') {
                await this.loadSourcePreview();
            } else {
                await this.loadDiffPreview();
            }
        } catch (error) {
            console.error('Error loading preview:', error);
            previewContainer.innerHTML = `
            <div class="flex items-center justify-center h-full">
                <div class="text-center">
                    <span class="material-icons-round text-[var(--color-status-error)] text-4xl mb-3">error</span>
                    <p class="text-[var(--color-status-error)] dark:text-[var(--color-status-error)]">Failed to load preview</p>
                    <p class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mt-2">${error.message || 'Unknown error'}</p>
                </div>
            </div>
            `;
        } finally {
            this.isLoadingPreview = false;
        }
    }

    async loadSourcePreview() {
        const previewContainer = document.getElementById('versions-preview-content');
        if (!previewContainer) return;
        
        try {
            const response = await fetch(`/api/backup/file-content?file_path=${encodeURIComponent(this.currentFile.path)}&snapshot_id=${encodeURIComponent(this.selectedSnapshot)}`);
            const data = await response.json();
            
            if (data.success) {
                const snapshot = this.snapshots.find(s => s.id === this.selectedSnapshot);
                let headerText = '';
                
                if (snapshot.is_main_backup) {
                    headerText = `Primary Backup - ${snapshot.date} ${snapshot.time}`;
                } else {
                    const dateParts = snapshot.id.split('/');
                    headerText = `${dateParts[0]} ${dateParts[1].replace('-', ':')}`;
                }
                
                previewContainer.innerHTML = `
                <div class="bg-[var(--color-gray-900)] text-gray-100 rounded-lg overflow-hidden h-full flex flex-col">
                    <div class="px-4 py-2 bg-[var(--color-gray-800)] border-b border-[var(--color-gray-700)]">
                        <div class="text-xs text-[var(--color-text-secondary)]">${headerText}</div>
                    </div>
                    <div class="flex-1 overflow-auto p-4 font-mono text-sm">
                        <pre class="whitespace-pre-wrap">${this.escapeHtml(data.content)}</pre>
                    </div>
                </div>
                `;
            } else {
                throw new Error(data.error || 'Failed to load content');
            }
        } catch (error) {
            throw error;
        }
    }

    async loadDiffPreview() {
        const previewContainer = document.getElementById('versions-preview-content');
        if (!previewContainer) return;
        
        try {
            const response = await fetch(`/api/backup/file-diff?file_path=${encodeURIComponent(this.currentFile.path)}&snapshot_id=${encodeURIComponent(this.selectedSnapshot)}`);
            const data = await response.json();
            
            if (data.success) {
                const snapshot = this.snapshots.find(s => s.id === this.selectedSnapshot);
                
                if (!data.diff || data.diff.length === 0) {
                    previewContainer.innerHTML = `
                    <div class="flex items-center justify-center h-full">
                        <div class="text-center">
                            <span class="material-icons-round text-green-400 text-4xl mb-3">check_circle</span>
                            <p class="text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)] font-medium">No differences found</p>
                            <p class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mt-2">The snapshot is identical to the current version</p>
                        </div>
                    </div>
                    `;
                    return;
                }
                
                let headerText = '';
                if (snapshot.is_main_backup) {
                    headerText = `Original Backup - ${snapshot.date} ${snapshot.time}`;
                } else {
                    const dateParts = snapshot.id.split('/');
                    headerText = `${dateParts[0]} ${dateParts[1].replace('-', ':')}`;
                }
                
                const diffHtml = data.diff.map((line, index) => {
                    let bgClass = '';
                    let textClass = '';
                    let prefix = '';
                    
                    if (line.type === 'added') {
                        bgClass = 'bg-[var(--color-status-success-bg)] dark:bg-[var(--color-status-success-bg-dark)]';
                        textClass = 'text-[var(--color-status-success)] dark:text-green-200';
                        prefix = '<span class="text-[var(--color-status-success)] dark:text-[var(--color-status-success-dark)] mr-2">+</span>';
                    } else if (line.type === 'removed') {
                        bgClass = 'bg-[var(--color-status-error-bg)] dark:bg-[var(--color-status-error-bg-dark)]';
                        textClass = 'text-[var(--color-status-error-dark)] dark:text-[var(--color-status-error-dark)] line-through opacity-70';
                        prefix = '<span class="text-[var(--color-status-error)] dark:text-[var(--color-status-error)] mr-2">-</span>';
                    } else {
                        textClass = 'text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]';
                        prefix = '<span class="text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mr-2">&nbsp;</span>';
                    }
                    
                    return `
                    <div class="py-1 px-3 ${bgClass}">
                        <div class="flex">
                            ${prefix}
                            <span class="${textClass} font-mono text-sm whitespace-pre-wrap">${this.escapeHtml(line.content)}</span>
                        </div>
                    </div>
                    `;
                }).join('');
                
                previewContainer.innerHTML = `
                <div class="bg-[var(--color-system-background)] dark:bg-[var(--color-gray-900)] rounded-lg overflow-hidden h-full flex flex-col">
                    <div class="px-4 py-3 bg-[var(--color-gray-50)] dark:bg-[var(--color-gray-800)] border-b border-[var(--color-gray-200)] dark:border-[var(--color-gray-700)] flex items-center justify-between">
                        <div class="text-sm text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">
                            Comparing <span class="font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">${headerText}</span> with current
                        </div>
                        <div class="flex items-center space-x-4 text-xs">
                            <div class="flex items-center space-x-1">
                                <span class="w-2 h-2 bg-[var(--color-status-error-bg)] rounded-full"></span>
                                <span class="text-[var(--color-text-secondary)]">Removed</span>
                            </div>
                            <div class="flex items-center space-x-1">
                                <span class="w-2 h-2 bg-[var(--color-status-success)] rounded-full"></span>
                                <span class="text-[var(--color-text-secondary)]">Added</span>
                            </div>
                        </div>
                    </div>
                    <div class="flex-1 overflow-auto">
                        ${diffHtml}
                    </div>
                </div>
                `;
            } else {
                throw new Error(data.error || 'Failed to load diff');
            }
        } catch (error) {
            throw error;
        }
    }

    // Helper methods
    canShowTextPreview() {
        if (!this.currentFile) return false;
        const ext = this.currentFile.name.split('.').pop().toLowerCase();
        const textExts = [
            'adoc', 'bash', 'bat', 'c', 'cfg', 'conf', 'cpp', 'csv', 'css',
            'diff', 'dockerfile', 'env', 'gd', 'go', 'h', 'html', 'ini',
            'java', 'js', 'json', 'jsx', 'kt', 'kts', 'less', 'log', 'lua',
            'md', 'patch', 'php', 'pl', 'properties', 'ps1', 'py', 'rb',
            'rs', 'rst', 'sass', 'scala', 'scss', 'sh', 'sql', 'svelte',
            'swift', 'tex', 'toml', 'ts', 'tsx', 'txt', 'vb', 'vue', 'xml',
            'yaml', 'yml', 'zsh'
        ];
        return textExts.includes(ext);
    }

    selectSnapshot(snapshotId) {
        this.selectedSnapshot = snapshotId;
        this.updateUI();
        this.loadPreview();
    }

    updateUI() {
        const modal = document.getElementById('versions-modal');
        if (!modal) return;
        
        // Update snapshots panel
        const leftPanel = modal.querySelector('.w-80');
        if (leftPanel) {
            const contentDiv = leftPanel.querySelector('.p-4');
            if (contentDiv) {
                contentDiv.innerHTML = `
                    <h3 class="text-sm font-medium text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] mb-4">Available Versions (${this.snapshots.length})</h3>
                    ${this.isLoading ? this.renderLoadingSnapshots() : this.renderSnapshots()}
                `;
            }
        }
        
        // Update preview
        const previewContainer = document.getElementById('versions-preview-content');
        if (previewContainer) {
            previewContainer.innerHTML = this.renderPreview();
        }
        
        // Update restore button
        const getVersionsBtn = document.getElementById('get-version-button');
        if (getVersionsBtn) {
            getVersionsBtn.disabled = !this.selectedSnapshot;
            if (!this.selectedSnapshot) {
                getVersionsBtn.classList.add('disabled:opacity-50', 'disabled:cursor-not-allowed');
            } else {
                getVersionsBtn.classList.remove('disabled:opacity-50', 'disabled:cursor-not-allowed');
            }
        }
    }

    addEventListeners() {
        // Make window accessible globally
        window.versionsWindow = this;
        
        const modal = document.getElementById('versions-modal');
        if (!modal) return;
        
        // View mode buttons
        modal.querySelectorAll('[data-mode]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.viewMode = e.target.getAttribute('data-mode');
                
                // Update button styles
                modal.querySelectorAll('[data-mode]').forEach(b => {
                    if (b.getAttribute('data-mode') === this.viewMode) {
                        b.className = `px-3 py-1 text-sm rounded bg-[var(--color-system-background)] dark:bg-[var(--color-gray-600)] text-[var(--color-accent)] dark:text-[var(--color-accent)] shadow-sm`;
                    } else {
                        b.className = `px-3 py-1 text-sm rounded text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] hover:text-[var(--color-text-secondary)] dark:hover:text-[var(--color-text-secondary)]`;
                    }
                });
                
                // Reload preview
                this.loadPreview();
            });
        });
        
        // Restore button
        const getVersionsBtn = document.getElementById('get-version-button');
        if (getVersionsBtn) {
            getVersionsBtn.addEventListener('click', () => this.getVersion());
        }
        
        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.close();
            }
        });
    }

    async getVersion() {
        if (!this.selectedSnapshot) {
            this.showNotification('Please select a version to get', 'warning');
            return;
        }
        
        const snapshot = this.snapshots.find(s => s.id === this.selectedSnapshot);
        const versionType = snapshot.is_main_backup ? 'Original Backup' : 'Snapshot';
        const isFolder = this.currentFile.type === 'folder';
        
        // Customize confirmation message based on file type
        const confirmMessage = isFolder 
            ? `This will restore all files and folders inside "${this.currentFile.name}" to match the selected snapshot from ${snapshot.date} ${snapshot.time}. Files will be restored to a new folder in your home directory.`
            : `This will replace the current version of "${this.currentFile.name}" with the selected version from ${snapshot.date} ${snapshot.time}.`;
        
        const confirmGetVersion = await showConfirm(
            'Confirm Get Version',
            confirmMessage,
            {
                confirmText: 'Get Version',
                cancelText: 'Cancel',
                confirmType: 'primary'
            }
        );

        if (!confirmGetVersion) return;
        
        this.abortController = new AbortController();
        this.showProgress('Starting get version...', () => this.abortOperation());
        
        try {
            // Determine endpoint and data format based on file type
            let endpoint, requestData;
            
            if (isFolder) {
                // For folders, use the /api/restore-folder endpoint
                // Convert snapshot_id from "DD-MM-YYYY/HH-MM" to "DD-MM-YYYY|HH-MM"
                const snapshotIdForFolder = this.selectedSnapshot === '.main_backup' 
                    ? 'main'
                    : this.selectedSnapshot.replace('/', '|');
                
                endpoint = '/api/restore-folder';
                requestData = {
                    folder_path: this.currentFile.path,
                    snapshot_id: snapshotIdForFolder
                };
            } else {
                // For files, use the /api/backup/restore endpoint
                endpoint = '/api/backup/restore';
                requestData = {
                    file_path: this.currentFile.path,
                    snapshot_id: this.selectedSnapshot,
                    restore_to: 'original'
                };
            }
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            const data = await response.json();
            if (data.success && data.job_id) {
                this.activeJobId = data.job_id;
                const actionName = isFolder ? 'Restoring Folder' : 'Getting Version';
                await this.pollJob(data.job_id, actionName);
            } else {
                this.showNotification(`Failed to get version: ${data.error}`, 'error');
                this.hideProgress();
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                this.showNotification('Get version cancelled', 'info');
            } else {
                console.error('Get version error:', error);
                this.showNotification('Failed to get version. Please try again.', 'error');
            }
            this.hideProgress();
        }
    }


    async downloadBackedUpFile() {
        if (!this.selectedSnapshot) {
            this.showNotification('Please select a version to download.', 'warning');
            return;
        }

        this.abortController = new AbortController();
        this.showProgress(`Starting download...`, () => this.abortOperation());
        
        try {
            const response = await fetch('/api/backup/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    file_path: this.currentFile.path,
                    snapshot_id: this.selectedSnapshot
                })
            });
            
            const data = await response.json();
            if (data.success && data.job_id) {
                this.activeJobId = data.job_id;
                await this.pollJob(data.job_id, 'Downloading');
            } else {
                this.showNotification(`Failed to download: ${data.error}`, 'error');
                this.hideProgress();
            }
        } catch (error) {
            console.error('Download error:', error);
            this.showNotification('Failed to download file.', 'error');
            this.hideProgress();
        }
    }

    async pollJob(jobId, actionName) {
        const pollInterval = 500; // 0.5s
        
        const checkStatus = async () => {
            if (this.abortController && this.abortController.signal.aborted) return;

            try {
                const response = await fetch(`/api/task/status/${jobId}`);
                const data = await response.json();
                
                if (!data.success || !data.job) {
                    throw new Error('Failed to get job status');
                }
                
                const job = data.job;
                
                if (job.status === 'completed') {
                    this.updateProgress(100, 'Completed');
                    setTimeout(() => {
                        this.hideProgress();
                        if (job.result && job.result.checksum_verified) {
                            this.showNotification(`${actionName} completed and verified successfully!`, 'success');
                        } else {
                            this.showNotification(`${actionName} completed successfully!`, 'success');
                        }
                        
                        if (actionName === 'Getting Version') {
                            this.close();
                            if (window.foldersPage && window.foldersPage.loadFolderContents) {
                                window.foldersPage.loadFolderContents();
                            }
                            // Open location if available
                            if (job.result && job.result.restored_to) {
                                fetch('/api/open-location', {
                                    method: 'POST',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ file_path: job.result.restored_to })
                                });
                            }
                        }
                    }, 500);
                } else if (job.status === 'error' || job.status === 'aborted') {
                    this.hideProgress();
                    this.showNotification(`${actionName} failed: ${job.error || 'Unknown error'}`, 'error');
                } else {
                    // Update progress
                    let statusText = `${actionName}...`;
                    if (job.status === 'verifying') statusText = 'Verifying checksum...';
                    else if (job.status === 'preparing') statusText = 'Preparing...';
                    
                    // Format speed
                    let speedText = '';
                    if (job.speed && job.speed > 0) {
                        const mb = job.speed / (1024 * 1024);
                        speedText = `${mb.toFixed(1)} MB/s`;
                    }
                    
                    // Format ETA
                    let etaText = '';
                    if (job.eta && job.eta > 0) {
                        const s = Math.round(job.eta);
                        if (s < 60) etaText = `${s}s remaining`;
                        else if (s < 3600) etaText = `${Math.floor(s/60)}m ${s%60}s remaining`;
                        else etaText = `${Math.floor(s/3600)}h ${Math.floor((s%3600)/60)}m remaining`;
                    }
                    
                    this.updateProgress(job.percentage, statusText, speedText, etaText);
                    
                    // Poll again
                    setTimeout(checkStatus, pollInterval);
                }
            } catch (error) {
                console.error('Polling error:', error);
                // Don't stop polling on transient network errors immediately, but maybe implement a retry limit
                setTimeout(checkStatus, pollInterval);
            }
        };
        
        checkStatus();
    }

    abortOperation() {
        if (this.abortController) {
            this.abortController.abort();
        }
        if (this.activeJobId) {
            fetch(`/api/task/abort/${this.activeJobId}`, { method: 'POST' });
        }
    }

    async openBackedUpFile() {
        if (!this.selectedSnapshot) {
            this.showNotification('Please select a version to open.', 'warning');
            return;
        }

        const snapshot = this.snapshots.find(s => s.id === this.selectedSnapshot);
        if (!snapshot || !snapshot.full_path) {
            this.showNotification('Could not find the file path for the selected version.', 'error');
            return;
        }

        try {
            const response = await fetch('/api/open-file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_path: snapshot.full_path })
            });
            const data = await response.json();
            if (data.success) {
                this.showNotification('Attempting to open file from backup...', 'info');
            } else {
                this.showNotification(`Failed to open file: ${data.error}`, 'error');
            }
        } catch (error) {
            console.error('Open file error:', error);
            this.showNotification('An error occurred while trying to open the file.', 'error');
        }
    }

    async openBackedUpFileLocation() {
        if (!this.selectedSnapshot) {
            this.showNotification('Please select a version to open its location.', 'warning');
            return;
        }

        const snapshot = this.snapshots.find(s => s.id === this.selectedSnapshot);
        if (!snapshot || !snapshot.full_path) {
            this.showNotification('Could not find the file path for the selected version.', 'error');
            return;
        }

        try {
            const response = await fetch('/api/open-location', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ file_path: snapshot.full_path })
            });
            const data = await response.json();
            if (data.success) {
                this.showNotification('Attempting to open file location from backup...', 'info');
            } else {
                this.showNotification(`Failed to open location: ${data.error}`, 'error');
            }
        } catch (error) {
            console.error('Open location error:', error);
            this.showNotification('An error occurred while trying to open the file location.', 'error');
        }
    }

    showProgress(message, onCancel = null) {
        const modalContent = document.querySelector('#versions-modal > div');
        if (!modalContent) return;

        this.hideProgress();

        let cancelButtonHtml = '';
        if (onCancel) {
            cancelButtonHtml = `
                <button id="abort-operation-btn" class="mt-4 px-4 py-2 text-sm font-medium text-[var(--color-status-error)] bg-[var(--color-status-error-bg)] hover:bg-[var(--color-status-error-bg)] dark:bg-[var(--color-status-error-bg-dark)] dark:text-[var(--color-status-error)] dark:hover:bg-[var(--color-status-error-dark)]/30 rounded-lg transition-colors flex items-center">
                    <span class="material-icons-round text-sm mr-2">cancel</span>
                    Cancel
                </button>
            `;
        }

        const overlay = document.createElement('div');
        overlay.id = 'versions-progress-overlay';
        overlay.className = 'absolute inset-0 z-50 flex items-center justify-center bg-[var(--color-overlay)] rounded-lg transition-opacity duration-200';
        
        overlay.innerHTML = `
            <div class="flex flex-col items-center max-w-sm w-full px-8 py-6">
                <div class="w-16 h-16 mb-4 rounded-full bg-[var(--color-gray-50)] dark:bg-[var(--color-accent-light)]/30 flex items-center justify-center">
                    <div class="w-8 h-8 border-4 border-[var(--color-accent)] border-t-transparent rounded-full animate-spin"></div>
                </div>
                <h3 class="text-lg font-semibold text-[var(--color-text-primary)] dark:text-white mb-2">${message}</h3>
                
                <div class="w-full bg-[var(--color-gray-200)] rounded-full h-1.5 dark:bg-[var(--color-gray-700)] mt-2 mb-1 overflow-hidden">
                    <div id="versions-progress-bar" class="bg-[var(--color-accent)] h-1.5 rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
                <div class="flex justify-between w-full px-1 mb-2">
                    <p id="versions-progress-text" class="text-xs text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)]">Please wait...</p>
                    <p id="versions-progress-speed" class="text-xs text-[var(--color-text-secondary)] dark:text-[var(--color-text-secondary)] font-mono"></p>
                </div>
                ${cancelButtonHtml}
            </div>
        `;
        
        modalContent.appendChild(overlay);

        if (onCancel) {
            document.getElementById('abort-operation-btn').addEventListener('click', onCancel);
        }
    }

    updateProgress(percentage, statusText = null, speedText = null, etaText = null) {
        const bar = document.getElementById('versions-progress-bar');
        const text = document.getElementById('versions-progress-text');
        const speed = document.getElementById('versions-progress-speed');
        
        if (bar) {
            bar.style.width = `${Math.max(0, Math.min(100, percentage))}%`;
        }
        
        if (text) {
            if (statusText) {
                text.textContent = statusText;
            } else {
                text.textContent = `${Math.round(percentage)}%`;
            }
        }

        if (speed) {
            let content = speedText || '';
            if (etaText) {
                content = content ? `${content} • ${etaText}` : etaText;
            }
            speed.textContent = content;
        }
    }

    hideProgress() {
        const overlay = document.getElementById('versions-progress-overlay');
        if (overlay) overlay.remove();
    }

    showNotification(message, type = 'info') {
        // Use existing notification system or create a simple one
        if (window.showInfo) {
            window.showInfo(message, type);
        } else {
            // Fallback alert
            alert(`${type.toUpperCase()}: ${message}`);
        }
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Make available globally
if (typeof window !== 'undefined') {
    window.VersionsWindow = VersionsWindow;
}
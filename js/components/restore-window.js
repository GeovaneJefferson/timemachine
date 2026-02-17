// js/components/restore-window.js

export default class RestoreWindow {
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
        console.log('Opening restore window for:', fileName);

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
        const modal = document.getElementById('restore-modal');
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
        const existing = document.getElementById('restore-modal');
        if (existing) existing.remove();

        // Create modal
        const modal = document.createElement('div');
        modal.id = 'restore-modal';
        modal.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50';
        modal.innerHTML = this.getModalHTML();
        
        document.body.appendChild(modal);
        document.body.style.overflow = 'hidden';
        
        // Add event listeners
        this.addEventListeners();
    }

    getModalHTML() {
        return `
        <div class="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-6xl max-h-[90vh] overflow-hidden flex flex-col">
            <!-- Header -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
                <div>
                    <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Restore File</h2>
                    <p class="text-sm text-gray-600 dark:text-gray-400">${this.currentFile.name}</p>
                </div>
                <button class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300 p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700" onclick="window.restoreWindow.close()">
                    <span class="material-icons-round">close</span>
                </button>
            </div>
            
            <!-- Content -->
            <div class="flex flex-1 overflow-hidden">
                <!-- Left sidebar - Snapshots -->
                <div class="w-80 border-r border-gray-200 dark:border-gray-700 overflow-y-auto">
                    <div class="p-4">
                        <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">Available Versions (${this.snapshots.length})</h3>
                        
                        ${this.isLoading ? this.renderLoadingSnapshots() : this.renderSnapshots()}
                    </div>
                </div>
                
                <!-- Right panel - Preview -->
                <div class="flex-1 flex flex-col">
                    <!-- Preview header -->
                    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <span class="material-icons-round text-gray-500">preview</span>
                            <span class="font-medium text-gray-700 dark:text-gray-300">Preview</span>
                        </div>
                        ${this.canShowTextPreview() ? `
                        <div class="flex space-x-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
                            <button class="px-3 py-1 text-sm rounded ${this.viewMode === 'source' ? 'bg-white dark:bg-gray-600 text-blue-600 dark:text-blue-400 shadow-sm' : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300'}" data-mode="source">Source</button>
                            <button class="px-3 py-1 text-sm rounded ${this.viewMode === 'diff' ? 'bg-white dark:bg-gray-600 text-blue-600 dark:text-blue-400 shadow-sm' : 'text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300'}" data-mode="diff">Diff</button>
                        </div>
                        ` : ''}
                    </div>
                    
                    <!-- Preview content -->
                    <div class="flex-1 overflow-auto p-4" id="restore-preview-content">
                        ${this.renderPreview()}
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50">
                <div class="flex justify-between items-center">
                    <div class="flex space-x-3">
                        <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 flex items-center" onclick="window.restoreWindow.openBackedUpFile()">
                            <span class="material-icons-round text-sm mr-2">open_in_new</span>
                            Open
                        </button>
                        <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 flex items-center" onclick="window.restoreWindow.openBackedUpFileLocation()">
                            <span class="material-icons-round text-sm mr-2">folder_open</span>
                            Open Location
                        </button>
                        <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 flex items-center" onclick="window.restoreWindow.downloadBackedUpFile()">
                            <span class="material-icons-round text-sm mr-2">download</span>
                            Download
                        </button>
                    </div>
                    <div class="flex justify-end space-x-3">
                        <button class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600" onclick="window.restoreWindow.close()">
                            Cancel
                        </button>
                        <button class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center" 
                                id="restore-button"
                                ${!this.selectedSnapshot ? 'disabled' : ''}>
                            <span class="material-icons-round text-sm mr-2">restore</span>
                            Restore Selected Version
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
            <div class="p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-24 mb-2 animate-pulse"></div>
                <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16 animate-pulse"></div>
            </div>
            `).join('')}
        </div>
        `;
    }

    renderSnapshots() {
        if (this.snapshots.length === 0) {
            return `
            <div class="text-center py-8">
                <span class="material-icons-round text-gray-400 text-4xl mb-3">history</span>
                <p class="text-gray-500 dark:text-gray-400">No backup versions found</p>
                <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">This file or folder hasn't been backed up yet</p>
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
                <div class="p-3 border rounded-lg cursor-pointer transition-colors ${isSelected ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700'}"
                     onclick="window.restoreWindow.selectSnapshot('${snapshot.id}')">
                    <div class="flex justify-between items-start mb-1">
                        <div class="flex items-center">
                            <span class="font-medium ${isSelected ? 'text-blue-700 dark:text-blue-400' : 'text-gray-900 dark:text-white'}">${snapshot.time}</span>
                            ${isMainBackup ? '<span class="ml-2 text-xs px-2 py-0.5 bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300 rounded font-medium">Primary</span>' : ''}
                            ${isLatest ? '<span class="ml-2 text-xs px-2 py-0.5 bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300 rounded font-medium">Latest</span>' : ''}
                        </div>
                        <span class="text-xs ${isSelected ? 'text-blue-600 dark:text-blue-400' : 'text-gray-500 dark:text-gray-400'}">${sizeOrCount}</span>
                    </div>
                    <div class="text-sm ${isSelected ? 'text-blue-600 dark:text-blue-400' : 'text-gray-600 dark:text-gray-400'}">
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
                    <span class="material-icons-round text-gray-400 text-4xl mb-3">select_all</span>
                    <p class="text-gray-500 dark:text-gray-400">Select a version to preview</p>
                </div>
            </div>
            `;
        }

        if (this.isLoadingPreview) {
            return `
            <div class="flex items-center justify-center h-full">
                <div class="text-center">
                    <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-4"></div>
                    <p class="text-gray-500 dark:text-gray-400">Loading preview...</p>
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
                <div class="w-16 h-16 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-center mb-4">
                    <span class="material-icons-round text-gray-500 dark:text-gray-400 text-3xl">${icon}</span>
                </div>
                <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">${this.currentFile.name}</h3>
                <p class="text-gray-500 dark:text-gray-400 mb-6">Preview not available for this file type</p>
                <div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 w-full max-w-md">
                    <div class="space-y-2">
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600 dark:text-gray-400">Version:</span>
                            <span class="text-sm font-medium text-gray-900 dark:text-white">${snapshot.date} ${snapshot.time}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600 dark:text-gray-400">Size:</span>
                            <span class="text-sm font-medium text-gray-900 dark:text-white">${snapshot.size}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600 dark:text-gray-400">Backup Type:</span>
                            <span class="text-sm font-medium text-gray-900 dark:text-white">${snapshot.type}</span>
                        </div>
                    </div>
                </div>
            </div>
            `;
        }

        return `
        <div class="h-full">
            <div class="text-sm text-gray-500 dark:text-gray-400 mb-3">
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
        const previewContainer = document.getElementById('restore-preview-content');
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
                    <span class="material-icons-round text-red-400 text-4xl mb-3">error</span>
                    <p class="text-red-500 dark:text-red-400">Failed to load preview</p>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">${error.message || 'Unknown error'}</p>
                </div>
            </div>
            `;
        } finally {
            this.isLoadingPreview = false;
        }
    }

    async loadSourcePreview() {
        const previewContainer = document.getElementById('restore-preview-content');
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
                <div class="bg-gray-900 text-gray-100 rounded-lg overflow-hidden h-full flex flex-col">
                    <div class="px-4 py-2 bg-gray-800 border-b border-gray-700">
                        <div class="text-xs text-gray-400">${headerText}</div>
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
        const previewContainer = document.getElementById('restore-preview-content');
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
                            <p class="text-green-600 dark:text-green-400 font-medium">No differences found</p>
                            <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">The snapshot is identical to the current version</p>
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
                        bgClass = 'bg-green-50 dark:bg-green-900/20';
                        textClass = 'text-green-800 dark:text-green-200';
                        prefix = '<span class="text-green-600 dark:text-green-400 mr-2">+</span>';
                    } else if (line.type === 'removed') {
                        bgClass = 'bg-red-50 dark:bg-red-900/20';
                        textClass = 'text-red-800 dark:text-red-200 line-through opacity-70';
                        prefix = '<span class="text-red-600 dark:text-red-400 mr-2">-</span>';
                    } else {
                        textClass = 'text-gray-700 dark:text-gray-300';
                        prefix = '<span class="text-gray-500 dark:text-gray-500 mr-2">&nbsp;</span>';
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
                <div class="bg-white dark:bg-gray-900 rounded-lg overflow-hidden h-full flex flex-col">
                    <div class="px-4 py-3 bg-gray-50 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
                        <div class="text-sm text-gray-600 dark:text-gray-400">
                            Comparing <span class="font-medium text-gray-800 dark:text-gray-200">${headerText}</span> with current
                        </div>
                        <div class="flex items-center space-x-4 text-xs">
                            <div class="flex items-center space-x-1">
                                <span class="w-2 h-2 bg-red-500 rounded-full"></span>
                                <span class="text-gray-500">Removed</span>
                            </div>
                            <div class="flex items-center space-x-1">
                                <span class="w-2 h-2 bg-green-500 rounded-full"></span>
                                <span class="text-gray-500">Added</span>
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
        const modal = document.getElementById('restore-modal');
        if (!modal) return;
        
        // Update snapshots panel
        const leftPanel = modal.querySelector('.w-80');
        if (leftPanel) {
            const contentDiv = leftPanel.querySelector('.p-4');
            if (contentDiv) {
                contentDiv.innerHTML = `
                    <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">Available Versions (${this.snapshots.length})</h3>
                    ${this.isLoading ? this.renderLoadingSnapshots() : this.renderSnapshots()}
                `;
            }
        }
        
        // Update preview
        const previewContainer = document.getElementById('restore-preview-content');
        if (previewContainer) {
            previewContainer.innerHTML = this.renderPreview();
        }
        
        // Update restore button
        const restoreBtn = document.getElementById('restore-button');
        if (restoreBtn) {
            restoreBtn.disabled = !this.selectedSnapshot;
            if (!this.selectedSnapshot) {
                restoreBtn.classList.add('disabled:opacity-50', 'disabled:cursor-not-allowed');
            } else {
                restoreBtn.classList.remove('disabled:opacity-50', 'disabled:cursor-not-allowed');
            }
        }
    }

    addEventListeners() {
        // Make window accessible globally
        window.restoreWindow = this;
        
        const modal = document.getElementById('restore-modal');
        if (!modal) return;
        
        // View mode buttons
        modal.querySelectorAll('[data-mode]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.viewMode = e.target.getAttribute('data-mode');
                
                // Update button styles
                modal.querySelectorAll('[data-mode]').forEach(b => {
                    if (b.getAttribute('data-mode') === this.viewMode) {
                        b.className = `px-3 py-1 text-sm rounded bg-white dark:bg-gray-600 text-blue-600 dark:text-blue-400 shadow-sm`;
                    } else {
                        b.className = `px-3 py-1 text-sm rounded text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-300`;
                    }
                });
                
                // Reload preview
                this.loadPreview();
            });
        });
        
        // Restore button
        const restoreBtn = document.getElementById('restore-button');
        if (restoreBtn) {
            restoreBtn.addEventListener('click', () => this.restoreFile());
        }
        
        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.close();
            }
        });
    }

    async restoreFile() {
        if (!this.selectedSnapshot) {
            this.showNotification('Please select a version to restore', 'warning');
            return;
        }
        
        const snapshot = this.snapshots.find(s => s.id === this.selectedSnapshot);
        const versionType = snapshot.is_main_backup ? 'Original Backup' : 'Snapshot';
        // const confirmRestore = confirm(`Are you sure you want to restore "${this.currentFile.name}"?\nThis will replace the current version with the ${versionType} from ${snapshot.date} ${snapshot.time}`);
        const confirmRestore = await showConfirm(
            'Restore Confirmation',
            `Are you sure you want to restore "${this.currentFile.name}"?\nThis will replace the current version with the ${versionType} from ${snapshot.date} ${snapshot.time}`,
            {
                confirmText: 'Restore',
                cancelText: 'Cancel',
                confirmType: 'primary'
            }
        );

        if (!confirmRestore) return;
        
        this.abortController = new AbortController();
        this.showProgress('Starting restore...', () => this.abortOperation());
        
        try {
            const response = await fetch('/api/backup/restore', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    file_path: this.currentFile.path,
                    snapshot_id: this.selectedSnapshot,
                    restore_to: 'original'
                })
            });
            
            const data = await response.json();
            if (data.success && data.job_id) {
                this.activeJobId = data.job_id;
                await this.pollJob(data.job_id, 'Restoring');
            } else {
                this.showNotification(`Failed to restore: ${data.error}`, 'error');
                this.hideProgress();
            }
        } catch (error) {
            if (error.name === 'AbortError') {
                this.showNotification('Restore cancelled', 'info');
            } else {
                console.error('Restore error:', error);
                this.showNotification('Failed to restore file. Please try again.', 'error');
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
                        
                        if (actionName === 'Restoring') {
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
        const modalContent = document.querySelector('#restore-modal > div');
        if (!modalContent) return;

        this.hideProgress();

        let cancelButtonHtml = '';
        if (onCancel) {
            cancelButtonHtml = `
                <button id="abort-operation-btn" class="mt-4 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/30 rounded-lg transition-colors flex items-center">
                    <span class="material-icons-round text-sm mr-2">cancel</span>
                    Cancel
                </button>
            `;
        }

        const overlay = document.createElement('div');
        overlay.id = 'restore-progress-overlay';
        overlay.className = 'absolute inset-0 z-50 flex items-center justify-center bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm rounded-lg transition-opacity duration-200';
        
        overlay.innerHTML = `
            <div class="flex flex-col items-center max-w-sm w-full px-8 py-6">
                <div class="w-16 h-16 mb-4 rounded-full bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center">
                    <div class="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">${message}</h3>
                
                <div class="w-full bg-gray-200 rounded-full h-1.5 dark:bg-gray-700 mt-2 mb-1 overflow-hidden">
                    <div id="restore-progress-bar" class="bg-blue-600 h-1.5 rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
                <div class="flex justify-between w-full px-1 mb-2">
                    <p id="restore-progress-text" class="text-xs text-gray-500 dark:text-gray-400">Please wait...</p>
                    <p id="restore-progress-speed" class="text-xs text-gray-500 dark:text-gray-400 font-mono"></p>
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
        const bar = document.getElementById('restore-progress-bar');
        const text = document.getElementById('restore-progress-text');
        const speed = document.getElementById('restore-progress-speed');
        
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
        const overlay = document.getElementById('restore-progress-overlay');
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
    window.RestoreWindow = RestoreWindow;
}
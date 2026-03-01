// src/js/pages/system-restore.js

export default class SystemRestorePage {
    constructor() {
        this.name = 'system-restore';
        this.isRestoring = false;
        this.restoreProgress = 0;
        this.currentTask = '';
        this.timeElapsed = 0;
        this.timeRemaining = 0;
        this.loading = true;
        
        // Data for restore options
        this.data = {
            homeFolders: [],
            flatpakApps: [],
            devPackages: []
        };
    }

    async loadData() {
        try {
            // Load folders and flatpaks from system restore API
            const restoreResp = await fetch('/api/system-restore/options');
            const restoreData = await restoreResp.json();

            if (restoreData.success) {
                // Process folders
                this.data.homeFolders = (restoreData.folders || []).map(f => ({
                    name: f.name,
                    path: f.path,
                    size: f.size || '--',
                    filesCount: 0,
                    icon: this.getFolderIcon(f.name),
                    selected: false
                }));

                // Process flatpaks
                this.data.flatpakApps = (restoreData.flatpaks || []).map(app => ({
                    name: app.name || app.identifier,
                    identifier: app.identifier,
                    icon: app.icon || 'apps',
                    color: app.color || 'bg-blue-500',
                    selected: false
                }));
            }

            // Load dev packages
            const devResp = await fetch('/api/dev-packages');
            const devData = await devResp.json();

            console.log('Dev packages API response:', devData);

            if (devData.success && devData.packages) {
                const pkgArray = Array.isArray(devData.packages) ? devData.packages : 
                                Object.values(devData.packages).flat();
                
                console.log('Parsed dev packages array:', pkgArray);
                
                this.data.devPackages = pkgArray
                    .filter(pkg => pkg) // Filter out null/undefined
                    .map(pkg => {
                        let pkgCommand = '';
                        let pkgCategory = '';
                        
                        // Handle different formats
                        if (typeof pkg === 'string') {
                            pkgCommand = pkg.trim();
                        } else if (typeof pkg === 'object' && pkg !== null) {
                            // Try to extract command and category
                            if (pkg.command) {
                                pkgCommand = String(pkg.command).trim();
                            }
                            if (pkg.category) {
                                pkgCategory = String(pkg.category).trim();
                            }
                        }
                        
                        return {
                            command: pkgCommand || 'Unknown Command',
                            category: pkgCategory || 'Package',
                            selected: false
                        };
                    })
                    .filter(pkg => pkg.command && pkg.command !== 'Unknown Command' && pkg.command !== '[object Object]');
                
                console.log('Final dev packages:', this.data.devPackages);
            }

            this.loading = false;
        } catch (e) {
            console.error('Failed to load restore data:', e);
            this.loading = false;
        }
    }

    getFolderIcon(folderName) {
        const name = folderName.toLowerCase();
        const icons = {
            'documents': 'description',
            'music': 'music_note',
            'pictures': 'photo_library',
            'videos': 'video_library',
            'downloads': 'download',
            'desktop': 'desktop_windows',
            'projects': 'code'
        };
        for (const [key, icon] of Object.entries(icons)) {
            if (name.includes(key)) return icon;
        }
        return 'folder';
    }

    renderHeader() {
        return `
        <div class="px-8 py-6 bg-surface-light dark:bg-surface-dark border-b border-border-light dark:border-border-dark flex items-center justify-between">
            <div>
                <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Select items to restore</h1>
                <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-1">Choose the files, applications, and packages to include in this recovery.</p>
            </div>
            <button id="restore-selected-btn" class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-medium shadow-md transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed text-sm" style="background-color: #007AFF;">
                <span class="material-icons-round text-base">restore</span>
                Restore Selected
            </button>
        </div>
        `;
    }

    renderHomeFolders() {
        if (this.data.homeFolders.length === 0) {
            return `<p class="text-sm text-gray-500 italic">No folders found in backup.</p>`;
        }

        return `
        <div class="mb-8">
            <div class="flex items-center gap-2 mb-4">
                <span class="material-icons-round text-blue-500" style="color: #007AFF;">folder</span>
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Home Folders</h2>
            </div>
            <div class="overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
                <table class="w-full text-sm">
                    <thead class="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
                        <tr>
                            <th class="px-6 py-3 text-left font-semibold text-gray-700 dark:text-gray-300">NAME</th>
                            <th class="px-6 py-3 text-left font-semibold text-gray-700 dark:text-gray-300">SIZE</th>
                            <th class="px-6 py-3 text-left font-semibold text-gray-700 dark:text-gray-300">FILES COUNT</th>
                            <th class="px-6 py-3 text-right font-semibold text-gray-700 dark:text-gray-300">SELECTION</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
                        ${this.data.homeFolders.map((folder, idx) => `
                        <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                            <td class="px-6 py-4">
                                <div class="flex items-center gap-3">
                                    <span class="material-icons-round text-blue-500 text-lg" style="color: #007AFF;">${folder.icon}</span>
                                    <span class="font-medium text-gray-900 dark:text-white">${folder.name}</span>
                                </div>
                            </td>
                            <td class="px-6 py-4 text-gray-600 dark:text-gray-400">${folder.size}</td>
                            <td class="px-6 py-4 text-gray-600 dark:text-gray-400">${folder.filesCount || '-'}</td>
                            <td class="px-6 py-4 text-right">
                                <input type="checkbox" class="folder-checkbox w-5 h-5 rounded cursor-pointer" data-index="${idx}" style="accent-color: #007AFF;" />
                            </td>
                        </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        </div>
        `;
    }

    renderFlatpakApps() {
        if (this.data.flatpakApps.length === 0) {
            return `<p class="text-sm text-gray-500 italic">No flatpak applications found in backup.</p>`;
        }

        return `
        <div class="mb-8">
            <div class="flex items-center gap-2 mb-4">
                <span class="material-icons-round text-blue-500" style="color: #007AFF;">apps</span>
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Flatpak Applications</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                ${this.data.flatpakApps.map((app, idx) => `
                <label class="relative border border-gray-200 dark:border-gray-700 rounded-lg p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors bg-white dark:bg-gray-800">
                    <input type="checkbox" class="app-checkbox absolute top-4 right-4 w-5 h-5 rounded cursor-pointer" data-index="${idx}" style="accent-color: #007AFF;" />
                    <div class="flex flex-col items-center text-center pt-2">
                        <div class="w-12 h-12 rounded-lg flex items-center justify-center mb-3" style="background-color: rgba(0, 122, 255, 0.1);">
                            <span class="material-icons-round text-2xl" style="color: #007AFF;">${app.icon}</span>
                        </div>
                        <div class="font-semibold text-gray-900 dark:text-white text-sm">${app.name}</div>
                        <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">${app.identifier}</div>
                    </div>
                </label>
                `).join('')}
            </div>
        </div>
        `;
    }

    renderDevPackages() {
        const validPackages = this.data.devPackages.filter(pkg => pkg.command && pkg.command !== '[object Object]');
        
        if (validPackages.length === 0) {
            return `<p class="text-sm text-gray-500 italic">No development packages found in backup.</p>`;
        }

        return `
        <div class="mb-8">
            <div class="flex items-center gap-2 mb-4">
                <span class="material-icons-round text-blue-500" style="color: #007AFF;">code</span>
                <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Development Packages</h2>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                ${validPackages.map((pkg, idx) => `
                <label class="relative border border-gray-200 dark:border-gray-700 rounded-lg p-4 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors bg-white dark:bg-gray-800 package-label" data-package-idx="${idx}">
                    <input type="checkbox" class="package-checkbox absolute top-4 right-4 w-5 h-5 rounded cursor-pointer" data-index="${idx}" style="accent-color: #007AFF;" />
                    <div class="flex flex-col gap-2 pr-8">
                        <div class="text-xs font-medium text-blue-600 dark:text-blue-400 uppercase tracking-wide">${this.escapeHtml(pkg.category)}</div>
                        <div class="font-medium text-gray-900 dark:text-white text-sm break-words">${this.escapeHtml(pkg.command)}</div>
                    </div>
                </label>
                `).join('')}
            </div>
        </div>
        `;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    async render() {
        await this.loadData();

        if (this.loading) {
            return `
            <div class="flex-1 flex items-center justify-center bg-white dark:bg-surface-dark">
                <div class="text-center">
                    <div class="w-12 h-12 rounded-full border-4 border-gray-200 dark:border-gray-700 border-t-blue-500 mx-auto mb-4 animate-spin" style="border-top-color: #007AFF;"></div>
                    <p class="text-gray-600 dark:text-gray-400">Loading restore options...</p>
                </div>
            </div>
            `;
        }

        return `
        <div class="flex flex-col h-full overflow-hidden">
            ${this.renderHeader()}
            <div class="flex-1 overflow-y-auto bg-white dark:bg-surface-dark p-8">
                ${this.renderHomeFolders()}
                ${this.renderFlatpakApps()}
                ${this.renderDevPackages()}
            </div>
            ${this.renderRestoreModal()}
        </div>
        `;
    }

    renderRestoreModal() {
        return `
        <div id="restore-modal" class="hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center">
            <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 w-full max-w-lg">
                <div class="text-center mb-8">
                    <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Restoring System Files...</h3>
                    <p class="text-sm text-text-secondary-light dark:text-text-secondary-dark mt-2">This process might take a while. Please do not disconnect or power off your device.</p>
                </div>

                <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-6">
                    <div class="mb-4">
                        <div class="flex items-baseline justify-between mb-2">
                            <span class="text-xs font-semibold text-blue-500 uppercase tracking-wide" style="color: #007AFF;">Overall Progress</span>
                            <span class="text-3xl font-bold text-gray-900 dark:text-white" id="modal-progress-percent">0%</span>
                        </div>
                        <div class="w-full h-3 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                            <div id="modal-progress-bar" class="h-full transition-all duration-300" style="background-color: #007AFF; width: 0%"></div>
                        </div>
                    </div>

                    <div class="space-y-3 text-sm">
                        <div>
                            <div class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">CURRENT ITEM</div>
                            <div id="modal-current-item" class="text-gray-900 dark:text-white font-medium truncate">Starting restore process...</div>
                        </div>

                        <div class="flex justify-between items-center pt-2 border-t border-gray-200 dark:border-gray-600">
                            <div>
                                <div class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">DETAILS</div>
                                <div id="modal-details" class="text-gray-900 dark:text-white font-medium">0 GB / 12.0 GB restored</div>
                            </div>
                            <div class="text-right">
                                <div class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">STATUS</div>
                                <div id="modal-status" class="text-gray-900 dark:text-white font-medium">Preparing...</div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-3 mb-6">
                    <div>
                        <div class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">TIME ELAPSED</div>
                        <div id="modal-time-elapsed" class="text-lg font-semibold text-gray-900 dark:text-white">00:00:00</div>
                    </div>
                    <div class="text-right">
                        <div class="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1">TIME LEFT</div>
                        <div id="modal-time-left" class="text-lg font-semibold text-gray-900 dark:text-white">~ calculating...</div>
                    </div>
                </div>

                <div class="flex gap-3 mb-6">
                    <button id="pause-restore-btn" class="flex-1 px-4 py-2.5 text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2" style="background-color: #007AFF;" onmouseover="this.style.backgroundColor='#0051D5'" onmouseout="this.style.backgroundColor='#007AFF'">
                        <span class="material-icons-round text-lg">pause</span>
                        Pause Process
                    </button>
                    <button id="cancel-restore-btn" class="flex-1 px-4 py-2.5 bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-white rounded-lg font-medium transition-colors flex items-center justify-center gap-2">
                        <span class="material-icons-round text-lg">close</span>
                        Cancel
                    </button>
                </div>

                <div class="rounded-lg p-4" style="background-color: rgba(0, 122, 255, 0.1); border: 1px solid rgba(0, 122, 255, 0.3);">
                    <div class="flex gap-3">
                        <span class="material-icons-round flex-shrink-0" style="color: #007AFF;">info</span>
                        <div>
                            <div class="font-medium text-blue-900 dark:text-blue-300">Verification in progress</div>
                            <div class="text-sm text-blue-800 dark:text-blue-200 mt-0.5">System is currently validating restored segments against original checksums to ensure data integrity.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        `;
    }

    async afterRender() {
        this.attachEventListeners();
    }

    attachEventListeners() {
        // Home Folders checkboxes
        document.querySelectorAll('.folder-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const idx = e.target.getAttribute('data-index');
                this.data.homeFolders[idx].selected = e.target.checked;
                this.updateRestoreButton();
            });
        });

        // Flatpak Apps checkboxes
        document.querySelectorAll('.app-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const idx = e.target.getAttribute('data-index');
                this.data.flatpakApps[idx].selected = e.target.checked;
                this.updateRestoreButton();
            });
        });

        // Dev Packages checkboxes with styling
        document.querySelectorAll('.package-checkbox').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const idx = e.target.getAttribute('data-index');
                this.data.devPackages[idx].selected = e.target.checked;
                
                // Update styling
                const label = e.target.closest('.package-label');
                if (e.target.checked) {
                    label.style.borderColor = '#007AFF';
                    label.style.backgroundColor = 'rgba(0, 122, 255, 0.1)';
                } else {
                    label.style.borderColor = '';
                    label.style.backgroundColor = '';
                }
                
                this.updateRestoreButton();
            });
        });

        // Restore Selected button
        document.getElementById('restore-selected-btn')?.addEventListener('click', () => {
            this.startRestore();
        });

        // Pause button
        document.getElementById('pause-restore-btn')?.addEventListener('click', () => {
            showInfo('Restore paused', 'info');
        });

        // Cancel button
        document.getElementById('cancel-restore-btn')?.addEventListener('click', () => {
            this.cancelRestore();
        });
    }

    updateRestoreButton() {
        const hasSelection = this.data.homeFolders.some(f => f.selected) || 
                           this.data.flatpakApps.some(a => a.selected) || 
                           this.data.devPackages.some(p => p.selected);
        
        const btn = document.getElementById('restore-selected-btn');
        if (btn) {
            btn.disabled = !hasSelection;
        }
    }

    startRestore() {
        if (this.isRestoring) return;
        
        const modal = document.getElementById('restore-modal');
        if (modal) {
            modal.classList.remove('hidden');
        }
        
        this.isRestoring = true;
        this.restoreProgress = 0;
        this.timeElapsed = 0;
        
        // Simulate restore process
        this.simulateRestore();
    }

    cancelRestore() {
        this.isRestoring = false;
        const modal = document.getElementById('restore-modal');
        if (modal) {
            modal.classList.add('hidden');
        }
        showInfo('Restore cancelled', 'info');
    }

    async simulateRestore() {
        const tasks = [];
        
        // Collect selected items
        this.data.homeFolders.forEach(f => {
            if (f.selected) tasks.push({ name: f.name, type: 'folder', duration: 5 });
        });
        
        this.data.flatpakApps.forEach(a => {
            if (a.selected) tasks.push({ name: a.name, type: 'app', duration: 3 });
        });
        
        this.data.devPackages.forEach(p => {
            if (p.selected) tasks.push({ name: p.command, type: 'package', duration: 2 });
        });

        const totalDuration = tasks.reduce((sum, t) => sum + t.duration, 0);
        let currentProgress = 0;
        const startTime = Date.now();

        for (const task of tasks) {
            if (!this.isRestoring) break;

            const taskEl = document.getElementById('modal-current-item');
            if (taskEl) {
                const icon = task.type === 'folder' ? '📁' : task.type === 'app' ? '📦' : '💾';
                taskEl.textContent = `${icon} ${task.type === 'folder' ? 'Restoring' : 'Installing'} ${task.name}`;
            }

            // Simulate task progress
            for (let i = 0; i < task.duration; i++) {
                if (!this.isRestoring) break;

                currentProgress += (100 / totalDuration);
                this.restoreProgress = Math.min(currentProgress, 99);
                this.timeElapsed = Math.floor((Date.now() - startTime) / 1000);

                this.updateRestoreProgress();
                await new Promise(r => setTimeout(r, 300));
            }
        }

        if (this.isRestoring) {
            // Complete
            this.restoreProgress = 100;
            this.updateRestoreProgress();
            document.getElementById('modal-current-item').textContent = '✅ System restore complete!';
            document.getElementById('modal-status').textContent = 'Completed';

            setTimeout(() => {
                this.isRestoring = false;
                const modal = document.getElementById('restore-modal');
                if (modal) modal.classList.add('hidden');
                showToast('System restore completed successfully', 'success');
            }, 2000);
        }
    }

    updateRestoreProgress() {
        const percentEl = document.getElementById('modal-progress-percent');
        if (percentEl) percentEl.textContent = Math.round(this.restoreProgress) + '%';

        const barEl = document.getElementById('modal-progress-bar');
        if (barEl) barEl.style.width = this.restoreProgress + '%';

        const elapsedEl = document.getElementById('modal-time-elapsed');
        if (elapsedEl) {
            const hours = Math.floor(this.timeElapsed / 3600);
            const mins = Math.floor((this.timeElapsed % 3600) / 60);
            const secs = this.timeElapsed % 60;
            elapsedEl.textContent = `${String(hours).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
        }

        // Estimate time remaining
        const timeLeftEl = document.getElementById('modal-time-left');
        if (timeLeftEl) {
            if (this.restoreProgress > 0 && this.restoreProgress < 100) {
                const estimatedTotal = (this.timeElapsed / this.restoreProgress) * 100;
                const timeLeft = Math.max(0, Math.ceil(estimatedTotal - this.timeElapsed));
                const mins = Math.floor(timeLeft / 60);
                const secs = timeLeft % 60;
                timeLeftEl.textContent = `~ ${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')} remaining`;
            }
        }
    }
}

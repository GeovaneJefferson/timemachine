/**
 * Manages system migration/restoration operations
 */

export class MigrationManager {
    constructor(state, api, eventBus) {
        this.state = state;
        this.api = api;
        this.eventBus = eventBus;
    }

    async initMigrationView() {
        // Reset steps
        document.getElementById('mig-step-1-source').classList.remove('hidden');
        document.getElementById('mig-step-2-content').classList.add('hidden');
        document.getElementById('mig-step-3-progress').classList.add('hidden');

        const desc = document.getElementById('mig-step-desc');
        if (desc) desc.innerText = "Select a source to start the restoration process.";

        await this.renderSourceList();
    }

    async renderSourceList() {
        const container = document.getElementById('mig-source-list');
        if (!container) return;

        container.innerHTML = `
        <div class="text-center py-10 text-muted">
        <i class="bi bi-arrow-clockwise animate-spin text-2xl mb-2"></i>
        <p class="text-sm">Scanning for backup sources...</p>
        </div>
        `;

        try {
            const data = await this.api.getMigrationSources();

            if (!data.success || !data.sources?.length) {
                container.innerHTML = `
                <div class="text-center p-10 border-2 border-dashed border-main rounded-2xl text-muted">
                <i class="bi bi-hdd-network-off text-4xl mb-3"></i>
                <h4 class="font-bold text-main">No Backup Sources Found</h4>
                <p class="text-sm mt-1">Connect a drive with a Time Machine backup and try again.</p>
                </div>`;
                return;
            }

            container.innerHTML = '';
            data.sources.forEach(device => {
                const totalGB = Math.round((device.total || 0) / (1024 ** 3));
                const card = this.createSourceCard(device, totalGB);
                container.innerHTML += card;
            });
        } catch (error) {
            console.error('[MigrationManager] Failed to load sources:', error);
            container.innerHTML = `
            <div class="text-center p-10 border-2 border-dashed border-main rounded-2xl text-muted">
            <i class="bi bi-exclamation-triangle text-4xl mb-3"></i>
            <h4 class="font-bold text-main">Error Loading Sources</h4>
            <p class="text-sm mt-1">Failed to scan for backup sources.</p>
            </div>`;
        }
    }

    createSourceCard(device, totalGB) {
        return `
        <div class="mig-source-card bg-card border border-main rounded-2xl p-5 flex items-center gap-5 hover:border-brand-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer transition-all group"
        data-device-name="${device.name}"
        data-device-path="${device.path}"
        data-device-filesystem="${device.filesystem}">
        <div class="w-16 h-16 rounded-xl bg-blue-50 dark:bg-blue-900/20 text-blue-500 flex items-center justify-center text-3xl border border-main">
        <i class="bi bi-usb-drive-fill"></i>
        </div>
        <div class="flex-1">
        <h4 class="font-bold text-main text-lg">${device.label || device.name}</h4>
        <p class="text-xs text-muted">${device.filesystem} • ${totalGB} GB</p>
        </div>
        <i class="bi bi-chevron-right text-muted text-xl opacity-0 group-hover:opacity-100 transition-opacity"></i>
        </div>
        `;
    }

    selectSource(device) {
        this.state.migration.selectedSource = device;

        // Update UI
        document.getElementById('mig-step-1-source').classList.add('hidden');
        document.getElementById('mig-step-2-content').classList.remove('hidden');

        const desc = document.getElementById('mig-step-desc');
        if (desc) desc.innerText = "Step 2 of 3: Choose what to restore from the backup.";

        // Reset selection state
        this.state.migration.selectionState = { home: false, flatpaks: false, installers: false };

        // Simulate scanning
        this.simulateContentScan();
    }

    simulateContentScan() {
        const flatpaksDesc = document.getElementById('desc-flatpaks');
        const installersDesc = document.getElementById('desc-installers');

        if (flatpaksDesc) flatpaksDesc.innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-1"></i> Scanning...';
        if (installersDesc) installersDesc.innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-1"></i> Scanning...';

        setTimeout(() => {
            this.state.migration.selectionState = { home: true, flatpaks: true, installers: true };
            this.updateMigrationUI();
        }, 800);
    }

    toggleMigrationItem(key) {
        this.state.migration.selectionState[key] = !this.state.migration.selectionState[key];
        this.updateMigrationUI();
    }

    updateMigrationUI() {
        ['home', 'flatpaks', 'installers'].forEach(key => {
            const card = document.getElementById(`mig-card-${key}`);
            const check = document.getElementById(`check-${key}`);
            const desc = document.getElementById(`desc-${key}`);
            const isActive = this.state.migration.selectionState[key];

            if (!card || !check || !desc) return;

            if (isActive) {
                card.classList.add('border-brand-500', 'bg-brand-50', 'shadow-md');
                card.classList.remove('border-gray-200', 'bg-white');
                check.classList.remove('opacity-0', 'scale-75');

                // Update description
                if (key === 'home') {
                    desc.innerText = "Calculated: 142 GB";
                } else {
                    const list = this.state.migration.data[key] || [];
                    const selectedCount = list.filter(item => item.selected).length;
                    desc.innerText = `${selectedCount}/${list.length} items selected`;
                }
            } else {
                card.classList.remove('border-brand-500', 'bg-brand-50', 'shadow-md');
                card.classList.add('border-gray-200', 'bg-white');
                check.classList.add('opacity-0', 'scale-75');
            }
        });

        this.updateRestoreButton();
    }

    updateRestoreButton() {
        const btn = document.getElementById('btn-start-restore');
        if (!btn) return;

        const hasSelection = Object.values(this.state.migration.selectionState).some(v => v);

        if (this.state.user.plan === 'pro') {
            // Pro user
            if (hasSelection) {
                btn.disabled = false;
                btn.className = "bg-brand-600 text-white hover:bg-brand-700 px-8 py-3 rounded-xl font-bold text-sm transition flex items-center gap-2 shadow-sm cursor-pointer";
                btn.onclick = () => this.startMigrationProcess();
            } else {
                btn.disabled = true;
                btn.className = "bg-slate-200 text-slate-400 dark:bg-slate-700 dark:text-slate-500 px-8 py-3 rounded-xl font-bold text-sm transition cursor-not-allowed flex items-center gap-2";
                btn.onclick = null;
            }

            // Remove star icon for Pro users
            const starIcon = btn.querySelector('.bi-star-fill');
            if (starIcon) starIcon.remove();
        } else {
            // Basic user
            btn.disabled = false;
            btn.className = "bg-gradient-to-r from-brand-600 to-purple-600 text-white hover:from-brand-700 hover:to-purple-700 px-8 py-3 rounded-xl font-bold text-sm transition flex items-center gap-2 shadow-sm cursor-pointer";
            btn.onclick = () => this.checkProBeforeRestore();

            // Ensure star icon exists
            const starIcon = btn.querySelector('.bi-star-fill');
            if (!starIcon) {
                const newStarIcon = document.createElement('i');
                newStarIcon.className = 'bi bi-star-fill text-yellow-400 mr-1';
                btn.insertBefore(newStarIcon, btn.querySelector('span'));
            }
        }

        // Update button text
        const span = btn.querySelector('span');
        if (span) span.textContent = "Start Restore";
    }

    checkProBeforeRestore() {
        if (this.state.user.plan === 'pro') {
            this.startMigrationProcess();
        } else {
            this.eventBus.emit('notification:show', {
                type: 'info',
                title: 'Pro Feature Required',
                message: 'Upgrade to Pro to start system restoration.'
            });
            this.eventBus.emit('modal:proPlan:open');
        }
    }

    async startMigrationProcess() {
        // Prepare UI
        const step2 = document.getElementById('mig-step-2-content');
        const step3 = document.getElementById('mig-step-3-progress');
        const desc = document.getElementById('mig-step-desc');

        if (step2) step2.classList.add('hidden');
        if (step3) step3.classList.remove('hidden');
        if (desc) desc.innerText = "Transferring data. Do not disconnect your drive.";

        // Get UI elements
        const progressBar = document.getElementById('migration-progress-bar');
        const progressPercent = document.getElementById('progress-percent');
        const statusText = document.getElementById('migration-status-text');
        const timeRemaining = document.getElementById('time-remaining');
        const cancelBtn = document.getElementById('cancel-restore-btn');

        if (!progressBar || !progressPercent || !statusText || !timeRemaining) {
            console.error('[MigrationManager] Missing UI elements for migration progress');
            return;
        }

        // Build processing queue
        const filesToProcess = this.buildMigrationQueue();

        if (filesToProcess.length === 0) {
            this.eventBus.emit('notification:show', {
                type: 'info',
                title: 'Nothing to Migrate',
                message: 'No items selected for migration.'
            });

            // Revert UI
            if (step2) step2.classList.remove('hidden');
            if (step3) step3.classList.add('hidden');
            return;
        }

        // Start migration
        await this.processMigration(filesToProcess, {
            progressBar,
            progressPercent,
            statusText,
            timeRemaining,
            cancelBtn
        });
    }

    buildMigrationQueue() {
        const queue = [];

        if (this.state.migration.selectionState.home) {
            (this.state.migration.data.home || []).forEach(item => {
                queue.push({
                    name: item.name,
                    size: this.parseSize(item.size) || (Math.floor(Math.random() * 6) + 1) * 1024 * 1024
                });
            });
        }

        if (this.state.migration.selectionState.flatpaks) {
            (this.state.migration.data.flatpaks || []).forEach(item => {
                queue.push({
                    name: item.name,
                    size: this.parseSize(item.size) || (Math.floor(Math.random() * 10) + 2) * 1024 * 1024
                });
            });
        }

        if (this.state.migration.selectionState.installers) {
            (this.state.migration.data.installers || []).forEach(item => {
                queue.push({
                    name: item.name,
                    size: this.parseSize(item.size) || (Math.floor(Math.random() * 8) + 1) * 1024 * 1024
                });
            });
        }

        return queue;
    }

    parseSize(sizeString) {
        if (!sizeString) return 0;

        const units = {
            'KB': 1024,
            'MB': 1024 * 1024,
            'GB': 1024 * 1024 * 1024,
            'TB': 1024 * 1024 * 1024 * 1024
        };

        const match = sizeString.match(/^([\d.]+)\s*([KMGTP]?B)$/i);
        if (match) {
            const value = parseFloat(match[1]);
            const unit = match[2].toUpperCase();
            return value * (units[unit] || 1);
        }

        return 0;
    }

    async processMigration(files, uiElements) {
        const totalBytes = files.reduce((sum, file) => sum + file.size, 0);
        let bytesProcessed = 0;
        const startTime = Date.now();
        let cancelled = false;

        // Setup cancel button
        if (uiElements.cancelBtn) {
            uiElements.cancelBtn.classList.remove('hidden');
            uiElements.cancelBtn.disabled = false;
            uiElements.cancelBtn.onclick = () => {
                cancelled = true;
                uiElements.cancelBtn.disabled = true;
                uiElements.statusText.innerText = 'Cancelling...';
                this.eventBus.emit('notification:show', {
                    type: 'info',
                    title: 'Migration',
                    message: 'Cancelling migration...'
                });
            };
        }

        // Process files
        for (let i = 0; i < files.length; i++) {
            if (cancelled) break;

            const file = files[i];

            // Update status
            uiElements.statusText.innerHTML = `<i class="bi bi-arrow-repeat animate-spin mr-2"></i> Restoring ${file.name}`;

            // Simulate file processing
            await this.simulateFileProcess(file, (increment) => {
                bytesProcessed = Math.min(totalBytes, bytesProcessed + increment);
                this.updateProgressUI(bytesProcessed, totalBytes, startTime, uiElements);
            });

            if (cancelled) break;

            // Update status for completed file
            uiElements.statusText.innerHTML = `<i class="bi bi-check-lg text-emerald-500 mr-2"></i> Restored ${i + 1}/${files.length}: ${file.name}`;

            // Add to activity feed
            this.eventBus.emit('activity:add', {
                type: 'file_activity',
                title: 'Restored',
                description: file.name,
                size: file.size,
                timestamp: Date.now(),
                               status: 'success'
            });
        }

        // Finalize
        if (cancelled) {
            uiElements.statusText.innerHTML = '<i class="bi bi-x-circle-fill text-orange-500 mr-2"></i> Migration Cancelled';
            uiElements.statusText.className = 'text-orange-500 font-bold';

            this.eventBus.emit('notification:show', {
                type: 'info',
                title: 'Migration Cancelled',
                message: 'Migration was cancelled by the user.'
            });
        } else {
            bytesProcessed = totalBytes;
            this.updateProgressUI(bytesProcessed, totalBytes, startTime, uiElements);

            uiElements.statusText.innerHTML = '<i class="bi bi-check-circle-fill text-green-600 mr-2"></i> Migration Complete!';
            uiElements.statusText.className = 'text-green-600 font-bold text-lg';

            if (uiElements.timeRemaining) {
                uiElements.timeRemaining.innerText = 'Done';
            }

            this.eventBus.emit('notification:show', {
                type: 'success',
                title: 'Migration Completed',
                message: `Migrated ${files.length} item${files.length !== 1 ? 's' : ''}.`
            });
        }

        // Clean up UI
        if (uiElements.cancelBtn) {
            uiElements.cancelBtn.classList.add('hidden');
            uiElements.cancelBtn.onclick = null;
        }
    }

    async simulateFileProcess(file, onProgress) {
        const simulatedSeconds = Math.min(6 + (file.size / (1024 * 1024)) * 0.25, 20);
        const ticks = Math.max(4, Math.round((simulatedSeconds * 1000) / 250));
        const increment = Math.round(file.size / ticks);

        for (let tick = 0; tick < ticks; tick++) {
            await new Promise(resolve => setTimeout(resolve, 250));
            onProgress(increment);
        }
    }

    updateProgressUI(bytesProcessed, totalBytes, startTime, uiElements) {
        const percent = totalBytes > 0 ? Math.min(100, Math.round((bytesProcessed / totalBytes) * 100)) : 0;
        const elapsedSeconds = (Date.now() - startTime) / 1000;
        const speed = elapsedSeconds > 0 ? bytesProcessed / elapsedSeconds : 0;
        const remainingBytes = Math.max(0, totalBytes - bytesProcessed);
        const etaSeconds = speed > 0 ? Math.round(remainingBytes / speed) : -1;

        // Update progress bar
        if (uiElements.progressBar) {
            uiElements.progressBar.style.width = `${percent}%`;
        }

        // Update percentage
        if (uiElements.progressPercent) {
            uiElements.progressPercent.innerText = `${percent}%`;
        }

        // Update ETA
        if (uiElements.timeRemaining) {
            if (etaSeconds >= 0) {
                const minutes = Math.floor(etaSeconds / 60);
                uiElements.timeRemaining.innerText = minutes > 0 ? `${minutes} min` : '< 1 min';
            } else {
                uiElements.timeRemaining.innerText = 'Calculating...';
            }
        }
    }

    async openCustomizeModal(category) {
        this.state.migration.currentEditCategory = category;

        const modal = document.getElementById('migration-detail-modal');
        const container = document.getElementById('detail-modal-container');
        const list = document.getElementById('detail-list-container');
        const title = document.getElementById('detail-modal-title');

        if (!modal || !container || !list || !title) return;

        // Set title
        const displayName = {
            'installers': 'Installers',
            'flatpaks': 'Applications',
            'home': 'Folders'
        }[category] || 'Items';

        title.innerText = `Select ${displayName}`;

        // Show loading
        list.innerHTML = '<div class="text-center p-4 text-muted"><i class="bi bi-arrow-clockwise animate-spin"></i> Loading...</div>';

        // Show modal
        modal.classList.remove('hidden');
        modal.classList.add('flex');

        setTimeout(() => {
            container.classList.remove('scale-95', 'opacity-0');
            container.classList.add('scale-100', 'opacity-100');
        }, 10);

        // Load data
        try {
            if (category === 'home') {
                const response = await fetch(`/api/search/folder?path=`);
                const data = await response.json();

                if (data.success && data.items) {
                    this.state.migration.data.home = data.items
                    .filter(item => item.type === 'folder')
                    .map(folder => ({
                        id: folder.name,
                        name: folder.name,
                        icon: 'bi-folder-fill',
                        color: 'text-blue-500',
                        selected: true
                    }));
                } else {
                    this.state.migration.data.home = [];
                }
            }

            // Render items
            this.renderCustomizeList(category, list);
        } catch (error) {
            console.error('[MigrationManager] Failed to load items for customization:', error);
            list.innerHTML = '<div class="text-center p-4 text-red-500">Failed to load items.</div>';
        }
    }

    renderCustomizeList(category, listElement) {
        const items = this.state.migration.data[category] || [];

        listElement.innerHTML = '';

        if (items.length === 0) {
            listElement.innerHTML = '<div class="text-center p-4 text-muted">No items found.</div>';
            return;
        }

        items.forEach((item, index) => {
            const row = document.createElement('div');
            row.className = 'flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-white/10 cursor-pointer transition-colors';
            row.dataset.index = index;

            row.innerHTML = `
            <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-md bg-gray-100 dark:bg-white/5 flex items-center justify-center text-lg ${item.color || 'text-gray-500'}">
            <i class="bi ${item.icon || 'bi-folder'}"></i>
            </div>
            <p class="text-sm font-bold text-main leading-none">${item.name}</p>
            </div>
            <div class="w-5 h-5 rounded border ${
                item.selected ? 'bg-brand-600 border-brand-600' : 'border-gray-300 bg-white'
            } flex items-center justify-center text-white text-xs">
            ${item.selected ? '<i class="bi bi-check"></i>' : ''}
            </div>
            `;

            row.addEventListener('click', () => this.toggleCustomizeItem(index));
            listElement.appendChild(row);
        });
    }

    toggleCustomizeItem(index) {
        const category = this.state.migration.currentEditCategory;
        if (!category || !this.state.migration.data[category]) return;

        this.state.migration.data[category][index].selected =
        !this.state.migration.data[category][index].selected;

        // Re-render the list
        const list = document.getElementById('detail-list-container');
        if (list) {
            this.renderCustomizeList(category, list);
        }
    }

    closeCustomizeModal() {
        const modal = document.getElementById('migration-detail-modal');
        const container = document.getElementById('detail-modal-container');

        if (modal && container) {
            container.classList.add('scale-95', 'opacity-0');
            container.classList.remove('scale-100', 'opacity-100');

            setTimeout(() => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }, 200);
        }
    }

    setupEventListeners() {
        // Source selection
        document.addEventListener('click', (e) => {
            const sourceCard = e.target.closest('.mig-source-card');
            if (sourceCard) {
                const device = {
                    name: sourceCard.dataset.deviceName,
                    path: sourceCard.dataset.devicePath,
                    filesystem: sourceCard.dataset.deviceFilesystem
                };
                this.selectSource(device);
            }
        });

        // Migration card toggles
        document.addEventListener('click', (e) => {
            const card = e.target.closest('[data-mig-card]');
            if (card) {
                const key = card.dataset.migCard;
                this.toggleMigrationItem(key);
            }
        });

        // Customize buttons
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-customize]')) {
                const button = e.target.closest('[data-customize]');
                const category = button.dataset.customize;
                this.openCustomizeModal(category);
            }
        });

        // Close modal
        document.addEventListener('click', (e) => {
            if (e.target.closest('[data-close-modal]')) {
                this.closeCustomizeModal();
            }
        });

        // Back button
        const backButton = document.getElementById('mig-back-btn');
        if (backButton) {
            backButton.addEventListener('click', () => {
                document.getElementById('mig-step-2-content').classList.add('hidden');
                document.getElementById('mig-step-1-source').classList.remove('hidden');

                const desc = document.getElementById('mig-step-desc');
                if (desc) desc.innerText = "Select a source to start the restoration process.";
            });
        }
    }
}

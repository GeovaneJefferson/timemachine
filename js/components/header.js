// src/js/components/header.js

export default class Header {
    constructor() {
        this.query = '';
        this.currentPage = null;
        this.searchTimeout = null;
        this.DEBOUNCE_DELAY = 300;
        this.clearingInProgress = false;
        this.monitoringInterval = null;
        this.daemonRunning = false;
        this.daemonButtonLock = false;
        this.backupDeviceConnected = false;
    }

    async render() {
        return `
    <div class="flex items-center justify-between px-6 py-3 bg-gray-50/50 dark:bg-gray-800/50 border-b border-border-light dark:border-border-dark backdrop-blur-sm sticky top-0 z-10 h-16">
        <!-- Left side: Search input -->
        <div class="flex items-center gap-2 flex-1">
            <div class="relative w-64 md:w-80 shrink-0">
                <span class="material-icons-round absolute left-2.5 top-1.5 text-gray-400 text-lg pointer-events-none">search</span>
                <input
                    class="search-input w-full pl-9 pr-9 py-1.5 text-sm bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-md shadow-sm focus:ring-2 focus:ring-primary focus:border-primary dark:text-white transition-all"
                    placeholder="Search files..."
                    type="text"
                    value="${this.query}"
                    id="global-search-input"
                    autocomplete="off">
                <button
                    class="clear-search-btn absolute right-2.5 top-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 ${this.query ? '' : 'hidden'}"
                    id="clear-search-icon"
                    type="button"
                    aria-label="Clear search">
                    <span class="material-icons-round text-lg">close</span>
                </button>
            </div>
        </div>
        
        <!-- Center: Empty for balance -->
        <div class="flex-1"></div>
        
        <!-- Right side: Status indicators and buttons -->
        <div class="flex-1 flex justify-end items-center gap-4">
            <div class="monitoring-status flex items-center gap-2 text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark hover:text-gray-800 dark:hover:text-gray-200 transition-colors cursor-default">
                <span class="relative flex h-2 w-2">
                    <span class="monitor-ping animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                    <span class="monitor-dot relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
                <span class="monitoring-text">Monitoring files...</span>
            </div>
            <div class="device-status flex items-center gap-1.5 text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark hover:text-gray-800 dark:hover:text-gray-200 transition-colors cursor-default">
                <span class="material-icons-round device-icon text-green-500 text-sm">wifi</span>
                <span>Devices connection</span>
            </div>
            <div class="w-px h-4 bg-gray-300 dark:bg-gray-600 mx-1"></div>
            <button class="daemon-button flex items-center gap-1.5 px-3 py-1.5 bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors text-xs font-semibold text-gray-700 dark:text-gray-200">
                <span class="material-icons-round text-sm daemon-icon">sync</span>
                <span class="daemon-text">Checking...</span>
            </button>
        </div>
    </div>
    `;
    }

    afterRender() {
        console.log('Header initialized');
        this.setupSearch();
        this.setupDaemonButton();
        this.startMonitoringAnimation();
        this.checkBackupDevice();

        window.appHeader = this;

        // listen for external status changes (e.g. settings page toggles)
        document.addEventListener('daemon-status-changed', (evt) => {
            const running = evt.detail && evt.detail.running;
            if (typeof running === 'boolean') {
                this.daemonRunning = running;
                this.updateDaemonButton();
                this.updateMonitoringStatus();
            }
        });

        // Initial status check
        this.checkDaemonStatus();
    }

    async checkBackupDevice() {
        try {
            const response = await fetch('/api/backup/connection');
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.backupDeviceConnected = data.connected || false;
                    this.updateDeviceStatus();
                } else {
                    this.backupDeviceConnected = false;
                    this.updateDeviceStatus();
                }
            }
        } catch (error) {
            console.error('Error checking backup device:', error);
            this.backupDeviceConnected = false;
            this.updateDeviceStatus();
        }
    }

    updateDeviceStatus() {
        const deviceIcon = document.querySelector('.device-icon');
        
        if (deviceIcon) {
            if (this.backupDeviceConnected) {
                deviceIcon.textContent = 'wifi';
                deviceIcon.className = 'material-icons-round device-icon text-green-500 text-sm';
            } else {
                deviceIcon.textContent = 'wifi_off';
                deviceIcon.className = 'material-icons-round device-icon text-gray-400 text-sm';
            }
        }
    }

    async checkDaemonStatus() {
        try {
            console.log('Checking daemon status...');
            const response = await fetch('/api/daemon/ready-status');
            
            if (!response.ok) {
                throw new Error('Failed to fetch daemon status');
            }
            
            const data = await response.json();
            console.log('Daemon status response:', data);
            
            // Extract the running status from the response
            this.daemonRunning = data.running === true;
            console.log('Daemon is running:', this.daemonRunning);
            
            this.updateDaemonButton();
            this.updateMonitoringStatus();
        } catch (error) {
            console.error('Error checking daemon status:', error);
            this.daemonRunning = false;
            this.updateDaemonButton();
            this.updateMonitoringStatus();
        }
    }

    setupSearch() {
        const searchInput = document.getElementById('global-search-input');
        const clearBtn = document.getElementById('clear-search-icon');

        if (!searchInput) {
            console.error('Search input not found');
            return;
        }

        searchInput.addEventListener('input', (e) => {
            this.query = e.target.value;

            if (clearBtn) {
                if (this.query) {
                    clearBtn.classList.remove('hidden');
                } else {
                    clearBtn.classList.add('hidden');
                }
            }

            if (this.searchTimeout) {
                clearTimeout(this.searchTimeout);
            }

            if (this.query.trim().length >= 2) {
                this.searchTimeout = setTimeout(() => {
                    this.performSearch(this.query);
                }, this.DEBOUNCE_DELAY);
            } else if (this.query === '') {
                this.clearSearch();
            }
        });

        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.performSearch(this.query);
            }

            if (e.key === 'Escape') {
                e.preventDefault();
                this.clearSearch();
            }
        });

        if (clearBtn) {
            clearBtn.replaceWith(clearBtn.cloneNode(true));
            const newClearBtn = document.getElementById('clear-search-icon');

            newClearBtn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.clearSearch();
            });
        }

        searchInput.addEventListener('focus', () => {
            searchInput.classList.add('ring-2', 'ring-primary');
        });

        searchInput.addEventListener('blur', () => {
            searchInput.classList.remove('ring-2', 'ring-primary');
        });

        const searchIcon = document.querySelector('.relative .material-icons-round');
        if (searchIcon) {
            searchIcon.addEventListener('click', () => {
                searchInput.focus();
            });
        }
    }

    performSearch(query) {
        if (!query || query.trim() === '') {
            return;
        }

        const trimmedQuery = query.trim();
        const currentPage = window.currentPage || 'unknown';

        if (currentPage === 'folders') {
            const searchEvent = new CustomEvent('global-search', {
                detail: {
                    query: trimmedQuery,
                    source: 'header',
                    timestamp: new Date().toISOString()
                },
                bubbles: true
            });

            document.dispatchEvent(searchEvent);
        } else {
            if (typeof window.loadPage === 'function') {
                window.pendingSearchQuery = trimmedQuery;
                window.loadPage('folders');
            } else {
                console.error('loadPage function not available');
            }
        }
    }

    clearSearch() {
        if (this.clearingInProgress) {
            return;
        }

        this.clearingInProgress = true;

        try {
            const searchInput = document.getElementById('global-search-input');
            const clearBtn = document.getElementById('clear-search-icon');

            if (searchInput) {
                searchInput.value = '';
                this.query = '';
            }

            if (clearBtn) {
                clearBtn.classList.add('hidden');
            }

            const clearEvent = new CustomEvent('global-search-clear', {
                detail: {
                    source: 'header',
                    timestamp: new Date().toISOString()
                },
                bubbles: true
            });

            setTimeout(() => {
                document.dispatchEvent(clearEvent);
                if (searchInput) {
                    setTimeout(() => {
                        searchInput.blur();
                    }, 100);
                }
                this.clearingInProgress = false;
            }, 50);
        } catch (error) {
            console.error('Error in clearSearch:', error);
            this.clearingInProgress = false;
        }
    }

    async getDaemonStatus() {
        try {
            const response = await fetch('/api/daemon/status');
            if (!response.ok) {
                throw new Error('Failed to get daemon status');
            }
            return await response.json();
        } catch (error) {
            console.error('Error getting daemon status:', error);
            return { running: false };
        }
    }

    async startDaemon() {
        try {
            const response = await fetch('/api/daemon/start', { method: 'POST' });
            return await response.json();
        } catch (error) {
            console.error('Error starting daemon:', error);
            return { success: false, message: error.message };
        }
    }

    async stopDaemon() {
        try {
            const confirmed = await showConfirm(
                `Stop Monitoring Your Files?`,
                'The backup service will save all existing metadata and immediately cease all active surveillance of your files. All background tasks will stop.',
                {
                    confirmText: 'Stop Daemon',
                    cancelText: 'Cancel',
                    confirmType: 'danger',
                    onConfirm: async () => {
                        try {
                            console.log('Sending stop request to daemon...');
                            
                            // Temporarily disable button and show stopping state
                            const daemonBtn = document.querySelector('.daemon-button');
                            if (daemonBtn) {
                                daemonBtn.disabled = true;
                                const text = daemonBtn.querySelector('.daemon-text');
                                if (text) text.textContent = 'Stopping...';
                            }
                            
                            const response = await fetch('/api/daemon/stop', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ mode: 'graceful' })
                            });

                            console.log('Stop response status:', response.status, response.statusText);
                            
                            // Parse response
                            let data;
                            try {
                                data = await response.json();
                            } catch (jsonError) {
                                console.error('Failed to parse JSON response:', jsonError);
                                throw new Error('Invalid response from server');
                            }
                            
                            console.log('Stop response data:', data);
                            
                            if (!response.ok) {
                                // Server returned error status
                                throw new Error(data.message || data.error || `Server error: ${response.status}`);
                            }
                            
                            // Check if daemon was already stopped (handle both possible messages)
                            const alreadyStoppedMessage = data.message?.toLowerCase() || '';
                            if (data.result === 'already_stopped' || 
                                alreadyStoppedMessage.includes('daemon is already') ||
                                alreadyStoppedMessage.includes('daemon is not running')) {
                                
                                // Daemon is already stopped - treat as success
                                console.log('Daemon was already stopped:', data.message);
                                
                                // Update local state
                                this.daemonRunning = false;
                                this.updateDaemonButton();
                                
                                // Show info message
                                showInfo(data.message || 'Daemon is already stopped');
                                
                                // Reset button state
                                this.daemonButtonLock = false;
                                if (daemonBtn) daemonBtn.disabled = false;
                                return;
                            }
                            
                            if (data.success && data.result === 'ok') {
                                // SUCCESS: Daemon stop requested
                                showInfo('Daemon is cleaning up files and saving metadata...');
                                
                                // Update local state
                                this.daemonRunning = false;
                                
                                // Start monitoring daemon exit
                                this.monitorDaemonExit();
                                
                            } else {
                                // FAILURE: Daemon stop failed
                                throw new Error(data.message || data.error || 'Failed to stop daemon');
                            }

                        } catch (error) {
                            console.error('Stop daemon error:', error);
                            showError(`Daemon stop failed: ${error.message}`);
                            
                            // Reset UI state
                            this.daemonButtonLock = false;
                            const daemonBtn = document.querySelector('.daemon-button');
                            if (daemonBtn) {
                                daemonBtn.disabled = false;
                            }
                            
                            // Re-check actual status
                            setTimeout(() => this.checkDaemonStatus(), 1000);
                        }
                    },
                    onCancel: () => {
                        console.log('User cancelled daemon stop');
                        // Reset button lock
                        this.daemonButtonLock = false;
                        const daemonBtn = document.querySelector('.daemon-button');
                        if (daemonBtn) daemonBtn.disabled = false;
                    }
                }
            );
            
            // If user cancels, exit early
            if (!confirmed) {
                this.daemonButtonLock = false;
                const daemonBtn = document.querySelector('.daemon-button');
                if (daemonBtn) daemonBtn.disabled = false;
            }
        } catch (error) {
            console.error('Error in confirmation dialog:', error);
            this.daemonButtonLock = false;
            const daemonBtn = document.querySelector('.daemon-button');
            if (daemonBtn) daemonBtn.disabled = false;
        }
    }

    monitorDaemonExit() {
        let checkCount = 0;
        const maxChecks = 60;
        
        const exitCheckInterval = setInterval(async () => {
            checkCount++;
            
            try {
                console.log(`Checking if daemon stopped (attempt ${checkCount}/${maxChecks})...`);
                
                await this.checkDaemonStatus();
                
                // Check if daemon is now stopped
                if (!this.daemonRunning) {
                    console.log('✓ Daemon has stopped');
                    clearInterval(exitCheckInterval);
                    
                    // Update UI
                    this.updateDaemonButton();
                    showSuccess('Daemon stopped successfully');
                    
                    // Clean up
                    this.isStopping = false;
                    this.daemonButtonLock = false;
                    
                    // Re-enable periodic checks
                    this.startMonitoring();
                    
                } else if (checkCount >= maxChecks) {
                    // Timeout - daemon still running after max checks
                    console.log('✗ Daemon still running after timeout');
                    clearInterval(exitCheckInterval);
                    
                    showWarning(`Daemon still running after ${maxChecks} seconds`);
                    
                    // Reset state
                    this.isStopping = false;
                    this.daemonButtonLock = false;
                    this.updateDaemonButton();
                    
                    // Ask about force stop
                    this.promptForceStop(maxChecks);
                }
                
            } catch (error) {
                console.error('Error monitoring daemon exit:', error);
            }
        }, 1000); // Check every second
    }

    startMonitoring() {
        // Clear any existing interval
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
        }
        
        // Start periodic status checks (every 5 seconds)
        this.checkInterval = setInterval(() => {
            this.checkDaemonStatus();
        }, 5000);
    }

    async promptForceStop(secondsElapsed) {
        const shouldForceStop = await showConfirm(
            'Daemon Still Running',
            `Daemon still running after ${secondsElapsed} seconds. Force stop?`,
            {
                confirmText: 'Force Stop',
                cancelText: 'Keep Trying',
                confirmType: 'danger',
                onConfirm: async () => {
                    await this.forceStopDaemon();
                },
                onCancel: () => {
                    // User wants to keep trying, restart monitoring
                    this.checkDaemonStatus();
                }
            }
        );
    }

    async forceStopDaemon() {
        try {
            console.log('Force stopping daemon...');
            
            const response = await fetch('/api/daemon/stop', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mode: 'immediate' })
            });

            console.log('Force stop response:', response);
            
            if (!response.ok) {
                let errorText;
                try {
                    const errorData = await response.json();
                    errorText = errorData.error || errorData.message || `Server error: ${response.status}`;
                } catch {
                    errorText = await response.text();
                }
                throw new Error(errorText || `Server error: ${response.status}`);
            }

            const data = await response.json();
            console.log('Force stop data:', data);
            
            if (data.success && data.result === 'ok') {
                showWarning('Daemon force stop requested');
                
                // Update state
                this.daemonRunning = false;
                this.updateDaemonButton();
                
                // Force UI update after short delay
                setTimeout(() => {
                    this.isStopping = false;
                    this.checkDaemonStatus();
                }, 1000);

            } else {
                throw new Error(data.message || data.error || 'Force stop failed');
            }

        } catch (error) {
            console.error('Force stop error:', error);
            showError(`Force stop failed: ${error.message}`);
            
            // Reset state
            this.isStopping = false;
            
            // Re-check status
            setTimeout(() => {
                this.checkDaemonStatus();
            }, 1000);
        }
    }

    pollForDaemonReady() {
        let pollCount = 0;
        const maxPolls = 60; // 60 * 2s = 120 seconds timeout

        const pollInterval = setInterval(async () => {
            pollCount++;

            if (pollCount > maxPolls) {
                clearInterval(pollInterval);
                showWarning('Daemon startup is taking longer than expected');
                return;
            }

            try {
                const response = await fetch('/api/daemon/ready-status');
                if (response.ok) {
                    const data = await response.json();

                    if (data.ready) {
                        // Daemon is fully ready
                        clearInterval(pollInterval);
                        this.checkDaemonStatus(); // Update UI
                    }
                }
            } catch (error) {
                // Ignore polling errors
            }
        }, 2000); // Check every 2 seconds
    }

    // Public method to manually trigger status check
    refreshStatus() {
        this.checkDaemonStatus();
    }

    showStatusHistory() {
        console.log('=== Daemon Status History ===');
        this.statusHistory.forEach((status, i) => {
            const time = new Date(status.timestamp).toLocaleTimeString();
            console.log(`${i+1}. ${time} - Running: ${status.running}, Ready: ${status.ready}, Message: ${status.message}`);
        });
        console.log('=============================');
    }

    async cleanupZombies() {
        try {
            const response = await fetch('/api/daemon/cleanup-zombies', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                const data = await response.json();
                if (data.zombies_cleaned > 0) {
                    console.log(`Cleaned ${data.zombies_cleaned} zombie processes`);
                    showWarning(`Cleaned ${data.zombies_cleaned} zombie processes`);
                }
            }
        } catch (error) {
            console.debug('Zombie cleanup error:', error);
        }
    }

    // async stopDaemon() {
    //     try {
    //         const response = await fetch('/api/daemon/stop', { method: 'POST' });
    //         return await response.json();
    //     } catch (error) {
    //         console.error('Error stopping daemon:', error);
    //         return { success: false, message: error.message };
    //     }
    // }

    updateDaemonButton() {
        const daemonBtn = document.querySelector('.daemon-button');
        if (!daemonBtn) {
            console.warn('Daemon button not found in DOM');
            return;
        }

        const icon = daemonBtn.querySelector('.daemon-icon');
        const text = daemonBtn.querySelector('.daemon-text');

        if (!icon || !text) {
            console.warn('Daemon button icon or text not found');
            return;
        }

        // Reset all classes
        daemonBtn.className = 'daemon-button flex items-center gap-1.5 px-3 py-1.5 rounded-md shadow-sm transition-colors text-xs font-semibold';

        // Update monitoring status color based on daemon state
        this.updateMonitoringStatus();

        console.log('Updating button - daemonRunning:', this.daemonRunning);

        if (this.daemonRunning) {
            // DAEMON IS RUNNING - Show "Stop" button (red/orange)
            daemonBtn.classList.add('bg-red-500', 'hover:bg-red-600', 'text-white', 'border', 'border-transparent');
            icon.textContent = 'stop';
            text.textContent = 'Stop';
            console.log('✓ Button set to STOP (daemon is running)');
        } else {
            // DAEMON IS STOPPED - Show "Run" button (green)
            daemonBtn.classList.add('bg-green-500', 'hover:bg-green-600', 'text-white', 'border', 'border-transparent');
            icon.textContent = 'play_arrow';
            text.textContent = 'Run';
            console.log('✓ Button set to RUN (daemon is stopped)');
        }
    }

    updateMonitoringStatus() {
        // Update the text label
        this.startMonitoringAnimation();
        
        // Update the indicator colors
        const monitorPing = document.querySelector('.monitor-ping');
        const monitorDot = document.querySelector('.monitor-dot');
        
        if (monitorPing && monitorDot) {
            if (this.daemonRunning) {
                // Daemon running - green
                monitorPing.classList.remove('bg-gray-400', 'opacity-50');
                monitorPing.classList.add('bg-green-400', 'opacity-75');
                monitorDot.classList.remove('bg-gray-500');
                monitorDot.classList.add('bg-green-500');
            } else {
                // Daemon stopped - gray
                monitorPing.classList.remove('bg-green-400', 'opacity-75');
                monitorPing.classList.add('bg-gray-400', 'opacity-50');
                monitorDot.classList.remove('bg-green-500');
                monitorDot.classList.add('bg-gray-500');
            }
        }
    }

    async waitForDaemonState(targetState, maxWaitMs = 30000, pollIntervalMs = 500) {
        /**
         * Poll daemon status until it reaches the target state.
         * targetState: 'running' or 'stopped'
         * Returns: true if target state reached, false if timeout
         */
        const startTime = Date.now();
        const isRunning = targetState === 'running';
        
        while (Date.now() - startTime < maxWaitMs) {
            try {
                const response = await fetch('/api/daemon/ready-status');
                if (!response.ok) {
                    console.log('Status check failed, retrying...');
                    await new Promise(r => setTimeout(r, pollIntervalMs));
                    continue;
                }
                
                const data = await response.json();
                const elapsed = Math.round((Date.now() - startTime) / 1000);
                
                if (isRunning) {
                    // Waiting for daemon to be fully ready
                    if (data.ready && data.running) {
                        console.log(`✓ Daemon is READY (confirmed after ${elapsed}s)`);
                        return true;
                    } else {
                        console.log(`... Daemon starting... ready=${data.ready}, running=${data.running} (${elapsed}s)`);
                    }
                } else {
                    // Waiting for daemon to be fully stopped
                    if (!data.running) {
                        console.log(`✓ Daemon is STOPPED (confirmed after ${elapsed}s)`);
                        return true;
                    } else {
                        console.log(`... Daemon stopping... running=${data.running} (${elapsed}s)`);
                    }
                }
                
                // Wait before polling again
                await new Promise(r => setTimeout(r, pollIntervalMs));
            } catch (error) {
                console.log(`Poll error: ${error.message}, retrying...`);
                await new Promise(r => setTimeout(r, pollIntervalMs));
            }
        }
        
        console.error(`✗ Timeout waiting for daemon to be ${targetState} (waited ${maxWaitMs}ms)`);
        return false;
    }

    setupDaemonButton() {
        const daemonBtn = document.querySelector('.daemon-button');
        if (!daemonBtn) return;

        daemonBtn.addEventListener('click', async () => {
            // Prevent double clicks
            if (this.daemonButtonLock) {
                console.log('Button is locked, ignoring click');
                return;
            }

            this.daemonButtonLock = true;
            daemonBtn.disabled = true;
            
            // Show loading state
            const icon = daemonBtn.querySelector('.daemon-icon');
            const text = daemonBtn.querySelector('.daemon-text');
            const originalIcon = icon.textContent;
            const originalText = text.textContent;
            
            icon.textContent = 'sync';
            icon.classList.add('animate-spin');
            
            try {
                console.log('Button clicked - current daemonRunning:', this.daemonRunning);
                
                if (this.daemonRunning) {
                    // Daemon is running, so STOP it
                    console.log('→ Stopping daemon...');
                    text.textContent = 'Stopping...';
                    await this.stopDaemon();
                    // stopDaemon handles its own verification now
                } else {
                    // Daemon is stopped, so START it
                    console.log('→ Starting daemon...');
                    text.textContent = 'Starting...';
                    
                    const response = await fetch('/api/daemon/start', { 
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' }
                    });
                    
                    if (!response.ok) {
                        let errorText;
                        try {
                            const errorData = await response.json();
                            errorText = errorData.error || errorData.message || `Server error: ${response.status}`;
                        } catch {
                            errorText = await response.text();
                        }
                        throw new Error(errorText || `Server error: ${response.status}`);
                    }
                    
                    const result = await response.json();
                    console.log('Start response:', result);
                    
                    if (result.success) {
                        console.log('→ Waiting for daemon to be FULLY READY...');
                        text.textContent = 'Waiting for daemon...';
                        
                        // WAIT for daemon to be 100% ready before updating UI
                        const isReady = await this.waitForDaemonState('running', 30000, 500);
                        
                        if (isReady) {
                            // Only now update state and UI
                            this.daemonRunning = true;
                            console.log('✓ Daemon confirmed RUNNING - updating button');
                            showSuccess('Daemon started and ready');
                            
                            // Update button and monitoring status
                            this.updateDaemonButton();
                            this.updateMonitoringStatus();
                        } else {
                            throw new Error('Daemon start request sent, but daemon did not become ready in time');
                        }
                    } else {
                        throw new Error(result.message || 'Failed to start daemon');
                    }
                }
                
            } catch (error) {
                console.error('✗ Error in daemon button handler:', error);
                showError(error.message || 'Failed to perform daemon action');
                
                // Re-check status to ensure accuracy
                console.log('→ Re-checking daemon status...');
                await this.checkDaemonStatus();
                
            } finally {
                // Always remove spinning animation
                icon.classList.remove('animate-spin');
                
                // Only restore original text if button is no longer locked
                if (!this.daemonButtonLock) {
                    icon.textContent = originalIcon;
                    text.textContent = originalText;
                }
                
                // Re-enable button
                setTimeout(() => {
                    daemonBtn.disabled = false;
                    this.daemonButtonLock = false;
                }, 500);
            }
        });
    }

    startMonitoringAnimation() {
        // Keep the icon animation but don't change the label text
        const statusEl = document.querySelector('.monitoring-status');
        if (!statusEl) return;

        // Label stays fixed as "Monitoring files..." or updates based on daemon status
        const textSpan = statusEl.querySelector('.monitoring-text');
        if (textSpan && this.daemonRunning) {
            textSpan.textContent = 'Monitoring files...';
        } else if (textSpan) {
            textSpan.textContent = 'Idle';
        }
    }

    updateSearchValue(value) {
        const searchInput = document.getElementById('global-search-input');
        const clearBtn = document.getElementById('clear-search-icon');

        this.query = value;

        if (searchInput) {
            searchInput.value = value;
        }

        if (clearBtn) {
            if (value) {
                clearBtn.classList.remove('hidden');
            } else {
                clearBtn.classList.add('hidden');
            }
        }
    }

    clear() {
        this.updateSearchValue('');
    }

    setCurrentPage(page) {
        this.currentPage = page;
        console.log('Header: Current page set to', page);
    }

    destroy() {
        console.log('Cleaning up Header');

        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
            this.monitoringInterval = null;
        }

        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
            this.searchTimeout = null;
        }

        const searchInput = document.getElementById('global-search-input');
        const clearBtn = document.getElementById('clear-search-icon');
        const daemonBtn = document.querySelector('.daemon-button');

        if (searchInput) {
            searchInput.replaceWith(searchInput.cloneNode(true));
        }

        if (clearBtn) {
            clearBtn.replaceWith(clearBtn.cloneNode(true));
        }

        if (daemonBtn) {
            daemonBtn.replaceWith(daemonBtn.cloneNode(true));
        }

        delete window.appHeader;
    }
}
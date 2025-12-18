/**
 * Manages backup daemon control
 */

export class DaemonControlManager {
    constructor(state, api, eventBus) {
        this.state = state;
        this.api = api;
        this.eventBus = eventBus;

        this.isProcessing = false;
        this.checkInterval = null;
        this.isStopping = false;
    }

    async init() {
        const button = document.getElementById('btn-daemon-control');
        if (!button) return;

        button.addEventListener('click', (e) => this.handleButtonClick(e));

        // Check initial status
        await this.checkDaemonStatus();

        // Start periodic checks
        this.checkInterval = setInterval(() => this.checkDaemonStatus(), 5000);

        // Check when page becomes visible
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.checkDaemonStatus();
            }
        });
    }

    async checkDaemonStatus() {
        if (this.isProcessing) return;
        this.isProcessing = true;

        try {
            const data = await this.api.getDaemonStatus();

            // Ignore updates if we're in the process of stopping
            if (this.isStopping) {
                this.isProcessing = false;
                return;
            }

            this.updateUI(data.running, data.ready, data.message);
        } catch (error) {
            console.error('[DaemonControl] Status check error:', error);
            this.updateUI(false, false, 'Connection error');
        } finally {
            this.isProcessing = false;
        }
    }

    updateUI(isRunning, isReady, message) {
        const button = document.getElementById('btn-daemon-control');
        const statusInfo = document.getElementById('daemon-status-info');
        const statusDot = statusInfo?.querySelector('.daemon-status-dot');
        const statusText = statusInfo?.querySelector('.daemon-status-text');

        if (!button || !statusInfo || !statusDot || !statusText) return;

        // Remove all state classes
        button.classList.remove('run', 'running', 'pause', 'error', 'stopping');

        if (isReady && isRunning) {
            // Daemon ready and running
            button.classList.add('pause');
            this.updateButtonContent(button, 'Pause', 'bi-pause-fill', 'Stop the daemon');
            this.updateStatusInfo(statusDot, statusText, 'ready', 'Ready & Running');
        } else if (isRunning && !isReady) {
            // Daemon starting up
            button.classList.add('running');
            this.updateButtonContent(button, 'Running...', 'bi-arrow-repeat spin', 'Daemon is starting up');
            this.updateStatusInfo(statusDot, statusText, 'starting', message || 'Starting up...');
        } else if (!isRunning) {
            // Daemon stopped
            button.classList.add('run');
            this.updateButtonContent(button, 'Run', 'bi-play-fill', 'Start the daemon');
            this.updateStatusInfo(statusDot, statusText, 'stopped', 'Stopped');
        }

        // Show status info
        statusInfo.classList.remove('hidden');
    }

    updateButtonContent(button, text, iconClass, title) {
        const icon = button.querySelector('.daemon-icon');
        const textSpan = button.querySelector('.daemon-text');

        if (icon) icon.className = `bi ${iconClass} daemon-icon`;
        if (textSpan) textSpan.textContent = text;
        button.title = title;
        button.disabled = button.classList.contains('running') || button.classList.contains('stopping');
    }

    updateStatusInfo(statusDot, statusText, state, text) {
        statusDot.classList.remove('ready', 'running', 'starting', 'stopped', 'error');
        statusDot.classList.add(state);
        statusText.textContent = text;
    }

    async handleButtonClick(event) {
        if (this.isProcessing) return;

        const button = event.currentTarget;
        const isRunning = button.classList.contains('pause');

        if (isRunning) {
            await this.stopDaemon();
        } else {
            await this.startDaemon();
        }
    }

    async startDaemon() {
        const button = document.getElementById('btn-daemon-control');
        if (!button) return;

        this.isProcessing = true;
        this.updateButtonContent(button, 'Starting...', 'bi-arrow-repeat spin', 'Starting daemon...');

        try {
            // Give Flask a moment to recover
            await new Promise(resolve => setTimeout(resolve, 1500));

            const data = await this.api.startDaemon();

            if (data.success) {
                this.eventBus.emit('notification:show', {
                    type: 'success',
                    title: 'Daemon Started',
                    message: 'Daemon started successfully! Initializing...'
                });

                // Poll for daemon to become ready
                this.pollForDaemonReady();
            } else {
                throw new Error(data.error || 'Failed to start daemon');
            }
        } catch (error) {
            console.error('[DaemonControl] Start failed:', error);
            this.updateButtonContent(button, 'Error', 'bi-exclamation-triangle-fill', 'Start failed');

            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Start Failed',
                message: error.message
            });

            // Revert button after error
            setTimeout(() => {
                this.checkDaemonStatus();
            }, 3000);
        } finally {
            this.isProcessing = false;
        }
    }

    async stopDaemon() {
        const confirmed = confirm(
            'Stop the backup daemon?\n\n' +
            'This will save all metadata and clean up files before exiting.'
        );

        if (!confirmed) return;

        this.isStopping = true;
        const button = document.getElementById('btn-daemon-control');

        if (button) {
            this.updateButtonContent(button, 'Stopping...', 'bi-hourglass-split', 'Daemon is cleaning up...');
            button.disabled = true;
        }

        // Stop periodic status checks
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }

        try {
            const data = await this.api.stopDaemon('graceful');

            if (data.result === 'ok') {
                this.eventBus.emit('notification:show', {
                    type: 'info',
                    title: 'Daemon Stopping',
                    message: 'Daemon is cleaning up files and saving metadata...'
                });

                // Monitor daemon exit
                this.monitorDaemonExit();
            } else {
                throw new Error('Failed to stop daemon');
            }
        } catch (error) {
            console.error('[DaemonControl] Stop failed:', error);
            this.isStopping = false;

            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Stop Failed',
                message: error.message
            });

            // Restore status checks
            this.checkInterval = setInterval(() => this.checkDaemonStatus(), 5000);
            this.checkDaemonStatus();
        }
    }

    async monitorDaemonExit() {
        let checkCount = 0;
        const maxChecks = 60;

        const exitCheckInterval = setInterval(async () => {
            checkCount++;

            try {
                const data = await this.api.getDaemonStatus();

                if (!data.running) {
                    // Daemon has fully stopped
                    clearInterval(exitCheckInterval);
                    this.isStopping = false;

                    // Force UI update
                    setTimeout(() => {
                        this.checkDaemonStatus();
                        this.eventBus.emit('notification:show', {
                            type: 'success',
                            title: 'Daemon Stopped',
                            message: `Daemon stopped successfully (${checkCount}s)`
                        });
                    }, 2000);

                    // Restart status checks
                    this.checkInterval = setInterval(() => this.checkDaemonStatus(), 5000);
                } else if (checkCount >= maxChecks) {
                    // Timeout
                    clearInterval(exitCheckInterval);
                    this.isStopping = false;

                    const offerForce = confirm(
                        `Daemon still running after ${checkCount} seconds.\n` +
                        'Force stop?'
                    );

                    if (offerForce) {
                        await this.forceStopDaemon();
                    } else {
                        this.checkDaemonStatus();
                    }
                }
            } catch (error) {
                // Ignore errors during monitoring
            }
        }, 1000);
    }

    async forceStopDaemon() {
        const confirmed = confirm(
            'Force stop daemon?\n\n' +
            'This will immediately terminate all operations.'
        );

        if (!confirmed) return;

        try {
            const data = await this.api.stopDaemon('immediate');

            if (data.result === 'ok') {
                this.eventBus.emit('notification:show', {
                    type: 'warning',
                    title: 'Force Stop',
                    message: 'Daemon force stop requested'
                });

                setTimeout(() => {
                    this.isStopping = false;
                    this.checkDaemonStatus();
                }, 1000);
            }
        } catch (error) {
            console.error('[DaemonControl] Force stop error:', error);
            this.isStopping = false;
            this.eventBus.emit('notification:show', {
                type: 'error',
                title: 'Force Stop Failed',
                message: error.message
            });
        }
    }

    pollForDaemonReady() {
        let pollCount = 0;
        const maxPolls = 60;

        const pollInterval = setInterval(async () => {
            pollCount++;

            if (pollCount > maxPolls) {
                clearInterval(pollInterval);
                this.eventBus.emit('notification:show', {
                    type: 'warning',
                    title: 'Daemon Startup',
                    message: 'Daemon startup is taking longer than expected'
                });
                return;
            }

            try {
                const data = await this.api.getDaemonStatus();

                if (data.ready) {
                    clearInterval(pollInterval);
                    this.eventBus.emit('notification:show', {
                        type: 'success',
                        title: 'Daemon Ready',
                        message: 'Daemon is fully operational!'
                    });
                }
            } catch (error) {
                // Ignore polling errors
            }
        }, 2000);
    }
}

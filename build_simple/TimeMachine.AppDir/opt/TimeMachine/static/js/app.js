/**
 * Time Machine UI - Main Application Entry Point
 */

import { AppState } from './state/AppState.js';
import { ApiClient } from './services/ApiClient.js';
import { UIManager } from './ui/UIManager.js';
import { FileManager } from './services/FileManager.js';
import { DeviceManager } from './services/DeviceManager.js';
import { MigrationManager } from './services/MigrationManager.js';
import { SettingsManager } from './services/SettingsManager.js';
import { NotificationManager } from './ui/NotificationManager.js';
import { ThemeManager } from './ui/ThemeManager.js';
import { ActivityFeedManager } from './services/ActivityFeedManager.js';
import { BackupManager } from './services/BackupManager.js';
import { DaemonControlManager } from './services/DaemonControlManager.js';
import { WebSocketClient } from './services/WebSocketClient.js';
import { EventBus } from './core/EventBus.js';

class TimeMachineApp {
    constructor() {
        // Initialize core systems
        this.eventBus = new EventBus();
        this.state = new AppState();
        this.api = new ApiClient();

        // Initialize managers
        this.ui = new UIManager(this.state, this.eventBus);
        this.notifications = new NotificationManager();
        this.theme = new ThemeManager();
        this.fileManager = new FileManager(this.state, this.api, this.eventBus);
        this.deviceManager = new DeviceManager(this.state, this.api, this.eventBus);
        this.migrationManager = new MigrationManager(this.state, this.api, this.eventBus);
        this.settingsManager = new SettingsManager(this.state, this.api, this.eventBus);
        this.activityFeed = new ActivityFeedManager(this.state, this.eventBus);
        this.backupManager = new BackupManager(this.state, this.api, this.eventBus);
        this.daemonManager = new DaemonControlManager(this.state, this.api, this.eventBus);
        this.webSocket = new WebSocketClient(this.state, this.eventBus);

        // Set up event listeners
        this.setupEventListeners();
    }

    async init() {
        try {
            console.log('[App] Initializing Time Machine UI...');

            // Initialize core systems
            this.theme.init();
            await this.state.init();

            // Load initial data
            await Promise.all([
                this.fileManager.initializeFileSystem(),
                              this.deviceManager.loadDevices(),
                              this.settingsManager.loadSettings(),
                              this.backupManager.updateUsage()
            ]);

            // Connect WebSocket
            this.webSocket.connect();

            // Start polling for updates
            this.startPolling();

            // Update UI
            this.ui.updateGreeting();
            this.ui.navigateToTab('overview');

            console.log('[App] Initialization complete');
        } catch (error) {
            console.error('[App] Initialization failed:', error);
            this.notifications.show('error', 'Initialization Error', 'Failed to initialize application');
        }
    }

    setupEventListeners() {
        // Navigation
        document.addEventListener('click', (e) => {
            const navButton = e.target.closest('[data-nav]');
            if (navButton) {
                e.preventDefault();
                const tabId = navButton.dataset.nav;
                this.ui.navigateToTab(tabId);
            }
        });

        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('change', (e) => {
                this.theme.toggle(e.target.checked);
            });
        }

        // Global event handlers
        this.eventBus.on('file:selected', (file) => this.fileManager.handleFileSelection(file));
        this.eventBus.on('device:selected', (device) => this.deviceManager.selectDevice(device));
        this.eventBus.on('migration:start', (options) => this.migrationManager.startMigration(options));
        this.eventBus.on('restore:requested', (data) => this.fileManager.handleRestoreRequest(data));
        this.eventBus.on('notification:show', (data) => this.notifications.show(data.type, data.title, data.message));

        // Window events
        window.addEventListener('beforeunload', () => {
            this.webSocket.disconnect();
        });
    }

    startPolling() {
        // Check connection status every 3 seconds
        setInterval(() => this.backupManager.checkConnection(), 3000);

        // Update usage every 5 seconds
        setInterval(() => this.backupManager.updateUsage(), 5000);

        // Update greeting clock every second
        setInterval(() => this.ui.updateGreeting(), 1000);
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new TimeMachineApp();
    window.app.init().catch(console.error);
});

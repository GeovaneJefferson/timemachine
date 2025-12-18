/**
 * Centralized application state management
 */

export class AppState {
    constructor() {
        // User state
        this.user = {
            plan: 'basic', // 'basic' | 'pro'
            name: 'User',
            username: ''
        };

        // Connection state
        this.connection = {
            isDeviceConnected: false,
            lastCheck: null,
            webSocketConnected: false
        };

        // Navigation state
        this.navigation = {
            currentTab: 'overview',
            activeSettingsTab: 'folders',
            breadcrumbStack: []
        };

        // File system state
        this.files = {
            fileSystem: null,
            currentFolder: null,
            selectedFile: null,
            searchQuery: ''
        };

        // Migration state
        this.migration = {
            selectedSource: null,
            selectionState: {
                home: false,
                flatpaks: false,
                installers: false
            },
            data: {
                home: [],
                flatpaks: [],
                installers: []
            },
            currentEditCategory: null
        };

        // Devices state
        this.devices = {
            list: [],
            selectedDevice: null
        };

        // Settings state
        this.settings = {
            general: {
                autoStartup: false,
                autoUpdates: true,
                showNotifications: true
            },
            watchedFolders: [],
            homeFolders: []
        };

        // UI state
        this.ui = {
            pendingAction: null,
            modals: {
                confirmation: null,
                proPlan: null,
                migrationDetail: null
            }
        };

        // Constants
        this.constants = {
            MAX_TRANSFER_ITEMS: 15
        };
    }

    async init() {
        try {
            // Load user name from backend
            const response = await fetch('/api/username');
            const data = await response.json();
            this.user.username = data.username || 'User';
            this.user.name = data.username.charAt(0).toUpperCase() + data.username.slice(1);
        } catch (error) {
            console.warn('[State] Could not load username:', error);
        }
    }

    // Getters
    get isProUser() {
        return this.user.plan === 'pro';
    }

    get hasActiveDevice() {
        return this.connection.isDeviceConnected && this.devices.selectedDevice;
    }

    // State update methods
    updateUserPlan(plan) {
        this.user.plan = plan;
        this.emit('state:userPlanUpdated', { plan });
    }

    updateConnectionStatus(isConnected) {
        const wasConnected = this.connection.isDeviceConnected;
        this.connection.isDeviceConnected = isConnected;
        this.connection.lastCheck = Date.now();

        if (wasConnected !== isConnected) {
            this.emit('state:connectionChanged', {
                isConnected,
                wasConnected
            });
        }
    }

    // Event emitter for state changes
    subscribers = new Map();

    on(event, callback) {
        if (!this.subscribers.has(event)) {
            this.subscribers.set(event, new Set());
        }
        this.subscribers.get(event).add(callback);
    }

    off(event, callback) {
        if (this.subscribers.has(event)) {
            this.subscribers.get(event).delete(callback);
        }
    }

    emit(event, data) {
        if (this.subscribers.has(event)) {
            this.subscribers.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`[State] Error in event handler for ${event}:`, error);
                }
            });
        }
    }
}

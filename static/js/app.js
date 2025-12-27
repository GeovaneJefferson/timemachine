/**
 * @file app.js
 * @description Main application entry point
 */

import { BackupManager, ActivityFeedManager } from './modules/dashboard.js';
import { checkBackupConnection, initializeTheme, getUsersName, nav } from './modules/ui-helpers.js';
import { BackupStatusClient } from './modules/websocket-client.js';
import { initElements } from './modules/globals.js';
import { initializeFileSystem } from './modules/file-system.js';

// Alias for backward compatibility
const DaemonControlManager = BackupManager;

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Initializing Time Machine Backup...');

    // Initialize UI components
    initElements();
    initializeTheme();
    getUsersName();

    // Initialize file system
    await initializeFileSystem();

    // Start WebSocket client for real-time updates
    window.backupStatusClient = new BackupStatusClient();

    // Start connection monitoring
    setInterval(checkBackupConnection, 10000);
    checkBackupConnection();

    // Initialize activity feed
    ActivityFeedManager.init();

    // Check daemon status immediately and then periodically
    DaemonControlManager.checkDaemonStatus();
    setInterval(() => {
        DaemonControlManager.checkDaemonStatus();
        DaemonControlManager.updateUsage();
        ActivityFeedManager.updateTimeAgo();
    }, 5000);

    // Set initial navigation
    nav('overview');

    console.log('Time Machine Backup initialized successfully');
});

// Make functions available globally
window.DaemonControlManager = DaemonControlManager;
window.ActivityFeedManager = ActivityFeedManager;
window.loadFolderContents = async () => {
    const { loadFolderContents } = await import('./modules/files.js');
    return loadFolderContents();
};

/**
 * @file ui-helpers.js
 * @description UI helper functions for navigation, theme, and notifications
 */

import { state } from './globals.js';
import { loadFolderContents } from './files.js';
import { initMigrationView } from './migration.js';  // Changed from files.js to migration.js
import { renderSettings } from './settings.js';
import { DeviceManager } from './devices.js';

// =====================================================================
// --- NAVIGATION ---
// =====================================================================

export function nav(tabId) {
    state.currentTabId = tabId;

    // 1. Sidebar Active States
    document.querySelectorAll('.btn-nav').forEach(btn => {
        btn.classList.remove('active', 'bg-blue-50', 'text-blue-600', 'dark:bg-blue-900/20', 'dark:text-blue-400');
        btn.classList.add('text-secondary');
    });

    const targetBtn = document.getElementById('btn-' + tabId);
    if (targetBtn) {
        targetBtn.classList.add('active');
        targetBtn.classList.remove('text-secondary');
    }

    // 2. View Switching
    ['overview', 'files', 'devices', 'migration', 'settings', 'logs'].forEach(t => {
        const view = document.getElementById('view-' + t);
        if (view) view.classList.add('hidden');
    });

        const targetView = document.getElementById('view-' + tabId);
        if (targetView) {
            targetView.classList.remove('hidden');
            targetView.classList.add('animate-entry');
        }

        // 3. Page Title Update
        const titles = {
            overview: 'Dashboard',
            files: 'File Explorer',
            devices: 'Backup Sources',
            migration: 'System Restore',
            settings: 'Preferences',
            logs: 'Console'
        };
        const titleEl = document.getElementById('page-title');
        if (titleEl) titleEl.innerText = titles[tabId] || 'Dashboard';

        // 4. Lazy Load Data
        if (tabId === 'devices') DeviceManager.load();
        if (tabId === 'files') {
            // Always load folder contents when navigating to files tab
            const { loadFolderContents } = await import('./files.js');
            loadFolderContents();
        }
        if (tabId === 'migration') {
            const { initMigrationView } = await import('./migration.js');
            initMigrationView();
        }
        if (tabId === 'settings') {
            const { renderSettings } = await import('./settings.js');
            renderSettings();
        }
}

// =====================================================================
// --- THEME MANAGEMENT ---
// =====================================================================

export function toggleTheme(e) {
    const isDark = e.target.checked;
    document.documentElement.classList.toggle('dark', isDark);

    const icon = document.getElementById('theme-icon');
    if(isDark) {
        icon.className = 'bi bi-sun-fill text-yellow-400';
    } else {
        icon.className = 'bi bi-moon-stars-fill text-brand-500';
    }
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

export function initializeTheme() {
    const saved = localStorage.getItem('theme');
    const isDark = saved === 'dark' || saved === null;
    document.documentElement.classList.toggle('dark', isDark);
    document.getElementById('theme-toggle').checked = isDark;

    const icon = document.getElementById('theme-icon');
    if(isDark) {
        icon.className = 'bi bi-sun-fill text-yellow-400';
    } else {
        icon.className = 'bi bi-moon-stars-fill text-brand-500';
    }
}

// =====================================================================
// --- SYSTEM NOTIFICATIONS ---
// =====================================================================

export function showSystemNotification(type, title, message, duration = 6000) {
    const container = document.getElementById('notification-container');
    if (!container) return;

    let iconClass = '';
    let colorClass = '';

    switch (type) {
        case 'success':
            iconClass = 'bi-check-circle-fill';
            colorClass = 'bg-green-600 text-white';
            break;
        case 'error':
            iconClass = 'bi-x-octagon-fill';
            colorClass = 'bg-red-500 text-white';
            break;
        case 'info':
        default:
            iconClass = 'bi-info-circle-fill';
            colorClass = 'bg-blue-600 text-white';
            break;
    }

    const toast = document.createElement('div');
    toast.className = `w-80 p-4 rounded-xl shadow-lg flex items-start gap-3 transition-all transform duration-300 pointer-events-auto opacity-0 -translate-y-full ${colorClass}`;

    toast.innerHTML = `
    <i class="bi ${iconClass} text-xl flex-shrink-0"></i>
    <div class="flex-grow">
    <h5 class="font-bold text-sm">${title}</h5>
    <p class="text-xs opacity-90">${message}</p>
    </div>
    `;

    container.appendChild(toast);

    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            toast.classList.remove('opacity-0', '-translate-y-full');
            toast.classList.add('opacity-100', 'translate-y-0');
        });
    });

    setTimeout(() => {
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', '-translate-y-full');

        setTimeout(() => {
            if (container.contains(toast)) {
                container.removeChild(toast);
            }
        }, 300);
    }, duration);
}

// =====================================================================
// --- USER INFO ---
// =====================================================================

export function getUsersName() {
    fetch('/api/username')
    .then(response => response.json())
    .then(data => {
        const name = data.username || 'User';
        const greetEl = document.getElementById('greeting');
        state.username = name.charAt(0).toUpperCase() + name.slice(1);
        greetEl.innerText = `Hello, ${state.username}`;
    });
}

// =====================================================================
// --- CONNECTION CHECK ---
// =====================================================================

export function checkBackupConnection() {
    const staticDotElement = document.getElementById('devices-connection-ping');
    const pingElement = document.getElementById('devices-connection-ping-animation');

    const wasDisconnectedBefore = !state.isDeviceConnected;

    if (!staticDotElement || !pingElement) {
        console.warn('Status UI elements not found. Check HTML IDs.');
        return;
    }

    fetch('/api/backup/connection')
    .then(response => {
        if (!response.ok) throw new Error('API network error');
        return response.json();
    })
    .then(data => {
        const isConnectedNow = data.connected;
        state.isDeviceConnected = isConnectedNow;

        if (isConnectedNow) {
            staticDotElement.classList.replace('status-dot-disconnected', 'status-dot-connected');
            pingElement.classList.replace('animate-ping-disconnected', 'animate-ping-connected');
        } else {
            staticDotElement.classList.replace('status-dot-connected', 'status-dot-disconnected');
            pingElement.classList.replace('animate-ping-connected', 'animate-ping-disconnected');
        }

        if (state.currentTabId === 'files' && wasDisconnectedBefore && isConnectedNow) {
            console.log("Device reconnected while on Files tab. Loading contents once.");
            loadFolderContents();
        } else if (state.currentTabId === 'files' && !wasDisconnectedBefore && !isConnectedNow) {
            console.log("Device disconnected while on Files tab. Showing disconnection message once.");
            loadFolderContents();
        }
    })
    .catch(error => {
        console.error("Connection check failed, setting UI to disconnected.", error);
        staticDotElement.classList.replace('status-dot-connected', 'status-dot-disconnected');
        pingElement.classList.replace('animate-ping-connected', 'animate-ping-disconnected');
        state.isDeviceConnected = false;
    });
}

// Make functions available globally for onclick handlers
window.nav = nav;
window.toggleTheme = toggleTheme;
window.showSystemNotification = showSystemNotification;

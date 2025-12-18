/**
 * @file script.js
 * @description Main client-side script for the Time Machine UI.
 * Handles Navigation, Devices, Migration Assistant, Files, and Settings.
 */


// =====================================================================
// --- 1. GLOBAL DATA & STATE ---
// =====================================================================

let userPlan = 'pro';
let username = 'User';
var isDeviceConnected = false;
let activeSettingsTab = 'folders';
let currentTabId = 'overview';
let generalSettings = {
    autoStartup: false,
    autoUpdates: true,
    showNotifications: true
};
let currentFolder = null;
let selectedFile = null;
let currentEditCat = null;
let selectedSource = null;
let fileSystem = null;
let pendingAction = null;
let timeStampInterval = null;  // Use to update items rows timestamps
let breadcrumbStack = [];
let migSelectionState = { home: false, flatpaks: false, installers: false };
let homeFolders = [];
let deviceData = [];

const MAX_TRANSFER_ITEMS = 10;


// =====================================================================
// --- 2. FILE SYSTEM INITIALIZATION ---
// =====================================================================

// Initialize fileSystem from backend API
async function initializeFileSystem() {
    try {
        // Step 1: Trigger backend file scanning
        const initResponse = await fetch('/api/search/init', { method: 'POST' });
        const initData = await initResponse.json();

        // if (initData.success) {
        //     console.log(`[FileSystem] Search initialized with ${initData.file_count || 0} files`);
        // }

        // Step 2: Create the fileSystem root structure
        fileSystem = {
            name: '.main_backup',
            type: 'folder',
            children: []
        };

        // Step 3: Initialize navigation stack
        breadcrumbStack = [fileSystem];
        currentFolder = fileSystem;

        // console.log('[FileSystem] Ready for file operations');
    } catch (error) {
        console.error('[FileSystem] Failed to initialize:', error);
        // Fallback: Create empty fileSystem
        fileSystem = {
            name: '.main_backup',
            type: 'folder',
            children: []
        };
        breadcrumbStack = [fileSystem];
        currentFolder = fileSystem;
    }
}


// =====================================================================
// --- WEBSOCKET CLIENT FOR Transfers FEED ---
// =====================================================================
class BackupStatusClient {
    constructor() {
        this.ws = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 10;
        this.reconnectDelay = 3000; // 3 seconds
        this.url = this.getWebSocketURL();
        this.isConnecting = false;
        this.pendingMessages = []; // Queue for messages while connecting

        // Auto-connect on creation
        this.connect();
    }

    getWebSocketURL() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        return `${protocol}//${window.location.host}/ws/transfers-feed`;
    }

    connect() {
        if (this.isConnecting) return;
        
        this.isConnecting = true;
        
        try {
            console.log(`[WebSocket] Attempting to connect to ${this.url}`);
            this.ws = new WebSocket(this.url);

            this.ws.onopen = () => {
                console.log('[WebSocket] ✓ Connected to transfers feed');
                this.reconnectAttempts = 0;
                this.isConnecting = false;
                
                // Send any pending messages
                this.flushPendingMessages();
            };

            this.ws.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    console.log('[WebSocket] Received message:', message);
                    ActivityFeedManager.handleMessage(message);
                } catch (e) {
                    console.error('[WebSocket] Error parsing message:', e, event.data);
                }
            };

            this.ws.onerror = (error) => {
                console.error('[WebSocket] Connection error:', error);
                this.isConnecting = false;
            };

            this.ws.onclose = (event) => {
                console.log(`[WebSocket] Connection closed. Code: ${event.code}, Reason: ${event.reason}`);
                this.isConnecting = false;
                this.attemptReconnect();
            };
        } catch (error) {
            console.error('[WebSocket] Failed to create connection:', error);
            this.isConnecting = false;
            this.attemptReconnect();
        }
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = this.reconnectDelay * Math.pow(1.5, this.reconnectAttempts - 1);
            console.log(`[WebSocket] Reconnecting in ${Math.round(delay / 1000)}s (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            setTimeout(() => this.connect(), delay);
        } else {
            console.warn('[WebSocket] Max reconnect attempts reached. Activity feed will not receive live updates.');
        }
    }

    disconnect() {
        if (this.ws) {
            this.ws.close(1000, 'Client disconnecting');
            this.ws = null;
        }
        this.isConnecting = false;
        this.pendingMessages = [];
    }

    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }

    // Safe message sending
    send(message) {
        if (this.isConnected()) {
            try {
                this.ws.send(JSON.stringify(message));
            } catch (e) {
                console.warn('[WebSocket] Failed to send message:', e);
                // Queue the message for later
                this.pendingMessages.push(message);
            }
        } else {
            // Queue message until connected
            this.pendingMessages.push(message);
        }
    }

    // Send queued messages when connection is established
    flushPendingMessages() {
        while (this.pendingMessages.length > 0 && this.isConnected()) {
            const message = this.pendingMessages.shift();
            try {
                this.ws.send(JSON.stringify(message));
            } catch (e) {
                console.warn('[WebSocket] Failed to send pending message:', e);
                // Put it back in the queue
                    this.pendingMessages.unshift(message);
                    break;
                }
            }
        }
    }

// Initialize the global WebSocket client
window.backupStatusClient = new BackupStatusClient();


// DATA: Migration Content (Migration Step 2)
const migrationData = {
    home: [
        { id: 'h1', name: 'Documents', size: '12 GB', icon: 'bi-file-earmark-text', color: 'text-yellow-500', selected: true },
        { id: 'h2', name: 'Pictures', size: '45 GB', icon: 'bi-image', color: 'text-purple-500', selected: true },
        { id: 'h3', name: 'Music', size: '8 GB', icon: 'bi-music-note-beamed', color: 'text-pink-500', selected: true },
        { id: 'h4', name: '.ssh (Keys)', size: '4 KB', icon: 'bi-key-fill', color: 'text-slate-500', selected: true },
        { id: 'h5', name: '.config', size: '150 MB', icon: 'bi-gear-fill', color: 'text-slate-500', selected: true }
    ],
    flatpaks: [
        { id: 'f1', name: 'Spotify', desc: 'Music Streaming', icon: 'bi-spotify', color: 'text-green-500', selected: true },
        { id: 'f2', name: 'Obsidian', desc: 'Note Taking', icon: 'bi-journal-text', color: 'text-purple-600', selected: true },
        { id: 'f3', name: 'VLC Media Player', desc: 'Video', icon: 'bi-cone-striped', color: 'text-orange-500', selected: true }
    ],
    installers: [
        { id: 'i1', name: 'google-chrome-stable.deb', desc: 'Found in /Downloads', size: '105 MB', icon: 'bi-browser-chrome', color: 'text-red-500', selected: true },
        { id: 'i2', name: 'visual-studio-code.rpm', desc: 'Found in /Downloads', size: '120 MB', icon: 'bi-code-slash', color: 'text-blue-500', selected: true },
        { id: 'i3', name: 'discord-0.0.5.deb', desc: 'Found in /Downloads', size: '85 MB', icon: 'bi-discord', color: 'text-indigo-500', selected: true },
        { id: 'i4', name: 'steam_latest.deb', desc: 'Found in /Downloads', size: '12 MB', icon: 'bi-controller', color: 'text-slate-800', selected: true }
    ]
};


// =====================================================================
// --- PRO FEATURE: RESTRICT START RESTORE BUTTON ---
// =====================================================================

/**
 * Checks if user has Pro access before starting restore
 */
function checkProBeforeRestore() {
    if (userPlan === 'pro') {
        startMigrationProcess();
    } else {
        showSystemNotification('info', 'Pro Feature Required', 'Upgrade to Pro to start system restoration.');
        openProPlanModal();
    }
}

/**
 * Updates the restore button based on user plan and selection state
 */
function updateRestoreButton() {
    const btn = document.getElementById('btn-start-restore');
    if (!btn) return;

    const hasSelection = Object.values(migSelectionState).some(v => v);
    const span = btn.querySelector('span');
    const cancel_restore_btn = document.getElementById('cancel-restore-btn')

    if (userPlan === 'pro') {
        // Pro user: Use default brand colors
        if (hasSelection) {
            btn.disabled = false;
            btn.className = "bg-brand-600 text-white hover:bg-brand-700 px-8 py-3 rounded-xl font-bold text-sm transition flex items-center gap-2 shadow-sm cursor-pointer";
            btn.onclick = startMigrationProcess;
            // Show restore cancel button
            if (cancel_restore_btn) {
                cancel_restore_btn.classList.remove('hidden');
            }
        } else {
            btn.disabled = true;
            btn.className = "bg-slate-200 text-slate-400 dark:bg-slate-700 dark:text-slate-500 px-8 py-3 rounded-xl font-bold text-sm transition cursor-not-allowed flex items-center gap-2";
            btn.onclick = null;
        }
        // Remove star icon for Pro users
        const starIcon = btn.querySelector('.bi-star-fill');
        if (starIcon) {
            starIcon.remove();
        }
    } else {
        // Basic user: Show Pro upgrade style with gradient and star
        btn.disabled = false;
        btn.className = "bg-gradient-to-r from-brand-600 to-purple-600 text-white hover:from-brand-700 hover:to-purple-700 px-8 py-3 rounded-xl font-bold text-sm transition flex items-center gap-2 shadow-sm cursor-pointer";
        btn.onclick = checkProBeforeRestore;

        // Ensure star icon exists for Basic users
        const starIcon = btn.querySelector('.bi-star-fill');
        if (!starIcon) {
            const newStarIcon = document.createElement('i');
            newStarIcon.className = 'bi bi-star-fill text-yellow-400 mr-1';
            btn.insertBefore(newStarIcon, btn.querySelector('span'));
        }
    }

    // Always ensure correct button text
    if (span) {
        span.textContent = "Start Restore";
    }
}

/**
 * Updates user plan and UI accordingly
 */
function updateUserPlan(plan) {
    userPlan = plan;
    updateProUI();
}


/**
 * Updates all UI elements based on user plan
 */
function updateProUI() {
    // Update restore button first
    updateRestoreButton();

    // Update dashboard status
    updateDashboardStatus();
}


// =====================================================================
// --- UI HELPERS ---
// =====================================================================

function nav(tabId) {
    currentTabId = tabId;  // Track current tab globally

    // 1. Sidebar Active States
    document.querySelectorAll('.btn-nav').forEach(btn => {
        btn.classList.remove('active', 'bg-blue-50', 'text-blue-600', 'dark:bg-blue-900/20', 'dark:text-blue-400');
        // Reset to default
        btn.classList.add('text-secondary');
    });

    const targetBtn = document.getElementById('btn-' + tabId);
    if (targetBtn) {
        targetBtn.classList.add('active'); // CSS handles the styling via .active class
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
        // Add subtle entry animation class if supported
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
    if (tabId === 'files' && currentFolder && Array.isArray(currentFolder.children) && currentFolder.children.length === 0) loadFolderContents();
    if (tabId === 'migration') initMigrationView();
    if (tabId === 'settings') renderSettings();
}

function getUsersName() {
    // Greeting with real username from backend
    fetch('/api/username')
    .then(response => response.json())
    .then(data => {
        const name = data.username || 'User';
        const greetEl = document.getElementById('greeting');
        username = name.charAt(0).toUpperCase() + name.slice(1);
        greetEl.innerText = `Hello, ${username}`;
    });
}

function checkBackupConnection() {
    // 1. Get elements and capture PREVIOUS state
    const staticDotElement = document.getElementById('devices-connection-ping');
    const pingElement = document.getElementById('devices-connection-ping-animation');

    // Capture the state *before* the API call
    const wasDisconnectedBefore = !isDeviceConnected;

    if (!staticDotElement || !pingElement) {
        console.warn('Status UI elements not found. Check HTML IDs.');
        return;
    }

    // Check backup connection status from backend, in loop
    fetch('/api/backup/connection')
    .then(response => {
        if (!response.ok) throw new Error('API network error');
        return response.json();
    })
    .then(data => {
        const isConnectedNow = data.connected;
        isDeviceConnected = isConnectedNow; // Set the new state immediately

        // ------------------ UI UPDATE LOGIC ------------------
        if (isConnectedNow) {
            // Connected (Green)
            staticDotElement.classList.replace('status-dot-disconnected', 'status-dot-connected');
            pingElement.classList.replace('animate-ping-disconnected', 'animate-ping-connected');
        } else {
            // Disconnected (Red)
            staticDotElement.classList.replace('status-dot-connected', 'status-dot-disconnected');
            pingElement.classList.replace('animate-ping-connected', 'animate-ping-disconnected');
        }

        // ------------------ STATE TRANSITION LOGIC ------------------

        // 1. Check for RECONNECTION (Transition: Disconnected -> Connected)
        // wasDisconnectedBefore is true AND isConnectedNow is true
        if (currentTabId === 'files' && wasDisconnectedBefore && isConnectedNow) {
            console.log("Device reconnected while on Files tab. Loading contents once.");
            // loadFolderContents will now run knowing isDeviceConnected is TRUE.
            loadFolderContents();
        }

        // 2. Check for DISCONNECTION (Transition: Connected -> Disconnected)
        // wasDisconnectedBefore is false AND isConnectedNow is false
        else if (currentTabId === 'files' && !wasDisconnectedBefore && !isConnectedNow) {
            console.log("Device disconnected while on Files tab. Showing disconnection message once.");
            // loadFolderContents will now run knowing isDeviceConnected is FALSE.
            // This triggers your container.innerHTML logic.
            loadFolderContents();
        }
    })
    .catch(error => {
        // Disconnected (Red) on API failure
        console.error("Connection check failed, setting UI to disconnected.", error);

        // Ensure UI and global state reflect disconnection on error
        staticDotElement.classList.replace('status-dot-connected', 'status-dot-disconnected');
        pingElement.classList.replace('animate-ping-connected', 'animate-ping-disconnected');
        isDeviceConnected = false;
    });
}


// =====================================================================
// --- 3. DEVICES TAB LOGIC ---
// =====================================================================

function renderDevices(devices) {
    const container = document.getElementById('device-list-container');
    if (!container) return;
    container.innerHTML = '';

    if (!devices || devices.length === 0) {
        container.innerHTML = `<p class="text-gray-400 text-center col-span-3">No devices found.</p>`;
        return;
    }

    devices.forEach(device => {
        console.log(device);
        const usagePercent = Math.round((device.usedGB / device.totalGB) * 100);
        let statusBadgeClass = device.status === 'Active' ? 'bg-green-100 text-green-700' : (device.status === 'Error' ? 'bg-red-100 text-red-700' : 'bg-gray-100 text-gray-700');
        let statusIcon = device.status === 'Active' ? 'bi-check-circle-fill' : (device.status === 'Error' ? 'bi-exclamation-triangle-fill' : 'bi-power');
        let actionButton = device.status === 'Active'
            ? `<button disabled class="w-full py-2.5 rounded-lg text-xs font-bold bg-green-50 text-green-700 border border-green-200 cursor-default flex items-center justify-center gap-2"><i class="bi bi-check-circle-fill"></i> Currently Active</button>`
            : `<button onclick="useThisBackupDevice(${device})" class="w-full py-2.5 rounded-lg text-xs font-bold bg-white border border-brand-200 text-brand-600 hover:bg-brand-50 hover:border-brand-300 transition shadow-sm flex items-center justify-center gap-2"><i class="bi bi-hdd-network"></i> Use as backup device</button>`;

        const deviceCard = `
            <div id="device-${device.id}" class="bg-white p-6 rounded-xl border border-gray-200 shadow-lg hover:shadow-xl transition flex flex-col h-full">
                <div class="flex items-start justify-between mb-6">
                    <div class="flex items-center gap-4">
                        <i class="bi ${device.icon} text-3xl ${device.color}"></i>
                        <div>
                            <h4 class="font-bold text-lg">${device.name}</h4>
                            <span class="text-xs font-medium ${statusBadgeClass} px-2 py-0.5 rounded-full inline-flex items-center gap-1 mt-1"><i class="bi ${statusIcon} text-[10px]"></i> ${device.status}</span>
                        </div>
                    </div>
                </div>
                <div class="mb-6 flex-1">
                    <div class="flex justify-between text-xs text-gray-500 mb-2 font-medium"><span>Used: ${device.usedGB} GB</span><span>Total: ${device.totalGB} GB</span></div>
                    <div class="progress-bar-container h-2 bg-gray-100 rounded-full overflow-hidden"><div class="progress-bar-fill ${usagePercent > 80 ? 'bg-red-500' : 'bg-brand-500'} h-full rounded-full transition-all duration-500" style="width: ${usagePercent}%"></div></div>
                </div>
                <div class="pt-4 border-t border-gray-50 mt-auto">${actionButton}</div>
            </div>`;
        container.innerHTML += deviceCard;
    });
}

function refreshDevices() {
    const container = document.getElementById('device-list-container');
    if(container) {
        container.innerHTML = `
            <div class="col-span-3 bg-white p-10 rounded-xl border border-gray-200 shadow-sm flex flex-col items-center justify-center text-center">
                <i class="bi bi-arrow-clockwise animate-spin text-2xl text-brand-500 mb-3"></i>
                <p class="text-sm text-brand-600 font-medium">Scanning for new devices...</p>
            </div>`;
        DeviceManager.load();
    }
}


// =====================================================================
// --- 4. MIGRATION ASSISTANT LOGIC (Workflow) ---
// =====================================================================

function initMigrationView() {
    // Reset Steps
    document.getElementById('mig-step-1-source').classList.remove('hidden');
    document.getElementById('mig-step-2-content').classList.add('hidden');
    document.getElementById('mig-step-3-progress').classList.add('hidden');
    document.getElementById('mig-step-desc').innerText = "Select a source to start the restoration process.";

    // Auto-Scan
    renderSourceList();
}

function renderSourceList() {
    const container = document.getElementById('mig-source-list');
    if (!container) return;

    container.innerHTML = `
        <div class="text-center py-10 text-muted">
            <i class="bi bi-arrow-clockwise animate-spin text-2xl mb-2"></i>
            <p class="text-sm">Scanning for backup sources...</p>
        </div>
    `;

    fetch('/api/migration/sources')
        .then(res => res.json())
        .then(data => {            
            container.innerHTML = '';
            if (!data.success || !data.sources || data.sources.length === 0) {
                container.innerHTML = `
                    <div class="text-center p-10 border-2 border-dashed border-main rounded-2xl text-muted">
                        <i class="bi bi-hdd-network-off text-4xl mb-3"></i>
                        <h4 class="font-bold text-main">No Backup Sources Found</h4>
                        <p class="text-sm mt-1">Connect a drive with a Time Machine backup and try again.</p>
                    </div>`;
                return;
            }

            // Use the fetched sources to render the list
            data.sources.forEach(device => {
                console.log(device.mount_point);
                // Device's name
                const device_name = device.mount_point.split('/').pop();
                const totalGB = Math.round((device.total || 0) / (1024**3));
                const card = `
                    <div onclick='selectSource(${JSON.stringify(device).replace(/'/g, "\\'")})' class="bg-card border border-main rounded-2xl p-5 flex items-center gap-5 hover:border-brand-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer transition-all group">
                        <div class="w-16 h-16 rounded-xl bg-blue-50 dark:bg-blue-900/20 text-blue-500 flex items-center justify-center text-3xl border border-main">
                            <i class="bi bi-usb-drive-fill"></i>
                        </div>
                        <div class="flex-1">
                            <h4 class="font-bold text-main text-lg">${device_name}</h4>
                            <p class="text-xs text-muted">${device.filesystem} • ${totalGB} GB</p>
                        </div>
                        <i class="bi bi-chevron-right text-muted text-xl opacity-0 group-hover:opacity-100 transition-opacity"></i>
                    </div>
                `;
                container.innerHTML += card;
            });
        });
}

function selectSource(device) {
    if (!device) {
        console.error("Invalid device object passed to selectSource.");
        return;
    }
    selectedSource = device;

    document.getElementById('mig-step-1-source').classList.add('hidden');
    document.getElementById('mig-step-2-content').classList.remove('hidden');
    document.getElementById('mig-step-desc').innerText = "Step 2 of 3: Choose what to restore from the backup.";

    migSelectionState = { home: false, flatpaks: false, installers: false };

    // Simulate scanning for content
    document.getElementById('desc-flatpaks').innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-1"></i> Scanning...';
    document.getElementById('desc-installers').innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-1"></i> Scanning...';

    // Display total backup size
    const total_user_size_data = document.getElementById('total-user-size-data');
    if (!total_user_size_data) return;
    
    fetch('/api/backup/total-size')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Create a formatted display with icon
                total_user_size_data.innerHTML = `
                    <span class="inline-flex items-center gap-1">
                        <i class="bi bi-hdd-fill text-brand-500"></i>
                        ${data.human_readable}
                    </span>
                `;
                
                // Add tooltip with more info
                total_user_size_data.title = `Total backup size: ${data.human_readable}\nCalculated: ${new Date().toLocaleTimeString()}`;
                
                // Update visual indicators
                total_user_size_data.className = 'text-sm font-bold';
                
                // Color coding based on size
                const gbSize = data.total_bytes / (1024**3);
                if (gbSize > 100) {
                    total_user_size_data.classList.add('text-orange-500');
                } else if (gbSize > 10) {
                    total_user_size_data.classList.add('text-brand-600');
                } else {
                    total_user_size_data.classList.add('text-emerald-600');
                }
                
                // Also update other elements that might show backup size
                // updateBackupSizeInOtherElements(data);
                
            } else {
                // Show error
                total_user_size_data.innerHTML = `
                    <span class="inline-flex items-center gap-1 text-red-500">
                        <i class="bi bi-exclamation-triangle"></i>
                        N/A
                    </span>
                `;
                total_user_size_data.title = `Error: ${data.error || 'Failed to calculate backup size'}`;
            }
        })
        .catch(error => {
            console.error('Failed to fetch backup size:', error);
            total_user_size_data.innerHTML = `
                <span class="inline-flex items-center gap-1 text-red-500">
                    <i class="bi bi-wifi-off"></i>
                    Offline
                </span>
            `;
            total_user_size_data.title = 'Network error. Check connection.';
        });

    setTimeout(() => {
        migSelectionState = { home: true, flatpaks: true, installers: true };
    }, 800);
}

function backToSourceStep() {
    document.getElementById('mig-step-2-content').classList.add('hidden');
    document.getElementById('mig-step-1-source').classList.remove('hidden');
    document.getElementById('mig-step-desc').innerText = "Select a source to start the restoration process.";
}


function toggleMigrationItem(key) {
    migSelectionState[key] = !migSelectionState[key];
    updateMigrationsContentUI();
}

function updateMigrationsContentUI() {
    ['home', 'flatpaks', 'installers'].forEach(key => {
        const card = document.getElementById(`mig-card-${key}`);
        const check = document.getElementById(`check-${key}`);
        const desc = document.getElementById(`desc-${key}`);
        const isActive = migSelectionState[key];
        const list = migrationData[key];
        const selectedCount = list.filter(i => i.selected).length;

        if (key === 'home' && isActive && desc) desc.innerText = "Calculated: 142 GB";
        else if (key === 'flatpaks' && desc) desc.innerText = `${selectedCount}/${list.length} Apps selected`;
        else if (key === 'installers' && desc) desc.innerText = `${selectedCount}/${list.length} Files selected`;

        if (isActive) {
            if (key === 'home') { card.classList.add('ring-4', 'ring-brand-500'); card.classList.remove('border-transparent'); if(check) check.classList.remove('opacity-0', 'scale-75'); }
            else { card.classList.add('border-brand-500', 'bg-brand-50', 'shadow-md'); card.classList.remove('border-gray-200', 'bg-white'); if(check) check.classList.remove('opacity-0', 'scale-75'); }
            // Corrected styling for dark mode
            card.classList.remove('bg-card', 'border', 'border-main'); // Remove default card styling
            card.classList.add('bg-blue-50', 'dark:bg-blue-900/20', 'border-blue-500', 'dark:border-blue-400', 'shadow-md');
            if(check) check.classList.remove('opacity-0', 'scale-75');
        } else {
            if (key === 'home') { card.classList.remove('ring-4', 'ring-brand-500'); card.classList.add('border-transparent'); if(check) check.classList.add('opacity-0', 'scale-75'); }
            else { card.classList.remove('border-brand-500', 'bg-brand-50', 'shadow-md'); card.classList.add('border-gray-200', 'bg-white'); if(check) check.classList.add('opacity-0', 'scale-75'); }
            // Revert to default card styling
            card.classList.remove('bg-blue-50', 'dark:bg-blue-900/20', 'border-blue-500', 'dark:border-blue-400', 'shadow-md');
            card.classList.add('bg-card', 'border', 'border-main'); // Add default card styling back
            if(check) check.classList.add('opacity-0', 'scale-75');
        }
    });

    updateRestoreButton();
}

// =====================================================================
// --- BACKUP SIZE CALCULATION & DISPLAY ---
// =====================================================================

/**
 * Calculate and display total backup size
 */
function calculateBackupSize() {
    const container = document.getElementById('backup-size-display');
    if (!container) return;
    
    container.innerHTML = `
        <div class="flex items-center gap-2 text-muted">
            <i class="bi bi-arrow-clockwise animate-spin"></i>
            <span>Calculating backup size...</span>
        </div>
    `;
    
    fetch('/api/backup/total-size')
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Update main display
                container.innerHTML = `
                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="text-sm font-medium text-main">Total Backup Size:</span>
                            <span class="text-lg font-bold text-brand-600 dark:text-brand-400">
                                ${data.human_readable}
                            </span>
                        </div>
                        
                        ${data.breakdown ? `
                            <div class="text-xs text-muted space-y-1">
                                ${data.breakdown.main ? `
                                    <div class="flex justify-between">
                                        <span>Main backup:</span>
                                        <span>${data.breakdown.main.human_readable}</span>
                                    </div>
                                ` : ''}
                                
                                ${data.breakdown.incremental ? `
                                    <div class="flex justify-between">
                                        <span>Incremental backups:</span>
                                        <span>${data.breakdown.incremental.human_readable}</span>
                                    </div>
                                ` : ''}
                                
                                ${data.breakdown.user_home ? `
                                    <div class="flex justify-between">
                                        <span>User home data:</span>
                                        <span>${data.breakdown.user_home.human_readable}</span>
                                    </div>
                                ` : ''}
                            </div>
                        ` : ''}
                    </div>
                `;
                
                // Also update dashboard if needed
                updateDashboardBackupSize(data);
            } else {
                container.innerHTML = `
                    <div class="text-red-500 text-sm">
                        <i class="bi bi-exclamation-triangle mr-1"></i>
                        ${data.error || 'Failed to calculate backup size'}
                    </div>
                `;
            }
        })
        .catch(err => {
            console.error('Failed to get backup size:', err);
            container.innerHTML = `
                <div class="text-red-500 text-sm">
                    <i class="bi bi-exclamation-triangle mr-1"></i>
                    Network error
                </div>
            `;
        });
}

/**
 * Update dashboard with backup size
 */
function updateDashboardBackupSize(data) {
    // Update in dashboard status card
    const backupSizeElement = document.getElementById('dashboard-backup-size');
    if (backupSizeElement) {
        backupSizeElement.textContent = data.human_readable;
    }
    
    // Update in migration assistant
    const migBackupSizeElement = document.getElementById('migration-backup-size');
    if (migBackupSizeElement) {
        migBackupSizeElement.textContent = data.human_readable;
    }
}

/**
 * Calculate backup size for a specific device (for migration sources)
 */
function calculateDeviceBackupSize(device) {
    if (!device || !device.mount_point) {
        return Promise.reject('Invalid device');
    }
    
    return fetch(`/api/backup/device-size?path=${encodeURIComponent(device.mount_point)}`)
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                return {
                    ...device,
                    backup_size: data.total_bytes,
                    backup_size_human: data.human_readable,
                    has_backup: true
                };
            } else {
                return {
                    ...device,
                    backup_size: 0,
                    backup_size_human: '0 B',
                    has_backup: false
                };
            }
        });
}

/**
 * Update migration source list with backup sizes
 */
function renderSourceListWithSizes() {
    const container = document.getElementById('mig-source-list');
    if (!container) return;

    container.innerHTML = `
        <div class="text-center py-10 text-muted">
            <i class="bi bi-arrow-clockwise animate-spin text-2xl mb-2"></i>
            <p class="text-sm">Scanning backup sources...</p>
        </div>
    `;

    // First get all storage devices
    fetch('/api/storage/devices')
        .then(res => res.json())
        .then(data => {
            if (!data.success || !data.devices || data.devices.length === 0) {
                container.innerHTML = noDevicesHTML();
                return;
            }

            // Check each device for backups and calculate sizes
            const checkPromises = data.devices.map(device => 
                calculateDeviceBackupSize(device)
            );

            Promise.all(checkPromises)
                .then(results => {
                    // Filter devices with backups
                    const backupDevices = results.filter(r => r.has_backup);
                    
                    if (backupDevices.length === 0) {
                        container.innerHTML = noBackupHTML();
                        return;
                    }

                    container.innerHTML = '';
                    
                    backupDevices.forEach(device => {
                        const card = `
                            <div onclick='selectSource(${JSON.stringify(device).replace(/'/g, "\\'")})' 
                            class="bg-card border border-main rounded-2xl p-5 flex items-center gap-5 hover:border-brand-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer transition-all group">
                                <div class="w-16 h-16 rounded-xl bg-blue-50 dark:bg-blue-900/20 text-blue-500 flex items-center justify-center text-3xl border border-main">
                                    <i class="bi bi-usb-drive-fill"></i>
                                </div>
                                <div class="flex-1">
                                    <h4 class="font-bold text-main text-lg">${device.label || device.name}</h4>
                                    <div class="flex items-center gap-2 mt-1">
                                        <span class="text-xs text-muted">
                                            ${device.filesystem} • ${Math.round(device.total / (1024**3))} GB
                                        </span>
                                        <span class="px-2 py-0.5 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-xs rounded-full">
                                            <i class="bi bi-check-circle-fill mr-1"></i> Time Machine
                                        </span>
                                    </div>
                                    <div class="mt-2">
                                        <p class="text-xs text-brand-600 dark:text-brand-400 font-medium">
                                            <i class="bi bi-hdd mr-1"></i> Backup size: ${device.backup_size_human}
                                        </p>
                                        <p class="text-xs text-muted">
                                            ${device.usedGB} GB used of ${device.totalGB} GB
                                        </p>
                                    </div>
                                </div>
                                <i class="bi bi-chevron-right text-muted text-xl opacity-0 group-hover:opacity-100 transition-opacity"></i>
                            </div>
                        `;
                        container.innerHTML += card;
                    });
                });
        })
        .catch(err => {
            console.error('Failed to load migration sources:', err);
            container.innerHTML = errorHTML(err.message);
        });
}

// Helper HTML templates
function noDevicesHTML() {
    return `
        <div class="text-center p-10 border-2 border-dashed border-main rounded-2xl text-muted">
            <i class="bi bi-hdd-network-off text-4xl mb-3"></i>
            <h4 class="font-bold text-main">No Devices Found</h4>
            <p class="text-sm mt-1">Connect a drive and try again.</p>
        </div>
    `;
}

function noBackupHTML() {
    return `
        <div class="text-center p-10 border-2 border-dashed border-main rounded-2xl text-muted">
            <i class="bi bi-hdd-network-off text-4xl mb-3"></i>
            <h4 class="font-bold text-main">No Backup Sources Found</h4>
            <p class="text-sm mt-1">Connect a drive with a Time Machine backup and try again.</p>
            <button onclick="refreshDevices()" class="mt-4 px-4 py-2 bg-brand-600 text-white rounded-lg text-sm hover:bg-brand-700 transition">
                <i class="bi bi-arrow-clockwise mr-2"></i> Scan Again
            </button>
        </div>
    `;
}

function errorHTML(message) {
    return `
        <div class="text-center p-10 border-2 border-dashed border-red-200 rounded-2xl text-red-500">
            <i class="bi bi-exclamation-triangle text-4xl mb-3"></i>
            <h4 class="font-bold">Failed to Load Backup Sources</h4>
            <p class="text-sm mt-1">Error: ${message}</p>
        </div>
    `;
}

function startMigrationProcess() {
    // Prepare UI
    const step2 = document.getElementById('mig-step-2-content');
    const step3 = document.getElementById('mig-step-3-progress');
    const desc = document.getElementById('mig-step-desc');
    if (step2) step2.classList.add('hidden');
    if (step3) step3.classList.remove('hidden');
    if (desc) desc.innerText = "Transferring data. Do not disconnect your drive.";

    // Elements
    const bar = document.getElementById('migration-progress-bar');
    const pct = document.getElementById('progress-percent');
    const status = document.getElementById('migration-status-text');
    const time = document.getElementById('time-remaining');
    const cancelBtn = document.getElementById('cancel-restore-btn');

    // Cancel handling
    let cancelled = false;
    if (cancelBtn) {
        cancelBtn.classList.remove('hidden');
        cancelBtn.disabled = false;
        cancelBtn.onclick = () => {
            cancelled = true;
            cancelBtn.disabled = true;
            if (status) { status.innerText = 'Cancelling...'; }
            showSystemNotification('info', 'Migration', 'Cancelling migration...');
        };
    }

    // Build processing queue from selected migration cards
    const filesToProcess = [];
    if (migSelectionState.home) migrationData.home.forEach(f => filesToProcess.push({ name: f.name || f, size: (f.size && typeof f.size === 'number') ? f.size : (Math.floor(Math.random() * 6) + 1) * 1024 * 1024 }));
    if (migSelectionState.flatpaks) migrationData.flatpaks.forEach(f => filesToProcess.push({ name: f.name || f, size: (f.size && typeof f.size === 'number') ? f.size : (Math.floor(Math.random() * 10) + 2) * 1024 * 1024 }));
    if (migSelectionState.installers) migrationData.installers.forEach(f => filesToProcess.push({ name: f.name || f, size: (f.size && typeof f.size === 'number') ? f.size : (Math.floor(Math.random() * 8) + 1) * 1024 * 1024 }));

    if (filesToProcess.length === 0) {
        showSystemNotification('info', 'Nothing to Migrate', 'No items selected for migration.');
        // Revert UI
        if (step2) step2.classList.remove('hidden');
        if (step3) step3.classList.add('hidden');
        return;
    }

    // Calculate totals
    const totalFiles = filesToProcess.length;
    const totalBytes = filesToProcess.reduce((s, f) => s + (f.size || 0), 0);
    let bytesProcessed = 0;
    const startTime = Date.now();

    // Helper to update progress UI
    function updateUI() {
        const percent = totalBytes > 0 ? Math.min(100, Math.round((bytesProcessed / totalBytes) * 100)) : 0;
        if (bar) bar.style.width = `${percent}%`;
        if (pct) pct.innerText = `${percent}%`;
        // ETA estimation
        const elapsed = (Date.now() - startTime) / 1000; // seconds
        const speed = elapsed > 0 ? bytesProcessed / elapsed : 0; // bytes/sec
        const remaining = Math.max(0, totalBytes - bytesProcessed);
        const etaSec = speed > 0 ? Math.round(remaining / speed) : -1;
        if (etaSec >= 0) {
            const mins = Math.floor(etaSec / 60);
            time.innerText = mins > 0 ? `${mins} min` : '< 1 min';
        } else {
            time.innerText = 'Calculating...';
        }
    }

    // Sequentially process files (simulated durations based on size)
    (async () => {
        for (let i = 0; i < filesToProcess.length; i++) {
            if (cancelled) break;
            const file = filesToProcess[i];

            // Indicate which file is being processed (restore flow)
            if (status) status.innerHTML = `<i class="bi bi-arrow-repeat animate-spin mr-2"></i> Restoring ${file.name}`;

            // Simulate file backup duration proportional to size (but bounded)
            const simulatedSecs = Math.min(6 + (file.size / (1024 * 1024)) * 0.25, 20); // 0.25s per MB, min ~6s, max 20s
            const startFile = Date.now();
            const fileTarget = file.size || (1 * 1024 * 1024);
            let fileProcessed = 0;

            // Animate per-file progress in small ticks
            await new Promise(resolve => {
                const tickMs = 250;
                const ticks = Math.max(4, Math.round((simulatedSecs * 1000) / tickMs));
                let tick = 0;
                const interval = setInterval(() => {
                    if (cancelled) {
                        clearInterval(interval);
                        resolve();
                        return;
                    }
                    tick++;
                    // increment processed bytes for this file
                    const increment = Math.round(fileTarget / ticks);
                    fileProcessed = Math.min(fileTarget, fileProcessed + increment);
                    bytesProcessed += increment;
                    if (bytesProcessed > totalBytes) bytesProcessed = totalBytes;
                    updateUI();

                    // Every few ticks, optionally show a lightweight toast
                    if (tick % Math.max(1, Math.round(ticks / 3)) === 0) {
                        // no-op for now, UI is updating
                    }

                    if (tick >= ticks || fileProcessed >= fileTarget) {
                        clearInterval(interval);
                        // Count as file completed
                        bytesProcessed = Math.min(totalBytes, bytesProcessed + Math.max(0, fileTarget - fileProcessed));
                        updateUI();
                        resolve();
                    }
                }, tickMs);
            });

            if (cancelled) break;

            // Mark file as restored in the live feed (restore flow)
            try {
                if (ActivityFeedManager && ActivityFeedManager.handleMessage) {
                    ActivityFeedManager.handleMessage({
                        type: 'file_activity',
                        title: 'Restored',
                        description: file.name,
                        size: file.size || 0,
                        timestamp: Date.now(),
                        status: 'success'
                    });
                }
            } catch (e) {
                console.warn('Failed to push file activity to feed:', e);
            }

            // Update status label per-file (show check icon briefly)
            if (status) status.innerHTML = `<i class="bi bi-check-lg text-emerald-500 mr-2"></i> Restored ${i + 1}/${totalFiles}: ${file.name}`;
        }

        // Finalize
        if (cancelled) {
            if (status) { status.innerHTML = '<i class="bi bi-x-circle-fill text-orange-500 mr-2"></i> Migration Cancelled'; status.className = 'text-orange-500 font-bold'; }
            showSystemNotification('info', 'Migration Cancelled', 'Migration was cancelled by the user.');
        } else {
            bytesProcessed = totalBytes;
            updateUI();
            if (status) { status.innerHTML = '<i class="bi bi-check-circle-fill text-green-600 mr-2"></i> Migration Complete!'; status.className = 'text-green-600 font-bold text-lg'; }
            if (time) time.innerText = 'Done';
            showSystemNotification('success', 'Migration Completed', `Migrated ${totalFiles} item${totalFiles !== 1 ? 's' : ''}.`);
        }

        // Clean up UI
        if (cancelBtn) { cancelBtn.classList.add('hidden'); cancelBtn.onclick = null; }
    })();
}


async function openCustomizeModal(category) {
    currentEditCat = category;
    const modal = document.getElementById('migration-detail-modal');
    const container = document.getElementById('detail-modal-container');
    const list = document.getElementById('detail-list-container');
    const title = document.getElementById('detail-modal-title');

    if (!modal || !container || !list || !title) return;

    let displayName = category === 'installers' ? 'Installers' : (category === 'flatpaks' ? 'Applications' : 'Folders');
    title.innerText = `Select ${displayName}`;

    list.innerHTML = '<div class="text-center p-4 text-muted"><i class="bi bi-arrow-clockwise animate-spin"></i> Loading...</div>';

    // Show modal
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    setTimeout(() => { container.classList.remove('scale-95', 'opacity-0'); container.classList.add('scale-100', 'opacity-100'); }, 10);

    // Fetch data if it's for 'home' folders, otherwise use static data
    if (category === 'home') {
        try {
            const response = await fetch(`/api/search/folder?path=`);
            const data = await response.json();

            if (data.success && data.items) {
                // Filter for folders and map to the structure migrationData expects
                migrationData.home = data.items
                    .filter(item => item.type === 'folder')
                    .map(folder => ({
                        id: folder.name,
                        name: folder.name,
                        icon: 'bi-folder-fill',
                        color: 'text-blue-500',
                        selected: true // Default to selected
                    }));
            } else {
                migrationData.home = [];
            }
        } catch (error) {
            console.error("Failed to fetch home folders for migration:", error);
            // TO REMOVE THIS MAIN showNotification, can just use showSystemNotfication
            // showNotification();
            showSystemNotification('error', 'Erro',
                `Failed to fetch home folders for migration:`, error);
            migrationData.home = [];
            list.innerHTML = '<div class="text-center p-4 text-red-500">Failed to load folders.</div>';
        }
    }

    // Render items
    list.innerHTML = ''; // Clear loading
    if (migrationData[category].length === 0) {
        list.innerHTML = '<div class="text-center p-4 text-muted">No items found.</div>';
    } else {
        migrationData[category].forEach((item, idx) => {
            const row = `
                <div onclick="toggleDetailItem(${idx})" class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-white/10 cursor-pointer transition-colors">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded-md bg-gray-100 dark:bg-white/5 flex items-center justify-center text-lg ${item.color || 'text-gray-500'}">
                            <i class="bi ${item.icon || 'bi-folder'}"></i>
                        </div>
                        <p class="text-sm font-bold text-main leading-none">${item.name}</p>
                    </div>
                    <div class="w-5 h-5 rounded border ${item.selected ? 'bg-brand-600 border-brand-600' : 'border-gray-300 bg-white'} flex items-center justify-center text-white text-xs">
                        ${item.selected ? '<i class="bi bi-check"></i>' : ''}
                    </div>
                </div>`;
            list.innerHTML += row;
        });
    }
}

function toggleDetailItem(idx) {
    migrationData[currentEditCat][idx].selected = !migrationData[currentEditCat][idx].selected;
    openCustomizeModal(currentEditCat);
}

function closeCustomizeModal() {
    const modal = document.getElementById('migration-detail-modal');
    const container = document.getElementById('detail-modal-container');
    if (modal && container) {
        container.classList.add('scale-95', 'opacity-0');
        container.classList.remove('scale-100', 'opacity-100');
        setTimeout(() => { modal.classList.add('hidden'); modal.classList.remove('flex'); }, 200);
    }
}


// =====================================================================
// --- 5. FILES TAB LOGIC ---
// =====================================================================
/**
 * Load folder contents from backend API
 */
async function loadFolderContents(folderPath = '') {
    const container = document.getElementById('file-list-container');
    // console.log("Is devive connected?", isDeviceConnected);

    // Handle no backup connection
    if (!isDeviceConnected) {
        const fileSearchField = document.getElementById('file-search-input');
        // Disable search input
        fileSearchField.disabled = true;
        container.innerHTML = `
            <div class="p-8 text-center text-muted">
                <i class="bi bi-exclamation-triangle-fill text-3xl mb-3"></i>
                <h4 class="font-bold text-main">No Backup Device Connected</h4>
                <p class="text-sm mt-1">Please connect your backup device to browse files.</p>
            </div>`;
        return;
    }

    // Instead, handle empty path:
    if (folderPath === null || folderPath === undefined) {
        folderPath = '';
    }

    // Show loading state
    container.innerHTML = `
        <div class="flex items-center gap-2 text-slate-500">
            <i class="bi bi-arrow-clockwise animate-spin"></i>
            <span>Loading folder...</span>
        </div>`;

    try {
        // Make sure path is properly encoded
        const encodedPath = encodeURIComponent(folderPath);
        const response = await fetch(`/api/search/folder?path=${encodedPath}`);
        const data = await response.json();
        console.log("Folder contents response:", data);

        if (data.success && data.items && data.items.length > 0) {
            // Add icons and colors to file items
            const enrichedItems = data.items.map(item => {
                if (item.type === 'file') {
                    item.icon = getIconForFile(item.name);
                    item.color = getColorForFile(item.name);
                } else if (item.type === 'folder') {
                    // Add folder-specific icons
                    item.icon = 'bi-folder-fill';
                    item.color = 'text-blue-500';
                }
                return item;
            });

            // Update currentFolder with the loaded items
            if (currentFolder) {
                currentFolder.children = enrichedItems;
            }
            renderExplorer(enrichedItems);
        } else {
            container.innerHTML = '<p class="p-4 text-gray-400">Folder is empty.</p>';
        }
    } catch (error) {
        console.error('Failed to load folder contents:', error);
        showSystemNotification('error', 'Erro',
            `Failed to load folder contents:`, error);
        container.innerHTML = '<p class="p-4 text-red-500">Failed to load folder contents.</p>';
    }
}

function renderExplorer(items = null) {
    const container = document.getElementById('file-list-container');
    const breadcrumb = document.getElementById('file-path-breadcrumb');

    // Breadcrumbs (no change)
    breadcrumb.innerHTML = breadcrumbStack.map((folder, index) => {
        const isLast = index === breadcrumbStack.length - 1;
        const folderName = folder.name || '/';
        const displayName = folderName.length > 20 ? folderName.substring(0, 17) + '...' : folderName;

        return `
            <div class="flex items-center flex-shrink-0">
                <span class="${isLast ? 'font-bold text-main' : 'text-brand-500 hover:underline cursor-pointer'}"
                      title="${folderName}"
                      onclick="${!isLast ? `MapsFolder(${index})` : ''}">
                    ${displayName}
                </span>
                ${!isLast ? '<i class="bi bi-chevron-right text-[10px] mx-2 text-muted"></i>' : ''}
            </div>
        `;
    }).join('');

    const itemsToRender = items || (currentFolder && currentFolder.children) || [];
    container.innerHTML = '';

    if (itemsToRender.length === 0) {
        container.innerHTML = '<div class="p-8 text-center text-muted text-sm">Folder is empty</div>';
        return;
    }

    // Sort: Folders first, then files, both alphabetically (no change)
    itemsToRender.sort((a, b) => {
        if (a.type === 'folder' && b.type !== 'folder') return -1;
        if (a.type !== 'folder' && b.type === 'folder') return 1;
        return a.name.localeCompare(b.name);
    });

    itemsToRender.forEach(item => {
        const isFolder = item.type === 'folder';
        const iconClass = isFolder ? 'bi-folder-fill text-blue-400' : getIconForFile(item.name);
        const iconColor = isFolder ? '' : getColorForFile(item.name);

        // Truncate for display, keep full name in title (no change)
        let displayName = item.name;
        if (item.name.length > 50) {
            displayName = item.name.substring(0, 47) + '...';
        }

        console.log("ITEM", item);

        // ------------------------------------------------------------------
        // FIX: Update getRelativePath to check for both backup roots
        // ------------------------------------------------------------------
        const getRelativePath = (fullPath) => {
            // 1. Check for the main backup root
            let backupIndex = fullPath.indexOf('.main_backup/');
            if (backupIndex !== -1) {
                return fullPath.substring(backupIndex + '.main_backup/'.length);
            }

            // 2. Check for the incremental version root
            // Assuming the incremental folder is named '.incremental_version'
            backupIndex = fullPath.indexOf('.incremental_version/');
            if (backupIndex !== -1) {
                return fullPath.substring(backupIndex + '.incremental_version/'.length);
            }

            // Fallback: return the last few segments if neither is found
            const parts = fullPath.split('/');
            return parts.slice(-3).join('/');
        };

        const relativePath = getRelativePath(item.path);

        const el = document.createElement('div');
        el.className = 'flex items-center gap-3 p-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5 cursor-pointer transition-colors group';
        el.innerHTML = `
            <i class="bi ${iconClass} ${iconColor} text-lg flex-shrink-0"></i>
            <div class="flex-1 min-w-0">
            <div class="text-sm text-main font-medium truncate" title="${item.name}">${displayName}</div>
            <div class="text-xs text-muted truncate mt-0.5" title="${item.path}">${relativePath}</div>
            </div>
            <i class="bi bi-chevron-right text-xs text-muted opacity-0 group-hover:opacity-100 transition-opacity"></i>
        `;

        el.onclick = () => {
            if(isFolder) openFolder(item);
            else selectFile(item);
        };
        container.appendChild(el);
    });
}

function openFolder(folder) {
    // Clear search when entering a folder to avoid confusion
    const searchInput = document.getElementById('file-search-input');
    if(searchInput) searchInput.value = "";

    breadcrumbStack.push(folder);
    currentFolder = folder;

    // DON'T clear selectedFile when opening folders!
    // Only clear it if we're actually navigating away from the current file context
    // selectedFile = null; // REMOVE THIS LINE

    // Load folder contents from API
    const folderPath = folder.path ? folder.path.replace(/^.*\.main_backup\/?/, '') : folder.name;
    loadFolderContents(folderPath);
    // DON'T clear the file preview - keep whatever is currently shown
    // The file preview will persist even when browsing folders
}

function navigateFolder(index) {
    // Clear search when navigating breadcrumbs
    const searchInput = document.getElementById('file-search-input');
    if(searchInput) searchInput.value = "";

    breadcrumbStack = breadcrumbStack.slice(0, index + 1);
    currentFolder = breadcrumbStack[index];

    // DON'T clear selectedFile when navigating folders!
    // selectedFile = null; // REMOVE THIS LINE

    // Load folder contents from API
    const folderPath = currentFolder.path ? currentFolder.path.replace(/^.*\.main_backup\/?/, '') : currentFolder.name;
    loadFolderContents(folderPath);
    // DON'T clear the file preview - keep whatever is currently shown
}

function resetExplorer() {
    const searchInput = document.getElementById('file-search-input');
    if(searchInput) searchInput.value = "";

    breadcrumbStack = [fileSystem];
    currentFolder = fileSystem;

    // DON'T clear selectedFile when resetting!
    // selectedFile = null; // REMOVE THIS LINE

    renderExplorer();
    // DON'T clear the file preview - keep whatever is currently shown
}


/**
 * Get bootstrap icon class based on file extension
 */
function getIconForFile(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
        'blend': 'bi-box-fill', 'blend1': 'bi-box-fill',
        'pdf': 'bi-file-earmark-pdf-fill',
        'doc': 'bi-file-earmark-word-fill', 'docx': 'bi-file-earmark-word-fill',
        'xls': 'bi-file-earmark-excel-fill', 'xlsx': 'bi-file-earmark-excel-fill',
        'ppt': 'bi-file-earmark-slides-fill', 'pptx': 'bi-file-earmark-slides-fill',
        'txt': 'bi-file-earmark-text-fill', 'md': 'bi-file-earmark-text-fill',
        'jpg': 'bi-file-earmark-image-fill', 'jpeg': 'bi-file-earmark-image-fill',
        'png': 'bi-file-earmark-image-fill', 'gif': 'bi-file-earmark-image-fill',
        'zip': 'bi-file-earmark-zip-fill', 'rar': 'bi-file-earmark-zip-fill',
        'mp3': 'bi-file-earmark-music-fill', 'wav': 'bi-file-earmark-music-fill',
        'mp4': 'bi-file-earmark-play-fill', 'avi': 'bi-file-earmark-play-fill',
        'json': 'bi-file-earmark-code-fill', 'js': 'bi-file-earmark-code-fill',
        'py': 'bi-file-earmark-code-fill', 'html': 'bi-file-earmark-code-fill',
        'appimage': 'bi-box2-fill',
    };
    return icons[ext] || 'bi-file-earmark-fill';
}

/**
 * Get color class based on file extension
 */
function getColorForFile(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const colors = {
        'blend': 'text-amber-600', 'blend1': 'text-amber-600',
        'pdf': 'text-red-500',
        'doc': 'text-blue-500', 'docx': 'text-blue-500',
        'xls': 'text-emerald-600', 'xlsx': 'text-emerald-600',
        'ppt': 'text-orange-500', 'pptx': 'text-orange-500',
        'jpg': 'text-pink-500', 'jpeg': 'text-pink-500', 'png': 'text-pink-500',
        'zip': 'text-purple-500', 'rar': 'text-purple-500',
        'mp3': 'text-purple-500', 'wav': 'text-purple-500',
        'mp4': 'text-red-500', 'avi': 'text-red-500',
        'json': 'text-orange-500', 'js': 'text-yellow-500',
        'py': 'text-blue-600', 'html': 'text-red-600',
        'appimage': 'text-cyan-400',
    };
    return colors[ext] || 'text-gray-500';
}

function selectFile(file) {
    selectedFile = file;
    const preview = document.getElementById('preview-content');

    // Check connection status
    if (!isDeviceConnected) {
        selectedFile = null;
        preview.innerHTML = `
            <div class="p-8 text-center text-muted">
                <i class="bi bi-file-earmark-bar-graph text-3xl mb-3"></i>
                <h4 class="font-bold text-main">Device Disconnected</h4>
                <p class="text-sm mt-1">File preview unavailable until the backup device reconnects.</p>
            </div>`;
        return;
    }

    // Helper function to truncate path for display
    function truncatePath(path, maxLength = 50) {
        if (!path || path.length <= maxLength) return path;

        // If path is already short, return as-is
        if (path.length <= maxLength) return path;

        // Try to keep beginning and end of path
        const ellipsis = '...';
        const charsToKeep = maxLength - ellipsis.length;
        const start = Math.floor(charsToKeep * 0.4); // 40% from start
        const end = charsToKeep - start;

        return path.substring(0, start) + ellipsis + path.substring(path.length - end);
    }

    // Initial Loading State
    preview.innerHTML = `
        <div class="animate-entry h-full flex flex-col">
            <div class="flex items-start gap-4 mb-6 border-b border-main pb-6">
                <div class="w-16 h-16 rounded-2xl bg-gray-50 dark:bg-white/5 flex items-center justify-center text-3xl border border-main shadow-sm">
                    <i class="bi ${file.icon || 'bi-file-earmark-text-fill'} ${file.color || 'text-brand-500'}"></i>
                </div>
                <div class="flex-1 min-w-0">
                    <h4 class="font-bold text-main text-lg truncate" title="${file.name}">${file.name}</h4>
                    <div class="flex items-center gap-2 mt-1">
                        <span class="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/20 text-[10px] font-bold text-secondary border border-main uppercase tracking-wider">FILE</span>
                        <span id="preview-size" class="text-xs text-secondary">Loading size...</span>
                    </div>

                    <div class="flex items-center gap-2 mt-1">
                        <span class="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/20 text-[10px] font-bold text-secondary border border-main uppercase tracking-wider">LOCATION</span>
                        <span id="preview-location" class="text-xs text-secondary">Checking file location...</span>
                    </div>

                    <div class="flex items-center gap-2 mt-1">
                        <span class="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/20 text-[10px] font-bold text-secondary border border-main uppercase tracking-wider">STATUS</span>
                        <span id="preview-status" class="text-xs text-secondary">Checking file existence...</span>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-3 mb-6" id="preview-action-buttons">
                <!-- Action buttons will be populated here -->
            </div>

            <div class="flex-1 flex flex-col min-h-0">
                <div class="flex items-center justify-between mb-3">
                    <p class="text-xs font-bold text-muted uppercase tracking-wider">Version History</p>
                    <span class="text-[10px] text-brand-500 font-medium bg-blue-50 dark:bg-blue-900/20 px-2 py-0.5 rounded-full">Time Machine</span>
                </div>

                <div id="preview-versions-list" class="flex-1 overflow-y-auto space-y-3 pr-1 no-scrollbar pb-4">
                    <div class="text-center py-8 text-muted">
                        <i class="bi bi-arrow-clockwise animate-spin text-xl"></i>
                        <p class="text-xs mt-2">Fetching versions...</p>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Fetch File Info
    const filePath = file.path || file.name;

    fetch('/api/file-info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: filePath })
    })
    .then(res => res.json())
    // In the selectFile function, update the section where file info is fetched
    .then(data => {
        const sizeEl = document.getElementById('preview-size');
        const locationEl = document.getElementById('preview-location');
        const statusEl = document.getElementById('preview-status');
        const actionButtons = document.getElementById('preview-action-buttons');

        if (data.success) {
            // Update size
            sizeEl.innerText = data.size ? Utils.formatBytes(data.size) : 'Size unknown';

            // Determine actual display path
            let displayPath = data.home_path || 'Path unknown';
            let actualPath = data.actual_path || data.current_location || data.home_path;
            let isMoved = false;
            let isRenamed = false;

            if (data.exists) {
                if (data.actual_path) {
                    displayPath = data.actual_path;
                    actualPath = data.actual_path;
                } else if (data.current_location) {
                    displayPath = data.current_location;
                    actualPath = data.current_location;
                }

                // Check if file is moved/renamed
                isMoved = data.is_moved ||
                        (data.current_location && data.current_location !== data.home_path) ||
                        (data.actual_path && data.actual_path !== data.home_path);

                if (isMoved && data.actual_path && data.home_path) {
                    isRenamed = data.actual_path.split('/').pop() !== data.home_path.split('/').pop();
                }
            }

            // Truncate path for display (max 50 characters)
            const truncatedPath = truncatePath(displayPath, 50);

            // Update location display with appropriate icon - FIXED: Show full path in small font
            locationEl.innerHTML = `
                <div class="text-xs text-secondary break-all">
                    ${displayPath}
                </div>
            `;

            locationEl.title = displayPath; // Full path in tooltip

            // Update status with appropriate color - FIXED: MOVED=YELLOW, FOUND=GREEN, NOT FOUND=RED
            if (data.exists) {
                if (isMoved) {
                    if (isRenamed) {
                        statusEl.innerHTML = `RENAMED`;
                        statusEl.className = 'text-xs font-bold text-yellow-500'; // YELLOW
                    } else {
                        statusEl.innerHTML = `MOVED`;
                        statusEl.className = 'text-xs font-bold text-yellow-500'; // YELLOW
                    }
                } else {
                    statusEl.innerText = 'FOUND';
                    statusEl.className = 'text-xs font-bold text-green-500'; // GREEN
                }
            } else {
                statusEl.innerText = 'NOT FOUND';
                statusEl.className = 'text-xs font-bold text-red-500'; // RED
            }

            // Update action buttons - FIXED: Open + Open Location, disabled if MOVED
            let buttonsHtml = '';

            if (data.exists) {
                if (isMoved) {
                    // File is moved - disable both buttons
                    buttonsHtml = `
                        <button disabled
                                class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 cursor-not-allowed">
                            <i class="bi bi-eye-fill"></i> Open
                        </button>
                        <button disabled
                                class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 cursor-not-allowed">
                            <i class="bi bi-folder-fill"></i> Open Location
                        </button>
                    `;
                } else {
                    // File found in expected location - enable both buttons
                    buttonsHtml = `
                        <button onclick="openFile('${actualPath.replace(/'/g, "\\'")}')"
                                class="btn-normal flex items-center justify-center gap-2 py-2 hover:bg-gray-100 dark:hover:bg-white/10 cursor-pointer">
                            <i class="bi bi-eye-fill"></i> Open
                        </button>
                        <button onclick="openLocation('${actualPath.replace(/'/g, "\\'")}')"
                                class="btn-normal flex items-center justify-center gap-2 py-2 hover:bg-gray-100 dark:hover:bg-white/10 cursor-pointer">
                            <i class="bi bi-folder-fill"></i> Open Location
                        </button>
                    `;
                }
            } else {
                // File not found - Show Restore options directly
                buttonsHtml = `
                    <button disabled
                            class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 cursor-not-allowed">
                        <i class="bi bi-eye-fill"></i> Open
                    </button>
                    <button disabled
                            class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 cursor-not-allowed">
                        <i class="bi bi-folder-fill"></i> Open Location
                    </button>
            `;
            }

            actionButtons.innerHTML = buttonsHtml;
        } else {
            // API error
            sizeEl.innerText = 'Error';
            locationEl.innerText = 'Failed to get location';
            statusEl.innerText = 'ERROR';
            statusEl.className = 'text-xs text-red-500 font-bold';

            actionButtons.innerHTML = `
                <button disabled class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 select-none cursor-not-allowed">
                    <i class="bi bi-exclamation-triangle"></i> Error
                </button>
                <button disabled class="btn-normal flex items-center justify-center gap-2 py-2 opacity-50 select-none cursor-not-allowed">
                    <i class="bi bi-exclamation-triangle"></i> Error
                </button>
            `;
        }
    }).catch(err => {
        console.error('Failed to get file info:', err);
        const statusEl = document.getElementById('preview-status');
        if (statusEl) {
            statusEl.innerText = 'NETWORK ERROR';
            statusEl.className = 'text-xs text-red-500 font-bold';
        }
    });

    // Fetch Versions
    fetch(`/api/file-versions?file_path=${encodeURIComponent(filePath)}`)
        .then(res => res.json())
        .then(data => {
            const container = document.getElementById('preview-versions-list');
            if(!container) return;
            container.innerHTML = '';

            if (!data.success || !data.versions || data.versions.length === 0) {
                container.innerHTML = `
                    <div class="p-4 rounded-xl border border-dashed border-main text-center bg-gray-50 dark:bg-white/5">
                        <p class="text-xs text-muted">No history found for this file.</p>
                    </div>`;
                return;
            } else {
                // =========================================================
                // Sort versions DESCENDING (Latest on top)
                // =========================================================
                data.versions.sort((a, b) => {
                    // Convert timestamps to Date objects for comparison
                    const dateA = new Date(a.date || a.timestamp); 
                    const dateB = new Date(b.date || b.timestamp);
                    // Subtracting A from B puts the LATEST (newest) version on top
                    return dateB - dateA; 
                });
                // =========================================================
                
                // =========================================================
                // Corrected Sort Logic (Latest on top, 'main' at the bottom)
                // =========================================================
                data.versions.sort((a, b) => {
                    // Check for the special 'main' backup key
                    const isMainA = a.key === 'main';
                    const isMainB = b.key === 'main';

                    // Rule 1: If 'A' is 'main' and 'B' is not, 'A' must go AFTER 'B' (return 1)
                    if (isMainA && !isMainB) {
                        return 1;
                    } 
                    
                    // Rule 2: If 'B' is 'main' and 'A' is not, 'B' must go AFTER 'A' (return -1)
                    if (isMainB && !isMainA) {
                        return -1;
                    }
                    
                    // Rule 3: If both are or neither are 'main', sort by timestamp descending (newest first)
                    // The date is derived from the 'key' for non-main entries like "11-12-2025_09-42"
                    
                    // Attempt to parse date from key/timestamp/date
                    const getTime = (item) => {
                        // Use timestamp or date if available, otherwise try to parse from the key
                        if (item.timestamp) return new Date(item.timestamp).getTime();
                        if (item.date) return new Date(item.date).getTime();

                        // Custom parsing for your 'dd-mm-yyyy_hh-mm' key format
                        if (item.key && item.key !== 'main') {
                            const parts = item.key.match(/(\d{2})-(\d{2})-(\d{4})_(\d{2})-(\d{2})/);
                            if (parts) {
                                // Parts: [match, day, month, year, hour, minute]
                                // JavaScript Date is yyyy, mm-1, dd, hh, mm
                                // We parse DD-MM-YYYY as YYYY-MM-DD
                                return new Date(parts[3], parts[2] - 1, parts[1], parts[4], parts[5]).getTime();
                            }
                        }
                        return 0; // Fallback
                    };
                    
                    const tsA = getTime(a);
                    const tsB = getTime(b);
                    
                    return tsB - tsA; // Descending sort (Newest first)
                });
                // =========================================================
            }

            // Render Versions
            data.versions.forEach((v, idx) => {
                const isMain = v.key === 'main';
                const sizeStr = v.size ? Utils.formatBytes(v.size) : 'Unknown Size';
                const timeStr = v.time || 'Unknown Date';
                const pathStr = v.path || 'Unknown Path';

                // Update the version history buttons to match action button size
                const card = document.createElement('div');
                card.className = "bg-card border border-main rounded-xl p-3 hover:border-brand-500 transition-all duration-200 group relative";

                card.innerHTML = `
                    <div class="flex justify-between items-start mb-3">
                        <div class="flex items-center gap-3">
                            <div class="w-8 h-8 rounded-lg ${isMain ? 'bg-amber-50 text-amber-600 dark:bg-amber-900/20 dark:text-yellow-500' : 'bg-blue-50 text-blue-600 dark:bg-blue-900/20 dark:text-blue-500'} flex items-center justify-center text-sm font-bold border border-black/5">
                                ${isMain ? '<i class="bi bi-star-fill text-[10px]"></i>' : idx + 1}
                            </div>
                                <div class="min-w-0"> <p class="text-xs font-bold text-main leading-tight">${formatRelativeDate(timeStr)}</p>
                                <p class="text-xs text-secondary">${sizeStr}</p>
                                <p class="text-xs text-secondary break-all">${pathStr}</p>
                            </div>
                        </div>
                        ${isMain ? '<span class="text-[10px] font-bold text-amber-600 bg-amber-50 dark:bg-amber-900/20 px-2 py-0.5 rounded">ORIGINAL</span>' : ''}
                    </div>

                    <div class="grid grid-cols-3 gap-2 mt-2 pt-2 border-t border-main">
                        <button class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200" onclick="openFile('${v.path.replace(/\\/g, '\\\\')}')">
                            <i class="bi bi-eye-fill"></i> Open
                        </button>
                        <button class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200" onclick="openLocation('${v.path.replace(/\\/g, '\\\\')}')">
                            <i class="bi bi-folder-fill"></i> Open Location
                        </button>
                        <button class="btn-normal text-brand-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 dark:text-blue-400 cursor-pointer flex items-center justify-center gap-2 py-2" onclick="showRestoreOptions('${v.path.replace(/\\/g, '\\\\')}', '${file.name}')">
                            <i class="bi bi-arrow-counterclockwise"></i> Restore
                        </button>
                    </div>
                `;
                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error(err);
            showSystemNotification('error', 'Error while getting file backup version!', err)
            const container = document.getElementById('preview-versions-list');
            if(container) container.innerHTML = '<p class="text-xs text-red-500">Failed to load history.</p>';
        });
}

// Helper functions for the restore options
function restoreToOriginal(backupPath) {
    closeConfirmModal();
    // Find and click the restore button for this file
    const restoreButtons = document.querySelectorAll(`button[data-filepath="${backupPath}"]`);
    if (restoreButtons.length > 0) {
        restoreButtons[0].click();
    } else {
        // Fallback: create a mock button and call performRestore
        const mockButton = document.createElement('button');
        mockButton.dataset.filepath = backupPath;
        performRestore(backupPath, 'original', mockButton);
    }
}

// =====================================================================
// --- FIXED: SEARCH FOR MOVED FILE FUNCTION ---
// =====================================================================

function searchForMovedFile(backupPath, buttonElement) {
    // Handle case where buttonElement is not provided (called from modal)
    const container = buttonElement ? buttonElement.parentElement : null;

    // If no buttonElement provided, use a different approach
    if (!buttonElement) {
        // Show searching state in a modal or notification
        showSystemNotification('info', 'Searching', `Searching for moved file...`);

        fetch('/api/search-moved-file', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                file_path: backupPath,
                fast_search: true
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.found) {
                showSystemNotification('success', 'File Found',
                    `Found moved file at: ${data.current_location}`);
            } else {
                showSystemNotification('info', 'Not Found',
                    'File not found in home directory.');
            }
        })
        .catch(error => {
            console.error('Search error:', error);
            showSystemNotification('error', 'Search Failed',
                error.message || 'Network error');
        });
        return;
    }

    // Original code for when buttonElement is provided
    if (container) {
        container.innerHTML = `
            <div class="p-4 border border-amber-200 dark:border-amber-700 rounded-xl bg-amber-50 dark:bg-amber-900/20">
                <div class="flex items-center gap-3">
                    <div class="flex-1">
                        <h4 class="font-bold text-sm text-main">Searching for moved file...</h4>
                        <div class="mt-1">
                            <div class="flex items-center justify-between text-xs text-muted mb-1">
                                <span>Calculating file hash</span>
                                <span class="text-amber-600 font-medium">0%</span>
                            </div>
                            <div class="w-full bg-amber-200 dark:bg-amber-800 rounded-full h-1.5 overflow-hidden">
                                <div class="bg-amber-500 h-full rounded-full transition-all duration-300" style="width: 25%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    fetch('/api/search-moved-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file_path: backupPath,
            fast_search: true
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.found) {
            if (container) {
                container.innerHTML = `
                    <div class="p-4 border border-emerald-200 dark:border-emerald-700 rounded-xl bg-emerald-50 dark:bg-emerald-900/20">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                                    <i class="bi bi-check-lg text-lg"></i>
                                </div>
                                <div>
                                    <h4 class="font-bold text-sm text-main">Found moved file!</h4>
                                    <p class="text-xs text-muted truncate max-w-[200px]" title="${data.current_location}">
                                        ${data.current_location.replace(/^.*\//, '.../')}
                                    </p>
                                    <p class="text-xs text-emerald-600 dark:text-emerald-400 mt-1">
                                        <i class="bi bi-clock"></i> Found in ${data.search_time.toFixed(2)}s
                                    </p>
                                </div>
                            </div>
                            <button onclick="performRestore('${backupPath.replace(/'/g, "\\'")}', 'current', this)"
                                    class="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-1">
                                <i class="bi bi-download"></i> Restore Here
                            </button>
                        </div>
                    </div>
                `;
            }
        } else {
            if (container) {
                container.innerHTML = `
                    <div class="p-4 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-900/20">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 flex items-center justify-center">
                                <i class="bi bi-file-earmark-x text-lg"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm text-main">Moved file not found</h4>
                                <p class="text-xs text-muted mt-0.5">Search took ${data.search_time ? data.search_time.toFixed(2) : '?'}s</p>
                            </div>
                        </div>
                    </div>
                `;
            }
        }
    })
    .catch(error => {
        console.error('Search error:', error);
        if (container) {
            container.innerHTML = `
                <div class="p-4 border border-red-200 dark:border-red-700 rounded-xl bg-red-50 dark:bg-red-900/20">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 flex items-center justify-center">
                            <i class="bi bi-exclamation-triangle text-lg"></i>
                        </div>
                        <div>
                            <h4 class="font-bold text-sm text-main">Search failed</h4>
                            <p class="text-xs text-muted mt-0.5">Error searching for file: ${error.message || 'Unknown error'}</p>
                        </div>
                    </div>
                </div>
            `;
        }
    });
}

// Add this helper function for searching files (if not already defined)
function searchForFile(backupPath, buttonElement) {
    // Create a simple search modal
    openConfirmationModal(
        'Search for File',
        `Searching for file in your home directory...`,
        null,
        {
            showCancel: true,
            cancelText: 'Cancel',
            confirmText: '',
            customButtons: true
        }
    );

    // Call the search endpoint
    fetch('/api/search-moved-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file_path: backupPath,
            fast_search: true
        })
    })
    .then(response => response.json())
    .then(data => {
        closeConfirmModal(); // Close the search modal

        if (data.success && data.found) {
            showSystemNotification('success', 'File Found',
                `File found at: ${data.current_location}`);

            // Update the UI to show the file as found
            const fileName = backupPath.split('/').pop();
            showSystemNotification('info', 'Location Saved',
                `The system will remember this location for future restores.`);
        } else {
            showSystemNotification('info', 'File Not Found',
                'The file was not found in your home directory. You can restore it from backup.');
        }
    })
    .catch(error => {
        console.error('Search error:', error);
        showSystemNotification('error', 'Search Failed', 'Could not search for file.');
    });
}

// Helper function for showing location details
function showFileLocationDetails(backupPath) {
    fetch('/api/file-info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: backupPath })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            let message = '';
            let icon = '';
            let color = '';
            let status = '';

            // Check if file is in trash
            const isInTrash = data.actual_path &&
                              (data.actual_path.includes('/.local/share/Trash/') ||
                               data.actual_path.includes('/.Trash/') ||
                               data.actual_path.includes('/Trash/'));

            if (data.exists) {
                if (isInTrash) {
                    // File is in trash/bin
                    icon = 'bi-trash-fill';
                    color = 'text-red-500';
                    status = 'File is in Trash';

                    message = `
                        <div class="space-y-3">
                            <div class="flex items-start gap-3">
                                <i class="bi bi-trash-fill text-red-500 text-xl mt-0.5"></i>
                                <div class="flex-1">
                                    <p class="font-medium text-main mb-1">File is in Trash/Bin</p>
                                    <div class="space-y-2 text-sm">
                                        <div>
                                            <p class="text-xs text-muted mb-0.5">Trash Location:</p>
                                            <p class="font-mono text-xs bg-red-50 dark:bg-red-900/20 p-2 rounded">${data.actual_path}</p>
                                        </div>
                                        <div>
                                            <p class="text-xs text-muted mb-0.5">Original Expected Location:</p>
                                            <p class="font-mono text-xs bg-gray-50 dark:bg-gray-800 p-2 rounded line-through">${data.home_path}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-3 mt-2">
                                <p class="text-xs text-yellow-700 dark:text-yellow-300">
                                    <i class="bi bi-exclamation-triangle mr-1"></i>
                                    File was deleted and moved to Trash. You can restore it from Trash or use Time Machine to restore from backup.
                                </p>
                            </div>
                        </div>
                    `;

                } else if (data.is_moved && data.actual_path && data.home_path) {
                    // File was moved/renamed
                    const isRenamed = data.actual_path.split('/').pop() !== data.home_path.split('/').pop();

                    icon = isRenamed ? 'bi-input-cursor-text' : 'bi-arrow-right-circle-fill';
                    color = 'text-yellow-500';
                    status = isRenamed ? 'File was renamed' : 'File was moved';

                    message = `
                        <div class="space-y-3">
                            <div class="flex items-start gap-3">
                                <i class="bi ${icon} text-yellow-500 text-xl mt-0.5"></i>
                                <div class="flex-1">
                                    <p class="font-medium text-main mb-1">${status} </p>
                                    <div class="space-y-2 text-sm">
                                        <div>
                                            <p class="text-xs text-muted mb-0.5">${isRenamed ? 'New Name:' : 'Current Location:'}</p>
                                            <p class="font-mono text-xs bg-amber-50 dark:bg-amber-900/20 p-2 rounded">${data.actual_path}</p>
                                        </div>
                                        <div>
                                            <p class="text-xs text-muted mb-0.5">${isRenamed ? 'Original Name:' : 'Original Location:'}</p>
                                            <p class="font-mono text-xs bg-gray-50 dark:bg-gray-800 p-2 rounded line-through">${data.home_path}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <p class="text-xs text-emerald-500 mt-2">
                                <i class="bi bi-info-circle mr-1"></i>
                                The system remembers this location for future restores.
                            </p>
                        </div>
                    `;

                } else {
                    // File is in expected location
                    icon = 'bi-check-circle-fill';
                    color = 'text-emerald-500';
                    status = 'File found in expected location';

                    message = `
                        <div class="space-y-2">
                            <div class="flex items-start gap-3">
                                <i class="bi bi-check-circle-fill text-emerald-500 text-xl mt-0.5"></i>
                                <div>
                                    <p class="font-medium text-main mb-1">File Found</p>
                                    <p class="text-sm text-muted">File is in its expected location</p>
                                    <p class="font-mono text-xs bg-emerald-50 dark:bg-emerald-900/20 p-2 rounded mt-1">${data.actual_path || data.home_path}</p>
                                </div>
                            </div>
                        </div>
                    `;
                }
            } else {
                // File not found anywhere
                icon = 'bi-question-circle-fill';
                color = 'text-red-500';
                status = 'File not found';

                // Check if file was recently deleted (has location in database but file doesn't exist)
                if (data.current_location && !data.exists) {
                    status = 'File was deleted';
                    message = `
                        <div class="space-y-3">
                            <div class="flex items-start gap-3">
                                <i class="bi bi-x-octagon-fill text-red-500 text-xl mt-0.5"></i>
                                <div class="flex-1">
                                    <p class="font-medium text-main mb-1">File was deleted</p>
                                    <div class="space-y-2 text-sm">
                                        <div>
                                            <p class="text-xs text-muted mb-0.5">Last known location:</p>
                                            <p class="font-mono text-xs bg-gray-50 dark:bg-gray-800 p-2 rounded line-through">${data.current_location}</p>
                                        </div>
                                        <div>
                                            <p class="text-xs text-muted mb-0.5">Expected location:</p>
                                            <p class="font-mono text-xs bg-gray-50 dark:bg-gray-800 p-2 rounded line-through">${data.home_path}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3">
                                <p class="text-sm text-red-700 dark:text-red-300 mb-2">
                                    <i class="bi bi-exclamation-triangle mr-1"></i>
                                    This file was deleted from your system.
                                </p>
                                <p class="text-xs text-red-600 dark:text-red-400">
                                    You can restore it from a Time Machine backup using the "Restore" button.
                                </p>
                            </div>
                        </div>
                    `;
                } else {
                    message = `
                        <div class="space-y-2">
                            <div class="flex items-start gap-3">
                                <i class="bi bi-question-circle-fill text-red-500 text-xl mt-0.5"></i>
                                <div>
                                    <p class="font-medium text-main mb-1">File Not Found</p>
                                    <p class="text-sm text-muted">Expected location:</p>
                                    <p class="font-mono text-xs bg-gray-50 dark:bg-gray-800 p-2 rounded">${data.home_path || 'Unknown'}</p>
                                </div>
                            </div>
                            <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3 mt-2">
                                <p class="text-xs text-blue-700 dark:text-blue-300">
                                    <i class="bi bi-search mr-1"></i>
                                    The file is not in the expected location. It may have been:
                                </p>
                                <ul class="text-xs text-blue-600 dark:text-blue-400 mt-1 pl-4 list-disc">
                                    <li>Moved to a different folder</li>
                                    <li>Renamed</li>
                                    <li>Deleted (check Trash/Bin)</li>
                                </ul>
                            </div>
                        </div>
                    `;
                }
            }

            // Use your existing confirmation modal
            openConfirmationModal(
                status,
                message,
                null,
                {
                    showCancel: true,
                    cancelText: 'Close',
                    confirmText: '',
                    customButtons: true,
                    wideModal: true
                }
            );
        }
    })
    .catch(err => {
        console.error('Error getting location details:', err);
    });
}

// Used from index.html onclick handlers
function searchFiles() {
    const query = document.getElementById('file-search-input').value.toLowerCase();
    const container = document.getElementById('file-list-container');

    // If search is cleared, show folder view
    if (query.length === 0) return renderExplorer();

    // Show loading state
    container.innerHTML = `
        <div class="flex items-center gap-2 text-slate-100">
            <i class="bi bi-arrow-clockwise animate-spin"></i>
            <span>Searching...</span>
        </div>`;

    // Fetch search results from backend
    fetch(`/api/search?query=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            if (!data.files || data.files.length === 0) {
                container.innerHTML = '<p class="p-4 text-gray-400">No files found matching your search.</p>';
                return;
            }

            // Convert backend file results to displayable items
            const results = data.files.map(file => ({
                name: file.name,
                path: file.path,
                search_display_path: file.search_display_path,
                type: 'file',
                icon: getIconForFile(file.name),
                color: getColorForFile(file.name)
            }));

            renderExplorer(results);
        })
        .catch(err => {
            console.error('Search failed:', err);
            container.innerHTML = '<p class="p-4 text-red-500">Search failed. Please try again.</p>';
        });
}

/**
 * Get bootstrap icon class based on file extension
 */
function getIconForFile(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const icons = {
        'blend': 'bi-box-fill', 'blend1': 'bi-box-fill',
        'pdf': 'bi-file-earmark-pdf-fill',
        'doc': 'bi-file-earmark-word-fill', 'docx': 'bi-file-earmark-word-fill',
        'xls': 'bi-file-earmark-excel-fill', 'xlsx': 'bi-file-earmark-excel-fill',
        'ppt': 'bi-file-earmark-slides-fill', 'pptx': 'bi-file-earmark-slides-fill',
        'txt': 'bi-file-earmark-text-fill', 'md': 'bi-file-earmark-text-fill',
        'jpg': 'bi-file-earmark-image-fill', 'jpeg': 'bi-file-earmark-image-fill',
        'png': 'bi-file-earmark-image-fill', 'gif': 'bi-file-earmark-image-fill',
        'zip': 'bi-file-earmark-zip-fill', 'rar': 'bi-file-earmark-zip-fill',
        'mp3': 'bi-file-earmark-music-fill', 'wav': 'bi-file-earmark-music-fill',
        'mp4': 'bi-file-earmark-play-fill', 'avi': 'bi-file-earmark-play-fill',
        'json': 'bi-file-earmark-code-fill', 'js': 'bi-file-earmark-code-fill',
        'py': 'bi-file-earmark-code-fill', 'html': 'bi-file-earmark-code-fill'
    };
    return icons[ext] || 'bi-file-earmark-fill';
}

/**
 * Get color class based on file extension
 */
function getColorForFile(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    const colors = {
        'blend': 'text-amber-600', 'blend1': 'text-amber-600',
        'pdf': 'text-red-500',
        'doc': 'text-blue-500', 'docx': 'text-blue-500',
        'xls': 'text-emerald-600', 'xlsx': 'text-emerald-600',
        'ppt': 'text-orange-500', 'pptx': 'text-orange-500',
        'jpg': 'text-pink-500', 'jpeg': 'text-pink-500', 'png': 'text-pink-500',
        'zip': 'text-purple-500', 'rar': 'text-purple-500',
        'mp3': 'text-purple-500', 'wav': 'text-purple-500',
        'mp4': 'text-red-500', 'avi': 'text-red-500',
        'json': 'text-orange-500', 'js': 'text-yellow-500',
        'py': 'text-blue-600', 'html': 'text-red-600'
    };
    return colors[ext] || 'text-gray-500';
}

function renderFilePreview(file) {
    const nameEl = document.getElementById('preview-file-name');
    const contentEl = document.getElementById('preview-content');

    if (!file) {
        nameEl.innerText = "Select a file to view history";
        contentEl.className = "p-6 bg-gray-50 dark:bg-slate-700 flex-1 flex items-center justify-center text-gray-400 text-main text-sm";
        contentEl.innerHTML = '<p>No file selected.</p>';
        return;
    }

    nameEl.innerText = file.name;
    contentEl.className = "p-6 flex-1 space-y-4 no-scrollbar overflow-y-auto";

    // Construct the path to the current file in the user's home directory
    let currentFilePath = '';

    if (file.path) {
        // If file has a path, extract relative path from backup and map to home
        const backupPath = file.path;
        if (backupPath.includes('.main_backup')) {
            // Extract path relative to .main_backup
            const relativePath = backupPath.split('.main_backup')[1].replace(/^[\\/]+/, '');
            // We'll get the actual home path from the backend when needed
            currentFilePath = relativePath;
        } else {
            // For search results or other paths, use the file name directly
            currentFilePath = file.name;
        }
    } else if (file.search_display_path) {
        // For search results with display path
        const searchPath = file.search_display_path;
        if (searchPath.includes('.main_backup')) {
            const relativePath = searchPath.split('.main_backup')[1].replace(/^[\\/]+/, '');
            currentFilePath = relativePath;
        } else {
            currentFilePath = file.name;
        }
    } else {
        // Fallback: just use the file name
        currentFilePath = file.name;
    }

    // Normalize path separators
    currentFilePath = currentFilePath.replace(/\\/g, '/');

    contentEl.innerHTML = `
        <div class="mb-4 border-b border-gray-200 dark:border-slate-600 pb-4">
            <div class="flex items-center gap-2 mb-2">
                <i class="bi bi-clock text-blue"></i>
                <span class="text-sm font-bold text-blue">Current File (Latest)</span>
            </div>
            <div class="p-4 rounded-lg bg-card flex items-center justify-between">
                <div class="flex items-center gap-4">
                    <i class="bi ${file.icon} text-2xl ${file.color}"></i>
                    <div>
                        <p class="text-xs text-main font-bold">${file.name}</p>
                        <p id="preview-current-size" class="text-xs text-secondary">Size: Loading...</p>
                    </div>
                </div>
                <div class="flex gap-2">
                    <button id="preview-open-btn" class="btn-normal text-secondary"><i class="bi bi-eye-fill mr-1"></i> Open</button>
                    <button id="preview-open-location-btn" class="btn-normal text-secondary"><i class="bi bi-geo-alt-fill mr-1"></i> Open Location</button>
                </div>
            </div>
        </div>

        <div class="space-y-4 pr-2">
            <div class="flex items-center gap-2 mb-2">
                <i class="bi bi-clock-history text-main"></i>
                <span class="font-bold text-sm text-main">Backup Versions</span>
            </div>

            <div id="preview-versions-container" class="space-y-4">
                <div class="p-4 text-slate-500"><i class="bi bi-arrow-clockwise animate-spin mr-2"></i> Loading versions...</div>
            </div>
        </div>
    `;

    // Fetch and render backup versions (excluding current home file)
    (async () => {
        const versionsContainer = document.getElementById('preview-versions-container');
        if (!versionsContainer) return;
        try {
            const filePath = file.path || file.search_display_path || file.name;
            const resp = await fetch(`/api/file-versions?file_path=${encodeURIComponent(filePath)}`);
            const json = await resp.json();

            if (!json || !json.success || !Array.isArray(json.versions) || json.versions.length === 0) {
                versionsContainer.innerHTML = '<p class="p-4 text-gray-400">No previous versions found.</p>';
                return;
            }

            // Separate main backup (initial) from other versions
            const mainVersionIndex = json.versions.findIndex(v => v.key === 'main');
            let mainVersion = null;
            let incremental = json.versions.slice();
            if (mainVersionIndex !== -1) {
                mainVersion = incremental.splice(mainVersionIndex, 1)[0];
            }

            // Render incremental versions (already sorted newest-first by backend)
            versionsContainer.innerHTML = '';

            if (incremental.length === 0 && !mainVersion) {
                versionsContainer.innerHTML = '<p class="p-4 text-gray-400">No previous versions found.</p>';
                return;
            }

            incremental.forEach(v => {
                const displayTime = formatVersionTime(v.time || v.key || 'Backup');
                const displaySize = v.size ? Utils.formatBytes(v.size) : 'Unknown Size';

                const versionEl = document.createElement('div');
                versionEl.className = 'p-4 bg-card border rounded-lg flex items-center justify-between';

                const left = document.createElement('div');
                left.innerHTML = `<p class="text-xs text-main font-bold">${displayTime}</p><p class="text-xs text-secondary">Size: ${displaySize}</p>`;

                const right = document.createElement('div');
                right.className = 'flex gap-2';

                const openBtn = document.createElement('button');
                openBtn.className = 'btn-normal boder-main text-secondary border';
                openBtn.innerHTML = '<i class="bi bi-eye-fill"></i> Open';
                openBtn.onclick = () => openFile(v.path);

                const locBtn = document.createElement('button');
                locBtn.className = 'btn-normal boder-main text-secondary border';
                locBtn.innerHTML = '<i class="bi bi-geo-alt-fill"></i> Open Location';
                locBtn.onclick = () => openLocation(v.path);

                const restoreBtn = document.createElement('button');
                restoreBtn.className = 'btn-normal text-hyperlink';
                restoreBtn.innerHTML = '<i class="bi bi-download"></i> Restore File';
                restoreBtn.onclick = () => restoreFile(restoreBtn);
                restoreBtn.dataset.filepath = v.path;

                right.appendChild(openBtn);
                right.appendChild(locBtn);
                right.appendChild(restoreBtn);

                versionEl.appendChild(left);
                versionEl.appendChild(right);
                versionsContainer.appendChild(versionEl);
            });

            // Finally render the main backup as the last (Initial Backup)
            if (mainVersion) {
                const displayTime = formatVersionTime(mainVersion.time || 'Initial Backup');
                const displaySize = mainVersion.size ? Utils.formatBytes(mainVersion.size) : 'Unknown Size';

                const versionEl = document.createElement('div');
                versionEl.className = 'p-4 bg-card rounded-lg flex items-center justify-between';

                const left = document.createElement('div');
                left.innerHTML = `<p class="text-xs text-main font-bold">${displayTime} <span class="text-orange-500 ml-2 text-[11px] font-semibold">Initial Backup</span></p><p class="text-xs text-secondary">Size: ${displaySize}</p>`;

                const right = document.createElement('div');
                right.className = 'flex gap-2';

                const openBtn = document.createElement('button');
                openBtn.className = 'btn-normal text-secondary';
                openBtn.innerHTML = '<i class="bi bi-eye-fill"></i> Open';
                openBtn.onclick = () => openFile(mainVersion.path);

                const locBtn = document.createElement('button');
                locBtn.className = 'btn-normal text-secondary';
                locBtn.innerHTML = '<i class="bi bi-geo-alt-fill"></i> Open Location';
                locBtn.onclick = () => openLocation(mainVersion.path);

                const restoreBtn = document.createElement('button');
                restoreBtn.className = 'btn-normal text-hyperlink';
                restoreBtn.innerHTML = '<i class="bi bi-download"></i> Restore File';
                restoreBtn.onclick = () => restoreFile(restoreBtn);
                restoreBtn.dataset.filepath = mainVersion.path;

                right.appendChild(openBtn);
                right.appendChild(locBtn);
                right.appendChild(restoreBtn);

                versionEl.appendChild(left);
                versionEl.appendChild(right);
                versionsContainer.appendChild(versionEl);
            }

        } catch (err) {
            console.error('Failed to load file versions:', err);
            versionsContainer.innerHTML = '<p class="p-4 text-red-500">Failed to load versions.</p>';
        }
    })();
}

// Relative Date Formatting
function formatRelativeDate(dateString) {
    if (!dateString) return 'Unknown Date';

    // Clean up separators (replace spaces/colons/dots with hyphens for splitting)
    const cleanedString = dateString.trim().replace(/[\s\.:]/g, '-');
    const parts = cleanedString.split('-').filter(p => p.length > 0);

    // Ensure we have at least 5 parts: D, M, Y, H, M (or Y, M, D, H, M)
    if (parts.length < 5) return dateString;

    let day, month, year, hour, minute;
    const h = Number(parts[3]);
    const m = Number(parts[4]);

    // Detect format based on the first part: if length 4, assume YYYY-MM-DD (ISO 8601 style)
    if (parts[0].length === 4) {
        // Format: YYYY-MM-DD HH-MM
        [year, month, day] = parts.slice(0, 3).map(Number);
        [hour, minute] = [h, m];

    } else {
        // Format: D1-D2-Y HH-MM (Ambiguous or DD-MM-YYYY/MM-DD-YYYY)
        const d1 = Number(parts[0]);
        const d2 = Number(parts[1]);
        const y = Number(parts[2]);

        // Priority 1: Unambiguous DD-MM-YYYY (D1 > 12 means D1 must be the Day)
        if (d1 > 12) {
            // D1 = Day, D2 = Month
            [day, month, year, hour, minute] = [d1, d2, y, h, m];
        }
        // Priority 2: Unambiguous MM-DD-YYYY (D2 > 12 means D2 must be the Day)
        else if (d2 > 12) {
            // D2 = Day, D1 = Month
            [day, month, year, hour, minute] = [d2, d1, y, h, m];
        }
        // Priority 3: Ambiguous (D1 <= 12 AND D2 <= 12). Default to DD-MM-YYYY.
        else {
            // D1 = Day, D2 = Month (European/International Default)
            [day, month, year, hour, minute] = [d1, d2, y, h, m];
        }
    }

    // Convert to Date object: Month is 0-indexed in JS.
    const backupDate = new Date(year, month - 1, day, hour, minute);
    const now = new Date();

    // Calculate difference in days (ignoring time for 'Today'/'Yesterday' check)
    const startOfBackupDay = new Date(backupDate.getFullYear(), backupDate.getMonth(), backupDate.getDate()).getTime();
    const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime();

    const msPerDay = 1000 * 60 * 60 * 24;
    const dayDiffMs = startOfToday - startOfBackupDay;
    // Math.floor handles time zone offsets and ensures we count full days passed.
    const diffDays = Math.floor(dayDiffMs / msPerDay);

    // --- Time String Generation (24-Hour Format: HH:MM) ---
    // Use the values extracted from the Date object for reliability
    const formattedHours = String(backupDate.getHours()).padStart(2, '0');
    const formattedMinutes = String(backupDate.getMinutes()).padStart(2, '0');
    const time24H = `${formattedHours}:${formattedMinutes}`;

    if (diffDays === 0) {
        // Example: "Today, 10:00"
        return `Today, ${time24H}`;
    }
    if (diffDays === 1) {
        // Example: "Yesterday, 09:23"
        return `Yesterday, ${time24H}`;
    }

    // --- Older Dates Fallback: "MM-DD-YY, HH:MM" (24-hour, padded hour) ---
    // const yearShort = String(year).slice(-2);

    // Use the correctly parsed month and day for output, ensuring MM-DD-YY order
    const formattedMonth = String(month).padStart(2, '0');
    const formattedDay = String(day).padStart(2, '0');

    return `${formattedDay}/${formattedMonth}/${year}, ${time24H}`;
}


// Helper function to get user's home directory from backend
function getHomeDirectory() {
    return fetch('/api/backup/usage')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.users_home_path) {
                return data.users_home_path;
            } else {
                throw new Error('Could not get home directory from backend');
            }
        });
}

/**
 * Try to parse backend time strings into a human label.
 * Examples input: "13-11-2025 10:53", "2025-11-27 17:04", "Nov 18, 14:30", "27-11-2025 17-04"
 */
function formatVersionTime(raw) {
    if (!raw) return 'Unknown';
    try {
        let s = String(raw).trim();
        s = s.replace(/_/g, ':');

        // If already has month name, try Date.parse
        if (/^[A-Za-z]/.test(s)) {
            const d = new Date(s);
            if (!isNaN(d)) return humanLabel(d);
        }

        // Split into date and time
        const parts = s.split(' ');
        const datePart = parts[0];
        const timePart = parts[1] || '00:00';

        const dateTokens = datePart.split('-');
        let year, month, day;
        if (dateTokens.length === 3) {
            if (dateTokens[0].length === 4) {
                // YYYY-MM-DD
                year = dateTokens[0]; month = dateTokens[1]; day = dateTokens[2];
            } else {
                // DD-MM-YYYY
                day = dateTokens[0]; month = dateTokens[1]; year = dateTokens[2];
            }
        } else if (datePart.includes('/')) {
            const dt = new Date(datePart);
            if (!isNaN(dt)) return humanLabel(dt);
        } else {
            // Fallback: try Date.parse
            const dt = new Date(s);
            if (!isNaN(dt)) return humanLabel(dt);
        }

        // Normalize to ISO
        month = String(month).padStart(2, '0');
        day = String(day).padStart(2, '0');
        const iso = `${year}-${month}-${day}T${timePart}`;
        const dt = new Date(iso);
        if (isNaN(dt)) return raw;
        return humanLabel(dt);
    } catch (e) {
        return raw;
    }

    function humanLabel(dt) {
        const now = new Date();
        const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const diffDays = Math.floor((startOfToday - new Date(dt.getFullYear(), dt.getMonth(), dt.getDate())) / 86400000);
        const opts = { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false };
        const formatted = dt.toLocaleString('en-US', opts).replace(',', '');
        if (diffDays === 0) return `Today (${formatted})`;
        if (diffDays === -1) return `Tomorrow (${formatted})`;
        if (diffDays === 1) return `Yesterday (${formatted})`;
        return `${formatted}`;
    }
}

// Open file in system via backend
function openFile(path) {
    if (!path) return;
    fetch('/api/open-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: path })
    }).then(res => res.json()).then(j => {
        if (!j || !j.success) console.warn('Open file failed', j);
    }).catch(err => console.error('Open file error', err));
}

// Open location (folder) via backend
function openLocation(path) {
    if (!path) return;
    fetch('/api/open-location', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: path })
    }).then(res => res.json()).then(j => {
        if (!j || !j.success) console.warn('Open location failed', j);
    }).catch(
        err => console.error('Open location error', err)
    );
}

// New restoreFile function with moved file handling
async function restoreFile(buttonElement) {
    if (buttonElement.disabled) return;

    const backupPath = buttonElement.dataset.filepath;
    const fileName = backupPath.split('/').pop() || 'file';

    if (!backupPath) {
        console.warn("No file path provided for restoration.");
        return;
    }

    // Check if file exists in home (quick check)
    const fileInfo = await checkFileExistence(backupPath);

    if (fileInfo.exists) {
        // File exists - proceed with normal restore
        performRestore(backupPath, fileInfo.home_path, buttonElement);
        return;
    }
}

// File doesn't exist - ask user if they want to search for moved version
function showRestoreOptions(backupPath, fileName) {
    // First get file info to show accurate status
    fetch('/api/file-info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: backupPath })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            let statusColor = '';
            let statusIcon = '';
            let statusMessage = '';
            let originalPath = data.home_path || 'Unknown';
            let currentPath = data.actual_path || data.current_location || originalPath;
            let fileExists = data.exists;
            let isMoved = data.is_moved;

            // Set status colors and icons
            if (fileExists) {
                if (isMoved) {
                    statusColor = 'text-yellow-500';
                    statusIcon = 'bi-arrow-right-circle-fill';
                    statusMessage = 'File was moved';
                } else {
                    statusColor = 'text-emerald-500';
                    statusIcon = 'bi-check-circle-fill';
                    statusMessage = 'File found in expected location';
                }
            } else {
                statusColor = 'text-red-500';
                statusIcon = 'bi-question-circle-fill';
                statusMessage = 'File not found';
            }

            // Create options based on file status
            let restoreOptionsHtml = '';

            if (fileExists && isMoved) {
                // MOVED: Show both original and current location options
                restoreOptionsHtml = `
                    <div class="space-y-3">
                        <h4 class="text-sm font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">Restore Options</h4>

                        <!-- Option 1: Restore to Current Location -->
                        <div class="group cursor-pointer" onclick="restoreToCurrentLocation('${backupPath.replace(/'/g, "\\'")}')">
                            <div class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200">
                                <div class="flex items-center gap-4">
                                    <div class="flex-shrink-0">
                                        <div class="w-12 h-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                                            <i class="bi bi-geo-alt-fill text-xl text-xl"></i>
                                        </div>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h4 class="font-bold text-slate-900 dark:text-slate-100 text-sm mb-1">Restore to Current Location</h4>
                                        <p class="text-xs text-slate-600 dark:text-slate-400 break-all" title="${currentPath}">
                                            ${currentPath}
                                        </p>
                                    </div>
                                    <div class="flex-shrink-0">
                                        <i class="bi bi-chevron-right text-slate-400 group-hover:text-emerald-500 group-hover:translate-x-1 transition-all"></i>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Option 2: Restore to Original Location -->
                        <div class="group cursor-pointer" onclick="restoreToOriginal('${backupPath.replace(/'/g, "\\'")}')">
                            <div class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200">
                                <div class="flex items-center gap-4">
                                    <div class="flex-shrink-0">
                                        <div class="w-12 h-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                                            <i class="bi bi-house-fill text-xl"></i>
                                        </div>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h4 class="font-bold text-slate-900 dark:text-slate-100 text-sm mb-1">Restore to Original Location</h4>
                                        <p class="text-xs text-slate-600 dark:text-slate-400 break-all" title="${originalPath}">
                                            ${originalPath}
                                        </p>
                                    </div>
                                    <div class="flex-shrink-0">
                                        <i class="bi bi-chevron-right text-slate-400 group-hover:text-blue-500 group-hover:translate-x-1 transition-all"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } else if (!fileExists) {
                // NOT FOUND: Auto-search when clicking restore
                restoreOptionsHtml = `
                    <div class="space-y-4">
                        <div class="group cursor-pointer" onclick="startAutoSearchForFile('${backupPath.replace(/'/g, "\\'")}', '${fileName}')">
                            <div class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200">
                                <div class="flex items-center gap-4">
                                    <div class="flex-shrink-0">
                                        <div class="w-12 h-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                                            <i class="bi bi-geo-alt-fill text-xl"></i>
                                        </div>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h4 class="font-bold text-slate-900 dark:text-slate-100 text-sm mb-1">Restore to Current Location</h4>
                                        <p class="text-xs text-slate-600 dark:text-slate-400">
                                            File may be moved/deleted.
                                        </p>
                                        <p class="text-xs text-amber-600 dark:text-amber-400 mt-2">
                                            <i class="bi bi-info-circle"></i> Search for it, if found, restore it to the found location
                                        </p>
                                    </div>
                                    <div class="flex-shrink-0">
                                        <i class="bi bi-chevron-right text-slate-400 group-hover:text-yellow-500 group-hover:translate-x-1 transition-all"></i>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Option to restore directly to original location -->
                        <div class="group cursor-pointer" onclick="restoreToOriginal('${backupPath.replace(/'/g, "\\'")}')">
                            <div class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200">
                                <div class="flex items-center gap-4">
                                    <div class="flex-shrink-0">
                                        <div class="w-12 h-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                                            <i class="bi bi-house-fill text-xl"></i>
                                        </div>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h4 class="font-bold text-slate-900 dark:text-slate-100 text-sm mb-1">Restore to Original Location</h4>
                                        <p class="text-xs text-slate-600 dark:text-slate-400 break-all" title="${originalPath}">
                                            ${originalPath}
                                        </p>
                                        <p class="text-xs text-emerald-600 dark:text-emerald-400 mt-2">
                                            <i class="bi bi-info-circle"></i> File will be restored to the original location
                                        </p>
                                    </div>
                                    <div class="flex-shrink-0">
                                        <i class="bi bi-chevron-right text-slate-400 group-hover:text-blue-500 group-hover:translate-x-1 transition-all"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                // FOUND in expected location: Simple restore
                restoreOptionsHtml = `
                    <div class="space-y-3">
                        <h4 class="text-sm font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">Restore Options</h4>

                        <!-- Single option for found files -->
                        <div class="group cursor-pointer" onclick="restoreToOriginal('${backupPath.replace(/'/g, "\\'")}')">
                            <div class="p-4 btn-normal hover:bg-gray-100 dark:hover:bg-white/10 border border-slate-200 dark:border-slate-700 rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:shadow-md transition-all duration-200">
                                <div class="flex items-center gap-4">
                                    <div class="flex-shrink-0">
                                        <div class="w-12 h-12 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                                            <i class="bi bi-house-fill text-xl"></i>
                                        </div>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h4 class="font-bold text-slate-900 dark:text-slate-100 text-sm mb-1">Restore File</h4>
                                        <p class="text-xs text-slate-600 dark:text-slate-400 break-all" title="${currentPath}">
                                            ${currentPath}
                                        </p>
                                        <p class="text-xs text-emerald-600 dark:text-emerald-400 mt-2">
                                            <i class="bi bi-info-circle"></i> File found in expected location
                                        </p>
                                    </div>
                                    <div class="flex-shrink-0">
                                        <i class="bi bi-chevron-right text-slate-400 group-hover:text-emerald-500 group-hover:translate-x-1 transition-all"></i>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }

            // Create clean modal content
            const message = `
                <div class="space-y-6">
                    <!-- File Status Header -->
                    <div class="flex items-start gap-4">
                        <div class="flex-1">
                            <h3 class="font-bold text-main text-lg">${fileName}</h3>
                            <p class="text-sm ${statusColor} font-medium mt-1">${statusMessage}</p>
                        </div>
                    </div>

                    <!-- File Locations (only show if moved) -->
                    ${isMoved && fileExists ? `
                    <div class="space-y-3 bg-slate-50 dark:bg-slate-800/30 rounded-xl p-4">
                        <div class="flex items-start gap-3">
                            <div class="flex-1">
                                <p class="text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">Current Location</p>
                                <p class="font-mono text-sm text-slate-900 dark:text-slate-100 break-all bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                                    ${currentPath}
                                </p>
                            </div>
                        </div>

                        <div class="flex items-start gap-3">
                            <div class="flex-1">
                                <p class="text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">Original Location</p>
                                <p class="font-mono text-sm text-slate-900 dark:text-slate-100 break-all bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700 line-through">
                                    ${originalPath}
                                </p>
                            </div>
                        </div>
                    </div>
                    ` : ''}

                    <!-- Restore Options -->
                    ${restoreOptionsHtml}

                    <!-- File Info Summary -->
                    <div class="pt-4 border-t border-slate-200 dark:border-slate-700">
                        <div class="grid grid-cols-2 gap-4 text-xs">
                            <div>
                                <p class="text-slate-500 dark:text-slate-400 mb-1">Status</p>
                                <p class="font-medium ${statusColor}">${fileExists ? (isMoved ? 'MOVED' : 'FOUND') : 'NOT FOUND'}</p>
                            </div>
                            <div>
                                <p class="text-slate-500 dark:text-slate-400 mb-1">Size</p>
                                <p class="font-medium text-slate-900 dark:text-slate-100">${data.size ? Utils.formatBytes(data.size) : 'Unknown'}</p>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Use the updated confirmation modal
            openConfirmationModal(
                `Restore File`,
                message,
                null,
                {
                    showCancel: true,
                    cancelText: 'Cancel',
                    confirmText: '',
                    customButtons: true,
                    wideModal: true,
                    onCancel: () => {
                        // Any cleanup if needed
                    }
                }
            );

        }
    })
    .catch(err => {
        console.error('Error getting file info:', err);
    });
}

// Restoring to current location
// Update the restoreToCurrentLocation function:
function restoreToCurrentLocation(backupPath) {
    closeConfirmModal();

    // First check if file exists at current location
    fetch('/api/file-info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: backupPath })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.exists && data.actual_path) {
            // File already exists at current location - show confirmation
            const fileName = backupPath.split('/').pop() || 'file';
            const currentPath = data.actual_path;

            const message = `
                <div class="space-y-4">
                    <div class="flex items-center gap-3">
                        <div>
                            <h4 class="font-bold text-main text-sm">File Already Exists</h4>
                            <p class="text-xs text-secondary p-2">"${fileName}" already exists at:</p>
                            <p class="font-mono text-sm text-slate-900 dark:text-slate-100 break-all bg-white dark:bg-slate-800 p-2 rounded-lg border border-slate-200 dark:border-slate-700">
                                ${currentPath}
                            </p>
                        </div>
                    </div>

                    <div class="font-mono text-sm text-slate-900 dark:text-slate-100 break-all bg-white dark:bg-slate-800 p-2 rounded border border-slate-200 dark:border-slate-700">
                        <p class="text-xs text-amber-700 dark:text-amber-300">
                            <i class="bi bi-info-circle mr-1"></i>
                            Restoring will overwrite the existing file. Do you want to continue?
                        </p>
                    </div>
                </div>
            `;

            openConfirmationModal(
                'Overwrite File?',
                message,
                () => {
                    // User confirmed - proceed with restore
                    performRestoreToCurrent(backupPath);
                },
                {
                    showCancel: true,
                    cancelText: 'Cancel',
                    confirmText: 'Overwrite',
                    confirmColor: 'bg-amber-500 hover:bg-amber-600'
                }
            );
        } else {
            // File doesn't exist or location unknown, proceed with restore
            performRestoreToCurrent(backpackPath);
        }
    })
    .catch(error => {
        console.error('Error checking file existence:', error);
        // On error, proceed with restore
        showSystemNotification('warning', 'File Check Failed',
            'Could not verify if file exists. Proceeding with restore...');
        performRestoreToCurrent(backupPath);
    });
}

// Add this new function for restoring to current location
function performRestoreToCurrent(backupPath) {
    const fileName = backupPath.split('/').pop() || 'file';

    // Show loading/restoring state
    const message = `
        <div class="space-y-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                    <i class="bi bi-arrow-clockwise animate-spin text-lg"></i>
                </div>
                <div>
                    <h4 class="font-bold text-main text-sm">Restoring to Current Location</h4>
                    <p class="text-xs text-muted">Restoring "${fileName}" to its current location...</p>
                </div>
            </div>
        </div>
    `;

    openConfirmationModal(
        'Restoring File',
        message,
        null,
        {
            showCancel: true,
            cancelText: 'Cancel Restore',
            confirmText: '',
            customButtons: true,
            mediumModal: true,
            onCancel: () => {
                window.cancelRestore = true;
            }
        }
    );

    // Perform restore to current location
    performRestore(backupPath, 'current');
}

// Function to handle auto-search for NOT FOUND files
function startAutoSearchForFile(backupPath, fileName) {
    closeConfirmModal();

    // Show searching modal
    const message = `
        <div class="space-y-4">
            <div class="flex items-center gap-3">
                <div>
                    <h4 class="font-bold text-main text-sm">Searching for "${fileName}"</h4>
                    <p class="text-xs text-muted">Searching your home directory for this file...</p>
                </div>
            </div>

            <div class="space-y-2">
                <div class="flex items-center justify-between text-xs text-muted">
                    <span>Searching directories...</span>
                    <span id="search-progress" class="text-amber-600 font-medium">0%</span>
                </div>
                <div class="w-full bg-amber-200 dark:bg-amber-800 rounded-full h-2 overflow-hidden">
                    <div id="search-progress-bar" class="bg-amber-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>
        </div>
    `;

    openConfirmationModal(
        'Searching for File',
        message,
        null,
        {
            showCancel: true,
            cancelText: 'Cancel Search',
            confirmText: '',
            customButtons: true,
            mediumModal: true,
            onCancel: () => {
                window.searchCancelled = true;
            }
        }
    );

    // Start the search
    autoSearchAndRestore(backupPath, fileName);
}

// Auto search and restore function
function autoSearchAndRestore(backupPath, fileName) {
    window.searchCancelled = false;

    // Update progress
    document.getElementById('search-progress').textContent = 'Starting...';
    document.getElementById('search-progress-bar').style.width = '10%';

    fetch('/api/search-moved-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file_path: backupPath,
            fast_search: true
        })
    })
    .then(response => response.json())
    .then(data => {
        if (window.searchCancelled) return;

        document.getElementById('search-progress-bar').style.width = '100%';

        if (data.success && data.found) {
            // File found - update progress and proceed to restore
            document.getElementById('search-progress').textContent = 'Found!';
            document.getElementById('search-progress').className = 'text-emerald-600 font-medium';

            // Close search modal and show restore modal
            setTimeout(() => {
                closeConfirmModal();
                showSystemNotification('success', 'File Found',
                    `Found "${fileName}" at: ${data.current_location}`);

                // Automatically restore to found location
                restoreToFoundLocation(backupPath, data.current_location);
            }, 1000);
        } else {
            // File not found
            document.getElementById('search-progress').textContent = 'Not found';
            document.getElementById('search-progress').className = 'text-red-600 font-medium';

            setTimeout(() => {
                closeConfirmModal();

                // Offer to restore to original location
                const restoreMessage = `
                    <div class="space-y-4">
                        <div class="flex items-center gap-3">
                            <div>
                                <p class="text-xs text-secondary">File not found. Restore "${fileName}" from backup to original location?</p>
                            </div>
                        </div>
                    </div>
                `;

                openConfirmationModal(
                    'Restore from Backup',
                    restoreMessage,
                    () => {
                        restoreToOriginal(backupPath);
                    },
                    {
                        showCancel: true,
                        cancelText: 'Cancel',
                        confirmText: 'Restore',
                        mediumModal: true
                    }
                );
            }, 1500);
        }
    })
    .catch(error => {
        if (window.searchCancelled) return;

        console.error('Search error:', error);
        closeConfirmModal();
        showSystemNotification('error', 'Search Failed', 'Could not search for file.');
    });
}

// Function to restore to found location
function restoreToFoundLocation(backupPath, foundLocation) {
    const fileName = backupPath.split('/').pop() || 'file';

    // Show restoring modal
    const message = `
        <div class="space-y-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                    <i class="bi bi-arrow-clockwise animate-spin text-lg"></i>
                </div>
                <div>
                    <h4 class="font-bold text-main text-sm">Restoring "${fileName}"</h4>
                    <p class="text-xs text-muted break-all">To: ${foundLocation}</p>
                </div>
            </div>
        </div>
    `;

    openConfirmationModal(
        'Restoring File',
        message,
        null,
        {
            showCancel: true,
            cancelText: 'Cancel',
            confirmText: '',
            customButtons: true,
            mediumModal: true,
            onCancel: () => {
                window.cancelRestore = true;
            }
        }
    );

    // Perform restore to found location
    performRestore(backupPath, 'current');
}

// Update the existing performRestore function to handle 'current' location
async function performRestore(backupPath, restoreType = 'original') {
    const fileName = backupPath.split('/').pop() || 'file';

    // Close any open modals first
    closeConfirmModal();

    // Create a new modal for restore progress
    setTimeout(() => {
        const locationText = restoreType === 'current' ? 'Current Location' : 'Original Location';
        const progressMessage = `
            <div class="space-y-4">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                        <i class="bi bi-arrow-clockwise animate-spin text-lg"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-main text-sm">Restoring "${fileName}"</h4>
                        <p class="text-xs text-muted">Please wait while the file is being restored to ${locationText.toLowerCase()}...</p>
                    </div>
                </div>

                <div class="space-y-2">
                    <div class="flex items-center justify-between text-xs text-muted">
                        <span>Preparing restore...</span>
                        <span id="restore-progress" class="text-blue-600 font-medium">0%</span>
                    </div>
                    <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
                        <div id="restore-progress-bar" class="bg-blue-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                    </div>
                </div>
            </div>
        `;

        openConfirmationModal(
            'Restoring File',
            progressMessage,
            null,
            {
                showCancel: true,
                cancelText: 'Cancel Restore',
                confirmText: '',
                customButtons: true,
                mediumModal: true,
                onCancel: () => {
                    window.cancelRestore = true;
                }
            }
        );

        // Start the restore process
        startRestoreProcess(backupPath, restoreType);
    }, 300);
}


// =====================================================================
// FILE RESTORE FUNCTIONS
// =====================================================================

// Add the missing performRestore function
async function performRestore(backupPath, restoreType = 'original') {
    const fileName = backupPath.split('/').pop() || 'file';

    // Create a progress container
    // const modal = document.getElementById('confirmation-modal');
    // const modalContainer = document.getElementById('confirmation-modal-container');

    // Close any open modals first
    closeConfirmModal();

    // Create a new modal for restore progress
    setTimeout(() => {
        const progressMessage = `
            <div class="space-y-4">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center">
                        <i class="bi bi-arrow-clockwise animate-spin text-lg"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-main text-sm">Restoring "${fileName}"</h4>
                        <p class="text-xs text-muted">Please wait while the file is being restored...</p>
                    </div>
                </div>

                <div class="space-y-2">
                    <div class="flex items-center justify-between text-xs text-muted">
                        <span>Preparing restore...</span>
                        <span id="restore-progress" class="text-blue-600 font-medium">0%</span>
                    </div>
                    <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-2 overflow-hidden">
                        <div id="restore-progress-bar" class="bg-blue-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                    </div>
                </div>

                <div id="restore-details" class="text-xs text-muted">
                    <p>Restoring to: <span class="font-mono">${restoreType === 'original' ? 'Original location' : 'Current location'}</span></p>
                </div>
            </div>
        `;

        openConfirmationModal(
            'Restoring File',
            progressMessage,
            null,
            {
                showCancel: true,
                cancelText: 'Cancel Restore',
                confirmText: '',
                customButtons: true,
                mediumModal: true,
                onCancel: () => {
                    // Set a flag to cancel the restore
                    window.cancelRestore = true;
                }
            }
        );

        // Start the restore process
        startRestoreProcess(backupPath, restoreType);
    }, 300);
}

// New function to handle the actual restore process with progress
function startRestoreProcess(backupPath, restoreType) {
    const fileName = backupPath.split('/').pop() || 'file';
    window.cancelRestore = false;

    // Update progress
    updateRestoreProgress(10, 'Preparing restoration...');

    // Simulate progress while making API call
    let simulatedProgress = 10;
    const progressInterval = setInterval(() => {
        if (window.cancelRestore) {
            clearInterval(progressInterval);
            closeConfirmModal();
            showSystemNotification('info', 'Restore Cancelled', 'File restoration was cancelled.');
            return;
        }

        simulatedProgress += Math.random() * 5;
        if (simulatedProgress > 90) simulatedProgress = 90;

        const messages = [
            'Preparing restoration...',
            'Connecting to backup...',
            'Locating file versions...',
            'Preparing destination...',
            'Copying file data...'
        ];

        const messageIndex = Math.floor((simulatedProgress / 90) * (messages.length - 1));
        updateRestoreProgress(Math.floor(simulatedProgress), messages[messageIndex]);
    }, 500);

    // Make API call to backend
    fetch('/api/restore-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file_path: backupPath,
            restore_to: restoreType
        })
    })
    .then(response => {
        clearInterval(progressInterval);

        if (window.cancelRestore) {
            return Promise.reject(new Error('Cancelled by user'));
        }

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        return response.json();
    })
    .then(data => {
        if (window.cancelRestore) return;

        if (data && data.success) {
            // Success!
            updateRestoreProgress(100, 'Restoration complete!');

            setTimeout(() => {
                closeConfirmModal();
                showSystemNotification('success', 'File Restored',
                    `"${fileName}" has been restored successfully.`);

                // Refresh the file preview if it's open
                if (selectedFile) {
                    selectFile(selectedFile);
                }
            }, 1000);
        } else {
            // Error from server
            const errorMsg = data ? data.error : 'Unknown error occurred';
            showRestoreError(errorMsg);
        }
    })
    .catch(error => {
        clearInterval(progressInterval);

        if (window.cancelRestore) return;

        if (error.message === 'Cancelled by user') {
            closeConfirmModal();
        } else {
            showRestoreError(error.message || 'Network error');
        }
    });
}

function showRestoreError(errorMessage) {
    updateRestoreProgress(100, 'Restoration failed');

    setTimeout(() => {
        closeConfirmModal();
        showSystemNotification('error', 'Restoration Failed', errorMessage);
    }, 1000);
}

// Helper functions for restore progress
function updateRestoreProgress(percent, message) {
    const progressBar = document.getElementById('restore-progress-bar');
    const progressText = document.getElementById('restore-progress');
    const detailsEl = document.getElementById('restore-details');

    if (progressBar) {
        progressBar.style.width = `${percent}%`;
        progressBar.className = percent === 100 ?
            'bg-green-500 h-full rounded-full transition-all duration-300' :
            'bg-blue-500 h-full rounded-full transition-all duration-300';
    }

    if (progressText) {
        progressText.textContent = `${percent}%`;
        progressText.className = percent === 100 ?
            'text-green-600 font-medium' :
            'text-blue-600 font-medium';
    }

    if (detailsEl && message) {
        detailsEl.innerHTML = `<p>${message}</p>`;
    }
}

// Restore to original location
function restoreToOriginal(backupPath, buttonElement) {
    // First check if file exists at original location
    fetch('/api/file-info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: backupPath })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && data.exists) {
            // File already exists - show custom confirmation modal
            const fileName = backupPath.split('/').pop() || 'file';
            const originalPath = data.actual_path || data.home_path || 'Unknown location';

            const message = `
                <div class="space-y-4">
                    <div class="flex items-center gap-3">
                        <div>
                            <h4 class="font-bold text-main text-sm">File Already Exists</h4>
                            <p class="text-xs text-secondary p-2">"${fileName}" already exists at:</p>
                            <p class="font-mono text-sm text-slate-900 dark:text-slate-100 break-all bg-white dark:bg-slate-800 p-2 rounded border border-slate-200 dark:border-slate-700">
                                ${originalPath}
                            </p>
                        </div>
                    </div>

                    <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-2">
                        <p class="text-xs text-amber-700 dark:text-amber-300">
                            <i class="bi bi-info-circle mr-1"></i>
                            Restoring will overwrite the existing file. Do you want to continue?
                        </p>
                    </div>
                </div>
            `;

            openConfirmationModal(
                'Overwrite File?',
                message,
                () => {
                    // User confirmed - proceed with restore
                    closeConfirmModal();
                    performRestore(backupPath, 'original', buttonElement);
                },
                {
                    showCancel: true,
                    cancelText: 'Cancel',
                    confirmText: 'Overwrite',
                    confirmColor: 'bg-amber-500 hover:bg-amber-600'
                }
            );
        } else {
            // File doesn't exist, proceed with restore
            performRestore(backupPath, 'original', buttonElement);
        }
    })
    .catch(error => {
        console.error('Error checking file existence:', error);
        // On error, show notification and proceed with restore
        showSystemNotification('warning', 'File Check Failed',
            'Could not verify if file exists. Proceeding with restore...');
        performRestore(backupPath, 'original', buttonElement);
    });
}

// Restore to found location
function restoreToFoundLocation(backupPath, foundLocation) {
    // Create a mock button element for the restore process
    const mockButton = document.createElement('button');
    mockButton.innerHTML = '<i class="bi bi-download"></i> Restore File';
    mockButton.className = 'btn-normal text-hyperlink';

    // Perform restore to the found location
    fetch('/api/restore-file', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            file_path: backupPath,
            restore_to: 'current'  // Use current location from database
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSystemNotification('success', 'File Restored',
                `File restored to its current location.`);
            closeRestoreOptionsModal();
        } else {
            showSystemNotification('error', 'Restoration Failed',
                data.error || 'Failed to restore file.');
        }
    })
    .catch(error => {
        console.error('Restore error:', error);
        showSystemNotification('error', 'Network Error', 'Could not connect to server.');
    });
}

// Choose custom location
function chooseCustomLocation(backupPath, buttonElement) {
    // Simple implementation - you can enhance this with a file picker dialog
    const customPath = prompt('Enter custom directory path:');
    if (customPath && os.path.isdir(customPath)) {
        performRestore(backupPath, customPath, buttonElement);
    } else if (customPath) {
        alert('Invalid directory path. Please enter a valid directory.');
    }
}

// Update the restoreFile function to use performRestore
async function restoreFile(buttonElement) {
    if (buttonElement.disabled) return;

    const backupPath = buttonElement.dataset.filepath;
    const fileName = backupPath.split('/').pop() || 'file';

    if (!backupPath) {
        console.warn("No file path provided for restoration.");
        return;
    }

    // First, check file existence and location
    try {
        const response = await fetch('/api/file-info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: backupPath })
        });

        const data = await response.json();

        if (data.success) {
            if (data.exists) {
                // File exists - show options
                showRestoreOptionsModal(backupPath, fileName, buttonElement);
            } else {
                // File doesn't exist - show search options
                showRestoreOptionsModal(backupPath, fileName, buttonElement);
            }
        } else {
            // Fallback to simple restore
            performRestore(backupPath, 'original', buttonElement);
        }
    } catch (error) {
        console.error('Error checking file info:', error);
        // Fallback to simple restore
        performRestore(backupPath, 'original', buttonElement);
    }
}

// Replace the showRestoreOptionsModal function with this:
function showRestoreOptionsModal(backupPath, fileName, originalButton) {
    const expectedPath = getOriginalLocationFromBackup(backupPath);
    const fileBasename = fileName;

    // Create options content
    const optionsHtml = `
        <div class="space-y-4">
            <!-- Option 1: Restore to Original Location -->
            <div class="group cursor-pointer" onclick="selectRestoreOption('original', '${backupPath.replace(/'/g, "\\'")}', '${originalButton.id || 'restore-btn'}')">
                <div class="p-4 bg-card border border-main rounded-xl hover:border-blue-500 dark:hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all duration-200">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                            <i class="bi bi-folder2-open text-lg"></i>
                        </div>
                        <div class="flex-1">
                            <h4 class="font-bold text-main text-sm">Restore to Original Location</h4>
                            <p class="text-xs text-muted truncate mt-0.5" title="${expectedPath}">${expectedPath}</p>
                        </div>
                        <i class="bi bi-chevron-right text-muted group-hover:text-blue-500 group-hover:translate-x-1 transition-all"></i>
                    </div>
                </div>
            </div>

            <!-- Option 2: Search for Moved File -->
            <div class="group cursor-pointer" onclick="selectRestoreOption('search', '${backupPath.replace(/'/g, "\\'")}', '${originalButton.id || 'restore-btn'}')">
                <div class="p-4 bg-card border border-main rounded-xl hover:border-amber-500 dark:hover:border-amber-500 hover:bg-amber-50 dark:hover:bg-amber-900/20 transition-all duration-200">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-amber-100 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 flex items-center justify-center group-hover:scale-110 transition-transform">
                            <i class="bi bi-search text-lg"></i>
                        </div>
                        <div class="flex-1">
                            <h4 class="font-bold text-main text-sm">Search for Moved File</h4>
                            <p class="text-xs text-muted mt-0.5">Find where this file was moved in your home directory</p>
                        </div>
                        <i class="bi bi-chevron-right text-muted group-hover:text-yellow-500 group-hover:translate-x-1 transition-all"></i>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Use your existing confirmation modal
    openConfirmationModal(
        `Restore "${fileBasename}"`,
        optionsHtml,
        null, // No immediate action on confirm
        {
            showCancel: true,
            cancelText: 'Cancel',
            confirmText: '', // No confirm button needed
            customButtons: true,
            wideModal: true
        }
    );

    // Store the backup path and original button in global variables
    window.currentRestoreData = {
        backupPath: backupPath,
        fileName: fileName,
        originalButton: originalButton
    };
}

// Add this new function to handle option selection:
function selectRestoreOption(optionType, backupPath, buttonId) {
    closeConfirmModal(); // Close the confirmation modal

    const originalButton = window.currentRestoreData?.originalButton ||
                          document.getElementById(buttonId);

    switch(optionType) {
        case 'original':
            // Restore to original location
            restoreToOriginal(backupPath, originalButton);
            break;

        case 'search':
            // Search for moved file
            openSearchModal(backupPath, originalButton);
            break;
    }
}

// Add this function for the search modal:
function openSearchModal(backupPath, originalButton) {
    const fileName = window.currentRestoreData?.fileName || backupPath.split('/').pop();

    // Create search modal content
    const searchHtml = `
        <div class="space-y-4" id="search-modal-content">
            <div class="p-4 border border-amber-200 dark:border-amber-700 rounded-xl bg-amber-50 dark:bg-amber-900/20">
                <div class="flex items-center gap-3">
                    <div class="flex-1">
                        <h4 class="font-bold text-sm text-main">Searching for "${fileName}"</h4>
                        <p class="text-xs text-muted mt-0.5">Searching your home directory for this file...</p>
                    </div>
                </div>
            </div>

            <div class="space-y-2">
                <div class="flex items-center justify-between text-xs text-muted">
                    <span>Calculating file hash</span>
                    <span id="hash-progress" class="text-amber-600 font-medium">Starting...</span>
                </div>
                <div class="w-full bg-amber-200 dark:bg-amber-800 rounded-full h-2 overflow-hidden">
                    <div id="hash-progress-bar" class="bg-amber-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
                </div>
            </div>

            <div id="search-results" class="hidden">
                <!-- Results will be shown here -->
            </div>
        </div>
    `;

    // Open search modal
    openConfirmationModal(
        'Search for Moved File',
        searchHtml,
        null,
        {
            showCancel: true,
            cancelText: 'Close',
            confirmText: '',
            customButtons: true,
            wideModal: true,
            onCancel: () => {
                // Clean up any ongoing search
                window.searchCancelled = true;
            }
        }
    );

    // Start the search
    startFileSearch(backupPath, originalButton);
}

// Update the startFileSearch function:
function startFileSearch(backupPath, originalButton) {
    const fileName = window.currentRestoreData?.fileName || backupPath.split('/').pop();
    window.searchCancelled = false;

    // Update progress
    document.getElementById('hash-progress').textContent = 'Calculating...';
    document.getElementById('hash-progress-bar').style.width = '25%';

    fetch('/api/search-moved-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file_path: backupPath,
            fast_search: true
        })
    })
    .then(response => response.json())
    .then(data => {
        if (window.searchCancelled) return;

        document.getElementById('hash-progress-bar').style.width = '100%';

        if (data.success && data.found) {
            // File found
            document.getElementById('hash-progress').textContent = 'Found!';
            document.getElementById('hash-progress').className = 'text-emerald-600 font-medium';

            const resultsHtml = `
                <div class="p-4 border border-emerald-200 dark:border-emerald-700 rounded-xl bg-emerald-50 dark:bg-emerald-900/20 mt-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                                <i class="bi bi-check-lg text-lg"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm text-main">File Found!</h4>
                                <p class="text-xs text-muted truncate max-w-[200px]" title="${data.current_location}">
                                    ${data.current_location.replace(/^.*\//, '.../')}
                                </p>
                                <p class="text-xs text-emerald-600 dark:text-emerald-400 mt-1">
                                    <i class="bi bi-clock"></i> Found in ${data.search_time.toFixed(2)}s
                                </p>
                            </div>
                        </div>
                        <button onclick="restoreFoundFile('${backupPath.replace(/'/g, "\\'")}', '${data.current_location.replace(/'/g, "\\'")}', this)"
                                class="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-1">
                            <i class="bi bi-download"></i> Restore Here
                        </button>
                    </div>
                </div>
            `;

            document.getElementById('search-results').innerHTML = resultsHtml;
            document.getElementById('search-results').classList.remove('hidden');

        } else {
            // File not found
            document.getElementById('hash-progress').textContent = 'Not found';
            document.getElementById('hash-progress').className = 'text-red-600 font-medium';

            const resultsHtml = `
                <div class="p-4 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-900/20 mt-4">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 flex items-center justify-center">
                            <i class="bi bi-file-earmark-x text-lg"></i>
                        </div>
                        <div>
                            <h4 class="font-bold text-sm text-main">File Not Found</h4>
                            <p class="text-xs text-muted mt-0.5">The file was not found in your home directory.</p>
                            <p class="text-xs text-muted">Search took ${data.search_time ? data.search_time.toFixed(2) : '?'}s</p>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('search-results').innerHTML = resultsHtml;
            document.getElementById('search-results').classList.remove('hidden');
        }
    })
    .catch(error => {
        if (window.searchCancelled) return;

        document.getElementById('hash-progress').textContent = 'Error';
        document.getElementById('hash-progress').className = 'text-red-600 font-medium';

        const resultsHtml = `
            <div class="p-4 border border-red-200 dark:border-red-700 rounded-xl bg-red-50 dark:bg-red-900/20 mt-4">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 flex items-center justify-center">
                        <i class="bi bi-exclamation-triangle text-lg"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-sm text-main">Search Failed</h4>
                        <p class="text-xs text-muted mt-0.5">Error: ${error.message || 'Network error'}</p>
                    </div>
                </div>
            </div>
        `;

        document.getElementById('search-results').innerHTML = resultsHtml;
        document.getElementById('search-results').classList.remove('hidden');
    });
}

// Add this function to restore found files:
function restoreFoundFile(backupPath, foundLocation, buttonElement) {
    const fileName = window.currentRestoreData?.fileName || backupPath.split('/').pop();

    buttonElement.disabled = true;
    buttonElement.innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-2"></i> Restoring...';

    fetch('/api/restore-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file_path: backupPath,
            restore_to: 'current'  // Use current location from database
        })
    })
    .then(response => response.json())
    .then(data => {
        closeConfirmModal(); // Close the search modal

        if (data.success) {
            showSystemNotification('success', 'File Restored',
                `"${fileName}" has been restored to its current location.`);

            // Update the original restore button in the file preview
            const originalButton = window.currentRestoreData?.originalButton;
            if (originalButton) {
                originalButton.innerHTML = '<i class="bi bi-check-lg mr-2"></i> Restored!';
                originalButton.className = 'px-3 py-1.5 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 text-emerald-700 dark:text-emerald-400 rounded text-xs font-bold cursor-default flex items-center gap-2';
                originalButton.disabled = true;
            }
        } else {
            showSystemNotification('error', 'Restoration Failed',
                data.error || 'Failed to restore file.');
        }
    })
    .catch(error => {
        console.error('Restore error:', error);
        showSystemNotification('error', 'Network Error', 'Could not connect to server.');
    });
}

// function openConfirmationModal(title, desc, callback, options = {}) {
//     const modal = document.getElementById('confirmation-modal');
//     const modalContainer = document.getElementById('confirmation-modal-container');
//     const titleEl = document.getElementById('modal-title');
//     const descEl = document.getElementById('modal-desc');
//     const confirmBtn = document.getElementById('modal-confirm-btn');
//     const cancelBtn = document.getElementById('modal-cancel-btn');

//     console.log('Opening confirmation modal with options:', options);

//     if (modal && modalContainer && titleEl && descEl && confirmBtn && cancelBtn) {
//         titleEl.innerText = title;
//         descEl.innerHTML = desc;

//         // Set width based on options
//         if (options.wideModal) {
//             modalContainer.classList.remove('max-w-lg', 'max-w-md');
//             modalContainer.classList.add('max-w-2xl');
//         } else if (options.mediumModal) {
//             modalContainer.classList.remove('max-w-lg', 'max-w-2xl');
//             modalContainer.classList.add('max-w-md');
//         } else {
//             modalContainer.classList.remove('max-w-md', 'max-w-2xl');
//             modalContainer.classList.add('max-w-lg');
//         }

//         // Handle custom buttons
//         if (options.customButtons) {
//             confirmBtn.classList.add('hidden');
//             cancelBtn.textContent = options.cancelText || 'Cancel';
//             cancelBtn.className = "px-4 py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer";

//             if (options.onCancel) {
//                 cancelBtn.onclick = () => {
//                     closeConfirmModal();
//                     options.onCancel();
//                 };
//             } else {
//                 cancelBtn.onclick = closeConfirmModal;
//             }
//         } else {
//             confirmBtn.classList.remove('hidden');
//             confirmBtn.textContent = options.confirmText || 'Confirm';
//             cancelBtn.textContent = options.cancelText || 'Cancel';

//             // Use custom color if provided, otherwise use brand color
//             const confirmColor = options.confirmColor;
//             // confirmBtn.className = `px-4 py-2 rounded-lg ${confirmColor} text-white transition`;
//             confirmBtn.className = `btn-primary px-4 py-2 rounded-lg ${confirmColor} border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer`;
//             cancelBtn.className = 'px-4 py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer';
//             pendingAction = callback;

//             confirmBtn.onclick = confirmAction;
//             cancelBtn.onclick = closeConfirmModal;
//         }

//         // Add entrance animation
//         modalContainer.classList.remove('opacity-0', 'scale-95');
//         modalContainer.classList.add('opacity-100', 'scale-100');

//         modal.classList.remove('hidden');
//         modal.classList.add('flex');
//     }
// }

// function closeConfirmModal() {
//     const modal = document.getElementById('confirmation-modal');
//     const modalContainer = document.getElementById('confirmation-modal-container');

//     if (modal && modalContainer) {
//         // Exit animation
//         modalContainer.classList.remove('opacity-100', 'scale-100');
//         modalContainer.classList.add('opacity-0', 'scale-95');

//         setTimeout(() => {
//             modal.classList.add('hidden');
//             modal.classList.remove('flex');
//             // Reset to default width
//             modalContainer.classList.remove('max-w-md', 'max-w-2xl');
//             modalContainer.classList.add('max-w-lg');
//         }, 200);

//         pendingAction = null;
//     }
// }


/**
 * Opens a confirmation modal with customizable title, description, and buttons.
 *
 * @param {string} title - The title of the modal.
 * @param {string} desc - The HTML content for the modal's description.
 * @param {function} callback - The function to execute when the confirm button is clicked (if not using custom buttons).
 * @param {object} options - An object to customize the modal's behavior and appearance.
 * @param {boolean} [options.showCancel=true] - Whether to show the cancel button.
 * @param {string} [options.cancelText='Cancel'] - The text for the cancel button.
 * @param {string} [options.confirmText='Confirm'] - The text for the confirm button.
 * @param {string} [options.confirmColor='bg-blue-500 hover:bg-blue-600'] - Tailwind CSS classes for the confirm button's color.
 * @param {boolean} [options.customButtons=false] - If true, the confirm button is hidden, and the cancel button can be customized.
 * @param {boolean} [options.wideModal=false] - If true, the modal will be wider (max-w-2xl).
 * @param {boolean} [options.mediumModal=false] - If true, the modal will be medium width (max-w-md).
 * @param {function} [options.onCancel=null] - Callback function to execute when the cancel button is clicked.
 */
function openConfirmationModal(title, desc, callback, options = {}) {
    const modal = document.getElementById('confirmation-modal');
    const modalContainer = document.getElementById('confirmation-modal-container');
    const titleEl = document.getElementById('modal-title');
    const descEl = document.getElementById('modal-desc');
    const confirmBtn = document.getElementById('modal-confirm-btn');
    const cancelBtn = document.getElementById('modal-cancel-btn');

    console.log('Opening confirmation modal with options:', options);

    if (modal && modalContainer && titleEl && descEl && confirmBtn && cancelBtn) {
        titleEl.innerText = title;
        descEl.innerHTML = desc;

        // Set width based on options
        if (options.wideModal) {
            modalContainer.classList.remove('max-w-lg', 'max-w-md');
            modalContainer.classList.add('max-w-2xl');
        } else if (options.mediumModal) {
            modalContainer.classList.remove('max-w-lg', 'max-w-2xl');
            modalContainer.classList.add('max-w-md');
        } else {
            modalContainer.classList.remove('max-w-md', 'max-w-2xl');
            modalContainer.classList.add('max-w-lg');
        }

        // Handle custom buttons
        if (options.customButtons) {
            confirmBtn.classList.add('hidden');
            cancelBtn.textContent = options.cancelText || 'Cancel';
            cancelBtn.className = "px-4 py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer";

            if (options.onCancel) {
                cancelBtn.onclick = () => {
                    closeConfirmModal();
                    options.onCancel();
                };
            } else {
                cancelBtn.onclick = closeConfirmModal;
            }
        } else {
            // --- Standard Buttons Path ---
            confirmBtn.classList.remove('hidden');
            confirmBtn.textContent = options.confirmText || 'Confirm';
            cancelBtn.textContent = options.cancelText || 'Cancel';

            // Use custom color if provided, otherwise use brand color
            const confirmColor = options.confirmColor;
            confirmBtn.className = `btn-primary px-4 py-2 rounded-lg ${confirmColor} border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer`;
            cancelBtn.className = 'px-4 py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main font-bold transition cursor-pointer';

            // FIX: Prioritize options.onConfirm for the Confirm button
            if (options.onConfirm) {
                confirmBtn.onclick = () => {
                    closeConfirmModal(); // Close the modal first
                    options.onConfirm(); // Execute the confirmation callback
                };
            } else {
                // Fallback to the old method (using global `pendingAction` and `confirmAction`)
                pendingAction = callback;
                confirmBtn.onclick = confirmAction;
            }

            // FIX: Handle options.onCancel for the Cancel button
            if (options.onCancel) {
                cancelBtn.onclick = () => {
                    closeConfirmModal(); // Close the modal first
                    options.onCancel(); // Execute the cancel callback
                };
            } else {
                // Default cancel action: just close the modal
                cancelBtn.onclick = closeConfirmModal;
            }
            // --- End of Standard Buttons Path ---
        }

        // Add entrance animation
        modalContainer.classList.remove('opacity-0', 'scale-95');
        modalContainer.classList.add('opacity-100', 'scale-100');

        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }
}

// Keep closeConfirmModal function as is
function closeConfirmModal() {
    const modal = document.getElementById('confirmation-modal');
    const modalContainer = document.getElementById('confirmation-modal-container');

    if (modal && modalContainer) {
        // Exit animation
        modalContainer.classList.remove('opacity-100', 'scale-100');
        modalContainer.classList.add('opacity-0', 'scale-95');

        setTimeout(() => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
            // Reset to default width
            modalContainer.classList.remove('max-w-md', 'max-w-2xl');
            modalContainer.classList.add('max-w-lg');
        }, 200);

        pendingAction = null;
    }
}

function closeRestoreOptionsModal() {
    const modal = document.getElementById('restore-options-modal');
    if (modal) {
        modal.remove();
    }
}

// =====================================================================
// --- MODALS & CONFIRMATIONS ---
// =====================================================================

function openProModal() { document.getElementById('pro-modal').classList.remove('hidden'); }
function closeProModal() { document.getElementById('pro-modal').classList.add('hidden'); }

function closeConfirmModal() { document.getElementById('confirmation-modal').classList.add('hidden'); pendingAction = null; }
function confirmAction() { if (pendingAction) pendingAction(); closeConfirmModal(); }



function getOriginalLocationFromBackup(backupPath) {
    // Extract the relative path from .main_backup
    if (backupPath.includes('.main_backup')) {
        const relativePath = backupPath.split('.main_backup')[1].replace(/^[\\/]+/, '');
        return `~/${relativePath}`;
    }
    return backupPath;
}

function searchForMovedFile(backupPath, buttonElement) {
    const container = buttonElement.parentElement;

    // Show searching state
    container.innerHTML = `
        <div class="p-4 border border-amber-200 dark:border-amber-700 rounded-xl bg-amber-50 dark:bg-amber-900/20">
            <div class="flex items-center gap-3">
                <div class="flex-1">
                    <h4 class="font-bold text-sm text-main">Searching for moved file...</h4>
                    <div class="mt-1">
                        <div class="flex items-center justify-between text-xs text-muted mb-1">
                            <span>Calculating file hash</span>
                            <span class="text-amber-600 font-medium">0%</span>
                        </div>
                        <div class="w-full bg-amber-200 dark:bg-amber-800 rounded-full h-1.5 overflow-hidden">
                            <div class="bg-amber-500 h-full rounded-full transition-all duration-300" style="width: 25%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    fetch('/api/search-moved-file', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            file_path: backupPath,
            fast_search: true
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success && data.found) {
            // Found moved file - show success with restore option
            container.innerHTML = `
                <div class="p-4 border border-emerald-200 dark:border-emerald-700 rounded-xl bg-emerald-50 dark:bg-emerald-900/20">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-lg bg-emerald-100 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
                                <i class="bi bi-check-lg text-lg"></i>
                            </div>
                            <div>
                                <h4 class="font-bold text-sm text-main">Found moved file!</h4>
                                <p class="text-xs text-muted truncate max-w-[200px]" title="${data.current_location}">
                                    ${data.current_location.replace(/^.*\//, '.../')}
                                </p>
                                <p class="text-xs text-emerald-600 dark:text-emerald-400 mt-1">
                                    <i class="bi bi-clock"></i> Found in ${data.search_time.toFixed(2)}s
                                </p>
                            </div>
                        </div>
                        <button onclick="performRestore('${backupPath.replace(/'/g, "\\'")}', 'current', this)"
                                class="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-600 text-white text-xs font-bold rounded-lg transition-colors flex items-center gap-1">
                            <i class="bi bi-download"></i> Restore Here
                        </button>
                    </div>
                </div>
            `;
        } else {
            // Not found - show message
            container.innerHTML = `
                <div class="p-4 border border-slate-200 dark:border-slate-700 rounded-xl bg-slate-50 dark:bg-slate-900/20">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 flex items-center justify-center">
                            <i class="bi bi-file-earmark-x text-lg"></i>
                        </div>
                        <div>
                            <h4 class="font-bold text-sm text-main">Moved file not found</h4>
                            <p class="text-xs text-muted mt-0.5">Search took ${data.search_time ? data.search_time.toFixed(2) : '?'}s</p>
                        </div>
                    </div>
                </div>
            `;
        }
    })
    .catch(error => {
        console.error('Search error:', error);
        container.innerHTML = `
            <div class="p-4 border border-red-200 dark:border-red-700 rounded-xl bg-red-50 dark:bg-red-900/20">
                <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-lg bg-red-100 dark:bg-red-900/30 text-red-600 dark:text-red-400 flex items-center justify-center">
                        <i class="bi bi-exclamation-triangle text-lg"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-sm text-main">Search failed</h4>
                        <p class="text-xs text-muted mt-0.5">Error searching for file: ${error.message || 'Unknown error'}</p>
                    </div>
                </div>
            </div>
        `;
    });
}

async function checkFileExistence(backupPath) {
    try {
        const response = await fetch('/api/file-info', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ file_path: backupPath })
        });
        return await response.json();
    } catch (error) {
        console.error('Error checking file existence:', error);
        return { exists: false };
    }
}


function switchSettingsTab(tabName) {
    activeSettingsTab = tabName;
    ['folders', 'general'].forEach(t => {
        const btn = document.getElementById(`sub-tab-btn-${t}`);
        const content = document.getElementById(`settings-tab-${t}`);
        if (t === tabName) {
            btn.className = "px-4 py-2 text-sm font-bold text-sm font-bold text-hyperlink border-b-2 cursor-pointer border-hyperlink";
            content.classList.remove('hidden');
        } else {
            btn.className = "px-4 py-2 text-sm font-bold text-secondary border-b-2 border-transparent hover:text-secondary hover:text-secondary cursor-pointer";
            content.classList.add('hidden');
        }
    });
}

/**
 * Triggers the confirmation modal before saving settings (watched folders).
 */
function initiateSettingsSave() {
    const count = homeFolders.filter(f => f.selected).length;

    openConfirmationModal(
        "Update Watched Folders?",
        // Improved confirmation message:
        `You are about to set <span class="font-bold text-slate-800">${count} folder${count !== 1 ? 's' : ''}</span> for continuous, real-time backup. Are you sure?`,
        // This is the callback function that runs on CONFIRM:
        () => {
            showSystemNotification(
                'info',
                'Backup Settings Saved',
                `${count} folder${count !== 1 ? 's have' : ' has'} been set for real-time backup.`
            );
            // Optionally add other save logic here (e.g., calling a backend save function)
        }
    );
}


// =====================================================================
// --- GENERAL SETTINGS LOGIC ---
// =====================================================================

function toggleGeneralSetting(settingKey) {
    switch(settingKey) {
        case 'updates':
            generalSettings.autoUpdates = document.getElementById('chk-auto-updates').checked;
            // Save to localStorage or backend
            // saveGeneralSettings();
            break;

        case 'notifications':
            generalSettings.showNotifications = document.getElementById('chk-show-notifications').checked;
            // Save to localStorage or backend
            // saveGeneralSettings();
            break;
    }
    console.log('General settings updated:', generalSettings);
}

// Add this function to save general settings
function saveGeneralSettings() {
    const saveBtn = document.querySelector('button[onclick="saveGeneralSettings()"]');
    if (!saveBtn) return;

    const originalText = saveBtn.innerHTML;
    saveBtn.innerHTML = '<i class="bi bi-arrow-clockwise animate-spin"></i> Saving...';
    saveBtn.disabled = true;

    setTimeout(() => {
        try {
            // Save to localStorage
            localStorage.setItem('timeMachine_generalSettings', JSON.stringify(generalSettings));

            showSystemNotification('success', 'Settings Saved', 'General preferences have been saved successfully.');
            console.log('General settings saved:', generalSettings);
        } catch (error) {
            showSystemNotification('error', 'Save Failed', 'Could not save settings. Please try again.');
        } finally {
            saveBtn.innerHTML = originalText;
            saveBtn.disabled = false;
        }
    }, 800);
}

// Add this function to load saved settings
function loadGeneralSettings() {
    try {
        const saved = localStorage.getItem('timeMachine_generalSettings');
        if (saved) {
            const parsed = JSON.parse(saved);
            generalSettings = { ...generalSettings, ...parsed };

            // Update checkboxes if they exist
            const startupCheckbox = document.getElementById('chk-auto-startup');
            const updatesCheckbox = document.getElementById('chk-auto-updates');
            const notificationsCheckbox = document.getElementById('chk-show-notifications');

            if (startupCheckbox) startupCheckbox.checked = generalSettings.autoStartup;
            if (updatesCheckbox) updatesCheckbox.checked = generalSettings.autoUpdates;
            if (notificationsCheckbox) notificationsCheckbox.checked = generalSettings.showNotifications;
        }
    } catch (error) {
        console.log('No saved general settings found, using defaults.');
    }
}

function renderSettings() {
    const container = document.getElementById('folder-selection-list');
    if (!container) return;

    // Show loading
    container.innerHTML = '<div class="p-4 text-center text-slate-500">Scanning home folders...</div>';

    // Get user's home folders
    fetch('/api/backup-folders')
        .then(res => res.json())
        .then(data => {
            if (!data.success) {
                container.innerHTML = `<div class="p-4 text-red-500">${data.error}</div>`;
                return;
            }

            homeFolders = data.folders; // Update global array
            renderFolderList();        // Render the UI based on new data
            updateSummaryText();       // Update the count
            loadGeneralSettings();     // Load general settings
        })
        .catch(err => {
            container.innerHTML = '<div class="p-4 text-red-500">Failed to load folders from server.</div>';
        });
}


// **********************************************
// 2. REQUIRED SUPPORT FUNCTIONS (Implement or verify existence)
// **********************************************

// Required to update in-memory state when a checkbox is clicked
function toggleFolder(index) {
    if (homeFolders[index]) {
        homeFolders[index].selected = !homeFolders[index].selected;
        updateSummaryText();
    }
}

// Required to send the selection to the backend
function initiateSettingsSave() {
    // Filter only the paths that have 'selected: true'
    const selectedPaths = homeFolders.filter(f => f.selected).map(f => f.path);

    // Saved selected folders to backup to backend
    fetch('/api/save-backup-folders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ folders: selectedPaths })
    })
    .then(res => res.json())
    .then(data => {
        if(data.success) {
            // Assuming showSystemNotification exists
            showSystemNotification('success', 'Saved', 'Backup configuration updated.');
        } else {
            showSystemNotification('error', 'Error', data.error);
        }
    })
    .catch(err => {
        showSystemNotification('error', 'Error', 'Network request failed.');
    });
}

// Backup
// function updateSummaryText() {
//     const count = homeFolders.filter(f => f.selected).length;
//     const el = document.getElementById('backup-summary-text');
//     if(el) el.innerText = `${count} folder(s) selected`;
// }

function updateSummaryText() {
    const count = homeFolders.filter(f => f.selected).length;
    const el = document.getElementById('backup-summary-text');
    if(el) el.innerText = `${count} folders selected for monitoring`;
}

function toggleAllFolders(state) {
    if (!Array.isArray(homeFolders)) return;

    // 1. Loop through the global array and update the state
    homeFolders.forEach(folder => {
        folder.selected = state;
    });

    // 2. Re-render the list to update the visual state of the checkboxes
    renderFolderList();

    // 3. Update the visible count
    updateSummaryText();
}


// =====================================================================
// --- SETTINGS (Pure Gray Style) ---
// =====================================================================
// Backup
// function renderFolderList() {
//     const container = document.getElementById('folder-selection-list');
//     if (!container) return;

//     container.innerHTML = ''; // Clear previous content

//     if (homeFolders.length === 0) {
//         container.innerHTML = '<div class="p-4 text-center">No folders found.</div>';
//         return;
//     }

//     // Render every folder found in Home
//     homeFolders.forEach((folder, index) => {
//         const isChecked = folder.selected ? 'checked' : '';

//         // This is your existing HTML template:
//         container.innerHTML += `
//         <div class="flex items-center justify-between p-4">
//             <div class="flex items-center gap-4">
//                 <div class="w-10 h-10 btn-normal rounded-lg text-hyperlink text-xl flex items-center justify-center">
//                     <i class="bi ${folder.icon}"></i>
//                 </div>
//                 <div>
//                     <h5 class="font-bold text-main text-sm">${folder.name}</h5>
//                     <p class="text-xs text-slate-400 font-mono">${folder.path}</p>
//                 </div>
//             </div>
//             <label class="relative inline-flex items-center cursor-pointer">
//                 <input type="checkbox" class="sr-only peer" onchange="toggleFolder(${index})" ${isChecked}>
//                 <div class="checkbox-normal"></div>
//             </label>
//         </div>`;
//     });
// }

function renderFolderList() {
    const container = document.getElementById('folder-selection-list');
    if (!container) return;
    container.innerHTML = '';

    if (homeFolders.length === 0) {
        return;
    }

    homeFolders.forEach((folder, idx) => {
        container.innerHTML += `
            <div class="flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors">
                <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-lg bg-gray-100 dark:bg-white/10 text-main flex items-center justify-center">
                        <i class="bi ${folder.icon || 'bi-folder'}"></i>
                    </div>
                    <div>
                        <h5 class="text-sm font-bold text-main">${folder.name}</h5>
                        <p class="text-xs text-muted font-mono">${folder.path}</p>
                    </div>
                </div>
                <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" class="sr-only peer" ${folder.selected ? 'checked' : ''} onchange="toggleFolder(${idx})">
                    <div class="checkbox-normal"></div>
                </label>
            </div>
        `;
    });
    updateSummaryText();
}


// =====================================================================
// --- 8. CUSTOM SYSTEM NOTIFICATIONS (Toast Logic) ---
// =====================================================================

/**
 * Shows a custom, non-blocking notification toast at the bottom center.
 * @param {string} type - The type of notification ('success', 'error', 'info').
 * @param {string} title - The main title of the notification.
 * @param {string} message - The detailed message.
 * @param {number} duration - How long to show the notification (in ms). Default is 4000.
 */
function showSystemNotification(type, title, message, duration = 4000) {
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
    // Animate from top-center
    toast.className = `w-80 p-4 rounded-xl shadow-lg flex items-start gap-3 transition-all transform duration-300 pointer-events-auto opacity-0 -translate-y-full ${colorClass}`;

    // Structure for the notification content
    toast.innerHTML = `
        <i class="bi ${iconClass} text-xl flex-shrink-0"></i>
        <div class="flex-grow">
            <h5 class="font-bold text-sm">${title}</h5>
            <p class="text-xs opacity-90">${message}</p>
        </div>
    `;

    // 1. Append to container
    container.appendChild(toast);

    // 2. Force reflow and then animate in
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            toast.classList.remove('opacity-0', '-translate-y-full');
            toast.classList.add('opacity-100', 'translate-y-0');
        });
    });

    // 3. Auto-hide after duration
    setTimeout(() => {
        // Animate out (Slide UP)
        toast.classList.remove('opacity-100', 'translate-y-0');
        toast.classList.add('opacity-0', '-translate-y-full');

        // Remove from DOM after animation completes (300ms)
        setTimeout(() => {
            if (container.contains(toast)) {
                container.removeChild(toast);
            }
        }, 300);
    }, duration);
}


// =====================================================================
// --- THEME LOGIC ---
// =====================================================================
// Backup
// function toggleTheme(event) {
//     const isDark = event.target.checked;

//     // 1. Set the class on the html element
//     document.documentElement.classList.toggle('dark', isDark);

//     // 2. Save the user's explicit choice
//     localStorage.setItem('theme', isDark ? 'dark' : 'light');
// }

function toggleTheme(e) {
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

function initializeTheme() {
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
// --- PRO PLAN MODAL PURCHASE ---
// =====================================================================

/**
 * Opens the Pro Plan upgrade modal
 */
function openProPlanModal() {
    const modal = document.getElementById('pro-plan-modal');
    if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('flex');

        // Add entrance animation
        setTimeout(() => {
            modal.style.opacity = '1';
        }, 10);
    }
}

/**
 * Closes the Pro Plan upgrade modal
 */
function closeProPlanModal() {
    const modal = document.getElementById('pro-plan-modal');
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }, 300);
    }
}

/**
 * Handles the Pro Plan purchase process
 */
function purchaseProPlan() {
    const button = document.querySelector('#pro-plan-modal button[onclick="purchaseProPlan()"]');
    const originalText = button.innerHTML;

    // Show loading state
    button.innerHTML = '<i class="bi bi-arrow-clockwise animate-spin mr-2"></i> Processing...';
    button.disabled = true;

    // Simulate purchase process
    setTimeout(() => {
        // Update user plan to Pro
        userPlan = 'pro';

        // Update ALL UI elements
        updateProUI();

        // Show success state
        button.innerHTML = '<i class="bi bi-check-lg mr-2"></i> Purchase Successful!';
        button.classList.remove('from-brand-600', 'to-purple-600');
        button.classList.add('bg-green-500', 'text-white');

        // Close modal after success
        setTimeout(() => {
            closeProPlanModal();
            showSystemNotification('success', 'Welcome to Pro!', 'Your Pro Plan features are now active.');
        }, 1500);
    }, 2000);
}

/**
 * Updates the UI to reflect Pro Plan status
 */
function updateUserToPro() {
    // Update the user profile section
    // const userPlanElement = document.querySelector('.text-brand-600.dark\\:text-brand-400');
    // if (userPlanElement) {
    //     userPlanElement.innerHTML = '<i class="bi bi-star-fill text-yellow-400"></i> Pro Plan';
    // }

    // Update any other UI elements that should change for Pro users
    const proElements = document.querySelectorAll('.pro-feature-locked');
    proElements.forEach(el => {
        el.classList.remove('pro-feature-locked');
        el.classList.add('pro-feature-unlocked');
    });
}

/**
 * Example function to show Pro features that are locked
 */
function showProFeatureLocked(featureName) {
    showSystemNotification('info', 'Pro Feature', `${featureName} is available in the Pro Plan.`);
    openProPlanModal();
}

// =====================================================================
// --- DASHBOARD STATUS UPDATES ---
// =====================================================================

/**
 * Updates the dashboard status card based on user plan
 */
function updateDashboardStatus() {
    // Elements may not exist in current HTML structure, so check before updating
    const statusBadge = document.getElementById('user-plan-badge');
    const protectionStatus = document.getElementById('protection-status');

    // If these elements don't exist, function cannot proceed
    if (!statusBadge || !protectionStatus) {
        // Silently return - these elements may not be in the HTML
        return;
    }

    if (userPlan === 'pro') {
        // Pro user styling
        statusBadge.textContent = 'Pro';
        statusBadge.className = 'text-xl font-mono font-bold text-purple-200';
        protectionStatus.textContent = 'Advanced protection with unlimited version history & cloud sync.';
        protectionStatus.className = 'text-purple-100 text-sm mt-1';

    } else {
        // Basic user styling
        statusBadge.textContent = 'Basic';
        statusBadge.className = 'text-xl font-mono font-bold text-green-200';
        protectionStatus.textContent = 'Real-time monitoring is active across 4 watched folders.';
        protectionStatus.className = 'text-green-100 text-sm mt-1';
    }
}


// =============================================
// DOM ELEMENTS
// =============================================
class Elements {
    constructor() {
        this.backupLocation = document.getElementById('backupLocation');
        // this.sourceLocation = document.getElementById('sourceLocation');

        // this.backupProgress = document.getElementById('backupProgress');
        this.backupUsage = document.getElementById('backup-usage');
        this.backupUsagePercent = document.getElementById('backup-usage-percent');
        this.backupLocationPath = document.getElementById('backup-location-path');

        // this.homeUsage = document.getElementById('homeUsage');

        // this.deviceUsed = document.getElementById('deviceUsed');
        // this.deviceFree = document.getElementById('deviceFree');
        // this.deviceTotal = document.getElementById('deviceTotal');

        this.devicesContainer = document.getElementById('device-list-container');
        // this.selectedDevicePath = document.getElementById('selectedDevicePath');
        // this.selectedDeviceStats = document.getElementById('selectedDeviceStats');
        // this.selectedDeviceInfo = document.getElementById('selectedDeviceInfo');
        // this.confirmSelectionBtn = document.getElementById('confirmSelectionBtn');

        // this.devicesName = document.getElementById('devicesName');
        // this.deviceMountPoint = document.getElementById('deviceMountPoint');
        // this.devicesFilesystem = document.getElementById('devicesFilesystem');
        // this.devicesModel = document.getElementById('devicesModel');
        // this.devicesUsageBar = document.getElementById('devicesUsageBar');

        this.filesImagesCount = document.getElementById('files-images-count');
        this.filesVideosCount = document.getElementById('files-videos-count');
        this.filesDocumentsCount = document.getElementById('files-documents-count');
        this.filesOtherCount = document.getElementById('files-others-count');

        this.filesImagesSize = document.getElementById('files-images-size');
        this.filesVideosSize = document.getElementById('files-videos-size');
        this.filesDocumentsSize = document.getElementById('files-documents-size');
        this.filesOtherSize = document.getElementById('files-others-size');

        // this.logContainer = document.getElementById('logContainer');
        // this.leftSidebar = document.getElementById('leftSidebar');
        // this.mainTitle = document.getElementById('mainTitle');

        this.fileSearchInput = document.getElementById('file-search-input');
        // this.deviceInfoSection = document.getElementById('deviceInfoSection');
        // this.rightSidebar = document.getElementById('rightSidebar');

    }
}

const elements = new Elements();


// =============================================
// APPLICATION STATE
// =============================================
class AppState {
    constructor() {
        this.backup = {
            running: true,
        };
        this.intervals = {
            backup: null,
            device: null,
            storage: null
        };
        this.selectedDevice = null;
    }
}

const appState = new AppState();


// =============================================
// UTILITY FUNCTIONS
// =============================================
class Utils {
    static formatBytes(bytes, decimals = 2) {
            // FIX: Safely convert input to a number and check for invalid/non-positive values.
            const safeBytes = Number(bytes);

            if (isNaN(safeBytes) || safeBytes <= 0) return '0 Bytes';

            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

            // Use safeBytes for calculation
            const i = Math.floor(Math.log(safeBytes) / Math.log(k));
            const effectiveIndex = Math.min(i, sizes.length - 1);

            return parseFloat((safeBytes / Math.pow(k, effectiveIndex)).toFixed(decimals)) + ' ' + sizes[effectiveIndex];
        };

    static getDeviceIcon(device) {
        if (!device) return 'bi-usb-c';
        return getFileIconDetails(device.filesystem).iconClass;  // Return correct icon class
    };

    static getDeviceIconClass(device) {
        if (!device || !device.total || device.total === 0) return 'bg-gray-100 text-gray-600';
        const freePercent = (device.total - device.used) / device.total;
        if (freePercent < 0.2) return 'bg-red-100 text-red-600';
        if (freePercent < 0.5) return 'bg-yellow-100 text-yellow-600';
        return 'bg-green-100 text-green-600';
    };

    static getUsageColorClass(percent) {
        if (percent > 90) return 'bg-red-500';
        if (percent > 70) return 'bg-yellow-500';
        return 'bg-green-500';
    }

    static handleResponse(response) {
        if (response.status === 204) {  // Handle no-content responses
            return null;
        }

        // First parse the JSON
        return response.json().then(data => {
            // Then check for success flag if the endpoint uses it
            if (data.hasOwnProperty('success') && !data.success) {
                const errorMsg = data.error || 'Request failed';
                console.error('API error:', errorMsg); // Log the error for debugging
                throw new Error(errorMsg);
            }
            return data;
        }).catch(error => {
            console.error('Response parsing error:', error);
            throw error;
        });
    }

    static getFileThumbnail(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const thumbnails = {
            pdf: { bg: 'bg-red-50', icon: 'fa-file-pdf', color: 'text-red-600' },
            doc: { bg: 'bg-blue-50', icon: 'fa-file-word', color: 'text-blue-600' },
            docx: { bg: 'bg-blue-50', icon: 'fa-file-word', color: 'text-blue-600' },
            xls: { bg: 'bg-green-50', icon: 'fa-file-excel', color: 'text-green-600' },
            xlsx: { bg: 'bg-green-50', icon: 'fa-file-excel', color: 'text-green-600' },
            jpg: { bg: 'bg-purple-50', icon: 'fa-file-image', color: 'text-purple-600' },
            jpeg: { bg: 'bg-purple-50', icon: 'fa-file-image', color: 'text-purple-600' },
            gif: { bg: 'bg-purple-50', icon: 'fa-file-image', color: 'text-purple-600' },
            png: { bg: 'bg-purple-50', icon: 'fa-file-image', color: 'text-purple-600' },
            png: { bg: 'bg-purple-50', icon: 'fa-file-image', color: 'text-purple-600' },
            default: { bg: 'bg-gray-50', icon: 'fa-file', color: 'text-gray-600' }
        };

        return thumbnails[ext] || thumbnails.default;
    }
};


// =============================================
// EXTENSION MANAGER
// ============================================
/**
 * Determines the icon and color class based on the file extension.
 * @param {string} filename The name of the file.
 * @returns {object} An object containing the iconClass and iconColor.
 */
function getFileIconDetails(filename) {
    if (typeof filename !== 'string' || !filename) {
        return { iconClass: 'bi bi-file-earmark-text-fill', iconColor: 'text-gray-500', thumbnail: null };
    }
    const ext = filename.split('.').pop().toLowerCase();
    let iconClass = 'bi bi-file-earmark-text-fill';
    let iconColor = 'text-gray-500'; // Default grey color
    let thumbnail = null;

    if (ext === 'txt') {
        iconClass = 'bi bi-file-earmark-text-fill';
        iconColor = 'text-green-500';
    } else if (ext === 'blend') {
        iconClass = 'bi bi-box-fill-fill';
        iconColor = 'text-orange-500';
    }
    else if (['md', 'txt', 'log', 'ini', 'config', 'cfg', 'conf', 'sh', 'py', 'js', 'html', 'css'].includes(ext)) {
        iconClass = 'bi bi-file-code-fill';
        iconColor = 'text-indigo-500';
    } else if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp'].includes(ext)) {

        iconClass = 'bi bi-file-earmark-image-fill';
        iconColor = 'text-purple-500';
        thumbnail = `/static/data/images/${ext}.png`; // Example thumbnail path
    } else if (['zip', 'rar', '7z', 'tar', 'gz'].includes(ext)) {
        iconClass = 'bi bi-file-earmark-zip-fill';
        iconColor = 'text-blue-500';
    } else if (['mp4', 'avi', 'mov', 'mkv'].includes(ext)) {
        iconClass = 'bi bi-file-earmark-play-fill';
        iconColor = 'text-red-500';
    }  else if (['mp3', 'wav', 'flac', 'aac'].includes(ext)) {
        iconClass = 'bi bi-file-earmark-music-fill';
        iconColor = 'text-blue-500';
    }
    else if (['usb', 'vnmw', 'sd', 'mmc', 'sd-card', 'hd', 'memory', 'ext4'].includes(ext)) {
        iconClass = 'bi bi-device-hdd-fill';
        iconColor = 'text-green-500';
    }
    return { iconClass, iconColor, thumbnail };
}


// =============================================
// TIME FORMATTING UTILITY
// =============================================
/**
 * Converts a Unix timestamp to a human-readable relative time string.
 * Examples: "just now", "2 minutes ago", "1 hour ago", "3 days ago"
 * @param {number} timestamp - Unix timestamp in seconds
 * @returns {string} Human-readable relative time
 */
function timeSince(timestamp) {
    // Handle both seconds and milliseconds
    const ts = typeof timestamp === 'number' ? timestamp : parseInt(timestamp);
    const timestampMs = ts < 10000000000 ? ts * 1000 : ts; // Convert to ms if needed
    const now = Date.now();
    const secondsAgo = Math.floor((now - timestampMs) / 1000);

    if (secondsAgo < 0) return 'just now';
    if (secondsAgo === 0) return 'just now';
    if (secondsAgo < 60) return `${secondsAgo} second${secondsAgo !== 1 ? 's' : ''} ago`;

    const minutesAgo = Math.floor(secondsAgo / 60);
    if (minutesAgo < 60) return `${minutesAgo} minute${minutesAgo !== 1 ? 's' : ''} ago`;

    const hoursAgo = Math.floor(minutesAgo / 60);
    if (hoursAgo < 24) return `${hoursAgo} hour${hoursAgo !== 1 ? 's' : ''} ago`;

    const daysAgo = Math.floor(hoursAgo / 24);
    if (daysAgo < 7) return `${daysAgo} day${daysAgo !== 1 ? 's' : ''} ago`;

    const weeksAgo = Math.floor(daysAgo / 7);
    if (weeksAgo < 4) return `${weeksAgo} week${weeksAgo !== 1 ? 's' : ''} ago`;

    const monthsAgo = Math.floor(daysAgo / 30);
    return `${monthsAgo} month${monthsAgo !== 1 ? 's' : ''} ago`;
}


// =============================================
// BACKUP FUNCTIONS
// =============================================
const BackupManager = {
    updateUsage: () => {
        fetch('/api/backup/usage')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    BackupManager.updateUI(data);
                }
            })
            .catch(error => {
                console.error('Backup usage check failed:', error);
            });
    },

    updateUI: (data) => {
        if (data.success) {
            // Storate (Dashboard)
            elements.backupUsage.textContent =
                `${data.human_used} Used / ${data.human_total} (${data.percent_used}% used)`;
            elements.backupUsagePercent.textContent = `${data.percent_used}%`;
            elements.backupLocationPath.textContent = `${data.location}`;
            
            const usageCircle = document.querySelector('svg .text-blue-500'); 
            const percent = data.percent_used;
            const CIRCUMFERENCE = 251.2;
            const offset = CIRCUMFERENCE - (percent / 100) * CIRCUMFERENCE;
            usageCircle.style.strokeDashoffset = offset;
            
            // 1.2 TB Used / 800 GB Free
            // 32.1 GB used of 72.8 GB (44.1% used)

            // Source device info "Left Side" HOME
            // elements.deviceUsed.textContent = `${data.human_used} `;
            // elements.deviceFree.textContent = `${data.human_free}`;
            // elements.deviceTotal.textContent = `${data.human_total}`;

            // elements.backupProgress.className = 'h-2 rounded-full';
            // elements.backupProgress.classList.add(Utils.getUsageColorClass(data.percent_used));

            // Update the UI with the devices used space
            // elements.devicesUsageBar.style.width = `${data.percent_used}%`;
            // elements.devicesUsageBar.className = 'h-2 rounded-full';
            // elements.devicesUsageBar.classList.add(Utils.getUsageColorClass(data.percent_used));

            // Update device details in the UI
            // if (data.filesystem) {
            //     elements.devicesFilesystem.textContent = data.filesystem;
            // }
            // if (data.model) {
            //     elements.devicesModel.textContent = data.model;
            // }

            // Update image count from summary if available
            if (data.summary && data.summary.categories) {
                const imagesCategory = data.summary.categories.find(cat => cat.name === "Image");
                const documentsCategory = data.summary.categories.find(cat => cat.name === "Document");
                const videosCategory = data.summary.categories.find(cat => cat.name === "Video");
                const otherCategory = data.summary.categories.find(cat => cat.name === "Others");

                // Images
                if (imagesCategory) {
                    elements.filesImagesCount.textContent = `${imagesCategory.count.toLocaleString()} files`;
                    elements.filesImagesSize.textContent = `${imagesCategory.size_str}`;
                }
                // Videos
                if (videosCategory) {
                    elements.filesVideosCount.textContent = `${videosCategory.count.toLocaleString()} files`;
                    elements.filesVideosSize.textContent = `${videosCategory.size_str}`;
                }
                // Documents
                if (documentsCategory) {
                    elements.filesDocumentsCount.textContent = `${documentsCategory.count.toLocaleString()} files`;
                    elements.filesDocumentsSize.textContent = `${documentsCategory.size_str}`;
                }
                // Other files
                if (otherCategory) {
                    elements.filesOtherCount.textContent = `${otherCategory.count.toLocaleString()} files`;
                    elements.filesOtherSize.textContent = `${otherCategory.size_str}`;
                }
            }
        }
    },

    checkDaemonStatus: () => {
        // Check if daemon is running via WebSocket connection status
        if (window.backupStatusClient && window.backupStatusClient.ws) {
            const isConnected = window.backupStatusClient.ws.readyState === WebSocket.OPEN;
            const realTimeStatusLabel = document.getElementById('realTimeStatusLabel');

            if (realTimeStatusLabel) {
                if (isConnected) {
                    realTimeStatusLabel.className = 'bi bi-circle-fill text-green-500 mr-1 text-xs';
                    realTimeStatusLabel.title = 'Real-time backup active';
                } else {
                    realTimeStatusLabel.className = 'bi bi-circle-fill text-red-500 mr-1 text-xs';
                    realTimeStatusLabel.title = 'Real-time backup inactive';
                }
            }
        } else {
            // No WebSocket connection - daemon not running
            const realTimeStatusLabel = document.getElementById('realTimeStatusLabel');
            if (realTimeStatusLabel) {
                realTimeStatusLabel.className = 'bi bi-circle-fill text-red-500 mr-1 text-xs';
                realTimeStatusLabel.title = 'Real-time backup not running';
            }
        }
    },


    //////////////////////////////////////////////////////////////////////////
    // AUTOMATICALLY REALTIME CHECKBOX
    //////////////////////////////////////////////////////////////////////////
    toggle: () => {
        const realTimeCheckbox = document.getElementById('realTimeCheckbox');

        // 1. DISABLE INPUT immediately to prevent multiple clicks
        realTimeCheckbox.disabled = true;

        // Determine intended state based on current click
        const isChecked = realTimeCheckbox.checked;

        // Optimistic UI Update (Update visuals immediately)
        BackupManager.updateVisualStatus(isChecked);

        // 2. Send Request
        BackupManager.updateRealTimeBackupState(isChecked)
            .finally(() => {
                // 3. RE-ENABLE INPUT when request finishes
                realTimeCheckbox.disabled = false;
            });
    },

    updateVisualStatus: (isActive) => {
        appState.backup.running = isActive;
        const statusLabel = document.getElementById('realTimeStatusLabel');

        if (statusLabel) {
            if (isActive) {
                statusLabel.classList.replace('text-red-500', 'text-green-500');
                statusLabel.classList.replace('far', 'fas');
                statusLabel.title = "Real-time backup active";
            } else {
                statusLabel.classList.replace('text-green-500', 'text-red-500');
                statusLabel.classList.replace('fas', 'far');
                statusLabel.title = "Real-time backup inactive";
            }
        }
    },

    updateRealTimeBackupState: (isChecked) => {
        return fetch('/api/realtime-backup/daemon', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ is_active: isChecked }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error("Error toggling daemon:", data.error);
                alert("Failed to toggle backup: " + data.error);

                // Revert UI on error
                document.getElementById('realTimeCheckbox').checked = !isChecked;
                BackupManager.updateVisualStatus(!isChecked);
            } else {
                console.log("Daemon status updated:", data.status);
            }
        })
        .catch(err => {
            console.error("Network error:", err);
            // Revert UI on error
            document.getElementById('realTimeCheckbox').checked = !isChecked;
            BackupManager.updateVisualStatus(!isChecked);
        });
    },
};


// =====================================================================
// --- DEVICE MANAGEMENT ---
// =====================================================================
const DeviceManager = {
    load: () => {
        const container = document.getElementById('device-list-container');
        if (!container) return;

        container.innerHTML = `
            <div class="col-span-full flex flex-col items-center justify-center py-12 text-muted">
                <i class="bi bi-arrow-clockwise animate-spin text-2xl mb-2"></i>
                <p>Scanning sources...</p>
            </div>`;

        // Fetch both devices and config concurrently
        Promise.all([
            fetch('/api/storage/devices').then(res => res.json()),
            fetch('/api/config').then(res => res.json())
        ])
        .then(([devicesData, configData]) => {
            if (!devicesData.success || !devicesData.devices || devicesData.devices.length === 0) {
                DeviceManager.render([]); // Render empty state
                return;
            }

            const activePath = configData?.DEVICE_INFO?.path;

            // Add an 'isActive' property to each device
            const updatedDevices = devicesData.devices.map(device => {
                return {
                    ...device,
                    isActive: device.mount_point === activePath
                }
            });

            DeviceManager.render(updatedDevices);
        })
        .catch(error => {
            console.error("Failed to load devices or config:", error);
            DeviceManager.render([]); // Render empty state on error
        });
    },

    normalize: (device) => {
        // Safely handle numeric conversion
        const total = Number(device.total) || 0;
        const used = Number(device.used) || 0;
        const free = Number(device.free) || 0;

        // Calculate GB for display if the backend doesn't provide it formatted
        const totalGB = Math.round(total / (1024**3));
        const usedGB = Math.round(used / (1024**3));

        // Determine status based on mount point or other flags from backend
        // Adjust this logic based on how your backend identifies the active backup drive
        let status = 'Inactive';
        let color = 'text-slate-400';

        if (device.mount_point === '/' || device.mount_point === 'C:\\') {
            status = 'System';
            color = 'text-blue-300';
        }

        return {
            id: device.id || Math.random().toString(36).substr(2, 9),
            name: device.label || device.name || device.device || 'Unknown Device',
            mount_point: device.mount_point || '',
            filesystem: device.filesystem || 'Unknown',
            total: total,
            used: used,
            free: free,
            totalGB: totalGB,
            usedGB: usedGB,
            status: status,
            icon: (device.mount_point === '/' || device.mount_point === 'C:\\') ? 'bi-pc-display' : 'bi-usb-drive-fill',
            color: color,
            isActive: false // Will be set later based on config
        };
    },

    render: (devices) => {
        const container = document.getElementById('device-list-container');
        if (!container) return;
        container.innerHTML = '';

        if (devices.length === 0) {
            container.innerHTML = `
                <div class="col-span-full border-2 border-dashed border-main rounded-2xl p-10 text-center">
                    <i class="bi bi-hdd text-4xl text-muted mb-3 block"></i>
                    <h4 class="font-bold text-main">No Devices Found</h4>
                    <p class="text-sm text-muted">Connect a USB drive to get started.</p>
                </div>`;
            return;
        }

        // console.log("Rendering devices:", devices);

        devices.forEach(device => {
            const usedGB = Math.round((device.used || 0) / (1024**3));
            const totalGB = Math.round((device.total || 0) / (1024**3));
            const percent = totalGB > 0 ? Math.round((usedGB / totalGB) * 100) : 0;
            const isSSD = device.is_ssd;  // Check if the device is SSD

            // Logic for active device
            const isActive = device.isActive;
            const statusColor = isActive ? 'text-emerald-500' : 'text-muted';
            const statusText = isActive ? 'Active' : 'Ready';
            const borderClass = isActive ? 'border-emerald-500 ring-1 ring-emerald-500' : 'border-main hover:border-brand-300';

            // Create a safe string for the onclick handler
            const deviceId = device.id || Math.random().toString(36).substr(2, 9);

            const card = `
            <div class="bg-card p-6 rounded-2xl border ${borderClass} group cursor-pointer transition-all duration-200" data-device-id="${deviceId}">
                <div class="flex items-start justify-between mb-4">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 rounded-xl bg-gray-50 dark:bg-white/5 flex items-center justify-center text-xl text-main">
                            ${isSSD
                                ? '<i class="bi bi-device-ssd-fill"></i>'
                                : '<i class="bi bi-hdd-fill"></i>'
                            }
                        </div>
                        <div>
                            <h4 class="font-bold text-main text-base">${device.label || device.name || 'Unnamed Drive'}</h4>
                            <div class="flex items-center gap-1.5 mt-0.5">
                                <span class="w-1.5 h-1.5 rounded-full ${isActive ? 'bg-emerald-500' : 'bg-gray-400'}"></span>
                                <span class="text-xs font-medium ${statusColor}">${statusText}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mb-4">
                    <div class="flex justify-between text-xs font-medium text-secondary mb-2">
                        <span>${usedGB} GB Used</span>
                        <span>${totalGB} GB Total</span>
                    </div>
                    <div class="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-2 overflow-hidden">
                        <div class="h-full bg-brand-500 rounded-full" style="width: ${percent}%"></div>
                    </div>
                </div>

                ${isActive
                    ? `<button disabled class="w-full py-2 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center justify-center gap-2"><i class="bi bi-check-circle-fill"></i> Backup Location</button>`
                    : `<button onclick="handleDeviceSelection('${deviceId}')" class="w-full py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main text-xs font-bold transition cursor-pointer">Set as Backup</button>`
                }
            </div>`;
            container.innerHTML += card;

            // Store device data in a global map for lookup
            if (!window.deviceMap) window.deviceMap = {};
            window.deviceMap[deviceId] = device;
        });
    },

    createCard: (device) => {
        const card = document.createElement('div');

        // 1. Calculate Usage Percentage
        let percentUsed = 0;
        if (device.total > 0) {
            percentUsed = Math.round((device.used / device.total) * 100);
        } else if (device.totalGB > 0) {
            percentUsed = Math.round((device.usedGB / device.totalGB) * 100);
        }

        // Formatted strings
        const usedStr = Utils.formatBytes(device.used);
        const totalStr = Utils.formatBytes(device.total);

        // 2. Determine Visuals
        const progressColor = percentUsed > 90 ? 'bg-red-500' : 'bg-brand-600';
        const iconName = device.icon.replace('bi ', ''); // Clean icon class

        // 3. Check if device is active (use the isActive property we set)
        const isActive = device.isActive || device.status === 'Active';

        // 4. Setup Container Classes - Green border for active devices
        card.className = `device-card bg-white dark:bg-slate-800 p-6 rounded-xl border ${isActive ? 'border-green-500 ring-1 ring-green-500' : 'border-slate-200 dark:border-slate-700'} shadow-md hover:shadow-xl transition-all duration-200 flex flex-col h-full cursor-pointer group`;

        // 5. Set Data Attributes
        const devicesId = device.id;
        const devicesPath = device.mount_point;

        card.setAttribute('data-device-id', devicesId);
        card.setAttribute('data-device-path', devicesPath);

        // 6. Button Logic - Updated with checkmark icon and green styling
        let buttonHtml = '';
        if (isActive) {
            buttonHtml = `
                <button disabled class="w-full py-2.5 rounded-lg text-xs font-bold bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800 cursor-default flex items-center justify-center gap-2">
                    <i class="bi bi-check-circle-fill"></i> Currently Active
                </button>`;
        } else {
            buttonHtml = `
                <button onclick="DeviceManager.selectDevice(${JSON.stringify(device).replace(/"/g, '&quot;')})" class="w-full py-2.5 rounded-lg text-xs font-bold bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 text-brand-700 dark:text-slate-200 hover:bg-brand-50 dark:hover:bg-blue-300 hover:border-brand-200 transition shadow-sm flex items-center justify-center gap-2">
                    Use as Backup Device
                </button>`;
        }

        // 7. Render HTML
        card.innerHTML = `
            <div class="flex items-start justify-between mb-6">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-xl bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-xl text-muted group-hover:text-brand-600 transition-colors">
                        <i class="bi ${iconName}"></i>
                    </div>
                    <div>
                        <h4 class="font-bold text-main text-lg truncate max-w-[180px]" title="${device.name}">
                            ${device.name}
                        </h4>
                        <span class="text-xs font-medium ${isActive ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' : 'bg-slate-100 dark:bg-slate-700 text-secondary dark:text-slate-300'} px-2 py-0.5 rounded-full inline-flex items-center gap-1 mt-1">
                            <i class="bi ${isActive ? 'bi-check-circle-fill' : 'bi-hdd-network'} text-[10px]"></i> ${isActive ? 'Active' : (device.filesystem || 'Drive')}
                        </span>
                    </div>
                </div>
            </div>

            <div class="mb-6 flex-1">
                <div class="flex justify-between text-xs text-muted mb-2 font-medium">
                    <span>Used: ${usedStr}</span>
                    <span>Total: ${totalStr}</span>
                </div>
                <div class="progress-bar-container h-2 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
                    <div class="progress-bar-fill ${progressColor} h-full rounded-full transition-all duration-500" style="width: ${percentUsed}%"></div>
                </div>
            </div>

            <div class="pt-4 border-t border-slate-100 dark:border-slate-700 mt-auto">
                ${buttonHtml}
            </div>
        `;

        return card;
    },

    showNoDevices: () => {
        const container = document.getElementById('device-list-container');
        if (container) {
            container.innerHTML = `
                <div class="col-span-3 text-center py-10 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl">
                    <i class="bi bi-hdd-fill text-slate-300 dark:text-secondary text-4xl mb-2 block"></i>
                    <div class="text-muted font-medium">No storage devices found</div>
                    <div class="text-sm text-slate-400 dark:text-slate-500 mt-1">Connect a USB drive and click Refresh</div>
                </div>
            `;
        }
    },

    showError: (error) => {
        const container = document.getElementById('device-list-container');
        if (container) {
            container.innerHTML = `
                <div class="col-span-3 text-center py-10 border-2 border-red-100 dark:border-red-900/30 bg-red-50 dark:bg-red-900/10 rounded-xl">
                    <i class="bi bi-exclamation-triangle text-red-400 text-3xl mb-2 block"></i>
                    <div class="text-red-600 dark:text-red-400 font-bold">Error loading devices</div>
                    <div class="text-sm text-red-500 dark:text-red-300 mt-1">${error.message || 'Connection failed'}</div>
                </div>
            `;
        }
    },

    selectDevice: async (device) => {
        console.log("Selecting device:", device);

        try {
            const response = await fetch('/api/backup/select-device', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    device_info: device
                })
            });

            const result = await response.json();

            if (result.success) {
                console.log('Device configured successfully:', result.path);
                showSystemNotification('success', 'Device Configured', `${device.name} is now your backup device.`);

                // Refresh the devices list to show the new active device
                DeviceManager.load();

                // Refresh usage stats
                if (typeof BackupManager !== 'NaN') {
                    BackupManager.updateUsage();
                }
            } else {
                throw new Error(result.error || 'Server rejected the selection.');
            }

        } catch (error) {
            console.error('Network error during device selection:', error);
            showSystemNotification('error', 'Configuration Failed', error.message || 'Could not connect to server.');
        }
    },

    setupSelection: () => {
        document.querySelectorAll('.device-card').forEach(card => {
            card.addEventListener('click', function() {
                console.log('Device clicked:', this.getAttribute('data-device-path'));
                console.log('Device info:', this.getAttribute('data-device-info'));

                document.querySelectorAll('.device-card').forEach(c => {
                    c.classList.remove('selected');
                });

                this.classList.add('selected');
                appState.selectedDevice = {
                    path: this.getAttribute('data-device-path'),
                    info: JSON.parse(this.getAttribute('data-device-info'))
                };

                console.log('Selected device state:', appState.selectedDevice);
                DeviceManager.updateSelectionUI();
            });
        });
    },
};

/**
 * Helper function to handle device selection safely
 */
function handleDeviceSelection(deviceId) {
    if (!window.deviceMap || !window.deviceMap[deviceId]) {
        console.error('Device not found:', deviceId);
        showSystemNotification('error', 'Device Error', 'Could not find device information.');
        return;
    }

    const device = window.deviceMap[deviceId];
    useThisBackupDevice(device);
}


// =============================================
// DEVICE SELECTION HANDLER
// =============================================
function useThisBackupDevice(device) {
    console.log("Device object for selection:", device);

    if (!device || !device.mount_point) {
        showSystemNotification('error', 'Invalid Device', 'Device information is incomplete.');
        return;
    }

    // Ensure all numeric values are properly formatted
    const deviceInfo = {
        ...device,
        total: parseInt(device.total || device.total_size || 0),
        used: parseInt(device.used || 0),
        free: parseInt(device.free || 0),
        is_ssd: Boolean(device.is_ssd)
    };

    openConfirmationModal(
        "Set Backup Device?",
        `Are you sure you want to set <span class="font-bold text-main">${device.label || device.name || 'this device'}</span> as your backup destination?`,
        async () => {
            try {
                const response = await fetch('/api/backup/select-device', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        device_info: deviceInfo  // Use the processed device info
                    })
                });

                const result = await response.json();

                if (result.success) {
                    console.log('Device configured successfully:', result.path);

                    // Refresh the devices list
                    DeviceManager.load();

                    // Refresh usage stats
                    BackupManager.updateUsage();

                    showSystemNotification('success', 'Device Configured',
                        `${device.label || device.name} is now your backup device.`);

                    // Create necessary folders inside the choose backup device
                    try {
                        const creationResponse = await fetch('/api/base-folders-creation', {
                            method: 'GET'
                        });

                        const creation = await creationResponse.json();
                        console.log(creation);
                        if (creation.success) {
                            return;
                            // showSystemNotification('info', 'Time Machine', `Time Machine base folders created successfully!`);
                        } else {
                            showSystemNotification('error', 'Error', `Failed to create base folders: ${creation.error || 'Unknown error'}`);
                        }
                    } catch (error) {
                        console.error('Error during folder creation fetch:', error);
                    }

                } else {
                    throw new Error(result.error || 'Server rejected the selection.');
                }

            } catch (error) {
                console.error('Network error during device selection:', error);
                showSystemNotification('error', 'Configuration Failed',
                    error.message || 'Could not connect to server.');
            }
        }
    );
}


// =====================================================================
// --- CONFIG CHECK FOR ACTIVE DEVICE ---
// =====================================================================

/**
 * Checks if a device is the currently active backup device by comparing with config
 */
async function isDeviceActive(device) {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();

        // Check if DEVICE_INFO section exists and path matches
        if (config.DEVICE_INFO && config.DEVICE_INFO.path) {
            const activePath = config.DEVICE_INFO.path;
            return activePath === device.mount_point;
        }
        return false;
    } catch (error) {
        console.error('Error checking device status:', error);
        return false;
    }
}

/**
 * Updates device status based on config and re-renders devices
 */
async function updateDeviceStatuses() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        const activePath = config.DEVICE_INFO?.path;

        // Update deviceData with active status
        deviceData.forEach(device => {
            device.isActive = device.mount_point === activePath;
        });

        // Re-render devices with updated status
        DeviceManager.render(deviceData);
    } catch (error) {
        console.error('Error updating device statuses:', error);
    }
}


// =============================================
// SIZE FORMATTER UTILITY
// =============================================
function humanFileSize(size) {
  const i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
  return (
    +(size / Math.pow(1024, i)).toFixed(2) * 1 +
    " " +
    ["B", "kB", "MB", "GB", "TB"][i]
  );
}

// =============================================
// ACTIVITY FEED MANAGER
// =============================================
const ActivityFeedManager = {
    feedContainer: null,
    storageKey: 'timemachine_activity_feed',
    maxStoredItems: 50,
    activeRows: new Map(),

    init() {
        this.feedContainer = document.querySelector('#live-activities-feed');
        if (!this.feedContainer) {
            console.error("Activity feed container not found (#live-activities-feed).");
            return;
        }
        this.loadFromStorage();
        this._sortRowsByTimestamp();
    },

    saveToStorage(activities) {
        try {
            localStorage.setItem(this.storageKey, JSON.stringify(activities));
        } catch (e) {
            console.warn('[ActivityFeed] Could not save to localStorage:', e);
        }
    },

    loadFromStorage() {
        try {
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                const activities = JSON.parse(stored);
                activities.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
                
                this.feedContainer.innerHTML = '';
                this.activeRows.clear();
                
                const latestActivities = {};
                activities.forEach(activity => {
                    const fileName = (activity.description || "").split('/').pop();
                    if (!latestActivities[fileName] || 
                        (activity.timestamp || 0) > (latestActivities[fileName].timestamp || 0)) {
                        latestActivities[fileName] = activity;
                    }
                });
                
                const uniqueActivities = Object.values(latestActivities);
                uniqueActivities.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
                
                const activitiesToShow = Math.min(uniqueActivities.length, MAX_TRANSFER_ITEMS);
                
                for (let i = 0; i < activitiesToShow; i++) {
                    this._addRowToFeed(uniqueActivities[i]);
                }
            }
        } catch (e) {
            console.warn('[ActivityFeed] Could not load from localStorage:', e);
        }
    },

    // FIXED: Create row with proper data-timestamp attribute and cell classes
    _createRowHtml(activity, rowId) {
        if (!activity) return '';

        const { title, description, size, timestamp } = activity;
        const safeDescription = description || "";
        const safeTitle = title || "";
        const fileName = safeDescription.split('/').pop();
        const fileData = getFileIconDetails(fileName);

        let actionLabel = "Processing";
        let actionColorClass = "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400";

        if (safeTitle.includes('Backed Up') || safeTitle.includes('Hardlinked')) {
            actionLabel = 'Backed Up';
            actionColorClass = "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400";
        } else if (safeTitle.includes('Modified')) {
            actionLabel = 'Modified';
            actionColorClass = "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400";
        }

        const formattedTime = timeSince(timestamp);
        const finalRowId = rowId || `activity-${btoa(fileName).slice(0, 10)}`;

        // FIX: Add data-timestamp to <tr> and add proper classes to cells
        return `
        <tr id="${finalRowId}" 
            class="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition activity-row" 
            data-timestamp="${timestamp}">
            <td class="px-6 py-3 flex items-center gap-3 file-name-cell">
                <i class="bi ${fileData.iconClass} ${fileData.iconColor} text-main"></i>
                ${fileName}
                ${safeTitle === 'Processing' ? '<i class="bi bi-arrow-clockwise animate-spin text-blue-500 text-xs ml-2"></i>' : ''}
            </td>
            <td class="px-6 py-3 status-cell">
                <span class="px-2 py-0.5 ${actionColorClass} rounded text-xs font-bold">${actionLabel}</span>
            </td>
            <td class="px-6 py-3 text-muted size-cell">${humanFileSize(size)}</td>
            <td class="px-6 py-3 action-cell">
                <button class="text-hyperlink hover:text-hyperlink dark:hover:text-blue-300 text-xs font-medium transition hover:underline cursor-pointer" 
                        onclick="if (window.isDeviceConnected) { ActivityFeedManager.viewSnapshots('${fileName.replace(/'/g, "\\'")}') }">
                    View Snapshots
                </button>
            </td>
            <td class="px-6 py-3 text-right text-muted font-medium text-xs time-ago-cell">${formattedTime}</td>
        </tr>
        `;
    },

    _addRowToFeed(activity) {
        if (!this.feedContainer) return;

        const { description, title, timestamp } = activity; 
        const filePath = description || "";
        const fileName = filePath.split('/').pop();
        
        let existingRowId = this.activeRows.get(fileName);
        let existingRow = existingRowId ? document.getElementById(existingRowId) : null;
        const newRowId = existingRowId || `activity-${fileName.replace(/[^a-zA-Z0-9]/g, '')}-${Date.now()}`;
        
        if (existingRow) {
            this._updateExistingRow(existingRow, activity);
        } else {
            const newRowHtml = this._createRowHtml(activity, newRowId);
            this.feedContainer.insertAdjacentHTML('afterbegin', newRowHtml);
            this.activeRows.set(fileName, newRowId);
            this._trimToMax();
        }
        
        this._sortRowsByTimestamp(); 
    },

    _trimToMax() {
        if (!this.feedContainer) return;
        
        const rows = Array.from(this.feedContainer.children);
        
        if (rows.length <= MAX_TRANSFER_ITEMS) return;
        
        while (rows.length > MAX_TRANSFER_ITEMS) {
            const row = rows.pop(); 
            
            const fileNameCell = row.querySelector('td:first-child');
            if (fileNameCell) {
                const fileName = fileNameCell.textContent.trim().split('\n')[0].trim(); 
                this.activeRows.delete(fileName);
            }
            
            row.remove();
        }
    },

    // FIXED: Update existing row with proper timestamp attribute
    _updateExistingRow(row, activity) {
        const { title, description, timestamp, progress = 0, size } = activity;
        const fileName = description.split('/').pop();
        const formattedTime = timeSince(timestamp);

        const statusCell = row.querySelector('.status-cell');
        const sizeCell = row.querySelector('.size-cell');
        const actionCell = row.querySelector('.action-cell');
        const timeCell = row.querySelector('.time-ago-cell');

        // FIX 1: Update timestamp attribute on the row
        row.setAttribute('data-timestamp', timestamp);

        // Update Status
        if (statusCell) {
            let actionLabel = "Processing";
            let actionColorClass = "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400";

            if (title.includes('Backed Up') || title.includes('Hardlinked')) {
                actionLabel = 'Backed Up';
                actionColorClass = "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400";
            }

            statusCell.innerHTML = `<span class="px-2 py-0.5 ${actionColorClass} rounded text-xs font-bold">${actionLabel}</span>`;
        }

        // Update Size/Progress
        if (sizeCell) {
            if (title === 'Backed Up' || title === 'Failed') {
                sizeCell.innerHTML = `<span class="text-sm text-muted">${humanFileSize(size)}</span>`;
            } else {
                let progressBar = sizeCell.querySelector('.progress-bar');
                if (!progressBar) {
                    sizeCell.innerHTML = `
                        <div class="w-full bg-gray-200 rounded-full dark:bg-white/10 h-1.5">
                            <div class="bg-brand-500 h-1.5 rounded-full progress-bar" style="width: ${progress}%"></div>
                        </div>`;
                    progressBar = sizeCell.querySelector('.progress-bar');
                }
                if (progressBar) {
                    progressBar.style.width = `${progress}%`;
                }
            }
        }
        
        // Update Action
        if (actionCell) {
            let actionHtml;
            if (title === 'Backed Up') {
                actionHtml = `
                    <button onclick="ActivityFeedManager.viewSnapshots('${fileName.replace(/'/g, "\\'")}', ${timestamp})" 
                            class="text-hyperlink hover:text-hyperlink dark:hover:text-blue-300 text-xs font-medium transition hover:underline cursor-pointer">
                        View Snapshots
                    </button>`;
            } else {
                actionHtml = `<span class="text-xs text-muted">...</span>`;
            }
            actionCell.innerHTML = actionHtml;
        }
        
        // FIX 2: Update Time Cell with proper content
        if (timeCell) {
            timeCell.textContent = formattedTime;
        }

        this._sortRowsByTimestamp(); 
    },

_sortRowsByTimestamp() {
        if (!this.feedContainer) return;

        const rows = Array.from(this.feedContainer.querySelectorAll('.activity-row'));

        // FIXED: Sort DESCENDING (newest first) so newest appears at top
        rows.sort((a, b) => {
            const tsA = parseInt(a.getAttribute('data-timestamp') || '0', 10);
            const tsB = parseInt(b.getAttribute('data-timestamp') || '0', 10);
            
            const timeA = isNaN(tsA) ? 0 : tsA;
            const timeB = isNaN(tsB) ? 0 : tsB;

            // Descending: B - A (newest first)
            return timeB - timeA; 
        });

        // Append in order: newest rows will be at the top
        rows.forEach(row => {
            this.feedContainer.appendChild(row);
        });
    },

    updateTimeAgo() {
        if (!this.feedContainer) return;
        
        const rows = this.feedContainer.querySelectorAll('tr[data-timestamp]');
        
        console.log(`[ActivityFeed] Updating ${rows.length} row timestamps`);
        
        rows.forEach(row => {
            const timestamp = parseInt(row.dataset.timestamp, 10);
            const timeCell = row.querySelector('.time-ago-cell');
            
            if (timeCell && !isNaN(timestamp)) {
                timeCell.textContent = timeSince(timestamp);
            }
        });
    },

    clearFeed() {
        if (!this.feedContainer) return;
        this.feedContainer.innerHTML = '';
        this.activeRows.clear();
        try { 
            localStorage.removeItem(this.storageKey); 
        } catch (e) {}
    },

    handleMessage(message) {
        if (!this.feedContainer) return;

        if (message.type === 'backup_progress') {
            this._handleBackupProgress(message);
            return;
        }

        if (!message.timestamp) {
            message.timestamp = Date.now();
        }

        if (message.requiresResponse) {
            window.backupStatusClient.send({
                type: 'response',
                data: 'response data'
            });
        }
        
        this._addRowToFeed(message);
        
        if (message.title && message.title !== 'Processing') {
            this._persistToStorage(message);
        }
        
        this._sortRowsByTimestamp();
    },

    _persistToStorage(message) {
        try {
            let allActivities = [];
            const stored = localStorage.getItem(this.storageKey);
            if (stored) {
                allActivities = JSON.parse(stored);
            }

            if (!message.timestamp) {
                message.timestamp = Date.now();
            }

            allActivities = allActivities.filter(activity => 
                activity.description !== message.description
            );

            allActivities.push(message);
            allActivities.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
            allActivities = allActivities.slice(0, 20);

            this.saveToStorage(allActivities);
        } catch (e) {
            console.warn('[ActivityFeed] Could not persist activity:', e);
        }
    },

    _handleBackupProgress(message) {
        const { progress, status, current_file, bytes_processed } = message;

        if (current_file) {
            let activityTitle = 'Processing';
            if (status === 'completed') {
                activityTitle = 'Backed Up';
            } else if (status === 'failed' || status === 'error') {
                activityTitle = 'Error';
            }

            const activity = {
                title: activityTitle,
                description: current_file,
                size: bytes_processed || 0,
                timestamp: Date.now()
            };

            this._addRowToFeed(activity);

            if (status === 'completed' || status === 'failed') {
                try {
                    let allActivities = [];
                    const stored = localStorage.getItem(this.storageKey);
                    if (stored) allActivities = JSON.parse(stored);
                    allActivities.unshift(activity);
                    allActivities = allActivities.slice(0, this.maxStoredItems);
                    this.saveToStorage(allActivities);
                } catch (e) {
                    console.warn('[ActivityFeed] Could not persist activity:', e);
                }
            }
        }
    },

    viewSnapshots(fileName) {
        nav('files');
        const searchInput = document.getElementById('file-search-input');
        if (searchInput) {
            searchInput.value = fileName;
            searchInput.dispatchEvent(new Event('keyup'));
        }
    }
};

// Helper function for time formatting (keep as-is)
function timeSince(timestamp) {
    const ts = typeof timestamp === 'number' ? timestamp : parseInt(timestamp);
    const timestampMs = ts < 10000000000 ? ts * 1000 : ts;
    const now = Date.now();
    const secondsAgo = Math.floor((now - timestampMs) / 1000);

    if (secondsAgo < 0) return 'just now';
    if (secondsAgo === 0) return 'just now';
    if (secondsAgo < 60) return `${secondsAgo} second${secondsAgo !== 1 ? 's' : ''} ago`;

    const minutesAgo = Math.floor(secondsAgo / 60);
    if (minutesAgo < 60) return `${minutesAgo} minute${minutesAgo !== 1 ? 's' : ''} ago`;

    const hoursAgo = Math.floor(minutesAgo / 60);
    if (hoursAgo < 24) return `${hoursAgo} hour${hoursAgo !== 1 ? 's' : ''} ago`;

    const daysAgo = Math.floor(hoursAgo / 24);
    if (daysAgo < 7) return `${daysAgo} day${daysAgo !== 1 ? 's' : ''} ago`;

    const weeksAgo = Math.floor(daysAgo / 7);
    if (weeksAgo < 4) return `${weeksAgo} week${weeksAgo !== 1 ? 's' : ''} ago`;

    const monthsAgo = Math.floor(daysAgo / 30);
    return `${monthsAgo} month${monthsAgo !== 1 ? 's' : ''} ago`;
}

// Helper function for file size formatting
function humanFileSize(size) {
    const i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
    return (
        +(size / Math.pow(1024, i)).toFixed(2) * 1 +
        " " +
        ["B", "kB", "MB", "GB", "TB"][i]
    );
}


// =====================================================================
// --- DAEMON CONTROL
// =====================================================================
class DaemonControlManager {
    constructor() {
        this.button = document.getElementById('btn-daemon-control');
        this.statusInfo = document.getElementById('daemon-status-info');
        this.statusDot = this.statusInfo?.querySelector('.daemon-status-dot');
        this.statusText = this.statusInfo?.querySelector('.daemon-status-text');
        this.checkInterval = null;
        this.isProcessing = false;
        this.isStopping = false;
        this.stopStartTime = 0;
        this.statusHistory = [];
        this.maxHistory = 20;

        if (this.button) {
            this.init();
        }
    }

    async init() {
        // Setup button click handler
        this.button.addEventListener('click', (e) => this.handleButtonClick(e));

        // Check initial status
        await this.checkDaemonStatus();

        // Check status every 5 seconds
        this.checkInterval = setInterval(() => this.checkDaemonStatus(), 5000);

        // Also check when page becomes visible
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
            // Check daemon status using the new endpoint
            const response = await fetch('/api/daemon/ready-status');
            if (!response.ok) {
                // Try old endpoint for backward compatibility
                const oldResponse = await fetch('/api/daemon/status');
                if (!oldResponse.ok) {
                    this.updateUI(false, false, 'Daemon not running');
                    return;
                }

                const data = await oldResponse.json();
                this.updateUI(data.running, false, data.message || 'Unknown status');
                return;
            }

            const data = await response.json();

            // Record status history
            this.statusHistory.push({
                timestamp: Date.now(),
                running: data.running,
                ready: data.ready,
                message: data.message
            });

            // Keep only recent history
            if (this.statusHistory.length > this.maxHistory) {
                this.statusHistory.shift();
            }

            this.updateUI(data.running, data.ready, data.message);

        } catch (error) {
            console.error('Daemon status check error:', error);
            this.updateUI(false, false, 'Connection error');
        } finally {
            this.isProcessing = false;
        }
    }

    updateUI(isRunning, isReady, message) {
        // If we're in the process of stopping, IGNORE all status updates
        // The monitorDaemonExit() method handles UI updates during shutdown
        if (this.isStopping) {
            return; // Don't update UI - monitorDaemonExit() handles it
        }

        // Debug
        // console.log(`Daemon Status: Running=${isRunning}, Ready=${isReady}, Message=${message}`);

        // Normal state handling (only when NOT stopping)
        if (isReady && isRunning) {
            this.setButtonState('pause', 'Pause', 'Click to stop monitoring');
            this.setStatusInfo('ready', 'Monitoring files...');
        } else if (isRunning && !isReady) {
            this.setButtonState('running', 'Running...', 'Monitoring will start shortly...');
            this.setStatusInfo('starting', message || 'Warming up...');
        } else if (!isRunning) {
            this.setButtonState('run', 'Run', 'Click to start monitoring');
            this.setStatusInfo('stopped', 'Monitoring disabled');
        }
    }

    stopMonitoring() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
    }

    startMonitoring() {
        if (!this.checkInterval) {
            this.checkInterval = setInterval(() => this.checkDaemonStatus(), 5000);
        }
    }

    setButtonState(state, text, tooltip) {
        if (!this.button) return;

        // Remove all state classes
        this.button.classList.remove('run', 'running', 'pause', 'error', 'stopping');

        // Add current state class
        this.button.classList.add(state);

        // Update button text and icon
        const icon = this.button.querySelector('.daemon-icon');
        const textSpan = this.button.querySelector('.daemon-text');

        switch(state) {
            case 'run':
                if (icon) icon.className = 'bi bi-play-fill daemon-icon';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Start the daemon';
                this.button.disabled = false;
                break;

            case 'running':
                if (icon) icon.className = 'bi bi-arrow-repeat daemon-icon spin';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Daemon is starting...';
                this.button.disabled = true;
                break;

            case 'pause':
                if (icon) icon.className = 'bi bi-pause-fill daemon-icon';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Stop the daemon\n\nClick to initiate graceful shutdown';
                this.button.disabled = false;
                break;

            case 'error':
                if (icon) icon.className = 'bi bi-exclamation-triangle-fill daemon-icon';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Error occurred';
                this.button.disabled = false;
                break;

            case 'stopping': // New state
                if (icon) icon.className = 'bi bi-hourglass-split daemon-icon';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Daemon is cleaning up and shutting down...';
                this.button.disabled = true;
                break;
        }
    }

    setStatusInfo(state, text) {
        const statusInfo = document.getElementById('daemon-status-info');
        const statusText = document.getElementById('daemon-status-text');
        const staticDotElement = document.getElementById('daemon-connection-ping');
        const pingElement = document.getElementById('daemon-connection-ping-animation');
        
        if (!statusInfo || !statusText || !staticDotElement || !pingElement) {
            console.error("Could not find daemon status elements");
            return;
        }

        // Show status info
        statusInfo.classList.remove('hidden');
        
        // Remove all animation classes
        pingElement.classList.remove(
            'animate-ping-connected',
            'animate-ping-starting', 
            'animate-ping-disconnected',
            'animate-ping-stopped'
        );
        
        // Remove all dot color classes
        staticDotElement.classList.remove(
            'daemon-status-dot-connected',
            'daemon-status-dot-starting',
            'daemon-status-dot-disconnected',
            'daemon-status-dot-stopped'
        );

        // Set classes based on state
        switch(state) {
            case 'running':
                pingElement.classList.add('animate-ping-connected');
                staticDotElement.classList.add('daemon-status-dot-connected');
                break;
                
            case 'ready':
                pingElement.classList.add('animate-ping-connected');
                staticDotElement.classList.add('daemon-status-dot-connected');
                break;
                
            case 'starting':
            case 'stopping': // Use starting style for stopping too
                pingElement.classList.add('animate-ping-starting');
                staticDotElement.classList.add('daemon-status-dot-starting');
                break;
                
            case 'stopped':
                pingElement.classList.add('animate-ping-stopped'); // No animation
                staticDotElement.classList.add('daemon-status-dot-stopped');
                break;
                
            case 'error':
                pingElement.classList.add('animate-ping-disconnected');
                staticDotElement.classList.add('daemon-status-dot-disconnected');
                break;
                
            default:
                pingElement.classList.add('animate-ping-stopped');
                staticDotElement.classList.add('daemon-status-dot-stopped');
                break;
        }

        // Update status text
        statusText.textContent = text;
    }

    // And update the setButtonState to call this correctly:
    setButtonState(state, text, tooltip) {
        if (!this.button) return;

        // Remove all state classes
        this.button.classList.remove('run', 'running', 'pause', 'error', 'stopping');

        // Add current state class
        this.button.classList.add(state);

        // Update button text and icon
        const icon = this.button.querySelector('.daemon-icon');
        const textSpan = this.button.querySelector('.daemon-text');

        switch(state) {
            case 'run':
                if (icon) icon.className = 'bi bi-play-fill daemon-icon';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Start the daemon';
                this.button.disabled = false;
                break;

            case 'running':
                if (icon) icon.className = 'bi bi-arrow-repeat daemon-icon spin';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Daemon is running';
                this.button.disabled = true;
                break;

            case 'pause':
                if (icon) icon.className = 'bi bi-pause-fill daemon-icon';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Stop the daemon\n\nClick to initiate graceful shutdown';
                this.button.disabled = false;
                break;

            case 'error':
                if (icon) icon.className = 'bi bi-exclamation-triangle-fill daemon-icon';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Error occurred';
                this.button.disabled = false;
                break;

            case 'stopping':
                if (icon) icon.className = 'bi bi-hourglass-split daemon-icon';
                if (textSpan) textSpan.textContent = text;
                this.button.title = tooltip || 'Daemon is cleaning up and shutting down...';
                this.button.disabled = true;
                break;
        }
        
        // Also update the status indicator
        this.setStatusInfo(state === 'run' ? 'stopped' : state, text);
    }

    async handleButtonClick(event) {
        if (this.isProcessing) return;

        this.isProcessing = true;
        const currentState = this.button.classList.contains('run') ? 'stopped' :
                        this.button.classList.contains('pause') ? 'running' : 'unknown';

        try {
            if (currentState === 'stopped') {
                await this.startDaemon();
            } else if (currentState === 'running') {
                await this.stopDaemon();
            }
        } catch (error) {
            console.error('Daemon control error:', error);
            showSystemNotification('error', 'Daemon control error', error);
            // Always check status to sync button state
            setTimeout(() => this.checkDaemonStatus(), 2000);

        } finally {
            this.isProcessing = false;
        }
    }

    async startDaemon() {
        console.log('Starting daemon...');
        this.setButtonState('running', 'Starting...', 'Starting daemon...');

        // Give Flask a moment to recover after stop
        await new Promise(resolve => setTimeout(resolve, 1500));

        let retryCount = 0;
        const maxRetries = 3;

        while (retryCount < maxRetries) {
            try {
                console.log(`Start attempt ${retryCount + 1}/${maxRetries}`);

                // Add timeout to prevent hanging
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 8000);

                const response = await fetch('/api/daemon/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }

                const data = await response.json();

                if (data.success) {
                    this.pollForDaemonReady();
                    return; // Success!
                } else {
                    throw new Error(data.error || 'Failed to start daemon');
                }

            } catch (error) {
                retryCount++;
                console.warn(`Start attempt ${retryCount} failed:`, error.message);

                if (retryCount >= maxRetries) {
                    // Final failure
                    this.setButtonState('error', 'Error', 'Start failed');
                    showSystemNotification(`Failed after ${maxRetries} attempts. Please wait and try again.`, 'error');

                    // Revert button to "Run" after error
                    setTimeout(() => {
                        this.setButtonState('run', 'Run', 'Click to start daemon');
                    }, 3000);

                    throw error;
                }

                // Wait longer between each retry (1s, 2s, 3s...)
                await new Promise(resolve => setTimeout(resolve, 1000 * retryCount));
            }
        }
    }

async stopDaemon() {
        openConfirmationModal(
            `Stop Monitoring Your Files?`,
            'The backup service will save all existing metadata and immediately cease all active surveillance of your files. All background tasks will stop.',
            null,
            {
                showCancel: true,
                cancelText: 'Cancel',
                confirmText: 'Stop Daemon',
                customButtons: false,
                wideModal: false,
                
                // === ALL DAEMON STOPPING LOGIC GOES HERE ===
                onConfirm: async () => {
                    // Disable the periodic status checks
                    if (this.checkInterval) {
                        clearInterval(this.checkInterval);
                    }

                    this.setButtonState('stopping', 'Stopping...', 'Daemon is cleaning up...');
                    this.isStopping = true;
                    this.stopStartTime = Date.now();

                    try {
                        const response = await fetch('/api/backup/cancel', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ mode: 'graceful' })
                        });

                        const data = await response.json();

                        if (data.result === 'ok') {
                            showSystemNotification('info', 'Stopping monitoring...', 'Daemon is cleaning up files and saving metadata...');
                            // Start monitoring - NO automatic status checks
                            this.monitorDaemonExit();

                        } else {
                            throw new Error('Failed to stop daemon');
                        }

                    } catch (error) {
                        this.setButtonState('error', 'Error', 'Stop failed');
                        this.isStopping = false;
                        // Restore status checks
                        this.checkInterval = setInterval(() => this.checkDaemonStatus(), 5000);
                        showSystemNotification('error', 'Error while stopping the monitoring!', 'Daemon stop failed:', error.message);
                        // throw error; // Optionally throw if you need to propagate the error further
                    }
                },
                // === END OF CONFIRM LOGIC ===

                // === LOGIC FOR CANCEL ACTION (User aborts) ===
                onCancel: () => {
                    // Any cleanup if needed (e.g., restoring pre-stop UI state)
                    return;
                }
            }
        );
    }

    monitorDaemonExit() {
        let checkCount = 0;
        const maxChecks = 60; // Increase to 60 seconds

        const exitCheckInterval = setInterval(async () => {
            checkCount++;
            const secondsElapsed = checkCount;

            try {
                const response = await fetch('/api/daemon/ready-status?t=' + Date.now());
                if (response.ok) {
                    const data = await response.json();

                    if (!data.running) {
                        // Daemon has fully stopped
                        clearInterval(exitCheckInterval);
                        this.isStopping = false;
                        this.stopCooldown = null;

                        // Force final UI update
                        setTimeout(() => {
                            this.setButtonState('run', 'Run', 'Click to start daemon');
                            this.setStatusInfo('stopped', 'Stopped');
                            this.startMonitoring();
                        }, 2000);

                    } else {
                        // Still running - update stopping message
                        this.setButtonState('stopping', 'Stopping...', `Cleaning up... (${secondsElapsed}s)`);
                        this.setStatusInfo('starting', `Cleaning up... (${secondsElapsed}s)`);

                        if (secondsElapsed >= maxChecks) {
                            // Timeout
                            clearInterval(exitCheckInterval);
                            this.isStopping = false;
                            this.stopCooldown = null;

                            const offerForce = confirm(
                                `Daemon still running after ${secondsElapsed} seconds.\n` +
                                'Force stop?'
                            );

                            if (offerForce) {
                                await this.forceStopDaemon();
                            } else {
                                this.checkDaemonStatus();
                            }
                        }
                    }
                }
            } catch (error) {
                console.debug('Exit monitor error:', error);
            }
        }, 1000); // Check every second
    }

    async forceStopDaemon() {
        if (!confirm('Force stop daemon?\n\nThis will immediately terminate all operations.')) {
            return;
        }

        this.setButtonState('running', 'Force Stopping...', 'Force stopping daemon');
        this.isStopping = true;

        try {
            const response = await fetch('/api/backup/cancel', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mode: 'immediate' })
            });

            const data = await response.json();

            if (data.result === 'ok') {
                showSystemNotification('Daemon force stop requested', 'warning');

                // Force UI update after short delay
                setTimeout(() => {
                    this.isStopping = false;
                    this.checkDaemonStatus();
                }, 1000);

            } else {
                throw new Error('Force stop failed');
            }

        } catch (error) {
            console.error('Force stop error:', error);
            this.setButtonState('error', 'Error', 'Force stop failed');
            this.isStopping = false;
            showSystemNotification('Force stop failed: ' + error.message, 'error');
        }
    }

    pollForDaemonReady() {
        let pollCount = 0;
        const maxPolls = 60; // 60 * 2s = 120 seconds timeout

        const pollInterval = setInterval(async () => {
            pollCount++;

            if (pollCount > maxPolls) {
                clearInterval(pollInterval);
                showSystemNotification('Daemon startup is taking longer than expected', 'warning');
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

    showNotification(message, type = 'info') {
        const container = document.getElementById('notification-container');
        if (!container) {
            // Fallback to alert if no notification container
            alert(message);
            return;
        }

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="px-4 py-3 rounded-xl border shadow-lg flex items-center gap-3 min-w-[300px] max-w-md bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
                <i class="bi ${type === 'success' ? 'bi-check-circle-fill text-green-500' :
                             type === 'error' ? 'bi-x-circle-fill text-red-500' :
                             type === 'warning' ? 'bi-exclamation-triangle-fill text-yellow-500' :
                             'bi-info-circle-fill text-blue-500'}"></i>
                <div class="flex-1">
                    <p class="text-sm font-medium text-gray-900 dark:text-white">${message}</p>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
                    <i class="bi bi-x"></i>
                </button>
            </div>
        `;

        container.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
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
                    showSystemNotification(`Cleaned ${data.zombies_cleaned} zombie processes`, 'warning');
                }
            }
        } catch (error) {
            console.debug('Zombie cleanup error:', error);
        }
    }
}

// Make it globally accessible
window.DaemonControlManager = DaemonControlManager;


// =====================================================================
// --- DOM
// =====================================================================
document.addEventListener('DOMContentLoaded', () => {
    App.init();

    // Initialize Activity Feed Manager
    ActivityFeedManager.init();

    // Update timestamps every 5 seconds, if nav('overview')    
    if (currentTabId === 'overview') {
        timeStampInterval = setInterval(() => ActivityFeedManager.updateTimeAgo(), 5000);  // Update every 5 secs.
    } else {
        clearInterval(timeStampInterval); // **Stop** the currently running update check.
    }

    // Initialize Daemon Manager
    window.daemonControl = new DaemonControlManager();

    // Make toggleDaemon available globally (for onclick attribute)
    window.toggleDaemon = () => window.daemonControl?.handleButtonClick();

    // Initialize WebSocket connection
    if (window.backupStatusClient) {
        // Ensure it's connected
        if (!window.backupStatusClient.isConnected()) {
            window.backupStatusClient.connect();
        }
    }

    // Initialize file system - load real backup files from server
    initializeFileSystem();  // Load files early
    initializeTheme();  // Set theme early

    nav(currentTabId);  // Default to overview tab
    checkBackupConnection();
    renderSettings();
    updateProUI();
});


// =============================================
// INITIALIZATION
// =============================================
const App = {
    init: () => {
        appState.intervals = {};

        // Get username
        getUsersName();

        setInterval(checkBackupConnection, 5000);  // Initial check

        // // Initialize ActivityManager FIRST to load persisted activities
        BackupManager.updateUsage();
        DeviceManager.load();

        // Interval to update UI
        appState.intervals.storage = setInterval(BackupManager.updateUsage, 5000);
    },
};

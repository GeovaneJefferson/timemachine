// Save this as `app.js` and update your HTML to:
// <script src="app.js"></script>

/**
 * Time Machine UI - Complete Single File
 */

// ============ GLOBAL STATE ============
window.TimeMachine = {
  state: {
    user: { plan: 'basic', name: 'User', username: '' },
    connection: { isDeviceConnected: false },
    navigation: { currentTab: 'overview', activeSettingsTab: 'folders' },
    files: { fileSystem: null, currentFolder: null, selectedFile: null },
    migration: {
      selectedSource: null,
      selectionState: { home: false, flatpaks: false, installers: false }
    },
    devices: { list: [] },
    settings: {
      general: { autoStartup: false, autoUpdates: true, showNotifications: true },
      homeFolders: []
    }
  },

  utils: {
    formatBytes(bytes, decimals = 2) {
      const safeBytes = Number(bytes);
      if (isNaN(safeBytes) || safeBytes <= 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
      const i = Math.floor(Math.log(safeBytes) / Math.log(k));
      const effectiveIndex = Math.min(i, sizes.length - 1);
      return parseFloat((safeBytes / Math.pow(k, effectiveIndex)).toFixed(decimals)) + ' ' + sizes[effectiveIndex];
    },

    getIconForFile(filename) {
      const ext = filename.split('.').pop().toLowerCase();
      const icons = {
        'pdf': 'bi-file-earmark-pdf-fill',
        'doc': 'bi-file-earmark-word-fill', 'docx': 'bi-file-earmark-word-fill',
        'xls': 'bi-file-earmark-excel-fill', 'xlsx': 'bi-file-earmark-excel-fill',
        'jpg': 'bi-file-earmark-image-fill', 'jpeg': 'bi-file-earmark-image-fill',
        'png': 'bi-file-earmark-image-fill', 'gif': 'bi-file-earmark-image-fill',
        'zip': 'bi-file-earmark-zip-fill', 'rar': 'bi-file-earmark-zip-fill',
        'mp3': 'bi-file-earmark-music-fill', 'wav': 'bi-file-earmark-music-fill',
        'mp4': 'bi-file-earmark-play-fill', 'avi': 'bi-file-earmark-play-fill',
      };
      return icons[ext] || 'bi-file-earmark-fill';
    },

    getColorForFile(filename) {
      const ext = filename.split('.').pop().toLowerCase();
      const colors = {
        'pdf': 'text-red-500',
        'doc': 'text-blue-500', 'docx': 'text-blue-500',
        'xls': 'text-emerald-600', 'xlsx': 'text-emerald-600',
        'jpg': 'text-pink-500', 'jpeg': 'text-pink-500', 'png': 'text-pink-500',
        'zip': 'text-purple-500', 'rar': 'text-purple-500',
        'mp3': 'text-purple-500', 'wav': 'text-purple-500',
        'mp4': 'text-red-500', 'avi': 'text-red-500',
      };
      return colors[ext] || 'text-gray-500';
    }
  },

  // Initialize the app
  init() {
    console.log('Time Machine UI Initializing...');

    // Load user name
    this.loadUsername();

    // Set up event listeners
    this.setupEventListeners();

    // Initialize theme
    this.initTheme();

    // Start polling
    this.startPolling();

    // Initial navigation
    this.nav('overview');
  },

  // ============ NAVIGATION ============
  nav(tabId) {
    TimeMachine.state.navigation.currentTab = tabId;

    // Update sidebar
    document.querySelectorAll('.btn-nav').forEach(btn => {
      btn.classList.remove('active', 'bg-blue-50', 'text-blue-600', 'dark:bg-blue-900/20', 'dark:text-blue-400');
      btn.classList.add('text-secondary');
    });

    const targetBtn = document.getElementById('btn-' + tabId);
    if (targetBtn) {
      targetBtn.classList.add('active');
      targetBtn.classList.remove('text-secondary');
    }

    // Switch views
    ['overview', 'files', 'devices', 'migration', 'settings', 'logs'].forEach(t => {
      const view = document.getElementById('view-' + t);
      if (view) view.classList.add('hidden');
    });

    const targetView = document.getElementById('view-' + tabId);
    if (targetView) {
      targetView.classList.remove('hidden');
      targetView.classList.add('animate-entry');
    }

    // Update page title
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

    // Load data for tab
    this.loadTabData(tabId);
  },

  loadTabData(tabId) {
    switch(tabId) {
      case 'devices':
        this.loadDevices();
        break;
      case 'files':
        if (TimeMachine.state.connection.isDeviceConnected) {
          this.loadFolderContents();
        }
        break;
      case 'migration':
        this.initMigrationView();
        break;
      case 'settings':
        this.renderSettings();
        break;
    }
  },

  // ============ FILE SYSTEM ============
  async loadFolderContents(folderPath = '') {
    const container = document.getElementById('file-list-container');

    if (!TimeMachine.state.connection.isDeviceConnected) {
      container.innerHTML = `
        <div class="p-8 text-center text-muted">
          <i class="bi bi-exclamation-triangle-fill text-3xl mb-3"></i>
          <h4 class="font-bold text-main">No Backup Device Connected</h4>
          <p class="text-sm mt-1">Please connect your backup device to browse files.</p>
        </div>`;
      return;
    }

    container.innerHTML = `
      <div class="flex items-center gap-2 text-slate-500">
        <i class="bi bi-arrow-clockwise animate-spin"></i>
        <span>Loading folder...</span>
      </div>`;

    try {
      const encodedPath = encodeURIComponent(folderPath);
      const response = await fetch(`/api/search/folder?path=${encodedPath}`);
      const data = await response.json();

      if (data.success && data.items?.length > 0) {
        this.renderExplorer(data.items);
      } else {
        container.innerHTML = '<p class="p-4 text-gray-400">Folder is empty.</p>';
      }
    } catch (error) {
      console.error('Failed to load folder contents:', error);
      container.innerHTML = '<p class="p-4 text-red-500">Failed to load folder contents.</p>';
    }
  },

  renderExplorer(items) {
    const container = document.getElementById('file-list-container');
    if (!container) return;

    container.innerHTML = '';

    items.sort((a, b) => {
      if (a.type === 'folder' && b.type !== 'folder') return -1;
      if (a.type !== 'folder' && b.type === 'folder') return 1;
      return a.name.localeCompare(b.name);
    });

    items.forEach(item => {
      const isFolder = item.type === 'folder';
      const iconClass = isFolder ? 'bi-folder-fill text-blue-400' : TimeMachine.utils.getIconForFile(item.name);
      const iconColor = isFolder ? '' : TimeMachine.utils.getColorForFile(item.name);

      const displayName = item.name.length > 50
        ? item.name.substring(0, 47) + '...'
        : item.name;

      const el = document.createElement('div');
      el.className = 'flex items-center gap-3 p-2.5 rounded-lg hover:bg-gray-100 dark:hover:bg-white/5 cursor-pointer transition-colors group';
      el.innerHTML = `
        <i class="bi ${iconClass} ${iconColor} text-lg flex-shrink-0"></i>
        <span class="text-sm text-main font-medium truncate flex-1" title="${item.name}">${displayName}</span>
        <i class="bi bi-chevron-right text-xs text-muted opacity-0 group-hover:opacity-100 transition-opacity"></i>
      `;

      el.onclick = () => {
        if (isFolder) {
          this.openFolder(item);
        } else {
          this.selectFile(item);
        }
      };

      container.appendChild(el);
    });
  },

  openFolder(folder) {
    // Implementation for opening folder
    console.log('Opening folder:', folder.name);
  },

  selectFile(file) {
    TimeMachine.state.files.selectedFile = file;
    console.log('Selected file:', file.name);
  },

  // ============ DEVICES ============
  async loadDevices() {
    const container = document.getElementById('device-list-container');
    if (!container) return;

    container.innerHTML = `
      <div class="col-span-full flex flex-col items-center justify-center py-12 text-muted">
        <i class="bi bi-arrow-clockwise animate-spin text-2xl mb-2"></i>
        <p>Scanning sources...</p>
      </div>`;

    try {
      const [devicesData, configData] = await Promise.all([
        fetch('/api/storage/devices').then(res => res.json()),
        fetch('/api/config').then(res => res.json())
      ]);

      if (!devicesData.success || !devicesData.devices?.length) {
        container.innerHTML = `
          <div class="col-span-full border-2 border-dashed border-main rounded-2xl p-10 text-center">
            <i class="bi bi-hdd text-4xl text-muted mb-3 block"></i>
            <h4 class="font-bold text-main">No Devices Found</h4>
            <p class="text-sm text-muted">Connect a USB drive to get started.</p>
          </div>`;
        return;
      }

      const activePath = configData?.DEVICE_INFO?.path;
      container.innerHTML = '';

      devicesData.devices.forEach(device => {
        const usedGB = Math.round((device.used || 0) / (1024 ** 3));
        const totalGB = Math.round((device.total || 0) / (1024 ** 3));
        const percent = totalGB > 0 ? Math.round((usedGB / totalGB) * 100) : 0;
        const isActive = device.mount_point === activePath;
        const isSSD = device.is_ssd;

        const card = `
          <div class="bg-card p-6 rounded-2xl border ${isActive ? 'border-emerald-500 ring-1 ring-emerald-500' : 'border-main hover:border-brand-300'} group cursor-pointer transition-all duration-200">
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center gap-4">
                <div class="w-12 h-12 rounded-xl bg-gray-50 dark:bg-white/5 flex items-center justify-center text-xl text-main">
                  ${isSSD ? '<i class="bi bi-device-ssd-fill"></i>' : '<i class="bi bi-hdd-fill"></i>'}
                </div>
                <div>
                  <h4 class="font-bold text-main text-base">${device.label || device.name || 'Unnamed Drive'}</h4>
                  <div class="flex items-center gap-1.5 mt-0.5">
                    <span class="w-1.5 h-1.5 rounded-full ${isActive ? 'bg-emerald-500' : 'bg-gray-400'}"></span>
                    <span class="text-xs font-medium ${isActive ? 'text-emerald-500' : 'text-muted'}">${isActive ? 'Active' : 'Ready'}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="mb-4">
              <div class="flex justify-between text-xs font-medium text-muted mb-2">
                <span>${usedGB} GB Used</span>
                <span>${totalGB} GB Total</span>
              </div>
              <div class="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-2 overflow-hidden">
                <div class="h-full bg-brand-500 rounded-full" style="width: ${percent}%"></div>
              </div>
            </div>
            ${isActive
              ? `<button disabled class="w-full py-2 rounded-lg bg-emerald-50 dark:bg-emerald-900/20 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center justify-center gap-2">
                   <i class="bi bi-check-circle-fill"></i> Backup Location
                 </button>`
              : `<button onclick="TimeMachine.selectDevice(${JSON.stringify(device).replace(/"/g, '&quot;')})"
                   class="w-full py-2 rounded-lg border border-main hover:bg-gray-50 dark:hover:bg-white/5 text-main text-xs font-bold transition cursor-pointer">
                   Set as Backup
                 </button>`
            }
          </div>`;

        container.innerHTML += card;
      });
    } catch (error) {
      console.error('Failed to load devices:', error);
      container.innerHTML = `
        <div class="col-span-full text-center py-10 border-2 border-red-100 dark:border-red-900/30 bg-red-50 dark:bg-red-900/10 rounded-xl">
          <i class="bi bi-exclamation-triangle text-red-400 text-3xl mb-2 block"></i>
          <div class="text-red-600 dark:text-red-400 font-bold">Error loading devices</div>
          <div class="text-sm text-red-500 dark:text-red-300 mt-1">Connection failed</div>
        </div>`;
    }
  },

  selectDevice(device) {
    console.log('Selecting device:', device);
    // Implementation for device selection
  },

  // ============ MIGRATION ============
  initMigrationView() {
    document.getElementById('mig-step-1-source').classList.remove('hidden');
    document.getElementById('mig-step-2-content').classList.add('hidden');
    document.getElementById('mig-step-3-progress').classList.add('hidden');
    document.getElementById('mig-step-desc').innerText = "Select a source to start the restoration process.";
    this.renderSourceList();
  },

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
      const response = await fetch('/api/migration/sources');
      const data = await response.json();

      container.innerHTML = '';

      if (!data.success || !data.sources?.length) {
        container.innerHTML = `
          <div class="text-center p-10 border-2 border-dashed border-main rounded-2xl text-muted">
            <i class="bi bi-hdd-network-off text-4xl mb-3"></i>
            <h4 class="font-bold text-main">No Backup Sources Found</h4>
            <p class="text-sm mt-1">Connect a drive with a Time Machine backup and try again.</p>
          </div>`;
        return;
      }

      data.sources.forEach(device => {
        const totalGB = Math.round((device.total || 0) / (1024 ** 3));
        container.innerHTML += `
          <div class="bg-card border border-main rounded-2xl p-5 flex items-center gap-5 hover:border-brand-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer transition-all group">
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
      });
    } catch (error) {
      console.error('Failed to load migration sources:', error);
    }
  },

  // ============ SETTINGS ============
  async renderSettings() {
    const container = document.getElementById('folder-selection-list');
    if (!container) return;

    container.innerHTML = '<div class="p-4 text-center text-slate-500">Loading settings...</div>';

    try {
      const response = await fetch('/api/backup-folders');
      const data = await response.json();

      if (data.success) {
        TimeMachine.state.settings.homeFolders = data.folders;
        this.renderFolderList();
        this.updateSummaryText();
      }
    } catch (error) {
      console.error('Failed to load settings:', error);
    }
  },

  renderFolderList() {
    const container = document.getElementById('folder-selection-list');
    if (!container) return;

    container.innerHTML = '';

    TimeMachine.state.settings.homeFolders.forEach((folder, idx) => {
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
            <input type="checkbox" class="sr-only peer" ${folder.selected ? 'checked' : ''}
                   onchange="TimeMachine.toggleFolder(${idx})">
            <div class="checkbox-normal"></div>
          </label>
        </div>
      `;
    });
  },

  toggleFolder(index) {
    if (TimeMachine.state.settings.homeFolders[index]) {
      TimeMachine.state.settings.homeFolders[index].selected =
        !TimeMachine.state.settings.homeFolders[index].selected;
      this.updateSummaryText();
    }
  },

  updateSummaryText() {
    const count = TimeMachine.state.settings.homeFolders.filter(f => f.selected).length;
    const el = document.getElementById('backup-summary-text');
    if (el) el.innerText = `${count} folders selected for monitoring`;
  },

  // ============ CONNECTION CHECKING ============
  async checkBackupConnection() {
    try {
      const response = await fetch('/api/backup/connection');
      const data = await response.json();

      const wasConnected = TimeMachine.state.connection.isDeviceConnected;
      const isConnectedNow = data.connected;

      TimeMachine.state.connection.isDeviceConnected = isConnectedNow;

      // Update UI
      const staticDot = document.getElementById('devices-connection-ping');
      const pingAnimation = document.getElementById('devices-connection-ping-animation');

      if (staticDot && pingAnimation) {
        if (isConnectedNow) {
          staticDot.classList.replace('status-dot-disconnected', 'status-dot-connected');
          pingAnimation.classList.replace('animate-ping-disconnected', 'animate-ping-connected');
        } else {
          staticDot.classList.replace('status-dot-connected', 'status-dot-disconnected');
          pingAnimation.classList.replace('animate-ping-connected', 'animate-ping-disconnected');
        }
      }

      // If on files tab and connection changed, reload
      if (TimeMachine.state.navigation.currentTab === 'files' && wasConnected !== isConnectedNow) {
        this.loadFolderContents();
      }
    } catch (error) {
      console.error('Connection check failed:', error);
      TimeMachine.state.connection.isDeviceConnected = false;
    }
  },

  // ============ UTILITY FUNCTIONS ============
  async loadUsername() {
    try {
      const response = await fetch('/api/username');
      const data = await response.json();
      const name = data.username || 'User';
      TimeMachine.state.user.name = name.charAt(0).toUpperCase() + name.slice(1);
      this.updateGreeting();
    } catch (error) {
      console.error('Failed to load username:', error);
    }
  },

  updateGreeting() {
    const greetEl = document.getElementById('greeting');
    if (greetEl) {
      greetEl.innerText = `Hello, ${TimeMachine.state.user.name}`;
    }
  },

  initTheme() {
    const saved = localStorage.getItem('theme');
    const isDark = saved === 'dark';
    document.documentElement.classList.toggle('dark', isDark);

    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) themeToggle.checked = isDark;

    const icon = document.getElementById('theme-icon');
    if (icon) {
      icon.className = isDark ? 'bi bi-sun-fill text-yellow-400' : 'bi bi-moon-stars-fill text-brand-500';
    }
  },

  toggleTheme(e) {
    const isDark = e.target.checked;
    document.documentElement.classList.toggle('dark', isDark);

    const icon = document.getElementById('theme-icon');
    if (isDark) {
      icon.className = 'bi bi-sun-fill text-yellow-400';
    } else {
      icon.className = 'bi bi-moon-stars-fill text-brand-500';
    }
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
  },

  startPolling() {
    // Check connection every 3 seconds
    setInterval(() => this.checkBackupConnection(), 3000);

    // Update greeting clock every second
    setInterval(() => {
      const now = new Date();
      const timeEl = document.getElementById('current-time');
      if (timeEl) timeEl.innerText = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      });
    }, 1000);
  },

  setupEventListeners() {
    // Navigation
    document.addEventListener('click', (e) => {
      const navButton = e.target.closest('.btn-nav');
      if (navButton && navButton.id) {
        const tabId = navButton.id.replace('btn-', '');
        this.nav(tabId);
      }
    });

    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('change', (e) => this.toggleTheme(e));
    }

    // File search
    const searchInput = document.getElementById('file-search-input');
    if (searchInput) {
      let searchTimeout;
      searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          this.searchFiles(e.target.value);
        }, 300);
      });
    }

    // Settings tabs
    document.addEventListener('click', (e) => {
      if (e.target.id === 'sub-tab-btn-folders') {
        this.switchSettingsTab('folders');
      } else if (e.target.id === 'sub-tab-btn-general') {
        this.switchSettingsTab('general');
      }
    });
  },

  async searchFiles(query) {
    const container = document.getElementById('file-list-container');
    if (!query.trim()) {
      this.renderExplorer(TimeMachine.state.files.currentFolder?.children || []);
      return;
    }

    try {
      const response = await fetch(`/api/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();

      if (data.files?.length > 0) {
        const results = data.files.map(file => ({
          name: file.name,
          path: file.path,
          type: 'file',
          icon: TimeMachine.utils.getIconForFile(file.name),
          color: TimeMachine.utils.getColorForFile(file.name)
        }));

        this.renderExplorer(results);
      } else {
        container.innerHTML = '<p class="p-4 text-gray-400">No files found matching your search.</p>';
      }
    } catch (error) {
      console.error('Search failed:', error);
      container.innerHTML = '<p class="p-4 text-red-500">Search failed. Please try again.</p>';
    }
  },

  switchSettingsTab(tabName) {
    TimeMachine.state.navigation.activeSettingsTab = tabName;

    ['folders', 'general'].forEach(t => {
      const btn = document.getElementById(`sub-tab-btn-${t}`);
      const content = document.getElementById(`settings-tab-${t}`);

      if (btn && content) {
        if (t === tabName) {
          btn.className = "px-4 py-2 text-sm font-bold text-hyperlink border-b-2 cursor-pointer border-hyperlink";
          content.classList.remove('hidden');
        } else {
          btn.className = "px-4 py-2 text-sm font-bold text-secondary border-b-2 border-transparent hover:text-secondary cursor-pointer";
          content.classList.add('hidden');
        }
      }
    });
  },

  // Notification system
  showNotification(type, title, message, duration = 6000) {
    const container = document.getElementById('notification-container');
    if (!container) return;

    let iconClass = '', colorClass = '';

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
        if (toast.parentNode === container) container.removeChild(toast);
      }, 300);
    }, duration);
  }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  TimeMachine.init();
});

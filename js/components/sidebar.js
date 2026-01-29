// src/js/components/sidebar.js

export default class Sidebar {
    constructor() {
        this.navigation = [
            { id: 'dashboard', title: 'Dashboard', icon: 'backup', active: true },
            { id: 'applications', title: 'Applications', icon: 'apps', active: false },
            { id: 'dev-packages', title: 'Dev Packages', icon: 'code', active: false }
            // Removed: Folders navigation item
        ];

        this.folders = []; // Will be populated from backup
        this.backupFolders = []; // Store folders from backup
        this.tags = [
            { name: 'Urgent', color: 'bg-red-500' },
            { name: 'Work', color: 'bg-blue-500' }
        ];

        this.settings = [
            { id: 'settings', name: 'Settings', icon: 'settings', active: false },
            { id: 'help', name: 'Help & Support', icon: 'help', active: false },
            { id: 'about', name: 'About', icon: 'info', active: false }
        ];

        this.devices = []; // Store devices from API
    }

    async render() {
        return `
        <div class="flex flex-col h-full">
        <div class="space-y-6 flex-1">
        ${this.renderNavigationSection()}
        ${await this.renderBackupFoldersSection()}
        ${await this.renderLocationsSection()}
        ${this.renderTagsSection()}
        </div>

        <!-- Settings Section at Bottom -->
        <div class="pt-6 mt-6 border-t border-gray-200 dark:border-gray-700">
        <div class="space-y-1">
        ${this.renderSettingsSection()}
        </div>
        </div>
        </div>
        `;
    }

    renderNavigationSection() {
        return `
        <div>
        <h3 class="px-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wide mb-1">Navigate</h3>
        <nav class="space-y-0.5">
        ${this.navigation.map(item => this.renderNavItem(item)).join('')}
        </nav>
        </div>
        `;
    }

    renderNavItem(item) {
        const activeClass = item.active ? 'sidebar-item-active font-medium' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50';

        return `
        <a href="#"
        data-route="${item.id}"
        class="flex items-center gap-2 px-2 py-1.5 text-sm rounded-md transition-colors cursor-pointer ${activeClass}">
        <span class="material-icons-round text-lg">${item.icon}</span>
        ${item.title}
        </a>
        `;
    }

    async renderBackupFoldersSection() {
        try {
            // Check if backup is configured and get folders
            const response = await fetch('/api/backup/path');
            const data = await response.json();

            let foldersHTML = '';

            if (data.success && data.device_configured && data.exists) {
                // Fetch backup folders
                const foldersResponse = await fetch('/api/backup/files?path=');
                const foldersData = await foldersResponse.json();

                console.log('Folders data response:', foldersData);

                if (foldersData.success && foldersData.items && foldersData.items.length > 0) {
                    console.log('Backup folders data:', foldersData);
                    // Filter only folders and sort alphanumerically by name
                    const folders = foldersData.items
                    .filter(item => item.type === 'folder')
                    .sort((a, b) => {
                        // Case-insensitive alphanumeric sort
                        return a.name.localeCompare(b.name, undefined, {
                            sensitivity: 'base',
                            numeric: true
                        });
                    });

                    this.backupFolders = folders;

                    if (this.backupFolders.length > 0) {
                        foldersHTML = this.backupFolders.map(folder => `
                        <a href="#"
                        class="backup-folder-link flex items-center gap-2 px-2 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50 rounded-md transition-colors cursor-pointer"
                        data-folder-path="${folder.path}"
                        data-folder-name="${folder.name}">
                        <span class="material-icons-round text-lg">${this.getFolderIcon(folder.name)}</span>
                        <span class="truncate" title="${folder.name}">${folder.name}</span>
                        </a>
                        `).join('');
                    } else {
                        foldersHTML = `
                        <div class="px-2 py-1.5 text-sm text-gray-500 dark:text-gray-400 italic">
                        No folders in backup
                        </div>
                        `;
                    }
                } else {
                    foldersHTML = `
                    <div class="px-2 py-1.5 text-sm text-gray-500 dark:text-gray-400 italic">
                    No backup files found
                    </div>
                    `;
                }
            } else {
                foldersHTML = `
                <div class="px-2 py-1.5 text-sm text-gray-500 dark:text-gray-400 italic">
                No backup device configured or connected
                </div>
                `;
            }

            return `
            <div id="backup-folders-section">
            <div class="flex items-center justify-between px-2 mb-1">
            <h3 class="text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wide">Backup Folders</h3>
            <button class="material-icons-round text-sm text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 refresh-backup-folders-btn cursor-pointer"
            title="Refresh backup folders">
            refresh
            </button>
            </div>
            <nav class="space-y-0.5" id="backup-folders-list">
            ${foldersHTML}
            </nav>
            </div>
            `;

        } catch (error) {
            console.error('Error loading backup folders:', error);
            return `
            <div id="backup-folders-section">
            <h3 class="px-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wide mb-1">Backup Folders</h3>
            <nav class="space-y-0.5">
            <div class="px-2 py-1.5 text-sm text-red-500 dark:text-red-400 cursor-default">
            Failed to load backup folders
            </div>
            </nav>
            </div>
            `;
        }
    }

    getFolderIcon(folderName) {
        const name = folderName.toLowerCase();
        if (name.includes('document') || name.includes('doc')) return 'description';
        if (name.includes('picture') || name.includes('image') || name.includes('photo')) return 'image';
        if (name.includes('music') || name.includes('audio')) return 'music_note';
        if (name.includes('video') || name.includes('movie')) return 'movie';
        if (name.includes('download')) return 'download';
        if (name.includes('desktop')) return 'desktop_windows';
        if (name.includes('project') || name.includes('code')) return 'code';
        if (name.includes('config') || name.includes('setting')) return 'settings';
        return 'folder';
    }

    async renderLocationsSection() {
        try {
            // Fetch devices from API
            const response = await fetch('/api/locations/sidebar-devices');
            const data = await response.json();

            let locationsHTML = '';

            if (data.success && data.devices && data.devices.length > 0) {
                this.devices = data.devices;
            } else {
                // No devices found
                locationsHTML = `
                <div class="px-2 py-1.5 cursor-default">
                <div class="text-sm text-gray-500 dark:text-gray-400 italic">
                ${data.error ? `Error: ${data.error}` : 'No storage devices found'}
                </div>
                <div class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                Connect a USB drive or check /media/ directory
                </div>
                </div>
                <a href="#" class="flex items-center gap-2 px-2 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50 rounded-md transition-colors cursor-pointer">
                <span class="material-icons-round text-lg">public</span>
                Network
                </a>
                `;
            }

            return `
            <div id="locations-section">
            <div class="flex items-center justify-between px-2 mb-1">
            <h3 class="text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wide">Locations</h3>
            <button class="material-icons-round text-sm text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 refresh-btn cursor-pointer"
            title="Refresh devices">
            refresh
            </button>
            </div>
            <nav class="space-y-0.5" id="devices-list">
            ${locationsHTML}
            </nav>
            </div>
            `;

        } catch (error) {
            console.error('Error loading devices:', error);
            return `
            <div id="locations-section">
            <h3 class="px-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wide mb-1">Locations</h3>
            <nav class="space-y-0.5">
            <div class="px-2 py-1.5 text-sm text-red-500 dark:text-red-400 cursor-default">
            Failed to load devices
            </div>
            <a href="#" class="flex items-center gap-2 px-2 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50 rounded-md transition-colors cursor-pointer">
            <span class="material-icons-round text-lg">public</span>
            Network
            </a>
            </nav>
            </div>
            `;
        }
    }

    renderTagsSection() {
        return `
        <div>
        <h3 class="px-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wide mb-1">Tags</h3>
        <nav class="space-y-0.5">
        ${this.tags.map(tag => `
            <a href="#" class="flex items-center gap-2 px-2 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50 rounded-md transition-colors cursor-pointer">
            <span class="w-2.5 h-2.5 rounded-full ${tag.color}"></span>
            ${tag.name}
            </a>
            `).join('')}
            </nav>
            </div>
            `;
    }

    renderSettingsSection() {
        return `
        <div>
        <h3 class="px-2 text-xs font-semibold text-text-secondary-light dark:text-text-secondary-dark uppercase tracking-wide mb-1">System</h3>
        <nav class="space-y-0.5">
        ${this.settings.map(setting => {
            const activeClass = setting.active ? 'sidebar-item-active font-medium' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50';
            return `
            <a href="#"
            data-route="${setting.id}"
            class="flex items-center gap-2 px-2 py-1.5 text-sm rounded-md transition-colors cursor-pointer ${activeClass}">
            <span class="material-icons-round text-lg">${setting.icon}</span>
            ${setting.name}
            </a>
            `;
        }).join('')}
        </nav>
        </div>
        `;
    }

    init() {
        console.log('Sidebar initialized');

        // Clear any stale device selection on init
        const currentPage = window.location.hash || '#dashboard';
        if (!currentPage.includes('location')) {
            sessionStorage.removeItem('selectedDevice');
        }

        this.attachEventListeners();
        this.refreshDevices(); // Initialize devices list
    }

    attachEventListeners() {
        // Handle navigation clicks (Dashboard, Applications, Dev Packages)
        document.addEventListener('click', (e) => {
            const navLink = e.target.closest('[data-route]');
            if (navLink) {
                e.preventDefault();
                const route = navLink.getAttribute('data-route');

                // Clear device highlights when clicking any nav item
                const deviceLinks = document.querySelectorAll('[data-action="select-device"]');
                deviceLinks.forEach(el => {
                    el.classList.remove('sidebar-item-active', 'font-medium');
                    if (!el.classList.contains('text-gray-700')) {
                        el.classList.add('text-gray-700', 'dark:text-gray-300');
                    }
                });

                // Force immediate DOM update/repaint
                void document.body.offsetHeight;

                // Clear sessionStorage
                sessionStorage.removeItem('selectedDevice');

                this.handleNavigation(route, navLink);
            }

            // Handle backup folder clicks - navigate to folders page
            const backupFolderLink = e.target.closest('.backup-folder-link');
            if (backupFolderLink) {
                e.preventDefault();
                const folderPath = backupFolderLink.getAttribute('data-folder-path');
                const folderName = backupFolderLink.getAttribute('data-folder-name');

                console.log(`Backup folder selected: ${folderName} (${folderPath})`);

                // Store selected folder in sessionStorage
                sessionStorage.setItem('selectedBackupFolder', JSON.stringify({
                    path: folderPath,
                    name: folderName
                }));

                // Load the folders page with this folder
                this.loadFoldersPageWithFolder(folderPath, folderName);

                // Highlight selected folder in sidebar
                this.highlightSelectedBackupFolder(folderPath);
            }

            // Handle device clicks - navigate to "locations" page with device
            const deviceLink = e.target.closest('[data-action="select-device"]');
            if (deviceLink) {
                e.preventDefault();
                const mountpoint = deviceLink.getAttribute('data-device-mountpoint');
                const deviceName = deviceLink.getAttribute('data-device-name');
                const device = this.devices.find(d => d.mountpoint === mountpoint);

                if (device) {
                    console.log(`Device selected: ${deviceName} (${mountpoint})`);

                    // Store selected device in sessionStorage
                    sessionStorage.setItem('selectedDevice', JSON.stringify(device));

                    // MANUALLY LOAD THE LOCATIONS PAGE
                    this.loadLocationsPage(device);

                    // Highlight selected device in sidebar
                    this.highlightSelectedDevice(mountpoint);
                }
            }

            // Handle refresh buttons
            if (e.target.closest('.refresh-btn')) {
                e.preventDefault();
                this.refreshDevices();
            }

            if (e.target.closest('.refresh-backup-folders-btn')) {
                e.preventDefault();
                this.refreshBackupFolders();
            }

            // Handle eject buttons on devices
            const ejectBtn = e.target.closest('.eject-btn');
            if (ejectBtn) {
                e.preventDefault();
                e.stopPropagation();
                const mountpoint = ejectBtn.getAttribute('data-mountpoint');
                const deviceName = ejectBtn.getAttribute('data-device-name');
                this.ejectDevice(mountpoint, deviceName);
            }
        });

        // Listen for external updates and refresh
        document.addEventListener('devices-updated', async () => {
            try {
                await this.refreshDevices();
            } catch (e) {
                console.error('Failed to refresh devices after update event', e);
            }
        });

        document.addEventListener('backup-configured', async () => {
            try {
                await this.refreshBackupFolders();
            } catch (e) {
                console.error('Failed to refresh backup folders after configuration', e);
            }
        });
    }

    async loadFoldersPageWithFolder(folderPath, folderName) {
        try {
            // Get the page content container
            const pageContent = document.getElementById('page-content');
            const loading = document.getElementById('loading');

            if (!pageContent) {
                console.error('Page content container not found');
                return;
            }

            // Show loading indicator
            if (loading) loading.classList.remove('hidden');

            // Import and load the folders page
            const FoldersModule = await import('../pages/folders.js');
            const FoldersPage = FoldersModule.default;
            const page = new FoldersPage();

            // Set the current path to the selected folder
            if (folderPath) {
                page.currentPath = folderPath.split('/').filter(segment => segment.length > 0);
            }

            // Render the page
            pageContent.innerHTML = await page.render();

            // Initialize the page
            if (page.afterRender) {
                await page.afterRender();
            }

            // Hide loading indicator
            if (loading) loading.classList.add('hidden');

            console.log('Folders page loaded with folder:', folderName);

        } catch (error) {
            console.error('Failed to load folders page:', error);
            showError('Failed to load folders page', 'error');

            // Show error in page content
            const pageContent = document.getElementById('page-content');
            if (pageContent) {
                pageContent.innerHTML = `
                <div class="p-8 text-center">
                <div class="text-red-500 text-5xl mb-4">⚠️</div>
                <h2 class="text-xl font-bold mb-2">Failed to Load Folders</h2>
                <p class="text-gray-600 mb-4">${error.message}</p>
                <button onclick="window.loadPage('dashboard')" class="px-4 py-2 bg-primary text-white rounded">
                Return to Dashboard
                </button>
                </div>
                `;
            }

            const loading = document.getElementById('loading');
            if (loading) loading.classList.add('hidden');
        }
    }

    async loadLocationsPage(device) {
        try {
            // Get the page content container
            const pageContent = document.getElementById('page-content');
            const loading = document.getElementById('loading');

            if (!pageContent) {
                console.error('Page content container not found');
                return;
            }

            // Show loading indicator
            if (loading) loading.classList.remove('hidden');

            // Import and load the locations page
            const LocationsModule = await import('../pages/locations.js');
            const LocationsPage = LocationsModule.default;
            const page = new LocationsPage();

            // Render the page
            pageContent.innerHTML = await page.render();

            // Initialize the page
            if (page.afterRender) {
                await page.afterRender();
            }

            // Update active state in sidebar (manually set locations as active)
            this.navigation.forEach(item => {
                item.active = false; // Reset all
            });
            this.updateActiveStates();

            // Hide loading indicator
            if (loading) loading.classList.add('hidden');

            console.log('Locations page loaded with device:', device.name);

        } catch (error) {
            console.error('Failed to load locations page:', error);
            showError('Failed to load locations page', 'error');

            // Show error in page content
            const pageContent = document.getElementById('page-content');
            if (pageContent) {
                pageContent.innerHTML = `
                <div class="p-8 text-center">
                <div class="text-red-500 text-5xl mb-4">⚠️</div>
                <h2 class="text-xl font-bold mb-2">Failed to Load Locations</h2>
                <p class="text-gray-600 mb-4">${error.message}</p>
                <button onclick="window.loadPage('dashboard')" class="px-4 py-2 bg-primary text-white rounded">
                Return to Dashboard
                </button>
                </div>
                `;
            }

            const loading = document.getElementById('loading');
            if (loading) loading.classList.add('hidden');
        }
    }

    async refreshBackupFolders() {
        const backupFoldersSection = document.getElementById('backup-folders-section');
        if (!backupFoldersSection) return;

        const refreshBtn = backupFoldersSection.querySelector('.refresh-backup-folders-btn');
        if (refreshBtn) refreshBtn.classList.add('animate-spin');

        try {
            // Check if backup is configured
            const response = await fetch('/api/backup/path');
            const data = await response.json();

            const foldersList = document.getElementById('backup-folders-list');
            if (!foldersList) return;

            // Clear current list
            foldersList.innerHTML = '';

            if (data.success && data.device_configured && data.exists) {
                // Fetch backup folders
                const foldersResponse = await fetch('/api/backup/files?path=');
                const foldersData = await foldersResponse.json();

                if (foldersData.success && foldersData.items && foldersData.items.length > 0) {
                    // Filter only folders and sort alphanumerically
                    const folders = foldersData.items
                    .filter(item => item.type === 'folder')
                    .sort((a, b) => {
                        // Case-insensitive alphanumeric sort
                        return a.name.localeCompare(b.name, undefined, {
                            sensitivity: 'base',
                            numeric: true
                        });
                    });

                    this.backupFolders = folders;

                    if (this.backupFolders.length > 0) {
                        this.backupFolders.forEach(folder => {
                            const a = document.createElement('a');
                            a.href = '#';
                            a.className = 'backup-folder-link flex items-center gap-2 px-2 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50 rounded-md transition-colors cursor-pointer';
                            a.setAttribute('data-folder-path', folder.path);
                            a.setAttribute('data-folder-name', folder.name);
                            a.title = `Open ${folder.name} in backup`;

                            const iconSpan = document.createElement('span');
                            iconSpan.className = 'material-icons-round text-lg';
                            iconSpan.textContent = this.getFolderIcon(folder.name);

                            const nameSpan = document.createElement('span');
                            nameSpan.className = 'truncate';
                            nameSpan.textContent = folder.name;
                            nameSpan.title = folder.name;

                            a.appendChild(iconSpan);
                            a.appendChild(nameSpan);
                            foldersList.appendChild(a);
                        });
                    } else {
                        const emptyDiv = document.createElement('div');
                        emptyDiv.className = 'px-2 py-1.5 text-sm text-gray-500 dark:text-gray-400 italic';
                        emptyDiv.textContent = 'No folders in backup';
                        foldersList.appendChild(emptyDiv);
                    }
                } else {
                    const emptyDiv = document.createElement('div');
                    emptyDiv.className = 'px-2 py-1.5 text-sm text-gray-500 dark:text-gray-400 italic';
                    emptyDiv.textContent = 'No backup files found';
                    foldersList.appendChild(emptyDiv);
                }
            } else {
                const emptyDiv = document.createElement('div');
                emptyDiv.className = 'px-2 py-1.5 text-sm text-gray-500 dark:text-gray-400 italic';
                emptyDiv.textContent = 'No backup device configured';
                foldersList.appendChild(emptyDiv);
            }

            // After rendering, check if we should highlight any folder
            const selectedFolder = sessionStorage.getItem('selectedBackupFolder');
            if (selectedFolder) {
                try {
                    const folder = JSON.parse(selectedFolder);
                    const currentPage = window.location.hash || '#dashboard';
                    if (currentPage.includes('folders')) {
                        this.highlightSelectedBackupFolder(folder.path);
                    } else {
                        // Clear it if we're not on folders page
                        sessionStorage.removeItem('selectedBackupFolder');
                    }
                } catch (e) {
                    sessionStorage.removeItem('selectedBackupFolder');
                }
            }

            console.log('Backup folders refreshed successfully');
        } catch (error) {
            console.error('Error refreshing backup folders:', error);
            showError('Failed to refresh backup folders', 'error');
        } finally {
            if (refreshBtn) refreshBtn.classList.remove('animate-spin');
        }
    }

    async refreshDevices() {
        const locationsSection = document.getElementById('locations-section');
        if (!locationsSection) return;

        const refreshBtn = locationsSection.querySelector('.refresh-btn');
        if (refreshBtn) refreshBtn.classList.add('animate-spin');

        try {
            // Fetch devices from the API
            const resp = await fetch('/api/locations/sidebar-devices');
            const data = await resp.json();

            const devicesList = document.getElementById('devices-list');
            if (!devicesList) return;

            // Clear current list
            devicesList.innerHTML = '';

            if (data.success && data.devices && data.devices.length > 0) {
                this.devices = data.devices;

                // Create SIMPLE device links
                this.devices.forEach(device => {
                    const a = document.createElement('a');
                    a.href = '#';
                    a.setAttribute('data-action', 'select-device');
                    a.setAttribute('data-device-mountpoint', device.mountpoint);
                    a.setAttribute('data-device-name', device.name);
                    a.title = `Configure backup for ${device.name}`;

                    // All devices get consistent styling - NO automatic highlighting
                    a.className = 'flex items-center justify-between px-2 py-1.5 text-sm rounded-md transition-colors cursor-pointer text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50';

                    const left = document.createElement('div');
                    left.className = 'flex items-center gap-2';

                    const iconSpan = document.createElement('span');
                    iconSpan.className = 'material-icons-round text-lg';
                    iconSpan.textContent = device.icon || 'storage';

                    const nameSpan = document.createElement('span');
                    // Add "(Backup)" label for backup device but keep styling consistent
                    const displayName = device.is_current_backup
                    ? `${device.display_name || device.name} (Backup)`
                    : device.display_name || device.name;
                    nameSpan.textContent = displayName;

                    left.appendChild(iconSpan);
                    left.appendChild(nameSpan);
                    a.appendChild(left);

                    // ADD EJECT BUTTON ON RIGHT SIDE (only for removable devices)
                    const rightDiv = document.createElement('div');
                    rightDiv.className = 'flex items-center';

                    if (device.is_removable && device.is_current_backup) { // Only show eject if removable AND is current backup
                        const ejectBtn = document.createElement('button');
                        ejectBtn.className = 'material-icons-round text-sm text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300 eject-btn p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700';
                        ejectBtn.setAttribute('data-mountpoint', device.mountpoint);
                        ejectBtn.setAttribute('data-device-name', device.name);
                        ejectBtn.title = `Eject ${device.name}`;
                        ejectBtn.textContent = 'eject';
                        ejectBtn.addEventListener('click', (ev) => {
                            ev.stopPropagation();
                            ev.preventDefault();
                            this.ejectDevice(device.mountpoint, device.name);
                        });
                        rightDiv.appendChild(ejectBtn);
                    }

                    a.appendChild(rightDiv);

                    devicesList.appendChild(a);
                });
            } else {
                this.devices = [];
                const emptyDiv = document.createElement('div');
                devicesList.appendChild(emptyDiv);
            }

            // Always include the Network option at the end
            const net = document.createElement('a');
            net.href = '#';
            net.className = 'flex items-center gap-2 px-2 py-1.5 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700/50 rounded-md transition-colors cursor-pointer';
            net.innerHTML = '<span class="material-icons-round text-lg">public</span>Network';
            devicesList.appendChild(net);

            // After rendering devices, check if we should highlight any
            // Only highlight if there's a selected device in sessionStorage AND we're on locations page
            const selectedDevice = sessionStorage.getItem('selectedDevice');
            if (selectedDevice) {
                try {
                    const device = JSON.parse(selectedDevice);
                    const currentPage = window.location.hash || '#dashboard';
                    // Only apply highlight if we're actually on a locations/device-related page
                    if (currentPage.includes('location')) {
                        this.highlightSelectedDevice(device.mountpoint);
                    } else {
                        // Clear it if we're not on locations page
                        sessionStorage.removeItem('selectedDevice');
                    }
                } catch (e) {
                    sessionStorage.removeItem('selectedDevice');
                }
            }

            console.log('Devices refreshed successfully');
        } catch (error) {
            console.error('Error refreshing devices:', error);
            showError('Failed to refresh devices', 'error');
        } finally {
            if (refreshBtn) refreshBtn.classList.remove('animate-spin');
        }
    }

    highlightSelectedBackupFolder(folderPath) {
        // Clear ALL highlights - nav items, backup folders, and devices
        document.querySelectorAll('[data-route]').forEach(el => {
            el.classList.remove('sidebar-item-active', 'font-medium');
            el.classList.add('text-gray-700', 'dark:text-gray-300');
        });
        document.querySelectorAll('.backup-folder-link').forEach(el => {
            el.classList.remove('sidebar-item-active', 'font-medium');
            el.classList.add('text-gray-700', 'dark:text-gray-300');
        });
        document.querySelectorAll('[data-action="select-device"]').forEach(el => {
            el.classList.remove('sidebar-item-active', 'font-medium');
            el.classList.add('text-gray-700', 'dark:text-gray-300');
        });

        // Highlight selected backup folder
        const selectedFolder = document.querySelector(`[data-folder-path="${folderPath}"]`);
        if (selectedFolder) {
            selectedFolder.classList.remove('text-gray-700', 'dark:text-gray-300', 'hover:bg-gray-200', 'dark:hover:bg-gray-700/50');
            selectedFolder.classList.add('sidebar-item-active', 'font-medium');
        }
    }

    highlightSelectedDevice(mountpoint) {
        // Clear ALL highlights - nav items, backup folders, and devices
        document.querySelectorAll('[data-route]').forEach(el => {
            el.classList.remove('sidebar-item-active', 'font-medium');
            el.classList.add('text-gray-700', 'dark:text-gray-300');
        });
        document.querySelectorAll('.backup-folder-link').forEach(el => {
            el.classList.remove('sidebar-item-active', 'font-medium');
            el.classList.add('text-gray-700', 'dark:text-gray-300');
        });
        document.querySelectorAll('[data-action="select-device"]').forEach(el => {
            el.classList.remove('sidebar-item-active', 'font-medium');
            el.classList.add('text-gray-700', 'dark:text-gray-300');
        });

        // Highlight selected device with consistent sidebar styling
        const selectedDevice = document.querySelector(`[data-device-mountpoint="${mountpoint}"]`);
        if (selectedDevice) {
            selectedDevice.classList.remove('text-gray-700', 'dark:text-gray-300', 'hover:bg-gray-200', 'dark:hover:bg-gray-700/50');
            selectedDevice.classList.add('sidebar-item-active', 'font-medium');
        }
    }

    async ejectDevice(mountpoint, deviceName) {
        // Use the new showConfirm dialog
        const shouldEject = await showConfirm(
            'Eject Device',
            `Eject "${deviceName}" from ${mountpoint}?\n\nMake sure no files are being accessed from this device.`,
            {
                confirmText: 'Eject',
                cancelText: 'Cancel',
                confirmType: 'danger'
            }
        );

        if (!shouldEject) {
            return;
        }

        try {
            showInfo(`Ejecting ${deviceName}...`, 'info');

            const response = await fetch('/api/locations/eject-device', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mountpoint: mountpoint })
            });

            const data = await response.json();

            if (data.success) {
                showToast(`${deviceName} ejected successfully`, 'success');

                // If ejected device was selected, clear it from sessionStorage
                const storedDevice = sessionStorage.getItem('selectedDevice');
                if (storedDevice) {
                    const parsedDevice = JSON.parse(storedDevice);
                    if (parsedDevice.mountpoint === mountpoint) {
                        sessionStorage.removeItem('selectedDevice');
                    }
                }

                // Dispatch BOTH events:
                // 1. device-ejected for locations page
                document.dispatchEvent(new CustomEvent('device-ejected', {
                    detail: {
                        mountpoint: mountpoint,
                        deviceName: deviceName,
                        wasBackupDevice: data.config_reset || false
                    }
                }));

                // 2. devices-updated for sidebar to refresh device list
                document.dispatchEvent(new CustomEvent('devices-updated'));

                // 3. Also refresh backup folders in case backup was on this device
                document.dispatchEvent(new CustomEvent('backup-configured'));
            } else {
                // If eject fails, refresh devices anyway to show current state
                await this.refreshDevices();
                document.dispatchEvent(new CustomEvent('locations-refresh-needed'));
                showError(`❌ Failed to eject: ${data.error || 'Unknown error'}`, 'error');
            }

        } catch (error) {
            showError(`❌ Error: ${error.message}`, 'error');
        }
    }

    handleNavigation(routeId, clickedElement) {
        // Update active state in sidebar FIRST - for BOTH navigation and settings
        this.navigation.forEach(item => {
            item.active = item.id === routeId;
        });

        this.settings.forEach(item => {
            item.active = item.id === routeId;
        });

        // Update UI immediately
        this.updateActiveStates();

        // Force immediate repaint
        void document.body.offsetHeight;

        // Clear selected device when navigating away from locations
        if (routeId !== 'locations') {
            sessionStorage.removeItem('selectedDevice');
            // Remove highlight from all devices
            document.querySelectorAll('[data-action="select-device"]').forEach(el => {
                el.classList.remove('sidebar-item-active', 'font-medium');
                el.classList.add('text-gray-700', 'dark:text-gray-300');
            });
        }

        // Clear selected backup folder when navigating away from folders
        if (routeId !== 'folders') {
            sessionStorage.removeItem('selectedBackupFolder');
            // Remove highlight from all backup folders
            document.querySelectorAll('.backup-folder-link').forEach(el => {
                el.classList.remove('sidebar-item-active', 'font-medium');
                el.classList.add('text-gray-700', 'dark:text-gray-300');
            });
        }

        // Dispatch custom event for app.js to handle page load (this happens AFTER visual updates)
        const event = new CustomEvent('route-change', {
            detail: { route: routeId },
            bubbles: true
        });

        if (clickedElement) {
            clickedElement.dispatchEvent(event);
        } else {
            document.dispatchEvent(event);
        }
    }

    updateActiveStates() {
        const navItems = document.querySelectorAll('[data-route]');
        navItems.forEach(item => {
            const routeId = item.getAttribute('data-route');

            // Check if this route is active in either navigation or settings arrays
            const navItem = this.navigation.find(nav => nav.id === routeId);
            const settingItem = this.settings.find(setting => setting.id === routeId);
            const isActive = (navItem && navItem.active) || (settingItem && settingItem.active);

            item.classList.remove('sidebar-item-active', 'font-medium');
            item.classList.add('text-gray-700', 'dark:text-gray-300', 'hover:bg-gray-200', 'dark:hover:bg-gray-700/50');

            if (isActive) {
                item.classList.remove('text-gray-700', 'dark:text-gray-300', 'hover:bg-gray-200', 'dark:hover:bg-gray-700/50');
                item.classList.add('sidebar-item-active', 'font-medium');
            }
        });
    }

    setActiveRoute(routeId) {
        this.navigation.forEach(item => {
            item.active = item.id === routeId;
        });
        this.settings.forEach(item => {
            item.active = item.id === routeId;
        });
        this.updateActiveStates();
    }

    showProfileMenu(buttonElement) {
        console.log('Show profile menu');

        // Create profile menu
        const menu = document.createElement('div');
        menu.className = 'fixed bg-white dark:bg-gray-800 shadow-lg rounded-md border border-gray-200 dark:border-gray-700 py-1 z-50';
        menu.style.right = '20px';
        menu.style.bottom = '20px';

        menu.innerHTML = `
        <button class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
        <span class="material-icons-round text-sm">account_circle</span>
        Profile Settings
        </button>
        <button class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2">
        <span class="material-icons-round text-sm">notifications</span>
        Notifications
        </button>
        <div class="h-px bg-gray-100 dark:bg-gray-700 my-1 mx-4"></div>
        <button class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 dark:hover:bg-gray-700 flex items-center gap-2 text-red-600">
        <span class="material-icons-round text-sm">logout</span>
        Sign Out
        </button>
        `;

        document.body.appendChild(menu);

        // Close menu when clicking elsewhere
        const closeMenu = (e) => {
            if (!menu.contains(e.target) && e.target !== buttonElement) {
                menu.remove();
                document.removeEventListener('click', closeMenu);
            }
        };

        setTimeout(() => {
            document.addEventListener('click', closeMenu);
        }, 0);

        // Handle menu actions
        menu.addEventListener('click', (e) => {
            const button = e.target.closest('button');
            if (button) {
                const action = button.textContent.trim();
                this.handleProfileAction(action);
                menu.remove();
            }
        });
    }

    handleProfileAction(action) {
        switch(action) {
            case 'Profile Settings':
                console.log('Opening profile settings');
                break;
            case 'Notifications':
                console.log('Opening notifications');
                break;
            case 'Sign Out':
                console.log('Signing out');
                if (confirm('Are you sure you want to sign out?')) {
                    window.location.href = '/login'; // Redirect to login page
                }
                break;
        }
    }

    showNotification(message, type = 'info') {
        // Simple notification implementation
        const notification = document.createElement('div');
        notification.className = `fixed bottom-4 right-4 px-4 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2 ${
            type === 'success' ? 'bg-green-100 text-green-800 border border-green-200 dark:bg-green-900/30 dark:text-green-300 dark:border-green-800' :
            type === 'error' ? 'bg-red-100 text-red-800 border border-red-200 dark:bg-red-900/30 dark:text-red-300 dark:border-red-800' :
            'bg-blue-100 text-blue-800 border border-blue-200 dark:bg-blue-900/30 dark:text-blue-300 dark:border-blue-800'
        }`;

        notification.innerHTML = `
        <span class="material-icons-round text-sm">
        ${type === 'success' ? 'check_circle' :
            type === 'error' ? 'error' :
            'info'}
            </span>
            <span>${message}</span>
            `;

            document.body.appendChild(notification);

            // Auto-remove after 3 seconds
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 3000);
    }
}

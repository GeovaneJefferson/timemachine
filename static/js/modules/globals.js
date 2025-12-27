/**
 * @file globals.js
 * @description Global state, constants, and shared variables
 */

// =====================================================================
// --- GLOBAL STATE & CONSTANTS ---
// =====================================================================

const MAX_TRANSFER_ITEMS = 10;

const state = {
    userPlan: 'pro',
    username: 'User',
    isDeviceConnected: false,
    activeSettingsTab: 'folders',
    currentTabId: 'overview',
    currentFolder: null,
    selectedFile: null,
    currentEditCat: null,
    selectedSource: null,
    fileSystem: null,
    pendingAction: null,
    timeStampInterval: null,
    breadcrumbStack: [],
    migSelectionState: { home: false, flatpaks: false, installers: false },
    homeFolders: [],
    deviceData: []
};

const generalSettings = {
    autoStartup: false,
    autoUpdates: true,
    showNotifications: true
};

// DOM Elements cache - with fallback to empty objects if not found
// In globals.js, update the elements object:
export const elements = {
    // Remove this line: backupLocation: null,
    backupUsage: null,
    backupUsagePercent: null,
    backupLocationPath: null,
    filesImagesCount: null,
    filesVideosCount: null,
    filesDocumentsCount: null,
    filesOtherCount: null,
    filesImagesSize: null,
    filesVideosSize: null,
    filesDocumentsSize: null,
    filesOtherSize: null,
    fileSearchInput: null,
    devicesContainer: null
};

// And update initElements to remove the reference:
export function initElements() {
    const getElement = (id) => {
        const el = document.getElementById(id);
        if (!el) console.warn(`Element with id "${id}" not found`);
        return el;
    };

    // Remove this line: elements.backupLocation = getElement('backupLocation');
    elements.backupUsage = getElement('backup-usage');
    elements.backupUsagePercent = getElement('backup-usage-percent');
    elements.backupLocationPath = getElement('backup-location-path');
    elements.filesImagesCount = getElement('files-images-count');
    elements.filesVideosCount = getElement('files-videos-count');
    elements.filesDocumentsCount = getElement('files-documents-count');
    elements.filesOtherCount = getElement('files-others-count');
    elements.filesImagesSize = getElement('files-images-size');
    elements.filesVideosSize = getElement('files-videos-size');
    elements.filesDocumentsSize = getElement('files-documents-size');
    elements.filesOtherSize = getElement('files-others-size');
    elements.fileSearchInput = getElement('file-search-input');
    elements.devicesContainer = getElement('device-list-container');

    console.log('Elements initialized:', Object.keys(elements).filter(key => elements[key] !== null));
}

// Migration data
export const migrationData = {
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

export { MAX_TRANSFER_ITEMS, state, generalSettings };

/**
 * Centralized API communication layer
 */

export class ApiClient {
    constructor() {
        this.baseUrl = '';
        this.defaultHeaders = {
            'Content-Type': 'application/json'
        };
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: { ...this.defaultHeaders, ...options.headers },
            ...options
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            // Handle 204 No Content
            if (response.status === 204) {
                return null;
            }

            const data = await response.json();

            // Check for API-specific success flag
            if (data.hasOwnProperty('success') && !data.success) {
                throw new Error(data.error || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error(`[API] ${endpoint} failed:`, error);
            throw error;
        }
    }

    // File operations
    async getFileInfo(filePath) {
        return this.request('/api/file-info', {
            method: 'POST',
            body: JSON.stringify({ file_path: filePath })
        });
    }

    async getFileVersions(filePath) {
        return this.request(`/api/file-versions?file_path=${encodeURIComponent(filePath)}`);
    }

    async restoreFile(backupPath, restoreType = 'original') {
        return this.request('/api/restore-file', {
            method: 'POST',
            body: JSON.stringify({
                file_path: backupPath,
                restore_to: restoreType
            })
        });
    }

    async searchFiles(query) {
        return this.request(`/api/search?query=${encodeURIComponent(query)}`);
    }

    async searchMovedFile(backupPath, fastSearch = true) {
        return this.request('/api/search-moved-file', {
            method: 'POST',
            body: JSON.stringify({
                file_path: backupPath,
                fast_search: fastSearch
            })
        });
    }

    // Device operations
    async getDevices() {
        return this.request('/api/storage/devices');
    }

    async selectDevice(deviceInfo) {
        return this.request('/api/backup/select-device', {
            method: 'POST',
            body: JSON.stringify({ device_info: deviceInfo })
        });
    }

    async checkConnection() {
        return this.request('/api/backup/connection');
    }

    async getBackupUsage() {
        return this.request('/api/backup/usage');
    }

    // Migration operations
    async getMigrationSources() {
        return this.request('/api/migration/sources');
    }

    // Settings operations
    async getBackupFolders() {
        return this.request('/api/backup-folders');
    }

    async saveBackupFolders(folders) {
        return this.request('/api/backup-folders', {
            method: 'POST',
            body: JSON.stringify({ folders })
        });
    }

    async getConfig() {
        return this.request('/api/config');
    }

    // Daemon operations
    async getDaemonStatus() {
        return this.request('/api/daemon/ready-status');
    }

    async startDaemon() {
        return this.request('/api/daemon/start', {
            method: 'POST'
        });
    }

    async stopDaemon(mode = 'graceful') {
        return this.request('/api/backup/cancel', {
            method: 'POST',
            body: JSON.stringify({ mode })
        });
    }

    // File system operations
    async initFileSearch() {
        return this.request('/api/search/init', {
            method: 'POST'
        });
    }

    async getFolderContents(path = '') {
        return this.request(`/api/search/folder?path=${encodeURIComponent(path)}`);
    }

    // System operations
    async openFile(path) {
        return this.request('/api/open-file', {
            method: 'POST',
            body: JSON.stringify({ file_path: path })
        });
    }

    async openLocation(path) {
        return this.request('/api/open-location', {
            method: 'POST',
            body: JSON.stringify({ file_path: path })
        });
    }
}

// preload.js runs in a special, sandboxed renderer environment where CommonJS
// `require` is guaranteed to work.  We used ESM before which caused the preload
// loader to fail with "Unable to load preload script" when installed, so switch
// back to a simple CommonJS style.

const { contextBridge, ipcRenderer } = require('electron');

/**
 * Exposed API for the renderer process
 * This provides a secure bridge between the frontend and Electron main process
 */
const api = {
  // API call proxy
  async apiCall(method, endpoint, data = null) {
    return ipcRenderer.invoke('api-call', method, endpoint, data);
  },

  // Convenience methods for common HTTP verbs
  async get(endpoint) {
    return this.apiCall('GET', endpoint);
  },

  async post(endpoint, data) {
    return this.apiCall('POST', endpoint, data);
  },

  async put(endpoint, data) {
    return this.apiCall('PUT', endpoint, data);
  },

  async delete(endpoint) {
    return this.apiCall('DELETE', endpoint);
  },

  // File operations
  async downloadFile(filePath, destinationPath) {
    return ipcRenderer.invoke('download-file', filePath, destinationPath);
  },

  // App window controls
  minimize() {
    return ipcRenderer.invoke('app-minimize');
  },

  maximize() {
    return ipcRenderer.invoke('app-maximize');
  },

  close() {
    return ipcRenderer.invoke('app-close');
  },

  toggleFullscreen() {
    return ipcRenderer.invoke('app-toggle-fullscreen');
  },

  // Platform info
  async getPlatformInfo() {
    return ipcRenderer.invoke('get-platform-info');
  },

  // Show notification
  showNotification(title, body) {
    return ipcRenderer.invoke('show-notification', title, body);
  },

  // Open a dedicated update window
  openUpdateWindow() {
    return ipcRenderer.invoke('open-update-window');
  },

  // Quit entire application
  quit() {
    return ipcRenderer.invoke('app-quit');
  }
};

/**
 * Expose the API to the renderer process
 */
contextBridge.exposeInMainWorld('electronAPI', api);

console.log('Preload script loaded - electronAPI available');

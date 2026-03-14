/**
 * Electron API Adapter
 * Provides compatibility layer between web fetch API and Electron IPC
 * This allows the existing frontend code to work with minimal changes
 */

export class ElectronAPIAdapter {
  constructor() {
    this.isElectron = typeof window !== 'undefined' && window.electronAPI !== undefined;
  }

  /**
   * Perform an API call
   * @param {string} method - HTTP method (GET, POST, PUT, DELETE)
   * @param {string} endpoint - API endpoint (e.g., '/api/backup/path')
   * @param {object} data - Request data for POST/PUT
   * @returns {Promise<object>} Response data
   */
  async apiCall(method, endpoint, data = null) {
    if (!this.isElectron) {
      // Fallback to fetch for web version
      return this.fetchCall(method, endpoint, data);
    }

    try {
      const response = await window.electronAPI.apiCall(method, endpoint, data);
      return response;
    } catch (error) {
      console.error(`API call failed: ${method} ${endpoint}`, error);
      return {
        success: false,
        error: error.message || 'API call failed'
      };
    }
  }

  /**
   * Fallback fetch implementation for web version
   */
  async fetchCall(method, endpoint, data = null) {
    try {
      const options = {
        method,
        headers: {
          'Content-Type': 'application/json'
        }
      };

      if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
      }

      const response = await fetch(endpoint, options);
      const json = await response.json();
      return json;
    } catch (error) {
      console.error(`Fetch failed: ${method} ${endpoint}`, error);
      return {
        success: false,
        error: error.message || 'Fetch failed'
      };
    }
  }

  // Convenience methods for HTTP verbs
  get(endpoint) {
    return this.apiCall('GET', endpoint);
  }

  post(endpoint, data) {
    return this.apiCall('POST', endpoint, data);
  }

  put(endpoint, data) {
    return this.apiCall('PUT', endpoint, data);
  }

  delete(endpoint) {
    return this.apiCall('DELETE', endpoint);
  }

  // App window control helpers (bridge to preload API)
  minimize() {
    if (this.isElectron) {
      return window.electronAPI.minimize();
    }
  }

  maximize() {
    if (this.isElectron) {
      return window.electronAPI.maximize();
    }
  }

  close() {
    if (this.isElectron) {
      return window.electronAPI.close();
    }
  }

  toggleFullscreen() {
    if (this.isElectron) {
      return window.electronAPI.toggleFullscreen();
    }
  }

  /**
   * Open a dedicated update window (Electron only).
   */
  // Update window removed; updates are detected and shown via notification toasts.

  /**
   * Quit the entire application.
   */
  quit() {
    if (this.isElectron && window.electronAPI.quit) {
      return window.electronAPI.quit();
    }
  }

  /**
   * Set the application theme, synchronizing with Electron's nativeTheme.
   * @param {string} theme - 'light', 'dark', or 'system'
   */
  setTheme(theme) {
    if (this.isElectron && window.electronAPI.setTheme) {
      return window.electronAPI.setTheme(theme);
    }
  }

  /**
   * Get platform information
   */
  async getPlatformInfo() {
    if (!this.isElectron) {
      return { platform: 'web', isDev: false };
    }
    return window.electronAPI.getPlatformInfo();
  }

  /**
   * Show a system notification
   * @param {string} title - Notification title
   * @param {string} body - Notification body
   */
  showNotification(title, body) {
    if (this.isElectron) {
      window.electronAPI.showNotification(title, body);
    } else {
      // Fallback for web version
      alert(`${title}\n\n${body}`);
    }
  }

  /**
   * Check if running in Electron
   */
  isRunningInElectron() {
    return this.isElectron;
  }
}

// Export singleton instance
export const electronAPI = new ElectronAPIAdapter();

/**
 * Drop-in replacement for fetch in global scope
 * This allows existing code using fetch to work with Electron
 */
if (typeof window !== 'undefined') {
  window.apiAdapter = electronAPI;
}

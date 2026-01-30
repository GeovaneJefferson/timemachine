import { app, BrowserWindow, ipcMain, Menu } from 'electron';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';
import axios from 'axios';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Set app name for window title and taskbar
app.name = 'TimeMachine';

let mainWindow;
let pythonProcess;
const API_BASE_URL = 'http://localhost:5000';

/**
 * Start the Python Flask backend
 */
function startPythonBackend() {
  return new Promise((resolve, reject) => {
    const pythonScript = path.join(__dirname, 'backend.py');
    const pythonPath = process.env.PYTHON_PATH || 'python3';

    // Spawn the Python process
    pythonProcess = spawn(pythonPath, [pythonScript], {
      stdio: 'pipe',
      detached: true,
      env: {
        ...process.env,
        PYTHONUNBUFFERED: '1'
      }
    });

    pythonProcess.on('error', (err) => {
      console.error('Failed to start Python backend:', err);
      reject(err);
    });

    // Give Python time to start
    setTimeout(() => {
      checkBackendReady(resolve, reject);
    }, 2000);
  });
}

/**
 * Check if backend is responding
 */
function checkBackendReady(resolve, reject, attempts = 0) {
  if (attempts > 30) {
    reject(new Error('Backend failed to start'));
    return;
  }

  axios.get(`${API_BASE_URL}/api/system-info`, { timeout: 1000 })
    .then(() => {
      console.log('Backend is ready');
      resolve();
    })
    .catch(() => {
      setTimeout(() => checkBackendReady(resolve, reject, attempts + 1), 500);
    });
}

/**
 * Create the main application window
 */
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 800,
    minHeight: 600,
    title: 'TimeMachine',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      sandbox: true
    },
    icon: path.join(__dirname, '..', 'assets', 'icon.png')
  });

  // Always load from Flask backend
  const startUrl = 'http://localhost:5000';

  mainWindow.loadURL(startUrl);

  // Don't open dev tools by default
  // mainWindow.webContents.openDevTools();

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  return mainWindow;
}

/**
 * Setup IPC handlers for API communication
 */
function setupIPC() {
  // Generic API handler - proxy all /api calls to Flask backend
  ipcMain.handle('api-call', async (event, method, endpoint, data = null) => {
    try {
      const url = `${API_BASE_URL}${endpoint}`;
      const config = {
        timeout: 30000,
        validateStatus: () => true // Accept all status codes
      };

      let response;
      switch (method.toUpperCase()) {
        case 'GET':
          response = await axios.get(url, config);
          break;
        case 'POST':
          response = await axios.post(url, data, config);
          break;
        case 'PUT':
          response = await axios.put(url, data, config);
          break;
        case 'DELETE':
          response = await axios.delete(url, config);
          break;
        default:
          throw new Error(`Unsupported method: ${method}`);
      }

      return response.data;
    } catch (error) {
      console.error(`API call failed: ${method} ${endpoint}`, error);
      return {
        success: false,
        error: error.message
      };
    }
  });

  // File download handler
  ipcMain.handle('download-file', async (event, filePath, destinationPath) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/stream/file`, {
        params: { path: filePath },
        responseType: 'arraybuffer'
      });

      // Save file (this would be handled by the frontend using native APIs)
      return { success: true, data: response.data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  });

  // App control handlers
  ipcMain.handle('app-minimize', () => mainWindow?.minimize());
  ipcMain.handle('app-maximize', () => mainWindow?.maximize());
  ipcMain.handle('app-close', () => mainWindow?.close());
  ipcMain.handle('app-toggle-fullscreen', () => {
    if (mainWindow) {
      mainWindow.setFullScreen(!mainWindow.isFullScreen());
    }
  });

  // Platform info handler
  ipcMain.handle('get-platform-info', () => ({
    platform: process.platform,
    arch: process.arch,
    version: app.getVersion(),
    isDev
  }));
}

/**
 * Create application menu
 */
function createMenu() {
  const template = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Exit',
          accelerator: 'CmdOrCtrl+Q',
          click: () => {
            app.quit();
          }
        }
      ]
    },
    {
      label: 'Edit',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' }
      ]
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'About',
          click: () => {
            // Could open an about dialog
          }
        }
      ]
    }
  ];

  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

/**
 * Kill Python process on app quit
 */
function killPythonProcess() {
  if (pythonProcess) {
    try {
      // Kill process group on Unix-like systems
      if (process.platform !== 'win32') {
        process.kill(-pythonProcess.pid, 'SIGTERM');
        // Give it a moment, then force kill if needed
        setTimeout(() => {
          if (!pythonProcess.killed) {
            process.kill(-pythonProcess.pid, 'SIGKILL');
          }
        }, 1000);
      } else {
        // Windows
        process.kill(pythonProcess.pid);
      }
    } catch (e) {
      console.log('Python process already terminated');
    }
  }
}

/**
 * App lifecycle handlers
 */
app.on('ready', async () => {
  try {
    console.log('Starting TimeMachine...');
    await startPythonBackend();
    setupIPC();
    createWindow();
    createMenu();
  } catch (error) {
    console.error('Failed to start application:', error);
    app.quit();
  }
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  killPythonProcess();
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// Handle any uncaught exceptions
process.on('uncaughtException', (error) => {
  console.error('Uncaught exception:', error);
});

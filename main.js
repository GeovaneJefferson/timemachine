const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const net = require('net');
const os = require('os');

// === CRITICAL FIX: Set Name EARLY ===
// This must run before app.whenReady() to correctly set WM_CLASS on Linux
// so the window manager associates the window with the .desktop file and icon.
if (process.platform === 'linux') {
  app.setName('timemachine');
}

let mainWindow;
let flaskProcess;
let flaskPort;
const portFile = path.join(os.homedir(), '.timemachine.flask_port');
const lockFile = path.join(os.tmpdir(), 'timemachine.lock');

// === FIRST: Single Instance Lock (BEFORE anything else) ===
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  console.log('❌ Another instance detected. Exiting immediately.');
  process.exit(0);
}

// Handle second instance attempts
app.on('second-instance', () => {
  console.log('⚠️ Second instance blocked, focusing existing window...');
  if (mainWindow) {
    if (mainWindow.isMinimized()) mainWindow.restore();
    mainWindow.show();
    mainWindow.focus();
  }
});

// === SECOND: PID Lock File ===
function createLockFile() {
  try {
    if (fs.existsSync(lockFile)) {
      const oldPid = parseInt(fs.readFileSync(lockFile, 'utf8').trim());
      try {
        process.kill(oldPid, 0);
        console.log(`❌ Process ${oldPid} already running. Exiting.`);
        process.exit(0);
      } catch {
        console.log('🧹 Removing stale lock file...');
        fs.unlinkSync(lockFile);
      }
    }
    fs.writeFileSync(lockFile, process.pid.toString());
    console.log(`✅ Lock created (PID: ${process.pid})`);
  } catch (err) {
    console.error('Lock error:', err);
    process.exit(1);
  }
}

createLockFile();

// Cleanup lock on exit
const cleanupLock = () => {
  try {
    if (fs.existsSync(lockFile)) {
      const currentPid = parseInt(fs.readFileSync(lockFile, 'utf8'));
      if (currentPid === process.pid) {
        fs.unlinkSync(lockFile);
        console.log('🧹 Lock cleaned up');
      }
    }
  } catch (e) {
    // Ignore errors during cleanup
  }
};

process.on('exit', cleanupLock);
process.on('SIGINT', () => { cleanupLock(); process.exit(0); });
process.on('SIGTERM', () => { cleanupLock(); process.exit(0); });

// Electron optimizations
app.commandLine.appendSwitch('--no-sandbox');
app.commandLine.appendSwitch('--disable-dev-shm-usage');
app.commandLine.appendSwitch('--disable-gpu-sandbox');

function startFlask() {
  return new Promise((resolve, reject) => {
    console.log('🚀 Starting Flask...');
    
    // Delete old port file BEFORE starting Flask
    if (fs.existsSync(portFile)) {
      fs.unlinkSync(portFile);
      console.log('🗑️ Deleted old port file');
    }
    
    // Spawn Flask process
    flaskProcess = spawn('python3', ['app.py', '--port', '0'], {
      cwd: __dirname,
      stdio: ['ignore', 'pipe', 'pipe'],
      detached: false
    });

    let resolved = false;

    // Listen for Flask output to know when it's ready
    flaskProcess.stdout.on('data', (data) => {
      const output = data.toString();
      if ((output.includes('Running on') || output.includes('Starting Time Machine')) && !resolved) {
        resolved = true;
        console.log('✅ Flask starting...');
        resolve();
      }
    });

    flaskProcess.stderr.on('data', (data) => {
      const output = data.toString();
      if ((output.includes('Running on') || output.includes('Starting Time Machine')) && !resolved) {
        resolved = true;
        console.log('✅ Flask starting...');
        resolve();
      }
    });

    flaskProcess.on('error', (error) => {
      if (!resolved) {
        console.error('❌ Flask start error:', error);
        reject(error);
      }
    });

    // Fallback timeout
    setTimeout(() => {
      if (!resolved) {
        console.log('⏰ Timeout waiting for Flask');
        resolve();
      }
    }, 5000);
  });
}

async function waitForPortFile(maxAttempts = 30) {
  console.log('📄 Waiting for Flask port file...');
  
  for (let i = 0; i < maxAttempts; i++) {
    if (fs.existsSync(portFile)) {
      try {
        const port = parseInt(fs.readFileSync(portFile, 'utf8').trim());
        if (port > 0 && port < 65536) {
          console.log(`✅ Port file found: ${port}`);
          return port;
        }
      } catch (e) {
        console.log(`⚠️ Port file corrupt, retrying... (${i + 1}/${maxAttempts})`);
      }
    }
    
    if (i < maxAttempts - 1) {
      await new Promise(resolve => setTimeout(resolve, 200));
    }
  }
  
  console.log('❌ Port file never appeared');
  return null;
}

async function checkFlaskReady(port, maxAttempts = 20) {
  console.log(`🔍 Checking Flask on port ${port}...`);
  
  for (let i = 0; i < maxAttempts; i++) {
    try {
      const isReady = await new Promise((resolve) => {
        const client = net.createConnection({ port, host: '127.0.0.1' }, () => {
          client.end();
          resolve(true);
        });
        
        client.on('error', () => resolve(false));
        client.setTimeout(300);
        client.on('timeout', () => {
          client.destroy();
          resolve(false);
        });
      });
      
      if (isReady) {
        console.log(`✅ Flask ready on port ${port}`);
        return true;
      }
    } catch (e) {
      // Continue trying
    }
    
    if (i < maxAttempts - 1) {
      await new Promise(resolve => setTimeout(resolve, 300));
    }
  }
  
  return false;
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: path.join(__dirname, 'icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: false
    },
    autoHideMenuBar: true,
    title: 'TimeMachine Backup',
    show: false, // Don't show until ready-to-show
    backgroundColor: '#1e293b'
  });

  const loadingHtml = path.join(__dirname, 'loading.html');
  mainWindow.loadFile(loadingHtml);

  mainWindow.once('ready-to-show', () => {
    console.log('✅ Window ready');
    mainWindow.show();
    mainWindow.focus();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

async function initializeApp() {
  try {
    // Start Flask
    await startFlask();
    
    // Wait for Flask to write port file
    flaskPort = await waitForPortFile(30);
    
    if (!flaskPort) {
      console.error('❌ Could not read Flask port');
      const errorHtml = path.join(__dirname, 'error.html');
      mainWindow.loadFile(errorHtml);
      return;
    }
    
    // Wait for Flask to be ready
    const isReady = await checkFlaskReady(flaskPort, 20);
    
    if (isReady) {
      console.log(`✅ Loading app from http://127.0.0.1:${flaskPort}`);
      mainWindow.loadURL(`http://127.0.0.1:${flaskPort}`);
    } else {
      console.error('❌ Flask not responding');
      const errorHtml = path.join(__dirname, 'error.html');
      mainWindow.loadFile(errorHtml);
    }

  } catch (error) {
    console.error('❌ Init error:', error);
    const errorHtml = path.join(__dirname, 'error.html');
    mainWindow.loadFile(errorHtml);
  }
}

app.whenReady().then(() => {
  createWindow();
  initializeApp();
});

app.on('window-all-closed', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
  
  if (fs.existsSync(portFile)) {
    fs.unlinkSync(portFile);
  }
  
  cleanupLock();
  app.quit();
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('before-quit', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
});
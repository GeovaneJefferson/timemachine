const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const net = require('net');
const os = require('os'); 

// =========================================================================
// CRITICAL FIX: SINGLE INSTANCE LOCK
app.setName('TimeMachineBackup'); 
if (process.platform === 'win32') {
    app.setAppUserModelId('com.geovane.timemachine'); 
}

const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
    console.log('Another instance is already running. Exiting.');
    app.quit();
    process.exit(0); // Force exit
}

app.on('second-instance', (event, commandLine, workingDirectory) => {
    console.log('Second instance attempted to start');
    if (mainWindow) {
        if (mainWindow.isMinimized()) mainWindow.restore();
        mainWindow.focus();
    }
});
// =========================================================================

app.commandLine.appendSwitch('no-sandbox');
app.disableHardwareAcceleration();

let mainWindow = null;
let flaskProcess = null;
let flaskPort = null; 
let flaskStarted = false; // CRITICAL: Prevent multiple Flask starts

// Simple loading HTML
const SIMPLE_LOADING_HTML = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Time Machine - Loading</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid rgba(255,255,255,0.3);
            border-top: 5px solid white;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .status {
            margin-top: 20px;
            font-size: 1.1em;
            opacity: 0.9;
        }
    </style>
</head>
<body>
    <h1>🕰️ Time Machine</h1>
    <p>Starting backup application...</p>
    <div class="spinner"></div>
    <div class="status" id="status">Initializing...</div>
    
    <script>
        const messages = [
            "Starting Flask server...",
            "Loading modules...",
            "Initializing database...",
            "Almost ready..."
        ];
        let idx = 0;
        const statusEl = document.getElementById('status');
        setInterval(() => {
            statusEl.textContent = messages[idx];
            idx = (idx + 1) % messages.length;
        }, 2000);
    </script>
</body>
</html>`;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 800,
        minWidth: 1400,
        minHeight: 800,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
        },
        icon: path.join(__dirname, 'static/vendor/favicon.png')
    });

    mainWindow.setTitle('Time Machine');
    mainWindow.on('closed', () => {
        mainWindow = null;
    });

    // Show loading screen
    const loadingPath = path.join(__dirname, 'loading.html');
    if (fs.existsSync(loadingPath)) {
        mainWindow.loadFile('loading.html');
    } else {
        mainWindow.loadURL(`data:text/html,${encodeURIComponent(SIMPLE_LOADING_HTML)}`);
    }
}

function checkPort(port) {
    return new Promise((resolve) => {
        const socket = new net.Socket();
        socket.setTimeout(1000);
        
        socket.on('connect', () => {
            socket.destroy();
            resolve(true);
        });
        
        socket.on('timeout', () => {
            socket.destroy();
            resolve(false);
        });
        
        socket.on('error', () => {
            resolve(false);
        });
        
        socket.connect(port, '127.0.0.1');
    });
}

async function waitForFlask(port, maxAttempts = 30) {
    for (let i = 0; i < maxAttempts; i++) {
        console.log(`Waiting for Flask on port ${port}... (${i + 1}/${maxAttempts})`);
        
        if (await checkPort(port)) {
            console.log(`✅ Flask is ready on port ${port}`);
            return true;
        }
        
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    console.log(`❌ Flask failed to start on port ${port}`);
    return false;
}

function startFlask() {
    // CRITICAL: Prevent multiple Flask instances
    if (flaskStarted) {
        console.log('⚠️ Flask already started, ignoring duplicate call');
        return;
    }
    
    flaskStarted = true;
    console.log('Starting Flask server...');

    flaskProcess = spawn('python3', ['app.py', '--port', '0'], {
        cwd: __dirname,
        stdio: ['ignore', 'pipe', 'pipe']
    });

    let appLoaded = false;
    let portDetected = false;
    
    flaskProcess.stdout.on('data', (data) => {
        const msg = data.toString().trim();
        console.log(`Flask stdout: ${msg}`);
        
        // Try to detect port from Flask output
        if (!portDetected) {
            const portMatch = msg.match(/Running on.*?:(\d{4,5})/);
            if (portMatch) {
                flaskPort = parseInt(portMatch[1]);
                portDetected = true;
                console.log(`✅ Detected Flask port from output: ${flaskPort}`);
            }
        }
        
        // Try to read port from file
        if (!portDetected) {
            const portFile = path.join(os.homedir(), '.timemachine.flask_port');
            if (fs.existsSync(portFile)) {
                try {
                    flaskPort = parseInt(fs.readFileSync(portFile, 'utf8').trim());
                    portDetected = true;
                    console.log(`✅ Read Flask port from file: ${flaskPort}`);
                } catch (e) {
                    console.error('Failed to read port file:', e);
                }
            }
        }
        
        // Load app once we have port and Flask is ready
        if (portDetected && !appLoaded && (msg.includes('Running on') || msg.includes('Serving Flask'))) {
            appLoaded = true;
            console.log('🚀 Flask reported ready, loading app...');
            
            setTimeout(async () => {
                if (await waitForFlask(flaskPort)) {
                    if (mainWindow) {
                        console.log(`✅ Loading app from http://127.0.0.1:${flaskPort}`);
                        mainWindow.loadURL(`http://127.0.0.1:${flaskPort}`).catch(err => {
                            console.error('Failed to load app:', err);
                        });
                    }
                } else {
                    if (mainWindow) {
                        mainWindow.loadURL(`data:text/html,${encodeURIComponent(`
                            <h1>Failed to Load App</h1>
                            <p>Flask reported port ${flaskPort} but is unreachable.</p>
                            <p>Check console for Python errors.</p>
                            <button onclick="location.reload()">Retry</button>
                        `)}`);
                    }
                }
            }, 1000);
        }
    });

    flaskProcess.stderr.on('data', (data) => {
        const msg = data.toString().trim();
        
        if (msg) {
            if (msg.startsWith('INFO:werkzeug') || msg.startsWith('INFO:app')) {
                console.log(`Flask info: ${msg}`);
            } else {
                console.error(`Flask error: ${msg}`);
            }
        }
        
        // Handle port conflict
        if (msg.includes('Address already in use') && !appLoaded) {
            appLoaded = true;
            if (mainWindow) {
                mainWindow.loadURL(`data:text/html,${encodeURIComponent(`
                    <h1>Startup Error</h1>
                    <p>Port conflict: A required port is already in use.</p>
                    <p>Please close the other application or restart Time Machine.</p>
                    <button onclick="location.reload()">Retry</button>
                `)}`);
            }
        }
    });

    flaskProcess.on('exit', (code) => {
        console.log(`Flask process exited with code ${code}`);
        flaskStarted = false; // Allow restart if needed
        
        if (code !== 0 && !appLoaded && mainWindow) {
            appLoaded = true;
            mainWindow.loadURL(`data:text/html,${encodeURIComponent(`
                <h1>Startup Failed</h1>
                <p>The Flask server exited unexpectedly (Code ${code}).</p>
                <p>Check console for details.</p>
                <button onclick="location.reload()">Retry</button>
            `)}`);
        }
    });
    
    // Timeout fallback
    setTimeout(() => {
        if (!appLoaded && mainWindow) {
            appLoaded = true;
            mainWindow.loadURL(`data:text/html,${encodeURIComponent(`
                <h1>Timeout Error</h1>
                <p>Flask failed to launch within 15 seconds.</p>
                <p>Check Python installation and dependencies.</p>
                <button onclick="location.reload()">Retry</button>
            `)}`);
        }
    }, 15000);
}

app.on('ready', () => {
    console.log('Electron app ready');
    createWindow();
    startFlask();
});

app.on('window-all-closed', () => {
    console.log('All windows closed');
    if (flaskProcess) {
        console.log('Killing Flask process...');
        flaskProcess.kill('SIGTERM');
        
        // Force kill after 2 seconds if still alive
        setTimeout(() => {
            if (flaskProcess) {
                flaskProcess.kill('SIGKILL');
            }
        }, 2000);
    }
    app.quit();
});

app.on('before-quit', () => {
    console.log('App quitting, cleaning up...');
    
    // Clean up port file
    const portFile = path.join(os.homedir(), '.timemachine.flask_port');
    if (fs.existsSync(portFile)) {
        try {
            fs.unlinkSync(portFile);
            console.log('Deleted port file');
        } catch (e) {
            console.error('Failed to delete port file:', e);
        }
    }
    
    // Clean up socket file
    const socketFile = '/tmp/timemachine_socket.sock';
    if (fs.existsSync(socketFile)) {
        try {
            fs.unlinkSync(socketFile);
            console.log('Deleted socket file');
        } catch (e) {
            console.warn('Failed to delete socket file:', e);
        }
    }
});
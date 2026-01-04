const { app, BrowserWindow, screen, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const { autoUpdater } = require('electron-updater');
const https = require('https');
const fs = require('fs');
const os = require('os');

const isDev = process.env.NODE_ENV === 'development';

let mainWindow;
let pythonProcess;

function createWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    mainWindow = new BrowserWindow({
        width: Math.min(1280, width),
        height: Math.min(800, height),
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false, // For simple MVP local communication
            webSecurity: false // Allow local fetching if needed
        },
        // Icon path would go here
        titleBarStyle: 'hidden', // Custom title bar style if we wanted
        backgroundColor: '#020617',
        show: false // Wait for ready-to-show
    });

    // Load the app
    if (isDev) {
        mainWindow.loadURL('http://localhost:5173');
        mainWindow.webContents.openDevTools({ mode: 'detach' });
    } else {
        mainWindow.loadFile(path.join(__dirname, 'dist', 'index.html'));
    }

    mainWindow.once('ready-to-show', () => {
        mainWindow.show();
        if (!isDev) {
            autoUpdater.checkForUpdatesAndNotify();
        }
    });

    mainWindow.on('closed', () => (mainWindow = null));

    // IPC Handlers for Window Controls
    ipcMain.on('window-minimize', () => mainWindow.minimize());
    ipcMain.on('window-maximize', () => {
        if (mainWindow.isMaximized()) {
            mainWindow.unmaximize();
        } else {
            mainWindow.maximize();
        }
    });
    ipcMain.on('window-close', () => mainWindow.close());
    ipcMain.on('app-is-maximized', (event) => {
        event.returnValue = mainWindow.isMaximized();
    });

    ipcMain.on('update-app', (event, { url }) => {
        console.log(`Downloading update from: ${url}`);
        const tempPath = path.join(os.tmpdir(), 'ColdEmailReachSetup_Update.exe');

        const downloadFile = (downloadUrl) => {
            https.get(downloadUrl, (response) => {
                // Handle Redirects
                if (response.statusCode === 301 || response.statusCode === 302) {
                    console.log(`Redirecting to: ${response.headers.location}`);
                    downloadFile(response.headers.location);
                    return;
                }

                if (response.statusCode !== 200) {
                    console.error(`Download failed with status: ${response.statusCode}`);
                    event.sender.send('update-error', `Download failed with status: ${response.statusCode}`);
                    return;
                }

                const totalBytes = parseInt(response.headers['content-length'], 10);
                let receivedBytes = 0;

                const file = fs.createWriteStream(tempPath);

                response.on('data', (chunk) => {
                    receivedBytes += chunk.length;
                    if (totalBytes) {
                        const usage = receivedBytes / totalBytes; // 0 to 1
                        event.sender.send('download-progress', usage);
                    }
                });

                response.pipe(file);

                file.on('finish', () => {
                    file.close(() => {
                        console.log("Update downloaded. Launching installer...");

                        // Verification
                        try {
                            const stats = fs.statSync(tempPath);
                            if (stats.size < 1000) {
                                throw new Error("File too small");
                            }
                        } catch (e) {
                            console.error("Verification failed:", e);
                            event.sender.send('update-error', "Verification failed");
                            return;
                        }

                        // Wait 1s to ensure file lock is released on Windows
                        setTimeout(() => {
                            // Use 'start' command on Windows to avoid EACCES and handle UAC better
                            // wrap path in quotes
                            const command = `start "" "${tempPath}" --update`;

                            const { exec } = require('child_process');
                            exec(command, { windowsHide: true }, (err) => {
                                if (err) {
                                    console.error("Failed to launch:", err);
                                    event.sender.send('update-error', err.message);
                                } else {
                                    // Quit app to allow installer to overwrite
                                    setTimeout(() => app.quit(), 500);
                                }
                            });
                        }, 1000);
                    });
                });
            }).on('error', (err) => {
                console.error("Download failed:", err);
                event.sender.send('update-error', err.message);
            });
        };

        downloadFile(url);
    });
}

// --- Python Backend Management ---

const PY_DIST_FOLDER = "backend_dist"; // Name of folder where exe lies in prod
const PY_MODULE = "backend_main"; // Name of exe

const getScriptPath = () => {
    if (app.isPackaged) {
        // Production: run python source from resources
        return path.join(process.resourcesPath, 'backend', 'main.py');
    }
    // Development / Unpacked Source: run python source from sibling folder
    return path.join(__dirname, '..', 'backend', 'main.py');
};

const createPythonProcess = () => {
    if (!app.isPackaged) {
        // Development: run python source with system Python
        const script = path.join(__dirname, '..', 'backend', 'main.py');
        console.log(`[DEV] Starting Python from: ${script}`);
        pythonProcess = spawn('python', [script], { detached: false });
    } else {
        // Production: use embedded Python
        const pythonExe = path.join(process.resourcesPath, 'python_embedded', 'python.exe');
        const backendScript = path.join(process.resourcesPath, 'backend', 'main.py');

        console.log(`[PROD] Python exe: ${pythonExe}`);
        console.log(`[PROD] Backend script: ${backendScript}`);

        if (!require('fs').existsSync(pythonExe)) {
            console.error(`Python executable not found at: ${pythonExe}`);
            return;
        }

        if (!require('fs').existsSync(backendScript)) {
            console.error(`Backend script not found at: ${backendScript}`);
            return;
        }

        pythonProcess = spawn(pythonExe, [backendScript], {
            detached: false,
            windowsHide: true,
            cwd: path.join(process.resourcesPath, 'backend')
        });
    }

    if (pythonProcess) {
        pythonProcess.stdout.on('data', (data) => console.log(`[Backend]: ${data}`));
        pythonProcess.stderr.on('data', (data) => console.error(`[Backend Error]: ${data}`));
        pythonProcess.on('error', (err) => console.error('Failed to start backend:', err));
        pythonProcess.on('exit', (code) => console.log(`Backend exited with code: ${code}`));
    }
};

const exitPythonProcess = () => {
    if (pythonProcess) {
        console.log("Killing Python process...");
        pythonProcess.kill();
        pythonProcess = null;
    }
};

app.on('ready', () => {
    createPythonProcess();
    createWindow();
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('will-quit', exitPythonProcess);

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow();
    }
});

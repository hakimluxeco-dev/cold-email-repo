import React, { useState, useEffect } from 'react';
import { Download, X, AlertCircle } from 'lucide-react';
import { APP_CONFIG } from '../config';
// We can use package.json version or config version. 
// Using config version for runtime checks is safer if we control it.

const UpdateBanner = () => {
    const [updateAvailable, setUpdateAvailable] = useState(false);
    const [updateInfo, setUpdateInfo] = useState(null);
    const [visible, setVisible] = useState(true);
    const [isDownloading, setIsDownloading] = useState(false);
    const [downloadProgress, setDownloadProgress] = useState(0);

    useEffect(() => {
        const checkUpdate = async () => {
            if (!APP_CONFIG.UPDATE_CHECK_URL || APP_CONFIG.UPDATE_CHECK_URL.includes("example.com")) {
                return;
            }

            try {
                const response = await fetch(APP_CONFIG.UPDATE_CHECK_URL);
                const data = await response.json();

                if (isNewerVersion(data.version, APP_CONFIG.CURRENT_VERSION)) {
                    setUpdateAvailable(true);
                    setUpdateInfo(data);
                }
            } catch (error) {
                console.error("Update check failed:", error);
            }
        };

        checkUpdate();

        // Listen for progress from Electron
        if (window.require) {
            const { ipcRenderer } = window.require('electron');

            const handleProgress = (event, progress) => {
                setDownloadProgress(progress * 100);
            };

            const handleError = (event, error) => {
                console.error("Update error:", error);
                setIsDownloading(false);
                alert("Update failed: " + error);
            };

            ipcRenderer.on('download-progress', handleProgress);
            ipcRenderer.on('update-error', handleError);

            return () => {
                ipcRenderer.removeListener('download-progress', handleProgress);
                ipcRenderer.removeListener('update-error', handleError);
            };
        }
    }, []);

    const isNewerVersion = (remote, local) => {
        const rParts = remote.split('.').map(Number);
        const lParts = local.split('.').map(Number);

        for (let i = 0; i < 3; i++) {
            if (rParts[i] > lParts[i]) return true;
            if (rParts[i] < lParts[i]) return false;
        }
        return false;
    };

    const handleUpdate = () => {
        if (!updateInfo?.downloadUrl || isDownloading) return;

        setIsDownloading(true);
        setDownloadProgress(0);

        try {
            if (window.require) {
                const { ipcRenderer } = window.require('electron');
                ipcRenderer.send('update-app', { url: updateInfo.downloadUrl });
            } else {
                console.warn("Electron IPC not available. Falling back to browser download.");
                window.open(updateInfo.downloadUrl, '_blank');
                setIsDownloading(false);
            }
        } catch (e) {
            console.error(e);
            window.open(updateInfo.downloadUrl, '_blank');
            setIsDownloading(false);
        }
    };

    if (!updateAvailable || !visible) return null;

    return (
        <div className="bg-primary/20 border-b border-primary/30 backdrop-blur-md px-6 py-3 relative z-50">
            <div className="flex items-center justify-between max-w-7xl mx-auto">
                <div className="flex items-center space-x-3">
                    <div className="bg-primary/20 p-2 rounded-full">
                        <AlertCircle className="text-primary" size={20} />
                    </div>
                    <div>
                        <h3 className="text-white font-semibold text-sm">New Version Available: v{updateInfo?.version}</h3>
                        <p className="text-primary/80 text-xs">{updateInfo?.releaseNotes || "Performance improvements and bug fixes."}</p>
                    </div>
                </div>

                <div className="flex items-center space-x-4">
                    {isDownloading ? (
                        <div className="flex flex-col w-48 space-y-1">
                            <div className="flex justify-between text-xs text-primary/80">
                                <span>Downloading...</span>
                                <span>{Math.round(downloadProgress)}%</span>
                            </div>
                            <div className="w-full bg-black/50 rounded-full h-1.5 overflow-hidden">
                                <div
                                    className="bg-primary h-full rounded-full transition-all duration-300"
                                    style={{ width: `${downloadProgress}%` }}
                                />
                            </div>
                        </div>
                    ) : (
                        <button
                            id="update-btn"
                            onClick={handleUpdate}
                            disabled={isDownloading}
                            className="flex items-center space-x-2 bg-primary hover:bg-primary/90 text-black px-4 py-2 rounded-lg text-xs font-bold transition-all shadow-lg shadow-primary/20 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Download size={14} />
                            <span>Update Now</span>
                        </button>
                    )}

                    {!isDownloading && (
                        <button
                            onClick={() => setVisible(false)}
                            className="text-gray-400 hover:text-white transition-colors"
                        >
                            <X size={18} />
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default UpdateBanner;

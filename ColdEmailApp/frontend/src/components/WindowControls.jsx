import React, { useState } from 'react';
import { Minus, Square, X, Monitor } from 'lucide-react';

const WindowControls = () => {
    const [isMaximized, setIsMaximized] = useState(false);

    // Helper to safely call IPC
    const ipcSend = (action) => {
        if (window.require) {
            try {
                const { ipcRenderer } = window.require('electron');
                ipcRenderer.send(action);
                if (action === 'window-maximize') {
                    // Start checking status or toggle local state optimistically
                    // Ideally we listen for an event, but this is MVP
                    setIsMaximized(!isMaximized);
                }
            } catch (e) {
                console.warn("Electron IPC not available");
            }
        } else {
            console.log(`Mock IPC: ${action}`);
        }
    };

    return (
        <div className="w-full h-10 bg-[#020617] border-b border-white/5 flex items-center justify-between select-none z-50">
            {/* Draggable Area - Spans most of the bar */}
            {/* -webkit-app-region: drag makes it draggable */}
            <div className="flex-1 h-full flex items-center px-4" style={{ WebkitAppRegion: 'drag' }}>
                <div className="text-xs text-gray-500 font-medium tracking-widest uppercase">
                    MAI Solutions <span className="text-primary/50 mx-2">//</span> Cold Email System
                </div>
            </div>

            {/* Window Controls - Non-draggable */}
            {/* -webkit-app-region: no-drag is needed on buttons */}
            <div className="flex items-center h-full mr-2" style={{ WebkitAppRegion: 'no-drag' }}>

                {/* Minimize */}
                <button
                    onClick={() => ipcSend('window-minimize')}
                    className="h-full px-4 text-gray-400 hover:bg-white/10 hover:text-white transition-colors"
                >
                    <Minus size={14} />
                </button>

                {/* Maximize / Restore */}
                <button
                    onClick={() => ipcSend('window-maximize')}
                    className="h-full px-4 text-gray-400 hover:bg-white/10 hover:text-white transition-colors"
                >
                    <Square size={12} strokeWidth={2} />
                </button>

                {/* Close */}
                <button
                    onClick={() => ipcSend('window-close')}
                    className="h-full px-4 text-gray-400 hover:bg-red-500 hover:text-white transition-colors group"
                >
                    <X size={14} className="group-hover:text-white" />
                </button>
            </div>
        </div>
    );
};

export default WindowControls;

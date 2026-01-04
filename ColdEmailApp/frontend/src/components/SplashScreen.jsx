import React, { useEffect, useState } from 'react';
import { APP_CONFIG } from '../config';

const SplashScreen = ({ onFinish }) => {
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        // Progress bar simulation
        const interval = setInterval(() => {
            setProgress(prev => {
                const next = prev + Math.random() * 10;
                if (next >= 100) {
                    clearInterval(interval);
                    return 100;
                }
                return next;
            });
        }, 150);

        // Completion timer
        const timer = setTimeout(() => {
            onFinish();
        }, 3000);

        return () => {
            clearInterval(interval);
            clearTimeout(timer);
        };
    }, [onFinish]);

    return (
        <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#020617] overflow-hidden">
            {/* Background effects */}
            <div className="absolute inset-0 bg-grid-pattern opacity-20 pointer-events-none" />
            <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#020617]/50 to-[#020617]" />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-primary/20 blur-[100px] rounded-full opacity-30 animate-pulse" />

            <div className="relative z-10 text-center animate-in flex flex-col items-center">
                {/* Logo Area */}
                <div className="animate-float mb-8">
                    <div className="relative">
                        <div className="absolute inset-0 bg-primary blur-2xl opacity-20" />
                        <svg width="80" height="80" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="relative z-10 text-primary drop-shadow-[0_0_15px_rgba(0,255,255,0.5)]">
                            <path d="M22 17.6536V13.0619C22.0007 12.9248 21.9678 12.7896 21.9042 12.6685C21.8406 12.5474 21.7483 12.4442 21.6356 12.368L12.5556 6.13623C12.394 6.0253 12.1983 5.96582 11.9998 5.96582C11.8013 5.96582 11.6056 6.0253 11.444 6.13623L2.36402 12.368C2.25127 12.4442 2.15895 12.5474 2.09536 12.6685C2.03176 12.7896 1.99882 12.9248 1.99955 13.0619V17.6536C2.00036 18.0673 2.16521 18.4637 2.45789 18.7558C2.75057 19.0478 3.14702 19.2117 3.56005 19.2117H20.4391C20.8521 19.2117 21.2486 19.0478 21.5412 18.7558C21.8339 18.4637 21.9987 18.0673 21.9996 17.6536Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <path d="M12 2L2 9L12 16L22 9L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            <path d="M2 13L12 20L22 13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                        </svg>
                    </div>
                </div>

                {/* Text */}
                <h1 className="text-5xl font-black tracking-tighter text-white mb-2">
                    MAI <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary to-cyan-400">SOLUTIONS</span>
                </h1>
                <p className="text-cyan-400/80 tracking-[0.3em] text-xs font-bold uppercase">Cold Email Reach</p>

                {/* Loading Bar */}
                <div className="mt-12 w-64 h-1 bg-white/10 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-gradient-to-r from-primary via-cyan-400 to-blue-500 transition-all duration-300 ease-out shadow-[0_0_10px_rgba(0,255,255,0.5)]"
                        style={{ width: `${progress}%` }}
                    />
                </div>

                <div className="mt-4 text-xs font-mono text-white/30">
                    Initializing System v{APP_CONFIG.CURRENT_VERSION}...
                </div>
            </div>
        </div>
    );
};

export default SplashScreen;

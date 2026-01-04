import React, { useEffect, useState } from 'react';
import { X, Sparkles, CheckCircle2 } from 'lucide-react';
import { APP_CONFIG } from '../config';
import { releaseNotes } from '../releaseNotes';

const WhatsNewModal = () => {
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        const checkVersion = () => {
            const lastSeen = localStorage.getItem('lastSeenVersion');
            const current = APP_CONFIG.CURRENT_VERSION;

            // Show if no last version (new user) or version changed
            // To be less annoying to new users, maybe only show if they are upgrading?
            // User request: "when a new update is rolled and the user updates... open the first time"
            // So if lastSeen exists AND is different, show it.
            // If lastSeen doesn't exist, it implies fresh install. Maybe show welcome? 
            // Let's go with: Show if lastSeen != current.

            if (lastSeen !== current) {
                setIsOpen(true);
            }
        };

        checkVersion();
    }, []);

    const handleClose = () => {
        localStorage.setItem('lastSeenVersion', APP_CONFIG.CURRENT_VERSION);
        setIsOpen(false);
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-sm"
                onClick={handleClose}
            />

            {/* Modal */}
            <div className="relative bg-[#0F172A] border border-white/10 rounded-2xl w-full max-w-lg shadow-[0_0_50px_rgba(0,0,0,0.5)] overflow-hidden animate-in fade-in zoom-in duration-300">
                {/* Header */}
                <div className="bg-gradient-to-r from-primary/20 to-purple-500/20 p-6 relative">
                    <div className="absolute top-4 right-4">
                        <button
                            onClick={handleClose}
                            className="text-white/50 hover:text-white transition-colors p-1"
                        >
                            <X size={20} />
                        </button>
                    </div>

                    <div className="flex items-center space-x-3 mb-2">
                        <div className="bg-primary p-2 rounded-lg text-black">
                            <Sparkles size={20} />
                        </div>
                        <span className="text-primary font-bold tracking-wider text-sm">WHAT'S NEW</span>
                    </div>
                    <h2 className="text-2xl font-bold text-white">{releaseNotes.title}</h2>
                    <p className="text-white/60 text-sm mt-1">Version {releaseNotes.version}</p>
                </div>

                {/* Content */}
                <div className="p-6 space-y-4 max-h-[60vh] overflow-y-auto custom-scrollbar">
                    {releaseNotes.features.map((feature, idx) => (
                        <div key={idx} className="flex items-start space-x-4 bg-white/5 p-4 rounded-xl border border-white/5">
                            <CheckCircle2 className="text-primary shrink-0 mt-0.5" size={18} />
                            <div>
                                <h3 className="text-white font-semibold text-sm">{feature.title}</h3>
                                <p className="text-gray-400 text-sm leading-relaxed mt-1">
                                    {feature.description}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>

                {/* Footer */}
                <div className="p-6 border-t border-white/10 bg-white/5 flex justify-end">
                    <button
                        onClick={handleClose}
                        className="bg-primary hover:bg-primary/90 text-black font-bold py-2.5 px-6 rounded-xl transition-all shadow-lg shadow-primary/20"
                    >
                        Got it!
                    </button>
                </div>
            </div>
        </div>
    );
};

export default WhatsNewModal;

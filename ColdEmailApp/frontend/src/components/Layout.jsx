import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, Send, Inbox, Settings, Zap } from 'lucide-react';
import clsx from 'clsx';
import { APP_CONFIG } from '../config';

const NavItem = ({ to, icon: Icon, label }) => {
    const location = useLocation();
    const isActive = location.pathname === to;

    return (
        <Link
            to={to}
            className={clsx(
                "relative flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-300 group overflow-hidden",
                isActive
                    ? "bg-gradient-to-r from-primary/10 to-transparent text-primary"
                    : "text-gray-400 hover:text-white hover:bg-white/5"
            )}
        >
            <Icon size={20} className={clsx("transition-transform duration-300", isActive ? "scale-110 drop-shadow-[0_0_8px_rgba(0,255,255,0.5)]" : "group-hover:scale-105")} />
            <span className="font-medium relative z-10">{label}</span>
            {isActive && (
                <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary shadow-[0_0_15px_#00FFFF]" />
            )}
        </Link>
    );
};

import WindowControls from './WindowControls';
import UpdateBanner from './UpdateBanner';
import WhatsNewModal from './WhatsNewModal';
import DashboardLogo from '../assets/dashboard_logo.png';

const Layout = () => {
    return (
        <div className="flex flex-col h-screen w-full bg-background text-white font-sans overflow-hidden">

            {/* Main App Workspace */}
            <div className="flex flex-1 overflow-hidden">
                {/* Sidebar */}
                <aside className="w-64 border-r border-white/5 bg-surface/30 backdrop-blur-xl flex flex-col pt-8 pb-4 relative z-20">
                    {/* Logo Area */}
                    <div className="px-6 mb-10">
                        <img src={DashboardLogo} alt="MAI Solutions" className="h-10 w-auto" />
                    </div>

                    {/* Navigation */}
                    <nav className="flex-1 px-4 space-y-2">
                        <div className="px-4 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-widest">Menu</div>
                        <NavItem to="/" icon={LayoutDashboard} label="Dashboard" />
                        <NavItem to="/leads" icon={Users} label="Lead Manager" />
                        <NavItem to="/campaigns" icon={Send} label="Campaigns" />
                        <NavItem to="/unibox" icon={Inbox} label="Unibox" />

                        <div className="mt-8 px-4 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-widest">System</div>
                        <NavItem to="/settings" icon={Settings} label="Settings" />
                    </nav>

                    {/* Status Chip */}
                    <div className="px-6 mt-auto">
                        <div className="bg-black/40 rounded-lg p-3 flex items-center space-x-3 border border-white/5">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-[0_0_8px_#22c55e]" />
                            <div className="flex flex-col">
                                <span className="text-xs font-medium text-gray-300">System Online</span>
                                <span className="text-[10px] text-gray-500">v{APP_CONFIG.CURRENT_VERSION} Stable</span>
                            </div>
                        </div>
                    </div>
                </aside>

                {/* Main Content Area */}
                <div className="flex-1 flex flex-col min-w-0 bg-[#020617] relative">
                    <WindowControls />
                    <UpdateBanner />
                    <WhatsNewModal />
                    <main className="flex-1 overflow-y-auto p-8 relative z-0">
                        {/* Top Glow */}
                        <div className="absolute top-0 left-0 w-full h-[500px] bg-primary/5 blur-[120px] pointer-events-none rounded-full transform -translate-y-1/2" />
                        <Outlet />
                    </main>
                </div>
            </div>
        </div>
    );
};

export default Layout;

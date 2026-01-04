import React from 'react';
import { useNavigate } from 'react-router-dom';

const DashboardHome = () => {
    const navigate = useNavigate();
    const [stats, setStats] = React.useState({
        active_leads: 0,
        emails_sent: 0,
        reply_rate: 0,
        replies_received: 0
    });

    React.useEffect(() => {
        const fetchStats = async () => {
            try {
                const res = await fetch('http://localhost:8000/stats');
                if (res.ok) {
                    const data = await res.json();
                    setStats(data);
                }
            } catch (e) {
                console.error("Failed to fetch stats", e);
            }
        };
        fetchStats();
        // Poll every 30s
        const interval = setInterval(fetchStats, 30000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="space-y-8">
            <div className="flex justify-between items-end">
                <div>
                    <h2 className="text-3xl font-bold text-white tracking-tight">Dashboard</h2>
                    <p className="text-gray-400 mt-1">Overview of your cold outreach performance.</p>
                </div>
                <button
                    onClick={() => navigate('/campaigns')}
                    className="bg-primary hover:bg-cyan-400 text-black font-bold py-2 px-6 rounded-lg transition-all shadow-[0_0_20px_rgba(0,255,255,0.3)] hover:shadow-[0_0_30px_rgba(0,255,255,0.5)]"
                >
                    Start New Campaign
                </button>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {[
                    { label: 'Total Leads', value: stats.active_leads, color: 'from-blue-500 to-cyan-500' },
                    { label: 'Emails Sent', value: stats.emails_sent, color: 'from-purple-500 to-pink-500' },
                    { label: 'Reply Rate', value: `${stats.reply_rate}%`, color: 'from-green-500 to-emerald-500' },
                ].map((stat, i) => (
                    <div key={i} className="bg-surface/50 backdrop-blur-md border border-white/10 p-6 rounded-2xl relative overflow-hidden group hover:border-white/20 transition-all">
                        <div className={`absolute top-0 right-0 w-24 h-24 bg-gradient-to-br ${stat.color} opacity-10 rounded-full blur-xl group-hover:opacity-20 transition-opacity`} />
                        <h3 className="text-gray-400 text-sm font-medium uppercase tracking-wider">{stat.label}</h3>
                        <div className="mt-2 flex items-baseline space-x-2">
                            <span className="text-4xl font-bold text-white">{stat.value}</span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Recent Activity */}
            <div className="bg-surface/30 border border-white/10 rounded-2xl p-6">
                <h3 className="text-xl font-bold mb-4">Live Activity Feed</h3>
                <div className="space-y-4">
                    <div className="flex items-center space-x-4 p-3 rounded-lg bg-white/5">
                        <div className="w-2 h-2 bg-primary rounded-full" />
                        <span className="text-sm text-gray-300">Sent email to <span className="text-white font-medium">john@example.com</span></span>
                        <span className="ml-auto text-xs text-gray-500">2 mins ago</span>
                    </div>
                    <div className="flex items-center space-x-4 p-3 rounded-lg bg-white/5">
                        <div className="w-2 h-2 bg-green-500 rounded-full" />
                        <span className="text-sm text-gray-300">New reply from <span className="text-white font-medium">sarah@business.co.za</span></span>
                        <span className="ml-auto text-xs text-gray-500">15 mins ago</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardHome;

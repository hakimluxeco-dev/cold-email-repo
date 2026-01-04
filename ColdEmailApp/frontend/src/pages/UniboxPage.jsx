import React, { useState, useEffect } from 'react';
import axios, { syncInbox } from '../api';
import { RefreshCw, MessageSquare } from 'lucide-react';

const UniboxPage = () => {
    const [replies, setReplies] = useState([]);
    const [loading, setLoading] = useState(true);
    const [syncing, setSyncing] = useState(false);

    useEffect(() => {
        fetchReplies();
    }, []);

    const fetchReplies = async () => {
        try {
            // Filter Leads by Status 'Interested' or 'Contacted' could be useful too
            // But for now, let's just show Interested
            const res = await axios.get('/leads');
            const interested = res.data.filter(l => l.status === 'Interested' || l.status === 'Not Interested');
            setReplies(interested);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const handleSync = async () => {
        setSyncing(true);
        try {
            const res = await syncInbox();
            if (res.updates > 0) {
                alert(`Sync complete! Found ${res.updates} new updates.`);
                fetchReplies();
            } else {
                alert("No new replies found.");
            }
        } catch (e) {
            console.error(e);
            alert("Sync failed. Check backend logs.");
        } finally {
            setSyncing(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-white tracking-tight">Unified Inbox</h2>
                    <p className="text-gray-400">Manage replies and opportunities.</p>
                </div>
                <button
                    onClick={handleSync}
                    disabled={syncing}
                    className="flex items-center space-x-2 px-4 py-2 bg-surface border border-white/10 rounded-lg hover:bg-white/5 transition-colors text-white"
                >
                    <RefreshCw size={18} className={syncing ? 'animate-spin' : ''} />
                    <span>{syncing ? 'Syncing...' : 'Sync Now'}</span>
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {loading ? (
                    <div className="text-gray-500 col-span-full text-center py-10">Loading conversations...</div>
                ) : replies.length === 0 ? (
                    <div className="text-gray-500 col-span-full text-center py-10 flex flex-col items-center">
                        <MessageSquare size={48} className="mb-4 opacity-20" />
                        <p>No replies yet. Start a campaign to get the ball rolling!</p>
                    </div>
                ) : (
                    replies.map(lead => (
                        <div key={lead.id} className="bg-surface/30 border border-white/10 rounded-xl p-6 hover:border-primary/30 transition-all cursor-pointer group">
                            <div className="flex justify-between items-start mb-4">
                                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center text-lg font-bold">
                                    {lead.name.substring(0, 2).toUpperCase()}
                                </div>
                                <span className={`px-2 py-1 rounded text-xs font-bold ${lead.status === 'Interested' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                                    }`}>
                                    {lead.status}
                                </span>
                            </div>

                            <h3 className="font-bold text-white truncate">{lead.name}</h3>
                            <p className="text-sm text-gray-400 mb-4">{lead.email}</p>

                            <div className="text-xs text-gray-500 bg-black/20 p-2 rounded border border-white/5">
                                Last interaction: {lead.last_contacted ? new Date(lead.last_contacted).toLocaleDateString() : 'Unknown'}
                            </div>

                            <button className="mt-4 w-full py-2 bg-white/5 hover:bg-white/10 rounded text-sm font-medium transition-colors">
                                Open Details
                            </button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default UniboxPage;

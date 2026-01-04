import React, { useState, useEffect } from 'react';
import axios from '../api';
import { Play, Pause, Save, Settings as SettingsIcon } from 'lucide-react';

const CampaignsPage = () => {
    const [settings, setSettings] = useState({
        email_template_subject: '',
        email_template_body: '',
        daily_limit: 50,
        smtp_user: ''
    });
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [sending, setSending] = useState(false);

    useEffect(() => {
        fetchSettings();
    }, []);

    const fetchSettings = async () => {
        try {
            const res = await axios.get('/settings');
            setSettings(res.data);
        } catch (e) {
            console.error(e);
        }
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            await axios.put('/settings', settings);
            // Show success toast?
        } catch (e) {
            console.error(e);
        } finally {
            setSaving(false);
        }
    };

    const handleStart = async () => {
        setSending(true);
        try {
            const res = await axios.post('/campaign/start');
            alert(`Batch sent! Sent ${res.data.emails_sent} emails.`);
        } catch (e) {
            console.error(e);
            alert("Failed to start campaign");
        } finally {
            setSending(false);
        }
    };

    return (
        <div className="space-y-8">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-white tracking-tight">Campaign Manager</h2>
                    <p className="text-gray-400">Configure your outreach sequence.</p>
                </div>

                <div className="flex space-x-4">
                    <button
                        onClick={handleSave}
                        disabled={saving}
                        className="flex items-center space-x-2 px-4 py-2 bg-surface border border-white/10 rounded-lg hover:bg-white/5 transition-colors text-gray-300"
                    >
                        <Save size={18} />
                        <span>{saving ? 'Saving...' : 'Save Draft'}</span>
                    </button>

                    <button
                        onClick={handleStart}
                        disabled={sending}
                        className="flex items-center space-x-2 px-6 py-2 bg-primary text-black font-bold rounded-lg shadow-[0_0_15px_rgba(0,255,255,0.4)] hover:bg-cyan-300 transition-all hover:scale-105"
                    >
                        {sending ? <Pause size={18} /> : <Play size={18} fill="black" />}
                        <span>{sending ? 'Sending...' : 'Start Campaign'}</span>
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Editor Column */}
                <div className="lg:col-span-2 space-y-6">
                    <div className="bg-surface/30 border border-white/10 rounded-xl p-6">
                        <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Email Subject</label>
                        <input
                            type="text"
                            value={settings.email_template_subject || ''}
                            onChange={(e) => setSettings({ ...settings, email_template_subject: e.target.value })}
                            className="w-full bg-background border border-white/10 rounded-lg px-4 py-3 text-white focus:border-primary/50 focus:outline-none font-medium"
                            placeholder="Quick question for [Business Name]"
                        />
                    </div>

                    <div className="bg-surface/30 border border-white/10 rounded-xl p-6 flex flex-col h-[500px]">
                        <div className="flex justify-between items-center mb-4">
                            <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest">Email Body</label>
                            <div className="text-xs text-gray-500">
                                Supported variables: <span className="text-primary">[Name]</span>, <span className="text-primary">[Business Name]</span>, <span className="text-primary">[Icebreaker]</span>
                            </div>
                        </div>
                        <textarea
                            value={settings.email_template_body || ''}
                            onChange={(e) => setSettings({ ...settings, email_template_body: e.target.value })}
                            className="flex-1 w-full bg-background border border-white/10 rounded-lg p-4 text-gray-300 focus:border-primary/50 focus:outline-none font-mono text-sm leading-relaxed resize-none"
                            placeholder="Hi [Name], ..."
                        />
                    </div>
                </div>

                {/* Settings Column */}
                <div className="space-y-6">
                    <div className="bg-surface/30 border border-white/10 rounded-xl p-6">
                        <div className="flex items-center space-x-2 mb-6">
                            <SettingsIcon size={20} className="text-primary" />
                            <h3 className="font-bold text-white">Campaign Settings</h3>
                        </div>

                        <div className="space-y-4">
                            <div>
                                <label className="block text-xs text-gray-500 mb-1">Sending Account</label>
                                <div className="text-sm font-medium text-white p-2 bg-white/5 rounded border border-white/5 truncate">
                                    {settings.smtp_user || 'No account connected'}
                                </div>
                            </div>

                            <div>
                                <label className="block text-xs text-gray-500 mb-1">Daily Limit</label>
                                <input
                                    type="number"
                                    value={settings.daily_limit || 50}
                                    onChange={(e) => setSettings({ ...settings, daily_limit: parseInt(e.target.value) })}
                                    className="w-full bg-background border border-white/10 rounded px-3 py-2 text-white"
                                />
                            </div>

                            <hr className="border-white/5 my-4" />

                            <div className="rounded-lg bg-blue-500/10 border border-blue-500/20 p-4">
                                <h4 className="text-blue-400 text-sm font-bold mb-1">Pro Tip</h4>
                                <p className="text-xs text-blue-300/80 leading-relaxed">
                                    Keep your daily limit under 50 to avoid spam filters. The system automatically adds random delays between emails.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CampaignsPage;

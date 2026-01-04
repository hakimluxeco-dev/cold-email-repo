import React, { useState, useEffect } from 'react';
import axios from '../api';
import { Save, Mail, Server, Shield } from 'lucide-react';

const SettingsPage = () => {
    const [settings, setSettings] = useState({
        smtp_user: '',
        smtp_password: '', // Should be masked in real app
        daily_limit: 50
    });
    const [saving, setSaving] = useState(false);

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
            // Only send fields that exist in the backend SettingsUpdate schema
            // to avoid validation errors with extra fields like 'id', 'created_at'.
            const payload = {
                smtp_user: settings.smtp_user,
                smtp_password: settings.smtp_password,
                daily_limit: settings.daily_limit,
                email_template_body: settings.email_template_body
            };
            await axios.put('/settings', payload);
            alert("Settings saved!");
        } catch (e) {
            console.error(e);
            // Show detailed error for debugging
            const errorMsg = e.response?.data?.detail
                ? JSON.stringify(e.response.data.detail)
                : e.message;
            alert(`Error saving settings: ${errorMsg}`);
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold text-white tracking-tight">System Settings</h2>
                    <p className="text-gray-400">Configure your email provider.</p>
                </div>
                <button
                    onClick={handleSave}
                    disabled={saving}
                    className="flex items-center space-x-2 px-6 py-2 bg-primary text-black font-bold rounded-lg shadow-[0_0_15px_rgba(0,255,255,0.4)] hover:bg-cyan-300 transition-all hover:scale-105"
                >
                    <Save size={18} />
                    <span>{saving ? 'Saving...' : 'Save Changes'}</span>
                </button>
            </div>

            <div className="bg-surface/30 border border-white/10 rounded-xl overflow-hidden">
                <div className="p-6 border-b border-white/10 bg-white/5">
                    <h3 className="text-lg font-bold flex items-center space-x-2">
                        <Mail className="text-primary" size={20} />
                        <span>Email Credentials (SMTP/IMAP)</span>
                    </h3>
                </div>

                <div className="p-8 space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">Email Address</label>
                            <div className="relative">
                                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={16} />
                                <input
                                    type="email"
                                    value={settings.smtp_user || ''}
                                    onChange={(e) => setSettings({ ...settings, smtp_user: e.target.value })}
                                    className="w-full bg-background border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white focus:border-primary/50 focus:outline-none"
                                    placeholder="you@gmail.com"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-xs font-bold text-gray-500 uppercase tracking-widest mb-2">App Password</label>
                            <div className="relative">
                                <Shield className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={16} />
                                <input
                                    type="password"
                                    value={settings.smtp_password || ''}
                                    onChange={(e) => setSettings({ ...settings, smtp_password: e.target.value })}
                                    className="w-full bg-background border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white focus:border-primary/50 focus:outline-none"
                                    placeholder="••••••••••••••••"
                                />
                            </div>
                            <p className="mt-2 text-xs text-gray-500">
                                For Gmail, use an <a href="https://myaccount.google.com/apppasswords" target="_blank" className="text-primary hover:underline">App Password</a>.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div className="bg-surface/30 border border-white/10 rounded-xl overflow-hidden opacity-50 pointer-events-none">
                <div className="p-6 border-b border-white/10 bg-white/5">
                    <h3 className="text-lg font-bold flex items-center space-x-2">
                        <Server className="text-gray-400" size={20} />
                        <span>Advanced Configuration (Locked)</span>
                    </h3>
                </div>
                <div className="p-6">
                    <p className="text-sm text-gray-500">Manual IMAP/SMTP server configuration is locked to Gmail/Outlook defaults for this version.</p>
                </div>
            </div>
        </div>
    );
};

export default SettingsPage;

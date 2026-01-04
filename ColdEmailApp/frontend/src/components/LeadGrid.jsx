import React, { useState, useEffect } from 'react';
import { getLeads, importLeads, deleteLeads } from '../api';
import { Upload, Search, Mail, Filter } from 'lucide-react';

const StatusBadge = ({ status }) => {
    const styles = {
        Pending: 'bg-gray-500/10 text-gray-400 border-gray-500/20',
        Contacted: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
        Interested: 'bg-green-500/10 text-green-400 border-green-500/20 shadow-[0_0_10px_rgba(34,197,94,0.2)]',
        'Not Interested': 'bg-red-500/10 text-red-400 border-red-500/20',
        Inactive: 'bg-slate-700/10 text-slate-500 border-slate-700/20',
    };

    return (
        <span className={`px-2 py-1 rounded-md text-xs font-medium border ${styles[status] || styles.Pending}`}>
            {status}
        </span>
    );
};

const LeadGrid = () => {
    const [leads, setLeads] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedLeads, setSelectedLeads] = useState(new Set());

    const fetchLeads = async () => {
        setLoading(true);
        try {
            const data = await getLeads();
            setLeads(data);
            setSelectedLeads(new Set()); // Reset selection on refresh
        } catch (error) {
            console.error("Failed to load leads", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchLeads();
    }, []);

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        try {
            const response = await importLeads(file);
            fetchLeads(); // Refresh
            alert(response.message || "Import successful!");
        } catch (e) {
            console.error(e);
            // DEBUG: Show actual error
            const msg = e.response?.data?.detail
                ? JSON.stringify(e.response.data.detail)
                : e.message;
            alert(`Import failed: ${msg}`);
        }
    };

    // --- Bulk Delete Logic ---

    const handleDeleteSelected = async () => {
        if (selectedLeads.size === 0) return;

        if (!window.confirm(`Are you sure you want to delete ${selectedLeads.size} leads?`)) {
            return;
        }

        try {
            // Ensure IDs are numbers
            const ids = Array.from(selectedLeads).map(id => Number(id));
            await deleteLeads(ids, false);
            fetchLeads();
            alert("Leads deleted successfully.");
        } catch (e) {
            console.error("Delete failed", e);
            const msg = e.response?.data?.detail
                ? JSON.stringify(e.response.data.detail)
                : (e.response?.data?.message || e.message);
            alert(`Failed to delete leads: ${msg}`);
        }
    };

    const toggleSelectAll = () => {
        if (selectedLeads.size === filteredLeads.length && filteredLeads.length > 0) {
            setSelectedLeads(new Set());
        } else {
            const allIds = new Set(filteredLeads.map(l => l.id));
            setSelectedLeads(allIds);
        }
    };

    const toggleSelect = (id) => {
        const newSelected = new Set(selectedLeads);
        if (newSelected.has(id)) {
            newSelected.delete(id);
        } else {
            newSelected.add(id);
        }
        setSelectedLeads(newSelected);
    };

    const filteredLeads = leads.filter(l =>
        l.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        l.email.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const isAllSelected = filteredLeads.length > 0 && selectedLeads.size === filteredLeads.length;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold text-white tracking-tight">Lead Manager</h2>

                <div className="flex space-x-3">
                    {selectedLeads.size > 0 && (
                        <button
                            onClick={handleDeleteSelected}
                            className="flex items-center space-x-2 bg-red-500/10 border border-red-500/20 text-red-400 px-4 py-2 rounded-lg hover:bg-red-500/20 transition-all"
                        >
                            <span>Delete Selected ({selectedLeads.size})</span>
                        </button>
                    )}

                    <label className="cursor-pointer flex items-center space-x-2 bg-surface border border-white/10 hover:bg-white/5 text-gray-300 px-4 py-2 rounded-lg transition-all">
                        <Upload size={16} />
                        <span>Import Leads</span>
                        <input type="file" className="hidden" accept=".csv,.md,.txt" onChange={handleFileUpload} />
                    </label>
                </div>
            </div>

            {/* Filters */}
            <div className="flex space-x-4 bg-surface/30 p-4 rounded-xl border border-white/5">
                <div className="relative flex-1">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500" size={18} />
                    <input
                        type="text"
                        placeholder="Search leads..."
                        className="w-full bg-background/50 border border-white/10 rounded-lg pl-10 pr-4 py-2 text-white focus:outline-none focus:border-primary/50 transition-all"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <button className="flex items-center space-x-2 px-4 py-2 bg-background/50 border border-white/10 rounded-lg text-gray-400 hover:text-white">
                    <Filter size={16} />
                    <span>Filter</span>
                </button>
            </div>

            {/* Grid */}
            <div className="bg-surface/30 border border-white/10 rounded-xl overflow-hidden shadow-2xl">
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead>
                            <tr className="bg-white/5 text-gray-400 text-xs uppercase tracking-wider">
                                <th className="px-6 py-4 font-semibold w-10">
                                    <input
                                        type="checkbox"
                                        className="rounded border-gray-600 bg-gray-700 text-primary focus:ring-primary"
                                        checked={isAllSelected}
                                        onChange={toggleSelectAll}
                                    />
                                </th>
                                <th className="px-6 py-4 font-semibold">Name</th>
                                <th className="px-6 py-4 font-semibold">Email</th>
                                <th className="px-6 py-4 font-semibold">Status</th>
                                <th className="px-6 py-4 font-semibold">Source</th>
                                <th className="px-6 py-4 font-semibold">Last Contact</th>
                                <th className="px-6 py-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-white/5">
                            {loading ? (
                                <tr><td colSpan="7" className="px-6 py-8 text-center text-gray-500">Loading leads...</td></tr>
                            ) : filteredLeads.length === 0 ? (
                                <tr><td colSpan="7" className="px-6 py-8 text-center text-gray-500">No leads found. Import some to get started.</td></tr>
                            ) : (
                                filteredLeads.map((lead) => (
                                    <tr key={lead.id} className={`hover:bg-white/5 transition-colors group ${selectedLeads.has(lead.id) ? 'bg-white/5' : ''}`}>
                                        <td className="px-6 py-4">
                                            <input
                                                type="checkbox"
                                                className="rounded border-gray-600 bg-gray-700 text-primary focus:ring-primary"
                                                checked={selectedLeads.has(lead.id)}
                                                onChange={() => toggleSelect(lead.id)}
                                            />
                                        </td>
                                        <td className="px-6 py-4 font-medium text-white">{lead.name}</td>
                                        <td className="px-6 py-4 text-gray-300 relative">
                                            {lead.email}
                                            <button className="absolute right-4 top-1/2 transform -translate-y-1/2 opacity-0 group-hover:opacity-100 text-primary hover:text-white transition-opacity">
                                                <Mail size={14} />
                                            </button>
                                        </td>
                                        <td className="px-6 py-4">
                                            <StatusBadge status={lead.status} />
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-500">{lead.source || '-'}</td>
                                        <td className="px-6 py-4 text-sm text-gray-500">
                                            {lead.last_contacted ? new Date(lead.last_contacted).toLocaleDateString() : 'Never'}
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <button className="text-gray-500 hover:text-primary transition-colors text-sm font-medium">Edit</button>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="text-center text-xs text-gray-500">
                Showing {filteredLeads.length} leads
            </div>
        </div>
    );
};

export default LeadGrid;

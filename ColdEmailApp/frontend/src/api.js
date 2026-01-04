import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getLeads = async (skip = 0, limit = 100) => {
    const response = await api.get(`/leads?skip=${skip}&limit=${limit}`);
    return response.data;
};

export const getStats = async () => {
    const response = await api.get('/stats');
    return response.data;
};

export const importLeads = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/import', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const syncInbox = async () => {
    const response = await api.post('/inbox/sync');
    return response.data;
};

export const deleteLeads = async (leadIds = [], deleteAll = false) => {
    const response = await api.post('/leads/delete', {
        lead_ids: leadIds,
        all: deleteAll
    });
    return response.data;
};

export default api;

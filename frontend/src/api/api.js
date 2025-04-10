import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const threatApi = {
  getThreats: (params) => api.get('/threats', { params }),
  getThreat: (id) => api.get(`/threats/${id}`),
  analyzeThreat: (data) => api.post('/threats/analyze', data),
  respondToThreat: (id, action) => api.post(`/threats/${id}/respond`, action),
};

export const alertApi = {
  getAlerts: (params) => api.get('/alerts', { params }),
  getAlert: (id) => api.get(`/alerts/${id}`),
  updateAlertStatus: (id, status) => api.put(`/alerts/${id}/status?status=${status}`),
  addComment: (id, comment) => api.post(`/alerts/${id}/comment`, comment),
  getStatistics: () => api.get('/alerts/statistics'),
};

export const modelApi = {
  getModels: () => api.get('/models'),
  getModelInfo: (name) => api.get(`/models/${name}`),
  trainModel: (name, data) => api.post(`/models/${name}/train`, data),
  predict: (name, data) => api.post(`/models/${name}/predict`, data),
  saveModel: (name, path) => api.post(`/models/${name}/save`, { path }),
  loadModel: (name, path) => api.post(`/models/${name}/load`, { path }),
};

export default api;

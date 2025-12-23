import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Business API
export const businessAPI = {
  getAll: (params = {}) => api.get('/businesses/', { params }),
  getById: (id) => api.get(`/businesses/${id}`),
  create: (data) => api.post('/businesses/', data),
  update: (id, data) => api.put(`/businesses/${id}`, data),
  delete: (id) => api.delete(`/businesses/${id}`),
  getCount: () => api.get('/businesses/stats/count'),
};

// Landing Page API
export const landingPageAPI = {
  generate: (businessId, customization = {}) =>
    api.post(`/landing-pages/generate/${businessId}`, customization),
  getAll: (params = {}) => api.get('/landing-pages/', { params }),
  getById: (id) => api.get(`/landing-pages/${id}`),
  update: (id, data) => api.put(`/landing-pages/${id}`, data),
  delete: (id) => api.delete(`/landing-pages/${id}`),
  publish: (id) => api.post(`/landing-pages/${id}/publish`),
  unpublish: (id) => api.post(`/landing-pages/${id}/unpublish`),
  trackView: (id) => api.post(`/landing-pages/${id}/view`),
  getCount: (businessId = null) => {
    const params = businessId ? { business_id: businessId } : {};
    return api.get('/landing-pages/stats/count', { params });
  },
};

// Health API
export const healthAPI = {
  check: () => api.get('/health/'),
  detailed: () => api.get('/health/detailed'),
  version: () => api.get('/health/version'),
};

export default api;

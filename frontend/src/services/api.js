import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dashboard APIs
export const getDashboardKPIs = () => api.get('/dashboard/kpis');

// Analytics APIs
export const getIncidentsByType = () => api.get('/analytics/incidents-by-type');
export const getIncidentsBySeverity = () => api.get('/analytics/incidents-by-severity');
export const getStateAnalysis = () => api.get('/analytics/by-state');
export const getMonthlyTrends = () => api.get('/analytics/monthly-trends');
export const getResponseTimeAnalysis = () => api.get('/analytics/response-time');
export const getTopCauses = () => api.get('/analytics/top-causes');
export const getGeographicData = () => api.get('/analytics/geographic');

// Vendor APIs
export const getVendorPerformance = () => api.get('/vendors/performance');

// Report APIs
export const generatePDFReport = () => {
  return api.post('/reports/generate-pdf', {}, { responseType: 'blob' });
};

export const generateExcelReport = () => {
  return api.post('/reports/generate-excel', {}, { responseType: 'blob' });
};

// File Upload
export const uploadDataFile = (formData) => {
  return api.post('/data/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export default api;

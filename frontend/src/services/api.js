import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  register: (email, username, fullName, password) =>
    api.post('/auth/register', { email, username, full_name: fullName, password }),
  
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  
  getCurrentUser: () => api.get('/auth/me'),
};

export const taskService = {
  getTasks: (skip = 0, limit = 10) =>
    api.get('/tasks', { params: { skip, limit } }),
  
  getTask: (taskId) =>
    api.get(`/tasks/${taskId}`),
  
  createTask: (title, description, priority) =>
    api.post('/tasks', { title, description, priority }),
  
  updateTask: (taskId, data) =>
    api.put(`/tasks/${taskId}`, data),
  
  deleteTask: (taskId) =>
    api.delete(`/tasks/${taskId}`),
};

export default api;

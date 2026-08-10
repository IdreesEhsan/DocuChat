import axios from 'axios';

const API = axios.create({ baseURL: '' });

// Interceptor to add token from localStorage to every request
API.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const registerAPI = async (userData) => {
  const response = await API.post('/api/auth/register', userData);
  return response.data;
};

export const loginAPI = async (email, password) => {
  const response = await API.post('/api/auth/login', { email, password });
  return response.data;
};

export const uploadFile = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return API.post('/upload/', formData);
};

export const streamChat = async (query, onEvent) => {
  const response = await fetch('/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify({ query }),
  });
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    for (const line of lines) {
      if (line.trim()) {
        try {
          const event = JSON.parse(line);
          onEvent(event);
        } catch (e) {
          console.warn('Failed to parse JSON:', line);
        }
      }
    }
  }
};
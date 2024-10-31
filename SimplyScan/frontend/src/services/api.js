import axios from 'axios';

const API_URL = 'https://your-api-url.com';

export const login = (email, password) => {
  return axios.post(`${API_URL}/login`, { email, password });
};

export const fetchProfile = () => {
  return axios.get(`${API_URL}/profile`);
};

export const saveProfile = (data) => {
  return axios.post(`${API_URL}/profile`, data);
};

export const fetchHistory = () => {
  return axios.get(`${API_URL}/history`);
};

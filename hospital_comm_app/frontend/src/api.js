import axios from 'axios';

const api = axios.create({
  baseURL: 'http://192.168.100.4:5000',  // Change this to your Flask backend URL
});

export const loginUser = (username, password) => {
  return api.post('/login', { username, password });
};

export const registerAdmin = (username, password) => {
  return api.post('/register_admin', { username, password });
};

export const createDepartment = (token, departmentName) => {
  return api.post('/departments', { name: departmentName }, {
    headers: { 'x-access-token': token }
  });
};

export const getDepartments = (token) => {
  return api.get('/departments', {
    headers: { 'x-access-token': token }
  });
};

export const getDepartmentInfo = (token, departmentId) => {
  return api.get(`/departments/${departmentId}`, {
    headers: { 'x-access-token': token }
  });
};

export const sendMessage = (token, departmentId, content) => {
  return api.post(`/departments/${departmentId}/messages`, { content }, {
    headers: { 'x-access-token': token }
  });
};


const API_URL = 'http://localhost:8000/api';

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` })
    };
    
    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: { ...headers, ...options.headers }
    });
    
    if (response.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login.html';
        return null;
    }
    
    return response;
}

async function get(endpoint) {
    const response = await apiRequest(endpoint);
    if (!response) return null;
    return response.json();
}

async function post(endpoint, data) {
    const response = await apiRequest(endpoint, {
        method: 'POST',
        body: JSON.stringify(data)
    });
    if (!response) return null;
    return response.json();
}

async function put(endpoint, data) {
    const response = await apiRequest(endpoint, {
        method: 'PUT',
        body: JSON.stringify(data)
    });
    if (!response) return null;
    return response.json();
}

async function del(endpoint) {
    const response = await apiRequest(endpoint, { method: 'DELETE' });
    if (!response) return null;
    return response.ok;
}

async function login(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username: email, password })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Ошибка входа');
    }
    
    const data = await response.json();
    localStorage.setItem('token', data.access_token);
    return data;
}

async function register(email, password) {
    const response = await fetch(`${API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Ошибка регистрации');
    }
    
    return response.json();
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login.html';
}

function isAuthenticated() {
    return !!localStorage.getItem('token');
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

async function request(endpoint, { method = 'GET', data = null, headers = {} } = {}) {
  const token = localStorage.getItem('blindspot_token');
  
  const config = {
    method,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  };

  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  if (data) {
    config.body = JSON.stringify(data);
  }

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, config);
    const result = await response.json().catch(() => null);

    if (!response.ok) {
      const errorMessage = result?.error?.message || result?.detail || `Error ${response.status}: Failed request`;
      const errorCode = result?.error?.code || `HTTP_${response.status}`;
      return {
        success: false,
        error: { code: errorCode, message: errorMessage },
        status: response.status
      };
    }

    return result || { success: true, data: null };
  } catch (err) {
    console.error(`Network error on ${endpoint}:`, err);
    return {
      success: false,
      error: {
        code: 'NETWORK_ERROR',
        message: 'Cannot reach backend server. Please check your connection.'
      }
    };
  }
}

export const api = {
  // Health
  checkHealth: () => request('/health'),

  // Auth
  register: (name, email, password) => request('/auth/register', {
    method: 'POST',
    data: { name, email, password }
  }),
  login: (email, password) => request('/auth/login', {
    method: 'POST',
    data: { email, password }
  }),
  getMe: () => request('/auth/me'),

  // Analysis
  analyzeDecision: (decision, context, reasoning) => request('/analysis', {
    method: 'POST',
    data: { decision, context, reasoning }
  }),

  // Decisions / History
  getDecisions: () => request('/decisions'),
  getDecisionById: (id) => request(`/decisions/${id}`),

  // Dashboard
  getDashboard: () => request('/dashboard'),
};

export default api;

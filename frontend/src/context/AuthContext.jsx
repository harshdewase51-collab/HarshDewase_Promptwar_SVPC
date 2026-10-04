import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('blindspot_token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadUser() {
      if (token) {
        const response = await api.getMe();
        if (response.success && response.data) {
          setUser(response.data);
        } else {
          // Token invalid or expired
          logout();
        }
      }
      setLoading(false);
    }
    loadUser();
  }, [token]);

  const login = async (email, password) => {
    const response = await api.login(email, password);
    if (response.success && response.data) {
      const { access_token, user: userData } = response.data;
      localStorage.setItem('blindspot_token', access_token);
      setToken(access_token);
      setUser(userData);
      return { success: true };
    }
    return {
      success: false,
      error: response.error?.message || 'Login failed'
    };
  };

  const register = async (name, email, password) => {
    const response = await api.register(name, email, password);
    if (response.success && response.data) {
      const { access_token, user: userData } = response.data;
      localStorage.setItem('blindspot_token', access_token);
      setToken(access_token);
      setUser(userData);
      return { success: true };
    }
    return {
      success: false,
      error: response.error?.message || 'Registration failed'
    };
  };

  const logout = () => {
    localStorage.removeItem('blindspot_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

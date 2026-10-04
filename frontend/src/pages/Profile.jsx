import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import api from '../services/api';
import { 
  User, 
  Mail, 
  Shield, 
  Compass, 
  Sun, 
  Moon, 
  LogOut, 
  ArrowLeft, 
  CheckCircle2, 
  Calendar,
  Sparkles
} from 'lucide-react';

export function Profile() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme, isDark } = useTheme();
  const navigate = useNavigate();
  const [stats, setStats] = useState({ total_decisions: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      const res = await api.getDashboard();
      if (res.success && res.data) {
        setStats(res.data);
      }
      setLoading(false);
    }
    loadStats();
  }, []);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const getInitials = (name) => {
    if (!name) return 'U';
    return name
      .split(' ')
      .map(part => part[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="page-container max-w-4xl">
      <div className="profile-header mb-8">
        <Link to="/dashboard" className="btn-back mb-4">
          <ArrowLeft size={16} />
          <span>Back to Dashboard</span>
        </Link>
        <div className="flex items-center gap-3">
          <div className="profile-avatar-large">
            <span>{getInitials(user?.name)}</span>
          </div>
          <div>
            <h1 className="profile-name">{user?.name || 'Reasoning Architect'}</h1>
            <p className="profile-email text-muted flex items-center gap-1.5">
              <Mail size={14} />
              <span>{user?.email}</span>
            </p>
          </div>
        </div>
      </div>

      <div className="profile-grid">
        {/* Account Details Card */}
        <div className="content-card">
          <div className="card-section-title flex items-center gap-2 mb-4">
            <User size={18} className="text-cyan-400" />
            <h2>Account Information</h2>
          </div>
          <div className="profile-details-list">
            <div className="profile-detail-row">
              <span className="detail-label">Full Name</span>
              <span className="detail-value font-medium">{user?.name || 'Not provided'}</span>
            </div>
            <div className="profile-detail-row">
              <span className="detail-label">Email Address</span>
              <span className="detail-value font-medium">{user?.email}</span>
            </div>
            <div className="profile-detail-row">
              <span className="detail-label">Account Role</span>
              <span className="badge-pill bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                Decision Maker
              </span>
            </div>
            <div className="profile-detail-row">
              <span className="detail-label">Platform</span>
              <span className="detail-value font-medium flex items-center gap-1 text-emerald-400">
                <CheckCircle2 size={14} />
                <span>BlindSpot AI Verified</span>
              </span>
            </div>
          </div>
        </div>

        {/* Reasoning Stats Card */}
        <div className="content-card">
          <div className="card-section-title flex items-center gap-2 mb-4">
            <Compass size={18} className="text-amber-400" />
            <h2>Reasoning Statistics</h2>
          </div>
          <div className="profile-stats-grid">
            <div className="profile-stat-box">
              <span className="stat-number text-cyan-400">
                {loading ? '...' : stats.total_decisions}
              </span>
              <span className="stat-desc">Decisions Audited</span>
            </div>
            <div className="profile-stat-box">
              <span className="stat-number text-emerald-400">100%</span>
              <span className="stat-desc">Sovereignty Retained</span>
            </div>
          </div>
          <div className="sovereignty-badge-box mt-4">
            <Shield size={16} className="text-cyan-400 flex-shrink-0" />
            <p className="text-xs text-muted">
              Zero prescriptive control. BlindSpot AI evaluates logic gaps while you maintain full decision ownership.
            </p>
          </div>
        </div>

        {/* Preferences & Appearance Card */}
        <div className="content-card col-span-full">
          <div className="card-section-title flex items-center gap-2 mb-4">
            <Sparkles size={18} className="text-purple-400" />
            <h2>Display & Theme Preferences</h2>
          </div>
          <div className="theme-toggle-section">
            <div>
              <p className="font-semibold text-main">Appearance Theme</p>
              <p className="text-sm text-muted">
                Choose between dark mode for focused evening analysis or light mode for crisp daytime readability.
              </p>
            </div>
            <div className="theme-selector-pills">
              <button
                type="button"
                onClick={() => theme !== 'dark' && toggleTheme()}
                className={`theme-pill ${isDark ? 'active' : ''}`}
              >
                <Moon size={16} />
                <span>Dark Mode</span>
              </button>
              <button
                type="button"
                onClick={() => theme !== 'light' && toggleTheme()}
                className={`theme-pill ${!isDark ? 'active' : ''}`}
              >
                <Sun size={16} />
                <span>Light Mode</span>
              </button>
            </div>
          </div>
        </div>

        {/* Session Management */}
        <div className="content-card col-span-full border-rose-500/20">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="text-rose-400 font-semibold mb-1">Session Management</h3>
              <p className="text-sm text-muted">Sign out of your current BlindSpot AI reasoning session.</p>
            </div>
            <button
              type="button"
              onClick={handleLogout}
              className="btn-danger flex items-center gap-2"
            >
              <LogOut size={16} />
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;

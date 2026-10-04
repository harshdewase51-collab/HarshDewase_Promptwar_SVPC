import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Compass, PlusCircle, Clock, LayoutDashboard, LogOut, LogIn, User } from 'lucide-react';

export function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <header className="navbar">
      <div className="nav-container">
        <Link to={isAuthenticated ? "/dashboard" : "/"} className="nav-brand">
          <div className="brand-icon">
            <Compass size={22} className="text-cyan-400" />
          </div>
          <div>
            <span className="brand-title">MindLens</span>
            <span className="brand-tagline">Reasoning Auditor</span>
          </div>
        </Link>

        <nav className="nav-links">
          {isAuthenticated ? (
            <>
              <Link 
                to="/dashboard" 
                className={`nav-link ${isActive('/dashboard') ? 'active' : ''}`}
              >
                <LayoutDashboard size={18} />
                <span>Dashboard</span>
              </Link>
              <Link 
                to="/new-decision" 
                className={`nav-link ${isActive('/new-decision') ? 'active' : ''}`}
              >
                <PlusCircle size={18} />
                <span>New Audit</span>
              </Link>
              <Link 
                to="/history" 
                className={`nav-link ${isActive('/history') ? 'active' : ''}`}
              >
                <Clock size={18} />
                <span>History</span>
              </Link>

              <div className="nav-divider"></div>

              <div className="user-profile-badge">
                <User size={16} />
                <span className="user-name">{user?.name || user?.email}</span>
              </div>

              <button onClick={handleLogout} className="btn-logout" title="Sign Out">
                <LogOut size={16} />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <div className="auth-buttons">
              <Link to="/login" className="btn-secondary">
                <LogIn size={16} />
                <span>Login</span>
              </Link>
              <Link to="/register" className="btn-primary">
                <span>Sign Up</span>
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  );
}

export default Navbar;

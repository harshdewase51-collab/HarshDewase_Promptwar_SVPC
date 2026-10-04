import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { 
  Compass, 
  PlusCircle, 
  Clock, 
  LayoutDashboard, 
  LogOut, 
  LogIn, 
  User, 
  Sun, 
  Moon, 
  Menu, 
  X 
} from 'lucide-react';

export function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const { theme, toggleTheme, isDark } = useTheme();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    setMobileMenuOpen(false);
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  const closeMobileMenu = () => setMobileMenuOpen(false);

  return (
    <header className="navbar">
      <div className="nav-container">
        <Link to={isAuthenticated ? "/dashboard" : "/"} className="nav-brand" onClick={closeMobileMenu}>
          <div className="brand-icon">
            <Compass size={22} className="text-cyan-400" />
          </div>
          <div>
            <span className="brand-title">BLINDSPOT</span>
            <span className="brand-tagline">Reasoning Auditor</span>
          </div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="nav-links desktop-only">
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

              {/* Theme Toggle Button */}
              <button
                type="button"
                onClick={toggleTheme}
                className="btn-theme-toggle"
                title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
                aria-label="Toggle display theme"
              >
                {isDark ? <Sun size={17} className="text-amber-400" /> : <Moon size={17} className="text-indigo-400" />}
              </button>

              {/* Profile Link */}
              <Link 
                to="/profile" 
                className={`user-profile-badge ${isActive('/profile') ? 'active' : ''}`}
                title="View Profile"
              >
                <div className="user-avatar-mini">
                  <User size={14} />
                </div>
                <span className="user-name">{user?.name || user?.email?.split('@')[0] || 'Profile'}</span>
              </Link>

              <button onClick={handleLogout} className="btn-logout" title="Sign Out">
                <LogOut size={16} />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <div className="auth-buttons flex items-center gap-3">
              <button
                type="button"
                onClick={toggleTheme}
                className="btn-theme-toggle mr-1"
                title={isDark ? "Switch to Light Mode" : "Switch to Dark Mode"}
                aria-label="Toggle display theme"
              >
                {isDark ? <Sun size={17} className="text-amber-400" /> : <Moon size={17} className="text-indigo-400" />}
              </button>
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

        {/* Mobile Menu & Theme Toggle Controls */}
        <div className="mobile-controls mobile-only">
          <button
            type="button"
            onClick={toggleTheme}
            className="btn-theme-toggle"
            aria-label="Toggle display theme"
          >
            {isDark ? <Sun size={18} className="text-amber-400" /> : <Moon size={18} className="text-indigo-400" />}
          </button>
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="btn-mobile-menu"
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="mobile-nav-drawer mobile-only">
          {isAuthenticated ? (
            <div className="mobile-nav-items">
              <Link 
                to="/dashboard" 
                onClick={closeMobileMenu}
                className={`mobile-nav-link ${isActive('/dashboard') ? 'active' : ''}`}
              >
                <LayoutDashboard size={18} />
                <span>Dashboard</span>
              </Link>
              <Link 
                to="/new-decision" 
                onClick={closeMobileMenu}
                className={`mobile-nav-link ${isActive('/new-decision') ? 'active' : ''}`}
              >
                <PlusCircle size={18} />
                <span>New Audit</span>
              </Link>
              <Link 
                to="/history" 
                onClick={closeMobileMenu}
                className={`mobile-nav-link ${isActive('/history') ? 'active' : ''}`}
              >
                <Clock size={18} />
                <span>History</span>
              </Link>
              <Link 
                to="/profile" 
                onClick={closeMobileMenu}
                className={`mobile-nav-link ${isActive('/profile') ? 'active' : ''}`}
              >
                <User size={18} />
                <span>Profile ({user?.name || user?.email?.split('@')[0]})</span>
              </Link>
              <button onClick={handleLogout} className="mobile-nav-logout">
                <LogOut size={18} />
                <span>Logout</span>
              </button>
            </div>
          ) : (
            <div className="mobile-auth-links">
              <Link to="/login" onClick={closeMobileMenu} className="btn-secondary w-full text-center">
                <span>Login</span>
              </Link>
              <Link to="/register" onClick={closeMobileMenu} className="btn-primary w-full text-center">
                <span>Sign Up</span>
              </Link>
            </div>
          )}
        </div>
      )}
    </header>
  );
}

export default Navbar;

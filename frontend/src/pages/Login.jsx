import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  Compass, 
  AlertTriangle, 
  ArrowRight, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  Search, 
  Brain, 
  HelpCircle 
} from 'lucide-react';

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/dashboard';

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
    if (error) setError('');
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
    if (error) setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (isSubmitting) return;

    setError('');
    setIsSubmitting(true);

    try {
      const res = await login(email.trim(), password);
      setIsSubmitting(false);

      if (res.success) {
        navigate(from, { replace: true });
      } else {
        // Controlled, friendly presentation without exposing raw stack traces or internal secrets
        const rawMsg = res.error || '';
        let friendlyMessage = 'Invalid email or password';

        if (rawMsg.includes('reach backend') || rawMsg.includes('Network') || rawMsg.includes('connection')) {
          friendlyMessage = 'Cannot connect to authentication service. Please check your connection.';
        } else if (rawMsg.toLowerCase().includes('rate limit')) {
          friendlyMessage = 'Too many attempts. Please try again shortly.';
        } else if (rawMsg && !rawMsg.includes('HTTP_') && !rawMsg.includes('Traceback') && rawMsg.length < 60) {
          friendlyMessage = rawMsg;
        }

        setError(friendlyMessage);
      }
    } catch {
      setIsSubmitting(false);
      setError('An unexpected error occurred. Please try again.');
    }
  };

  const fillDemo = () => {
    setEmail('test@blindspot.ai');
    setPassword('password123');
    if (error) setError('');
  };

  return (
    <div className="login-split-page">
      <div className="login-split-container">
        
        {/* LEFT SIDE: Clean BLINDSPOT Brand & Value Points */}
        <div className="login-hero-pane">
          <div className="login-brand-tag">
            <Compass size={14} className="text-cyan-400" />
            <span>BLINDSPOT</span>
          </div>

          <h1 className="login-hero-headline">
            Challenge your thinking.
            <span className="headline-highlight">Before you decide.</span>
          </h1>

          <p className="login-hero-subtitle">
            AI that audits your reasoning — not your decision.
          </p>

          <div className="login-value-points">
            <div className="login-value-item">
              <span className="value-item-icon-box text-cyan-400">
                <Search size={16} />
              </span>
              <span>Evidence-linked analysis</span>
            </div>

            <div className="login-value-item">
              <span className="value-item-icon-box text-amber-400">
                <Brain size={16} />
              </span>
              <span>Assumption detection</span>
            </div>

            <div className="login-value-item">
              <span className="value-item-icon-box text-purple-400">
                <HelpCircle size={16} />
              </span>
              <span>Critical questions</span>
            </div>
          </div>
        </div>

        {/* RIGHT SIDE: Premium Login Card */}
        <div className="login-card-pane">
          <div className="login-card-header">
            <div className="login-logo-wrapper">
              <Compass size={24} className="text-cyan-400" />
            </div>
            <span className="auth-brand-name">BLINDSPOT</span>
            <h2>Welcome back</h2>
            <p className="login-card-subtitle">
              Continue auditing the reasoning behind your decisions.
            </p>
          </div>

          {/* Compact inline error banner */}
          {error && (
            <div className="compact-auth-alert" role="alert">
              <AlertTriangle size={15} className="flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="auth-form" noValidate={false}>
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <div className="input-with-icon-wrapper">
                <Mail size={17} className="input-field-icon" />
                <input
                  id="email"
                  type="email"
                  required
                  autoComplete="email"
                  placeholder="alex@example.com"
                  value={email}
                  onChange={handleEmailChange}
                  className="input-with-icon"
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="input-with-icon-wrapper">
                <Lock size={17} className="input-field-icon" />
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  autoComplete="current-password"
                  placeholder="••••••••"
                  value={password}
                  onChange={handlePasswordChange}
                  className="input-with-icon input-has-toggle"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="password-toggle-btn"
                  title={showPassword ? 'Hide password' : 'Show password'}
                  aria-label={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              className="btn-submit btn-login-primary"
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <span className="btn-loading-content">
                  <span className="spinner-small" />
                  <span>Signing in...</span>
                </span>
              ) : (
                <span className="btn-label-content">
                  <span>Sign In</span>
                  <ArrowRight size={17} />
                </span>
              )}
            </button>
          </form>

          {/* Quick Demo Fill Helper */}
          <div className="demo-credentials-box">
            <button 
              type="button" 
              onClick={fillDemo} 
              className="btn-demo"
              title="Populate demo credentials"
            >
              Use Demo Account (test@blindspot.ai)
            </button>
          </div>

          <div className="auth-footer">
            Don't have an account?{' '}
            <Link to="/register" className="auth-link">
              Create Account
            </Link>
          </div>
        </div>

      </div>
    </div>
  );
}

export default Login;

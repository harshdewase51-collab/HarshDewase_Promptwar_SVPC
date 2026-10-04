import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Compass, AlertCircle, ArrowRight } from 'lucide-react';

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/dashboard';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    const res = await login(email, password);
    setIsSubmitting(false);

    if (res.success) {
      navigate(from, { replace: true });
    } else {
      setError(res.error || 'Invalid credentials. Please try again.');
    }
  };

  const fillDemo = () => {
    setEmail('test@blindspot.ai');
    setPassword('password123');
    setError('');
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <div className="auth-header">
          <div className="auth-icon-badge">
            <Compass size={28} className="text-cyan-400" />
          </div>
          <span className="auth-brand-name">BLINDSPOT</span>
          <h2>Sign In to BlindSpot</h2>
          <p className="auth-tagline">“Challenge your reasoning. Own your decision.”</p>
          <p className="auth-subtitle">AI that audits your thinking — not your decision.</p>
        </div>

        {error && (
          <div className="alert-error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              required
              placeholder="alex@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              required
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="btn-submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Signing in...' : 'Sign In'}
            <ArrowRight size={18} />
          </button>
        </form>

        <div className="demo-credentials-box">
          <button type="button" onClick={fillDemo} className="btn-demo">
            Use Demo Account (test@blindspot.ai)
          </button>
        </div>

        <div className="auth-footer">
          Don't have an account?{' '}
          <Link to="/register" className="auth-link">
            Create an account
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Login;

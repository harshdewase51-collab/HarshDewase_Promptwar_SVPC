import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import NewDecision from './pages/NewDecision';
import AnalysisResult from './pages/AnalysisResult';
import History from './pages/History';
import Profile from './pages/Profile';
import { Compass, ArrowRight, ShieldCheck, Eye, Lightbulb, AlertTriangle, CheckCircle2 } from 'lucide-react';

function LandingPage() {
  const { isAuthenticated } = useAuth();
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="landing-page">
      <div className="landing-hero">
        <div className="badge-pill mb-4">
          <Compass size={14} className="text-cyan-400" />
          <span>BLINDSPOT • OBJECTIVE REASONING MIRROR</span>
        </div>
        
        <h1 className="hero-heading">
          AI that audits your thinking —<br />
          <span className="text-gradient">not your decision.</span>
        </h1>

        <p className="hero-tagline">
          “Challenge your reasoning. Own your decision.”
        </p>

        <p className="hero-subheading">
          BlindSpot AI doesn't tell you what decision to make. It examines your reasoning before you commit. Uncover evidence-linked blind spots, unstated assumptions, and hidden tensions in your logic.
        </p>

        <div className="hero-cta-group">
          <Link to="/new-decision" className="btn-primary-large">
            <span>Audit a Decision Now</span>
            <ArrowRight size={20} />
          </Link>
          <Link to="/login" className="btn-secondary-large">
            <span>Sign In to Track History</span>
          </Link>
        </div>

        <div className="trust-indicators-row">
          <span className="trust-indicator-item">
            <CheckCircle2 size={16} className="text-emerald-400" />
            <span>Zero Prescriptive Directives</span>
          </span>
          <span className="trust-indicator-item">
            <CheckCircle2 size={16} className="text-cyan-400" />
            <span>Evidence-Linked Traceability</span>
          </span>
          <span className="trust-indicator-item">
            <CheckCircle2 size={16} className="text-purple-400" />
            <span>100% User Sovereignty</span>
          </span>
        </div>
      </div>

      <div className="features-preview-grid">
        <div className="feature-card">
          <Eye size={28} className="text-amber-400 mb-3" />
          <h3>Evidence-Linked Blind Spots</h3>
          <p>Flags unaddressed realities and overlooked operational dimensions grounded strictly in your words or explicit omissions.</p>
        </div>
        <div className="feature-card">
          <Lightbulb size={28} className="text-cyan-400 mb-3" />
          <h3>Assumption Verification</h3>
          <p>Surfaces unstated causal premises and provides concrete, actionable questions to verify them in the real world.</p>
        </div>
        <div className="feature-card">
          <AlertTriangle size={28} className="text-purple-400 mb-3" />
          <h3>Potential Tension Detection</h3>
          <p>Identifies internal conflicts between your stated priorities and justifications using cautious, non-judgmental framing.</p>
        </div>
        <div className="feature-card">
          <ShieldCheck size={28} className="text-emerald-400 mb-3" />
          <h3>Now You Decide</h3>
          <p>No sycophancy. No generic chatbot advice. BlindSpot stress-tests your logic, leaving the final choice entirely in your hands.</p>
        </div>
      </div>
    </div>
  );
}

export function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <div className="app-shell">
            <Navbar />
            <main className="main-content">
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/new-decision" element={<NewDecision />} />
                <Route path="/new" element={<Navigate to="/new-decision" replace />} />
                <Route path="/analysis/:id" element={<AnalysisResult />} />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/history"
                  element={
                    <ProtectedRoute>
                      <History />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/profile"
                  element={
                    <ProtectedRoute>
                      <Profile />
                    </ProtectedRoute>
                  }
                />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </main>
            <footer className="app-footer">
              <div className="footer-content">
                <div className="footer-brand-row">
                  <span className="footer-brand">BLINDSPOT AI</span>
                  <span className="footer-tagline">“Challenge your reasoning. Own your decision.”</span>
                </div>
                <p className="footer-disclaimer">
                  BlindSpot AI doesn't tell you what decision to make. It examines your reasoning before you commit.
                </p>
              </div>
            </footer>
          </div>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;

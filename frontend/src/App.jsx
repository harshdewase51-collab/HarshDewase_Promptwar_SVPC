import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import NewDecision from './pages/NewDecision';
import AnalysisResult from './pages/AnalysisResult';
import History from './pages/History';
import { Compass, ArrowRight, ShieldCheck, Eye, Lightbulb, AlertTriangle } from 'lucide-react';

function LandingPage() {
  const { isAuthenticated } = useAuth();
  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div className="landing-page">
      <div className="landing-hero">
        <div className="badge-pill">
          <span>The Blind Spot Hackathon Solution</span>
        </div>
        <h1 className="hero-heading">
          We don't make the decision for you.<br />
          <span className="text-gradient">We audit the reasoning behind it.</span>
        </h1>
        <p className="hero-subheading">
          MindLens is an objective, non-prescriptive AI mirror. Before you commit to a high-stakes internship, career move, or major purchase, uncover evidence-linked blind spots and unexamined assumptions in your logic.
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
      </div>

      <div className="features-preview-grid">
        <div className="feature-card">
          <Eye size={28} className="text-amber-400 mb-3" />
          <h3>Evidence-Linked Blind Spots</h3>
          <p>Flags unaddressed realities grounded directly in what you wrote or omitted.</p>
        </div>
        <div className="feature-card">
          <Lightbulb size={28} className="text-cyan-400 mb-3" />
          <h3>Assumption Verification</h3>
          <p>Surfaces unstated premises and provides actionable real-world ways to test them.</p>
        </div>
        <div className="feature-card">
          <AlertTriangle size={28} className="text-purple-400 mb-3" />
          <h3>Potential Tension Detection</h3>
          <p>Identifies possible conflicts between your goals and rationale using cautious framing.</p>
        </div>
        <div className="feature-card">
          <ShieldCheck size={28} className="text-emerald-400 mb-3" />
          <h3>User Sovereignty</h3>
          <p>Zero sycophancy. Zero prescriptive orders. You always make the final choice.</p>
        </div>
      </div>
    </div>
  );
}

export function App() {
  return (
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
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          <footer className="app-footer">
            <div className="footer-content">
              <span>MindLens (BlindSpot AI) • Built for the Blind Spot Hackathon</span>
              <span className="footer-disclaimer">
                "BlindSpot AI doesn't tell you what decision to make; it tells you what you might be missing before you make it."
              </span>
            </div>
          </footer>
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;

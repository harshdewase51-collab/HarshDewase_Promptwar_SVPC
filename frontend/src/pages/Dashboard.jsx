import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { PlusCircle, Compass, Clock, ArrowRight, ShieldCheck, Sparkles, AlertCircle } from 'lucide-react';

export function Dashboard() {
  const { user } = useAuth();
  const [data, setData] = useState({ total_decisions: 0, recent_decisions: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchDashboard() {
      const res = await api.getDashboard();
      if (res.success && res.data) {
        setData(res.data);
      } else {
        setError(res.error?.message || 'Failed to load dashboard metrics');
      }
      setLoading(false);
    }
    fetchDashboard();
  }, []);

  const greetingName = user?.name ? user.name.split(' ')[0] : 'Decision Maker';

  return (
    <div className="page-container">
      {/* Dashboard Greeting & Primary Action Hero */}
      <div className="dashboard-hero">
        <div className="hero-text">
          <div className="greeting-badge">
            <Sparkles size={14} className="text-cyan-400" />
            <span>Welcome back, {greetingName}</span>
          </div>
          <h1 className="dashboard-heading">Reasoning Audit Dashboard</h1>
          <p className="hero-subtitle">
            “BlindSpot AI doesn't tell you what decision to make. It examines your reasoning before you commit.”
          </p>
        </div>
        
        {/* Main CTA: Prominently styled */}
        <Link to="/new-decision" className="btn-primary-large btn-cta-glow">
          <PlusCircle size={22} />
          <span>+ New Decision Audit</span>
        </Link>
      </div>

      {/* Decision Statistics Grid */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon-wrapper text-cyan-400">
            <Compass size={24} />
          </div>
          <div>
            <div className="stat-value">{loading ? '...' : data.total_decisions}</div>
            <div className="stat-label">Total Decisions Audited</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon-wrapper text-emerald-400">
            <ShieldCheck size={24} />
          </div>
          <div>
            <div className="stat-value">100%</div>
            <div className="stat-label">Decision Sovereignty Retained</div>
          </div>
        </div>
      </div>

      {/* Recent Decisions Section */}
      <div className="content-card">
        <div className="content-card-header">
          <div className="flex items-center gap-2">
            <Clock size={20} className="text-cyan-400" />
            <h2>Recent Decision Audits</h2>
          </div>
          {data.recent_decisions?.length > 0 && (
            <Link to="/history" className="link-subtle">
              <span>View All History</span>
              <ArrowRight size={16} />
            </Link>
          )}
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading decision history...</p>
          </div>
        ) : error ? (
          <div className="alert-error flex items-center gap-2">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        ) : data.recent_decisions?.length === 0 ? (
          <div className="empty-state">
            <Compass size={48} className="empty-icon text-muted" />
            <h3>No Decisions Audited Yet</h3>
            <p>
              Before making your next high-stakes internship, career move, or major purchase, run your reasoning through BlindSpot.
            </p>
            <Link to="/new-decision" className="btn-primary mt-4">
              <PlusCircle size={18} />
              <span>+ New Decision Audit</span>
            </Link>
          </div>
        ) : (
          <div className="decision-list">
            {data.recent_decisions.map((item) => (
              <div key={item.id} className="decision-card-item">
                <div className="decision-info">
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <h3 className="decision-title">{item.decision}</h3>
                    <span className="badge-audited">Audited</span>
                  </div>
                  <p className="decision-reasoning-preview">
                    <strong>Reasoning:</strong> {item.reasoning}
                  </p>
                  <span className="decision-date">
                    {new Date(item.created_at).toLocaleDateString(undefined, {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                </div>
                <div className="decision-action-wrapper">
                  <Link to={`/analysis/${item.id}`} className="btn-secondary whitespace-nowrap">
                    <span>View Analysis</span>
                    <ArrowRight size={16} />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;

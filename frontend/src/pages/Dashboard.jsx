import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { PlusCircle, Compass, Clock, ArrowRight, ShieldCheck } from 'lucide-react';

export function Dashboard() {
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

  return (
    <div className="page-container">
      <div className="dashboard-hero">
        <div className="hero-text">
          <h1>Reasoning Audit Dashboard</h1>
          <p className="hero-subtitle">
            “We don't make the decision for you. We audit the reasoning behind your decision.”
          </p>
        </div>
        <Link to="/new-decision" className="btn-primary-large">
          <PlusCircle size={20} />
          <span>Audit New Decision</span>
        </Link>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon-wrapper text-cyan-400">
            <Compass size={24} />
          </div>
          <div>
            <div className="stat-value">{data.total_decisions}</div>
            <div className="stat-label">Total Decisions Audited</div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon-wrapper text-emerald-400">
            <ShieldCheck size={24} />
          </div>
          <div>
            <div className="stat-value">100%</div>
            <div className="stat-label">Decision Ownership Retained</div>
          </div>
        </div>
      </div>

      <div className="content-card">
        <div className="content-card-header">
          <div className="flex items-center gap-2">
            <Clock size={20} className="text-cyan-400" />
            <h2>Recent Decision Audits</h2>
          </div>
          {data.recent_decisions?.length > 0 && (
            <Link to="/history" className="link-subtle">
              View All History <ArrowRight size={16} />
            </Link>
          )}
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading decision history...</p>
          </div>
        ) : error ? (
          <div className="alert-error">{error}</div>
        ) : data.recent_decisions?.length === 0 ? (
          <div className="empty-state">
            <Compass size={48} className="empty-icon text-gray-500" />
            <h3>No Decisions Audited Yet</h3>
            <p>
              Before making your next important academic, career, or financial move, run your reasoning through MindLens.
            </p>
            <Link to="/new-decision" className="btn-primary">
              <PlusCircle size={18} />
              <span>Audit Your First Decision</span>
            </Link>
          </div>
        ) : (
          <div className="decision-list">
            {data.recent_decisions.map((item) => (
              <div key={item.id} className="decision-card-item">
                <div className="decision-info">
                  <h3 className="decision-title">{item.decision}</h3>
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
                <Link to={`/analysis/${item.id}`} className="btn-secondary">
                  <span>View Audit</span>
                  <ArrowRight size={16} />
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;

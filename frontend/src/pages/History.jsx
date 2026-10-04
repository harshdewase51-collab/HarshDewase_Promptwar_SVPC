import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { Clock, PlusCircle, ArrowRight, Search } from 'lucide-react';

export function History() {
  const [decisions, setDecisions] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadHistory() {
      const res = await api.getDecisions();
      if (res.success && res.data) {
        setDecisions(res.data);
      } else {
        setError(res.error?.message || 'Failed to load decision history');
      }
      setLoading(false);
    }
    loadHistory();
  }, []);

  const filteredDecisions = decisions.filter(d => 
    d.decision.toLowerCase().includes(searchTerm.toLowerCase()) ||
    d.reasoning.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="page-container">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h1>Decision Audit History</h1>
          <p className="subtitle">Review your past decision inquiries and reasoning diagnostics</p>
        </div>
        <Link to="/new-decision" className="btn-primary">
          <PlusCircle size={18} />
          <span>New Audit</span>
        </Link>
      </div>

      <div className="search-bar-wrapper mb-6">
        <Search size={18} className="search-icon" />
        <input
          type="text"
          placeholder="Search previous decisions or reasoning..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p className="mt-4 text-gray-400">Loading your history...</p>
        </div>
      ) : error ? (
        <div className="alert-error">{error}</div>
      ) : filteredDecisions.length === 0 ? (
        <div className="empty-state">
          <Clock size={48} className="empty-icon text-gray-500" />
          <h3>No Decisions Found</h3>
          <p>
            {searchTerm 
              ? "No decision records match your search criteria." 
              : "You haven't audited any decisions yet. Run your first reasoning audit to start building your reflective history."}
          </p>
          <Link to="/new-decision" className="btn-primary mt-4">
            <PlusCircle size={18} />
            <span>Audit a Decision</span>
          </Link>
        </div>
      ) : (
        <div className="history-grid">
          {filteredDecisions.map((item) => (
            <div key={item.id} className="history-card">
              <div className="history-card-body">
                <div className="flex justify-between items-start mb-2">
                  <span className="history-date">
                    {new Date(item.created_at).toLocaleDateString(undefined, {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric'
                    })}
                  </span>
                  <span className="badge-audited">Audited</span>
                </div>
                <h3 className="history-decision-title">{item.decision}</h3>
                {item.context && (
                  <p className="history-context-text">
                    <strong>Context:</strong> {item.context}
                  </p>
                )}
                <p className="history-reasoning-preview">
                  <strong>Reasoning:</strong> {item.reasoning}
                </p>
              </div>
              <div className="history-card-footer">
                <Link to={`/analysis/${item.id}`} className="btn-view-audit">
                  <span>View Analysis</span>
                  <ArrowRight size={16} />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default History;

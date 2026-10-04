import React, { useState, useEffect } from 'react';
import { useParams, useLocation, Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { 
  Eye, 
  Lightbulb, 
  CheckSquare, 
  AlertTriangle, 
  Layers, 
  HelpCircle, 
  ArrowLeft, 
  PlusCircle, 
  ShieldCheck,
  Share2,
  Check,
  ChevronDown,
  GitCommit
} from 'lucide-react';

function TraceDrawer({ trace }) {
  const [open, setOpen] = useState(false);
  if (!trace) return null;

  return (
    <div className="trace-accordion">
      <button 
        type="button" 
        onClick={() => setOpen(!open)} 
        className="trace-toggle-btn"
      >
        <span className="flex items-center gap-1.5 font-semibold text-cyan-400">
          <GitCommit size={14} />
          <span>Why did we identify this? (Why Detected)</span>
        </span>
        <ChevronDown size={16} className={`transition-transform duration-200 ${open ? 'rotate-180' : ''}`} />
      </button>

      {open && (
        <div className="trace-drawer-body">
          <div className="trace-chain-visual">
            <span className="chain-step">Trigger</span>
            <span className="chain-arrow">→</span>
            <span className="chain-step">Considered</span>
            <span className="chain-arrow">→</span>
            <span className="chain-step">Missing / Weak</span>
            <span className="chain-arrow">→</span>
            <span className="chain-step">Relevance</span>
          </div>

          <div className="trace-grid">
            <div className="trace-item">
              <span className="trace-label">Trigger (In Your Words):</span>
              <p className="trace-value text-amber-200">"{trace.trigger}"</p>
            </div>

            {trace.considered_factor && (
              <div className="trace-item">
                <span className="trace-label">You Considered:</span>
                <p className="trace-value text-slate-300">{trace.considered_factor}</p>
              </div>
            )}

            {trace.missing_or_weak_factor && (
              <div className="trace-item">
                <span className="trace-label">Potentially Missing / Weak:</span>
                <p className="trace-value text-rose-300 font-medium">{trace.missing_or_weak_factor}</p>
              </div>
            )}

            {trace.first_reasoning_point && (
              <div className="trace-item">
                <span className="trace-label">Stated Priority A:</span>
                <p className="trace-value text-purple-300">{trace.first_reasoning_point}</p>
              </div>
            )}

            {trace.second_reasoning_point && (
              <div className="trace-item">
                <span className="trace-label">Tension Factor B:</span>
                <p className="trace-value text-purple-300">{trace.second_reasoning_point}</p>
              </div>
            )}

            <div className="trace-item col-span-full">
              <span className="trace-label">Why It Matters to This Decision:</span>
              <p className="trace-value text-cyan-200">{trace.why_relevant}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export function AnalysisResult() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [audit, setAudit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    // 1. Check if passed via location state
    if (location.state?.auditData) {
      setAudit(location.state.auditData);
      setLoading(false);
      return;
    }

    // 2. Otherwise fetch from backend via id
    if (id && id !== 'preview') {
      async function loadDecision() {
        const res = await api.getDecisionById(id);
        if (res.success && res.data) {
          setAudit({
            decision: res.data.decision,
            context: res.data.context,
            reasoning: res.data.reasoning,
            analysis: res.data.analysis
          });
        } else {
          setError(res.error?.message || 'Could not load decision audit.');
        }
        setLoading(false);
      }
      loadDecision();
    } else {
      setLoading(false);
      setError('No audit data available. Please submit a new decision.');
    }
  }, [id, location.state]);

  const handleCopy = () => {
    if (!audit) return;
    const text = `BLINDSPOT AI AUDIT SUMMARY
DECISION: ${audit.decision}
REASONING: ${audit.reasoning}

BLIND SPOTS:
${audit.analysis?.blind_spots?.map(b => `- ${b.finding} (Evidence: ${b.evidence})`).join('\n')}

ASSUMPTIONS:
${audit.analysis?.assumptions?.map(a => `- ${a.assumption}`).join('\n')}

VERIFICATIONS:
${audit.analysis?.verification?.map(v => `- ${v.assumption}: ${v.verification}`).join('\n')}

POTENTIAL CONFLICTS:
${audit.analysis?.potential_conflicts?.map(c => `- ${c.conflict} (Question: ${c.question})`).join('\n')}

MISSING FACTORS:
${audit.analysis?.missing_factors?.map(m => `- ${m}`).join('\n')}

CRITICAL QUESTIONS:
${audit.analysis?.critical_questions?.map(q => `- ${q}`).join('\n')}
`;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  if (loading) {
    return (
      <div className="page-container loading-container">
        <div className="spinner"></div>
        <p className="mt-4 text-gray-400">Loading audit findings...</p>
      </div>
    );
  }

  if (error || !audit) {
    return (
      <div className="page-container max-w-3xl">
        <div className="alert-error mb-6">{error}</div>
        <Link to="/new-decision" className="btn-primary">
          <PlusCircle size={18} />
          <span>Audit a Decision</span>
        </Link>
      </div>
    );
  }

  const { decision, context, reasoning, analysis } = audit;

  return (
    <div className="page-container max-w-5xl">
      {/* Top Navigation Row */}
      <div className="audit-nav-row">
        <button onClick={() => navigate(-1)} className="btn-back">
          <ArrowLeft size={16} />
          <span>Back</span>
        </button>

        <div className="audit-actions">
          <button onClick={handleCopy} className="btn-copy">
            {copied ? <Check size={16} className="text-emerald-400" /> : <Share2 size={16} />}
            <span>{copied ? 'Copied Summary!' : 'Copy Summary'}</span>
          </button>
          <Link to="/new-decision" className="btn-primary-small">
            <PlusCircle size={16} />
            <span>New Decision</span>
          </Link>
        </div>
      </div>

      {/* Decision & Reasoning Overview Header */}
      <div className="decision-header-card">
        <div className="header-meta-badge">AUDIT SUBJECT</div>
        <div className="grid md:grid-cols-2 gap-6 mt-3">
          <div>
            <h3 className="section-label">YOUR DECISION</h3>
            <p className="decision-text">{decision}</p>
            {context && (
              <div className="mt-3">
                <span className="context-label">Context / Constraints:</span>
                <p className="context-text">{context}</p>
              </div>
            )}
          </div>
          <div className="reasoning-box">
            <h3 className="section-label">YOUR REASONING</h3>
            <p className="reasoning-text">"{reasoning}"</p>
          </div>
        </div>
      </div>

      {/* 6 Audit Categories */}
      <div className="audit-grid">
        {/* 1. Evidence-Linked Blind Spots */}
        <div className="audit-category-card border-amber-500/30">
          <div className="category-header text-amber-400">
            <Eye size={22} />
            <h2>1. Evidence-Linked Blind Spots</h2>
          </div>
          <p className="category-desc">Critical aspects omitted or overlooked relative to your stated rationale.</p>
          
          <div className="category-content-list">
            {analysis?.blind_spots?.length > 0 ? (
              analysis.blind_spots.map((item, idx) => (
                <div key={idx} className="finding-item">
                  <h4 className="finding-title">{item.finding}</h4>
                  <div className="evidence-pill">
                    <strong>Grounded Evidence:</strong> {item.evidence}
                  </div>
                  <p className="why-it-matters">
                    <strong>Why it matters:</strong> {item.why_it_matters}
                  </p>
                  <TraceDrawer trace={item.trace} />
                </div>
              ))
            ) : (
              <p className="empty-category-text">No overt blind spots detected in provided text.</p>
            )}
          </div>
        </div>

        {/* 2. Hidden Assumptions */}
        <div className="audit-category-card border-blue-500/30">
          <div className="category-header text-cyan-400">
            <Lightbulb size={22} />
            <h2>2. Hidden Assumptions</h2>
          </div>
          <p className="category-desc">Unverified premises your reasoning assumes to be automatically true.</p>

          <div className="category-content-list">
            {analysis?.assumptions?.length > 0 ? (
              analysis.assumptions.map((item, idx) => (
                <div key={idx} className="assumption-item">
                  <div className="flex justify-between items-start gap-2">
                    <p className="assumption-text">"{item.assumption}"</p>
                    {item.needs_verification && (
                      <span className="badge-needs-verify">Needs Verification</span>
                    )}
                  </div>
                  <p className="evidence-note">
                    <strong>Based on:</strong> {item.evidence}
                  </p>
                  <TraceDrawer trace={item.trace} />
                </div>
              ))
            ) : (
              <p className="empty-category-text">No unstated assumptions flagged.</p>
            )}
          </div>
        </div>

        {/* 3. How to Verify */}
        <div className="audit-category-card border-emerald-500/30">
          <div className="category-header text-emerald-400">
            <CheckSquare size={22} />
            <h2>3. How to Verify Assumptions</h2>
          </div>
          <p className="category-desc">Actionable real-world steps and inquiries to test your premises before committing.</p>

          <div className="category-content-list">
            {analysis?.verification?.length > 0 ? (
              analysis.verification.map((item, idx) => (
                <div key={idx} className="verification-item">
                  <p className="verify-target">
                    <strong>Assumption:</strong> {item.assumption}
                  </p>
                  <div className="verify-action-box">
                    <CheckSquare size={16} className="text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span>{item.verification}</span>
                  </div>
                </div>
              ))
            ) : (
              <p className="empty-category-text">No verification steps required.</p>
            )}
          </div>
        </div>

        {/* 4. Potential Conflicts & Tensions */}
        <div className="audit-category-card border-purple-500/30">
          <div className="category-header text-purple-400">
            <AlertTriangle size={22} />
            <h2>4. Potential Conflicts & Tensions</h2>
          </div>
          <p className="category-desc">Possible frictions or trade-offs between your priorities and rationale.</p>

          <div className="category-content-list">
            {analysis?.potential_conflicts?.length > 0 ? (
              analysis.potential_conflicts.map((item, idx) => (
                <div key={idx} className="conflict-item">
                  <p className="conflict-text">{item.conflict}</p>
                  <p className="conflict-evidence">
                    <strong>Observed Evidence:</strong> {item.evidence}
                  </p>
                  <div className="conflict-question-box">
                    <strong>Question to evaluate:</strong> {item.question}
                  </div>
                  <TraceDrawer trace={item.trace} />
                </div>
              ))
            ) : (
              <p className="empty-category-text">No obvious tensions detected.</p>
            )}
          </div>
        </div>

        {/* 5. Context-Specific Missing Factors */}
        <div className="audit-category-card border-teal-500/30">
          <div className="category-header text-teal-400">
            <Layers size={22} />
            <h2>5. Context-Specific Missing Factors</h2>
          </div>
          <p className="category-desc">Relevant operational and personal dimensions missing from this decision context.</p>

          <ul className="missing-factors-list">
            {analysis?.missing_factors?.length > 0 ? (
              analysis.missing_factors.map((factor, idx) => (
                <li key={idx} className="missing-factor-item">
                  <span className="bullet text-teal-400">•</span>
                  <span>{factor}</span>
                </li>
              ))
            ) : (
              <p className="empty-category-text">No key factors omitted.</p>
            )}
          </ul>
        </div>

        {/* 6. Critical Questions */}
        <div className="audit-category-card border-indigo-500/30">
          <div className="category-header text-indigo-400">
            <HelpCircle size={22} />
            <h2>6. Critical Questions to Consider</h2>
          </div>
          <p className="category-desc">Reflective prompts designed to expand your thinking before making your choice.</p>

          <div className="questions-list">
            {analysis?.critical_questions?.length > 0 ? (
              analysis.critical_questions.map((q, idx) => (
                <div key={idx} className="question-item">
                  <span className="question-number">Q{idx + 1}</span>
                  <p className="question-text">{q}</p>
                </div>
              ))
            ) : (
              <p className="empty-category-text">No critical questions generated.</p>
            )}
          </div>
        </div>
      </div>

      {/* Prominent Sovereignty Banner: NOW YOU DECIDE */}
      <div className="decision-sovereignty-banner">
        <div className="banner-icon-badge">
          <ShieldCheck size={32} className="text-cyan-400" />
        </div>
        <div>
          <h2 className="banner-title">NOW YOU DECIDE.</h2>
          <p className="banner-text">
            BlindSpot AI doesn't tell you what decision to make. It examines your reasoning before you commit.
            The final decision and ownership always belongs to you.
          </p>
        </div>
        <Link to="/new-decision" className="btn-primary-large">
          Audit Another Decision
        </Link>
      </div>
    </div>
  );
}

export default AnalysisResult;

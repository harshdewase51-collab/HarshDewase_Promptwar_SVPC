import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { Compass, Sparkles, AlertCircle, ArrowRight, CheckCircle2 } from 'lucide-react';

const PRESETS = [
  {
    title: '🎓 6-Month Internship Dilemma',
    decision: 'Accept a 6-month startup internship instead of completing my university semester on schedule.',
    context: 'Senior computer science student with 2 semesters remaining. The startup has 4 engineers. Monthly stipend is $3,500.',
    reasoning: 'The stipend is good and having real-world startup experience on my resume will guarantee higher-paying job offers later regardless of my graduation date.'
  },
  {
    title: '💻 High-End Laptop Purchase',
    decision: 'Purchase a $2,800 flagship laptop using credit installments.',
    context: 'Freelance frontend developer with a functional 3-year-old mid-tier laptop. Savings are around $4,000.',
    reasoning: 'The new device has top-tier benchmark speeds and an OLED screen which will immediately boost my productivity and earn back its cost in client work.'
  },
  {
    title: '🚀 Seed Startup vs Big Tech Offer',
    decision: 'Join a 5-person seed-funded startup as founding engineer instead of taking an established Big Tech offer.',
    context: '3 years of software engineering experience. Big Tech offer is $160k base with liquid RSUs; startup offer is $105k base with 1.2% equity.',
    reasoning: 'I want rapid career growth and leadership responsibility. Startups move faster and the equity upside will far outpace a corporate salary.'
  }
];

export function NewDecision() {
  const [decision, setDecision] = useState('');
  const [context, setContext] = useState('');
  const [reasoning, setReasoning] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStage, setLoadingStage] = useState('');
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const handleSelectPreset = (preset) => {
    setDecision(preset.decision);
    setContext(preset.context);
    setReasoning(preset.reasoning);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (decision.trim().length < 3) {
      setError('Please provide a specific decision you are considering.');
      return;
    }
    if (reasoning.trim().length < 5) {
      setError('Please detail your reasoning behind this choice so the AI can audit it.');
      return;
    }

    setLoading(true);
    setLoadingStage('Auditing rationale structure...');

    const timer1 = setTimeout(() => setLoadingStage('Evaluating evidence-linked blind spots...'), 1200);
    const timer2 = setTimeout(() => setLoadingStage('Scanning hidden assumptions and tensions...'), 2400);

    const res = await api.analyzeDecision(decision.trim(), context.trim(), reasoning.trim());

    clearTimeout(timer1);
    clearTimeout(timer2);
    setLoading(false);

    if (res.success && res.data) {
      const { decision_id, analysis } = res.data;
      if (decision_id) {
        navigate(`/analysis/${decision_id}`, { state: { auditData: res.data } });
      } else {
        // If anonymous, pass in location state
        navigate('/analysis/preview', { state: { auditData: res.data } });
      }
    } else {
      setError(res.error?.message || 'Failed to complete the reasoning audit. Please try again.');
    }
  };

  return (
    <div className="page-container max-w-4xl">
      <div className="form-header">
        <div className="flex items-center gap-2 text-cyan-400 font-semibold mb-2">
          <Compass size={22} />
          <span>REASONING AUDIT ENGINE</span>
        </div>
        <h1>Audit Your Decision</h1>
        <p className="subtitle">
          BlindSpot AI doesn't tell you what decision to make. It examines your premises, assumptions, and potential conflicts before you commit.
        </p>
      </div>

      <div className="presets-container">
        <span className="presets-label">
          <Sparkles size={16} className="text-amber-400" />
          <span>Quick Demo Presets:</span>
        </span>
        <div className="presets-pills">
          {PRESETS.map((p, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSelectPreset(p)}
              className="btn-preset"
            >
              {p.title}
            </button>
          ))}
        </div>
      </div>

      {error && (
        <div className="alert-error mb-6">
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="audit-form-card">
        <div className="form-field">
          <div className="field-header">
            <label htmlFor="decision">What decision are you considering?</label>
            <span className="field-badge required">Required</span>
          </div>
          <p className="field-hint">State the concrete action or choice being evaluated.</p>
          <textarea
            id="decision"
            rows={2}
            required
            value={decision}
            onChange={(e) => setDecision(e.target.value)}
            placeholder="e.g., Accept a 6-month startup internship instead of finishing college on schedule."
          />
        </div>

        <div className="form-field">
          <div className="field-header">
            <label htmlFor="context">Context & Constraints</label>
            <span className="field-badge optional">Optional</span>
          </div>
          <p className="field-hint">Background situation, timeline, financial constraints, team size, stakes.</p>
          <textarea
            id="context"
            rows={3}
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="e.g., Senior CS student with 2 semesters left. The startup has 4 engineers. Stipend is $3,500/mo."
          />
        </div>

        <div className="form-field">
          <div className="field-header">
            <label htmlFor="reasoning">My Reasoning</label>
            <span className="field-badge required">Required</span>
          </div>
          <p className="field-hint">Why do you believe this is the right move? What assumptions are you relying on?</p>
          <textarea
            id="reasoning"
            rows={4}
            required
            value={reasoning}
            onChange={(e) => setReasoning(e.target.value)}
            placeholder="e.g., The stipend is great and having real startup experience on my resume will guarantee higher-paying job offers later."
          />
        </div>

        <div className="form-submit-row">
          <div className="trust-reminder">
            <CheckCircle2 size={16} className="text-cyan-400" />
            <span>AI audits your logic; it never tells you what to choose.</span>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-audit-submit"
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <div className="spinner-small"></div>
                <span>{loadingStage || 'Auditing reasoning...'}</span>
              </div>
            ) : (
              <>
                <span>Audit My Reasoning</span>
                <ArrowRight size={18} />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}

export default NewDecision;

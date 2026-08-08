export default function FeedbackReport({ feedback, onRestart }) {
  if (!feedback) return null;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', overflowY: 'auto', flex: 1 }}>
      <div className="feedback-container">
        
        <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem' }}>
            <div style={{ width: '48px', height: '48px', borderRadius: '12px', background: 'var(--accent-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 25px var(--accent-glow)' }}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
            </div>
          </div>
          <h1 style={{ fontSize: '3rem', background: 'linear-gradient(135deg, #fff 0%, #a1a1aa 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', letterSpacing: '-0.02em', marginBottom: '0.5rem' }}>Assessment Complete</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem' }}>Candidate Evaluation Profile Generated</p>
        </div>

        <div className="glass-panel" style={{ padding: '2.5rem', marginBottom: '2rem', borderTop: '2px solid var(--accent-color)' }}>
          <h3 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
            Executive Summary
          </h3>
          <p style={{ fontSize: '1.15rem', color: 'var(--text-primary)', lineHeight: '1.7' }}>{feedback.summary}</p>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1.5rem', marginBottom: '3rem' }}>
          <div className="glass-panel" style={{ padding: '2rem 1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--text-primary)', fontFamily: 'var(--font-display)', marginBottom: '0.5rem' }}>{feedback.questions_completed || 0}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Questions Covered</div>
          </div>
          <div className="glass-panel" style={{ padding: '2rem 1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--text-primary)', fontFamily: 'var(--font-display)', marginBottom: '0.5rem' }}>{feedback.curriculum_areas_assessed || 0}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Curriculum Nodes</div>
          </div>
          <div className="glass-panel" style={{ padding: '2rem 1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '2.5rem', fontWeight: '700', color: 'var(--text-primary)', fontFamily: 'var(--font-display)', marginBottom: '0.5rem' }}>{feedback.adaptive_follow_ups || 0}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Adaptive Pivots</div>
          </div>
        </div>

        <div className="feedback-grid">
          <div className="feedback-card" style={{ borderTop: '2px solid var(--success)' }}>
            <h3>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--success)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Verified Strengths
            </h3>
            <ul className="feedback-list strengths">
              {feedback.strengths && feedback.strengths.length > 0 ? (
                feedback.strengths.map((str, idx) => (
                  <li key={idx}>{str}</li>
                ))
              ) : (
                <li style={{ color: 'var(--text-muted)' }}>No particular strengths highlighted.</li>
              )}
            </ul>
          </div>
          
          <div className="feedback-card" style={{ borderTop: '2px solid var(--warning)' }}>
            <h3>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--warning)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
              Identified Gaps
            </h3>
            <ul className="feedback-list gaps">
              {feedback.gaps && feedback.gaps.length > 0 ? (
                feedback.gaps.map((gap, idx) => (
                  <li key={idx}>{gap}</li>
                ))
              ) : (
                <li style={{ color: 'var(--text-muted)' }}>No significant gaps identified.</li>
              )}
            </ul>
          </div>
        </div>
        
        <div className="feedback-card" style={{ marginTop: '2rem', borderTop: '2px solid var(--accent-color)' }}>
          <h3>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--accent-color)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 16 16 12 12 8"></polyline><line x1="8" y1="12" x2="16" y2="12"></line></svg>
            Strategic Next Steps
          </h3>
          <ul className="feedback-list next">
            {feedback.next_steps && feedback.next_steps.length > 0 ? (
              feedback.next_steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))
            ) : (
              <li style={{ color: 'var(--text-muted)' }}>Proceed as currently planned.</li>
            )}
          </ul>
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '4rem', marginBottom: '2rem' }}>
          <button className="btn" onClick={onRestart} style={{ display: 'inline-flex', alignItems: 'center', gap: '0.75rem' }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
            <span>Return to Dashboard</span>
          </button>
        </div>
      </div>
    </div>
  );
}

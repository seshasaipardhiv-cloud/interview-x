export default function FeedbackReport({ feedback, onRestart }) {
  if (!feedback) return null;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', overflowY: 'auto', flex: 1 }}>
      <div className="feedback-container">
        <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '64px', height: '64px', borderRadius: '16px', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', marginBottom: '1.5rem' }}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--text-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          </div>
          <h1 style={{ fontSize: '3rem', margin: 0 }}>Final Assessment</h1>
          <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)' }}>Interview session telemetry analyzed successfully.</p>
        </div>
        
        <div className="glass-panel" style={{ padding: '2.5rem', marginBottom: '2rem' }}>
          <h3 style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-muted)', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
            Executive Summary
          </h3>
          <p style={{ fontSize: '1.25rem', color: 'var(--text-primary)', lineHeight: 1.6, margin: 0 }}>{feedback.summary}</p>
        </div>
        
        <div className="feedback-grid" style={{ marginBottom: '3rem' }}>
          <div className="feedback-card">
            <h3><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg> Interrogations</h3>
            <div className="metric-value">{feedback.questions_completed || 0}</div>
            <div className="metric-label">Total Questions</div>
          </div>
          <div className="feedback-card">
            <h3><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg> Coverage</h3>
            <div className="metric-value">{feedback.curriculum_areas_assessed || 0}</div>
            <div className="metric-label">Curriculum Nodes</div>
          </div>
          <div className="feedback-card">
            <h3><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg> Adaptability</h3>
            <div className="metric-value">{feedback.adaptive_follow_ups || 0}</div>
            <div className="metric-label">Dynamic Branches</div>
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
          <div className="glass-panel" style={{ padding: '2rem' }}>
            <h3 style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--success)', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
              Core Competencies
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {feedback.strengths && feedback.strengths.length > 0 ? (
                feedback.strengths.map((str, idx) => (
                  <li key={idx} style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                    <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--success)', marginTop: '0.5rem', flexShrink: 0 }}></div>
                    <span style={{ color: 'var(--text-secondary)' }}>{str}</span>
                  </li>
                ))
              ) : (
                <li style={{ color: 'var(--text-muted)' }}>No particular strengths highlighted.</li>
              )}
            </ul>
          </div>
          
          <div className="glass-panel" style={{ padding: '2rem' }}>
            <h3 style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--warning)', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
              Identified Deficits
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {feedback.gaps && feedback.gaps.length > 0 ? (
                feedback.gaps.map((gap, idx) => (
                  <li key={idx} style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                    <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--warning)', marginTop: '0.5rem', flexShrink: 0 }}></div>
                    <span style={{ color: 'var(--text-secondary)' }}>{gap}</span>
                  </li>
                ))
              ) : (
                <li style={{ color: 'var(--text-muted)' }}>No significant gaps identified.</li>
              )}
            </ul>
          </div>
        </div>
        
        <div className="glass-panel" style={{ padding: '2rem', marginBottom: '3rem' }}>
          <h3 style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--text-primary)', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
            Strategic Directives
          </h3>
          <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {feedback.next_steps && feedback.next_steps.length > 0 ? (
              feedback.next_steps.map((step, idx) => (
                <li key={idx} style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
                  <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--text-primary)', marginTop: '0.5rem', flexShrink: 0 }}></div>
                  <span style={{ color: 'var(--text-primary)' }}>{step}</span>
                </li>
              ))
            ) : (
              <li style={{ color: 'var(--text-muted)' }}>Proceed as currently planned.</li>
            )}
          </ul>
        </div>
        
        <div style={{ textAlign: 'center', marginBottom: '4rem' }}>
          <button className="btn" onClick={onRestart}>
            Initialize New Session
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginLeft: '0.5rem' }}><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          </button>
        </div>
      </div>
    </div>
  );
}

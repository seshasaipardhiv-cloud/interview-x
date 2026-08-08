export default function FeedbackReport({ feedback, onRestart }) {
  if (!feedback) return null;

  return (
    <div style={{ display: 'flex', justifyContent: 'center', overflowY: 'auto', flex: 1 }}>
      <div className="feedback-container">
        <h1 style={{ textAlign: 'center', marginBottom: '3rem', fontSize: '2.5rem' }}>Final Assessment</h1>
        
        <div className="glass-panel feedback-section">
          <h3>OVERALL ASSESSMENT</h3>
          <p style={{ fontSize: '1.1rem', color: 'var(--text-primary)' }}>{feedback.summary}</p>
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
          <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--accent-color)' }}>{feedback.questions_completed || 0}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Questions Completed</div>
          </div>
          <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--accent-color)' }}>{feedback.curriculum_areas_assessed || 0}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Curriculum Areas</div>
          </div>
          <div className="glass-panel" style={{ padding: '1.5rem', textAlign: 'center' }}>
            <div style={{ fontSize: '2rem', fontWeight: '700', color: 'var(--accent-color)' }}>{feedback.adaptive_follow_ups || 0}</div>
            <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Adaptive Follow-ups</div>
          </div>
        </div>

        <div className="glass-panel feedback-section">
          <h3 style={{ color: 'var(--success)' }}>STRENGTHS</h3>
          <ul className="feedback-list">
            {feedback.strengths && feedback.strengths.length > 0 ? (
              feedback.strengths.map((str, idx) => (
                <li key={idx}>{str}</li>
              ))
            ) : (
              <li>No particular strengths highlighted.</li>
            )}
          </ul>
        </div>
        
        <div className="glass-panel feedback-section">
          <h3 style={{ color: 'var(--warning)' }}>AREAS TO IMPROVE</h3>
          <ul className="feedback-list">
            {feedback.gaps && feedback.gaps.length > 0 ? (
              feedback.gaps.map((gap, idx) => (
                <li key={idx}>{gap}</li>
              ))
            ) : (
              <li>No significant gaps identified.</li>
            )}
          </ul>
        </div>
        
        <div className="glass-panel feedback-section">
          <h3 style={{ color: 'var(--accent-color)' }}>RECOMMENDED NEXT STEPS</h3>
          <ul className="feedback-list">
            {feedback.next_steps && feedback.next_steps.length > 0 ? (
              feedback.next_steps.map((step, idx) => (
                <li key={idx}>{step}</li>
              ))
            ) : (
              <li>Proceed as currently planned.</li>
            )}
          </ul>
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '3rem', marginBottom: '2rem' }}>
          <button className="btn" onClick={onRestart}>
            Start New Interview
          </button>
        </div>
      </div>
    </div>
  );
}

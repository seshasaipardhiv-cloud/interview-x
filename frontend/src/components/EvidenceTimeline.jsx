export default function EvidenceTimeline({ currentPhase, daysCovered }) {
  const phases = [
    { id: 'baseline', label: 'Baseline' },
    { id: 'core_concept', label: 'Core Concept' },
    { id: 'application', label: 'Application' },
    { id: 'deep_probe', label: 'Deep Probe' },
    { id: 'cross_topic', label: 'Cross Topic' },
    { id: 'production_scenario', label: 'Production' },
    { id: 'weak_area', label: 'Weak Area' },
    { id: 'final_synthesis', label: 'Synthesis' }
  ];

  // Helper to determine status icon for phase
  const getPhaseIcon = (phase, currentIndex, targetIndex) => {
    if (currentIndex > targetIndex) return '✓';
    if (currentIndex === targetIndex) return '→';
    return '○';
  };

  const getPhaseClass = (phase, currentIndex, targetIndex) => {
    if (currentIndex > targetIndex) return 'completed';
    if (currentIndex === targetIndex) return 'active';
    return '';
  };

  const currentPhaseIndex = phases.findIndex(p => p.id === currentPhase);

  return (
    <div className="side-panel">
      <h3 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        Interview Progress
      </h3>
      
      <div style={{ marginBottom: '3rem', position: 'relative' }}>
        {/* Subtle timeline track */}
        <div style={{ position: 'absolute', left: '16px', top: '24px', bottom: '24px', width: '2px', background: 'var(--border-color)', zIndex: 0 }}></div>
        
        {phases.map((phase, idx) => (
          <div key={phase.id} className={`checklist-item ${getPhaseClass(phase.id, currentPhaseIndex, idx)}`} style={{ position: 'relative', zIndex: 1 }}>
            <span className="icon">
              {currentPhaseIndex > idx && <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>}
              {currentPhaseIndex === idx && <div style={{ width: '8px', height: '8px', background: 'var(--accent-color)', borderRadius: '50%', boxShadow: '0 0 10px var(--accent-glow)' }}></div>}
              {currentPhaseIndex < idx && <div style={{ width: '6px', height: '6px', background: 'var(--text-muted)', borderRadius: '50%' }}></div>}
            </span>
            <span style={{ fontFamily: 'var(--font-display)', letterSpacing: '0.02em' }}>{phase.label}</span>
          </div>
        ))}
      </div>

      <h3 style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
        Curriculum Coverage
      </h3>
      
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem' }}>
        {daysCovered.length === 0 && <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', fontStyle: 'italic' }}>Awaiting data...</div>}
        {daysCovered.map((day) => (
          <div key={day} style={{ 
            background: 'rgba(16, 185, 129, 0.1)', 
            border: '1px solid rgba(16, 185, 129, 0.3)',
            color: 'var(--success)',
            padding: '0.4rem 0.8rem',
            borderRadius: '8px',
            fontSize: '0.85rem',
            fontFamily: 'var(--font-display)',
            fontWeight: '600',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem'
          }}>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
            Day {day}
          </div>
        ))}
      </div>
    </div>
  );
}

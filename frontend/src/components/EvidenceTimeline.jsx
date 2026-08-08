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
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem' }}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: 'var(--text-muted)' }}><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        <h3 style={{ fontSize: '0.85rem', margin: 0, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
          Assessment Vector
        </h3>
      </div>
      
      <div style={{ marginBottom: '3rem', paddingLeft: '0.5rem' }}>
        {phases.map((phase, idx) => (
          <div key={phase.id} className={`timeline-node ${getPhaseClass(phase.id, currentPhaseIndex, idx)}`}>
            <div className="node-indicator"></div>
            <div className="node-label">{phase.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '2rem' }}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" style={{ color: 'var(--text-muted)' }}><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
        <h3 style={{ fontSize: '0.85rem', margin: 0, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
          Curriculum Coverage
        </h3>
      </div>
      
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
        {daysCovered.length === 0 && <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Awaiting telemetry...</span>}
        {daysCovered.map((day) => (
          <div key={day} style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', background: 'rgba(5, 150, 105, 0.15)', color: 'var(--success)', padding: '0.25rem 0.6rem', borderRadius: '4px', fontSize: '0.8rem', fontWeight: '500', border: '1px solid rgba(5, 150, 105, 0.3)' }}>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
            Day {day}
          </div>
        ))}
      </div>
    </div>
  );
}

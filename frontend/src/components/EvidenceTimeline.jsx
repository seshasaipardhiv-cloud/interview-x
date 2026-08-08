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
      <h3 style={{ fontSize: '1.1rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
        Interview Progress
      </h3>
      
      <div style={{ marginBottom: '3rem' }}>
        {phases.map((phase, idx) => (
          <div key={phase.id} className={`checklist-item ${getPhaseClass(phase.id, currentPhaseIndex, idx)}`}>
            <span className="icon">{getPhaseIcon(phase.id, currentPhaseIndex, idx)}</span>
            <span>{phase.label}</span>
          </div>
        ))}
      </div>

      <h3 style={{ fontSize: '1.1rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--border-color)', paddingBottom: '0.5rem' }}>
        Curriculum Coverage
      </h3>
      
      <div>
        {daysCovered.length === 0 && <div className="checklist-item">No days covered yet.</div>}
        {daysCovered.map((day) => (
          <div key={day} className="checklist-item completed">
            <span className="icon">✓</span>
            <span>Day {day}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

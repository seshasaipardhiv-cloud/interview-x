import { useState, useEffect } from 'react';
import candidatesData from '../data/candidates.json';

export default function Home({ onStart }) {
  const [selectedCandidateId, setSelectedCandidateId] = useState('');
  const [candidates, setCandidates] = useState([]);

  const TARGET_CANDIDATES = ["Sarah Johnson", "Ethan Brooks", "Mia Alvarez"];

  useEffect(() => {
    if (candidatesData.candidates) {
      const filtered = candidatesData.candidates.filter(c => TARGET_CANDIDATES.includes(c.member.name));
      setCandidates(filtered);
      if (filtered.length > 0) {
        setSelectedCandidateId(filtered[0].member.id);
      }
    }
  }, []);

  const selectedCandidate = candidates.find(c => c.member.id === selectedCandidateId);

  const handleStart = () => {
    if (!selectedCandidateId) return;
    const candidate = candidates.find(c => c.member.id === selectedCandidateId);
    
    // Generate simple UUID-like string for demo
    const sessionId = `sess-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
    
    onStart({ sessionId, candidate });
  };

  return (
    <div className="app-main" style={{ justifyContent: 'center', alignItems: 'center', padding: '2rem' }}>
      <div className="glass-panel" style={{ padding: '3.5rem 3rem', maxWidth: '520px', width: '100%', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
        
        {/* Subtle decorative glow inside the panel */}
        <div style={{ position: 'absolute', top: '-50px', left: '50%', transform: 'translateX(-50%)', width: '200px', height: '100px', background: 'var(--accent-glow)', filter: 'blur(60px)', borderRadius: '50%', pointerEvents: 'none' }}></div>

        <h1 style={{ marginBottom: '0.75rem', fontSize: '2.5rem', background: 'linear-gradient(to right, #fff, #a1a1aa)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', letterSpacing: '-0.04em' }}>INTERVIEW-X</h1>
        <p style={{ marginBottom: '2.5rem', fontSize: '1.1rem', color: 'var(--text-secondary)' }}>Enterprise AI Technical Interview</p>
        
        <div style={{ marginBottom: '2.5rem', textAlign: 'left' }}>
          <label style={{ display: 'block', marginBottom: '0.75rem', color: 'var(--text-secondary)', fontSize: '0.9rem', fontWeight: '500', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Select Candidate Profile
          </label>
          <select 
            value={selectedCandidateId} 
            onChange={(e) => setSelectedCandidateId(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '1rem 1.25rem', 
              borderRadius: '12px', 
              backgroundColor: 'rgba(0, 0, 0, 0.2)',
              color: 'var(--text-primary)',
              border: '1px solid var(--border-highlight)',
              fontSize: '1.05rem',
              transition: 'all var(--transition-speed) ease',
              boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.1)'
            }}
            onFocus={(e) => {
              e.target.style.borderColor = 'var(--accent-color)';
              e.target.style.boxShadow = '0 0 0 3px rgba(56, 189, 248, 0.15)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = 'var(--border-highlight)';
              e.target.style.boxShadow = 'inset 0 2px 4px rgba(0,0,0,0.1)';
            }}
          >
            {candidates.map(c => (
              <option key={c.member.id} value={c.member.id}>
                {c.member.name} - {c.member.jobRole}
              </option>
            ))}
          </select>
        </div>

        {selectedCandidate && (
          <div style={{ marginBottom: '2.5rem', textAlign: 'left', background: 'rgba(255, 255, 255, 0.03)', padding: '1.5rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
            <h3 style={{ marginBottom: '1rem', fontSize: '1.2rem', color: 'var(--text-primary)' }}>Candidate Profile</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
              <div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Name</div>
                <div style={{ fontWeight: '500' }}>{selectedCandidate.member.name}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Role</div>
                <div style={{ fontWeight: '500' }}>{selectedCandidate.member.jobRole}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Experience</div>
                <div style={{ fontWeight: '500' }}>{selectedCandidate.member.yearsExperience} Years</div>
              </div>
              <div>
                <div style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Status</div>
                <div style={{ fontWeight: '500' }}>{selectedCandidate.member.status}</div>
              </div>
            </div>

            <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--accent-color)', fontWeight: '600', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Interview Strategy Prepared
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {['Personalized', 'Adaptive', 'Curriculum-aware', 'Evidence-conditioned'].map(tag => (
                  <span key={tag} style={{ background: 'rgba(56, 189, 248, 0.1)', color: 'var(--accent-color)', padding: '0.25rem 0.75rem', borderRadius: '100px', fontSize: '0.8rem', border: '1px solid rgba(56, 189, 248, 0.2)' }}>
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        <button className="btn" onClick={handleStart} style={{ width: '100%', padding: '1rem', fontSize: '1.1rem' }}>
          Initialize Interview Session
        </button>
      </div>
    </div>
  );
}

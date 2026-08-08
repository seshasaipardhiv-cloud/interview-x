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
      <div className="glass-panel" style={{ padding: '4rem 3.5rem', maxWidth: '580px', width: '100%', position: 'relative', overflow: 'hidden' }}>
        
        {/* Subtle decorative glow inside the panel */}
        <div style={{ position: 'absolute', top: '-100px', right: '-100px', width: '300px', height: '300px', background: 'var(--violet-glow)', filter: 'blur(80px)', borderRadius: '50%', pointerEvents: 'none', zIndex: -1 }}></div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
          <div style={{ width: '40px', height: '40px', borderRadius: '12px', background: 'var(--accent-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 20px var(--accent-glow)' }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          </div>
          <h1 style={{ fontSize: '2.5rem', letterSpacing: '-0.02em', background: 'linear-gradient(135deg, #fff 0%, #a1a1aa 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>INTERVIEW-X</h1>
        </div>
        
        <p style={{ marginBottom: '3rem', fontSize: '1.1rem', color: 'var(--text-secondary)' }}>Enterprise AI Technical Interview Platform</p>
        
        <div style={{ marginBottom: '2.5rem' }}>
          <label style={{ display: 'block', marginBottom: '1rem', color: 'var(--text-primary)', fontSize: '0.95rem', fontWeight: '500', fontFamily: 'var(--font-display)', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
            Initialize Candidate Session
          </label>
          <select 
            value={selectedCandidateId} 
            onChange={(e) => setSelectedCandidateId(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '1.15rem 1.25rem', 
              fontSize: '1.05rem',
            }}
          >
            {candidates.map(c => (
              <option key={c.member.id} value={c.member.id}>
                {c.member.name} • {c.member.jobRole}
              </option>
            ))}
          </select>
        </div>

        {selectedCandidate && (
          <div style={{ marginBottom: '3rem', background: 'rgba(255, 255, 255, 0.02)', padding: '1.75rem', borderRadius: '16px', border: '1px solid var(--border-color)', animation: 'slideUpFade 0.4s ease-out' }}>
            <h3 style={{ marginBottom: '1.25rem', fontSize: '0.9rem', color: 'var(--accent-color)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Profile Telemetry</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.75rem' }}>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Candidate</div>
                <div style={{ fontWeight: '500', fontSize: '1.05rem', color: 'var(--text-primary)' }}>{selectedCandidate.member.name}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Target Role</div>
                <div style={{ fontWeight: '500', fontSize: '1.05rem', color: 'var(--text-primary)' }}>{selectedCandidate.member.jobRole}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Experience</div>
                <div style={{ fontWeight: '500', fontSize: '1.05rem', color: 'var(--text-primary)' }}>{selectedCandidate.member.yearsExperience} Years</div>
              </div>
              <div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Status</div>
                <div style={{ fontWeight: '500', fontSize: '1.05rem', color: 'var(--success)' }}>{selectedCandidate.member.status}</div>
              </div>
            </div>

            <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '1.5rem' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem' }}>
                Active Heuristics
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {['Adaptive', 'Curriculum-Aware', 'Evidence-Driven'].map(tag => (
                  <span key={tag} style={{ background: 'rgba(255, 255, 255, 0.03)', color: 'var(--text-secondary)', padding: '0.35rem 0.85rem', borderRadius: '100px', fontSize: '0.85rem', border: '1px solid var(--border-color)' }}>
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        <button className="btn" onClick={handleStart} style={{ width: '100%', padding: '1.15rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem' }}>
          <span>Launch Session</span>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </button>
      </div>
    </div>
  );
}

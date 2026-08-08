import { useState, useEffect } from 'react';
import candidatesData from '../data/candidates.json';

export default function Home({ onStart }) {
  const [selectedCandidateId, setSelectedCandidateId] = useState('');
  const [candidates, setCandidates] = useState([]);

  useEffect(() => {
    if (candidatesData.candidates) {
      setCandidates(candidatesData.candidates);
      if (candidatesData.candidates.length > 0) {
        setSelectedCandidateId(candidatesData.candidates[0].member.id);
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
    <div className="app-container" style={{ alignItems: 'center', justifyContent: 'center' }}>
      <div className="glass-panel" style={{ width: '100%', maxWidth: '480px', padding: '3rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '48px', height: '48px', borderRadius: '12px', background: 'var(--text-primary)', color: 'var(--bg-base)', marginBottom: '1.5rem', boxShadow: '0 0 20px rgba(255,255,255,0.1)' }}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
          </div>
          <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>INTERVIEW-X</h1>
          <p style={{ fontSize: '0.95rem' }}>Enterprise Intelligence Platform</p>
        </div>
        
        <div style={{ marginBottom: '2rem' }}>
          <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: '500', color: 'var(--text-secondary)', marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Initialize Candidate Profile
          </label>
          <div style={{ position: 'relative' }}>
            <select 
              value={selectedCandidateId} 
              onChange={(e) => setSelectedCandidateId(e.target.value)}
              style={{ 
                width: '100%', 
                padding: '1rem 1.25rem', 
                borderRadius: 'var(--radius-sm)', 
                backgroundColor: 'rgba(0,0,0,0.4)',
                border: '1px solid var(--border-color)',
                color: 'var(--text-primary)',
                fontSize: '0.95rem',
                fontFamily: 'var(--font-sans)',
                transition: 'var(--transition-fast)',
                cursor: 'pointer'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = 'rgba(255,255,255,0.3)';
                e.target.style.boxShadow = '0 0 0 1px rgba(255,255,255,0.1)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = 'var(--border-color)';
                e.target.style.boxShadow = 'none';
              }}
            >
              {candidates.map(c => (
                <option key={c.member.id} value={c.member.id}>
                  {c.member.name} • {c.member.jobRole}
                </option>
              ))}
            </select>
          </div>
        </div>

        {selectedCandidate && (
          <div style={{ marginBottom: '2.5rem', padding: '1.25rem', background: 'rgba(255,255,255,0.03)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Candidate</div>
                <div style={{ fontSize: '0.95rem', fontWeight: '500' }}>{selectedCandidate.member.name}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Target Role</div>
                <div style={{ fontSize: '0.95rem', fontWeight: '500' }}>{selectedCandidate.member.jobRole}</div>
              </div>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Experience</div>
                <div style={{ fontSize: '0.95rem', fontWeight: '500' }}>{selectedCandidate.member.yearsExperience} YOE</div>
              </div>
              <div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem' }}>Clearance</div>
                <div style={{ fontSize: '0.95rem', fontWeight: '500', color: 'var(--success)' }}>VERIFIED</div>
              </div>
            </div>
          </div>
        )}

        <button className="btn" onClick={handleStart} style={{ width: '100%', height: '3rem' }}>
          Launch Session
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
        </button>
      </div>
    </div>
  );
}

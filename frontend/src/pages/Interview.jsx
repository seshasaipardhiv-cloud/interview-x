import { useState, useEffect } from 'react';
import InterviewPanel from '../components/InterviewPanel';
import EvidenceTimeline from '../components/EvidenceTimeline';
import { postInterview } from '../services/api';

export default function Interview({ session, onComplete, onAbort }) {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingText, setLoadingText] = useState('Starting interview...');
  const [error, setError] = useState(null);
  
  // Live indicators driven by backend state
  const [questionsAsked, setQuestionsAsked] = useState(0);
  const [daysCovered, setDaysCovered] = useState([]);
  const [currentPhase, setCurrentPhase] = useState('baseline');

  // Initialization
  useEffect(() => {
    let isMounted = true;
    
    async function startInterview() {
      try {
        const response = await postInterview({
          sessionId: session.sessionId,
          candidate: session.candidate
        });
        
        if (isMounted) {
          setHistory([{ role: 'ai', text: response.reply }]);
          setQuestionsAsked(response.question_count || 1);
          setDaysCovered(response.curriculum_days_covered || []);
          setCurrentPhase(response.current_phase || 'baseline');
          setLoading(false);
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message);
          setLoading(false);
        }
      }
    }
    
    startInterview();
    
    return () => { isMounted = false; };
  }, [session]);

  const handleAnswerSubmit = async (answer) => {
    if (!answer.trim() || loading) return;
    
    // Optimistic UI update
    setHistory(prev => [...prev, { role: 'candidate', text: answer }]);
    setLoading(true);
    setLoadingText('Analyzing your response...');
    setError(null);
    
    try {
      // Small timeout just to show the analyzing text nicely before switching
      setTimeout(() => setLoadingText('Preparing your next question...'), 1500);
      
      const response = await postInterview({
        sessionId: session.sessionId,
        message: answer
      });
      
      if (response.done) {
        setLoadingText('Preparing final assessment...');
        setTimeout(() => {
          onComplete(response.feedback);
        }, 1000);
      } else {
        if (response.is_adapting) {
          setLoadingText('Adapting next question...');
          await new Promise(resolve => setTimeout(resolve, 1500));
        }
        
        setHistory(prev => [...prev, { role: 'ai', text: response.reply }]);
        setQuestionsAsked(response.question_count || 1);
        setDaysCovered(response.curriculum_days_covered || []);
        setCurrentPhase(response.current_phase || 'baseline');
        
        setLoading(false);
      }
    } catch (err) {
      setError(err.message);
      setLoading(false);
      // Remove the optimistically added candidate message on error so they can retry?
      // Or just let them see the error and type a new one. For simplicity, just show error.
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: '32px', height: '32px', borderRadius: '8px', background: 'var(--text-primary)', color: 'var(--bg-base)' }}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
          </div>
          <div>
            <h2 style={{ fontSize: '1.25rem', margin: 0, lineHeight: 1 }}>INTERVIEW-X</h2>
            <p style={{ fontSize: '0.75rem', margin: 0, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginTop: '0.25rem' }}>Active Session</p>
          </div>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '2rem', textAlign: 'right' }}>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Candidate Target</div>
            <div style={{ fontSize: '0.9rem', fontWeight: '500', color: 'var(--text-primary)' }}>{session.candidate.member.name}</div>
          </div>
          <div style={{ width: '1px', height: '32px', background: 'var(--border-color)' }}></div>
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Progress</div>
            <div style={{ fontSize: '0.9rem', fontWeight: '500', color: 'var(--accent-color)' }}>Question {questionsAsked} / 8+</div>
          </div>
        </div>
      </header>
      
      <div className="app-main">
        <div className="interview-area">
          {error && (
            <div style={{ position: 'absolute', top: '1rem', left: '50%', transform: 'translateX(-50%)', zIndex: 50, backgroundColor: 'rgba(220, 38, 38, 0.1)', border: '1px solid var(--danger)', color: 'var(--danger)', padding: '0.75rem 1.5rem', borderRadius: 'var(--radius-sm)', display: 'flex', alignItems: 'center', gap: '1rem', backdropFilter: 'blur(8px)' }}>
              <span style={{ fontSize: '0.85rem', fontWeight: '500' }}>SYS_ERR: {error}</span>
              <button 
                onClick={() => setError(null)} 
                style={{ background: 'transparent', border: 'none', color: 'var(--text-primary)', cursor: 'pointer', padding: '0.25rem', opacity: 0.7 }}
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
              </button>
            </div>
          )}
          
          <InterviewPanel 
            history={history} 
            loading={loading} 
            loadingText={loadingText}
            onSubmit={handleAnswerSubmit} 
          />
        </div>
        
        <EvidenceTimeline 
          currentPhase={currentPhase} 
          daysCovered={daysCovered} 
        />
      </div>
    </div>
  );
}

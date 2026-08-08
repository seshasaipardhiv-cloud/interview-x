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
          <div style={{ width: '32px', height: '32px', borderRadius: '8px', background: 'var(--accent-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 0 15px var(--accent-glow)' }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#000" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          </div>
          <h2 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span>INTERVIEW-X</span>
            <span style={{ fontSize: '0.8rem', padding: '0.2rem 0.5rem', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '4px', color: 'var(--text-secondary)' }}>LIVE</span>
          </h2>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.2rem' }}>Candidate Telemetry</div>
            <div style={{ fontWeight: '600', color: 'var(--text-primary)', fontFamily: 'var(--font-display)' }}>{session.candidate.member.name}</div>
          </div>
          <div style={{ height: '30px', width: '1px', background: 'var(--border-color)' }}></div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.2rem' }}>Pipeline Progress</div>
            <div style={{ color: 'var(--accent-color)', fontWeight: '600', fontFamily: 'var(--font-display)' }}>
              Node {questionsAsked} / 8+
            </div>
          </div>
        </div>
      </header>
      
      <div className="app-main">
        <div className="interview-area">
          {error && (
            <div style={{ backgroundColor: 'var(--danger)', color: 'white', padding: '1rem', borderRadius: '8px', marginBottom: '1rem' }}>
              <strong>Error:</strong> {error}
              <button 
                onClick={() => setError(null)} 
                style={{ marginLeft: '1rem', background: 'transparent', border: '1px solid white', color: 'white', padding: '0.25rem 0.5rem', borderRadius: '4px', cursor: 'pointer' }}
              >
                Dismiss
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

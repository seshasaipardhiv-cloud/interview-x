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
        <div>
          <h2>INTERVIEW-X</h2>
          <p style={{ fontSize: '0.9rem' }}>AI Technical Interview</p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontWeight: '500' }}>Candidate: {session.candidate.member.name}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            Progress: Question {questionsAsked} / 8+
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

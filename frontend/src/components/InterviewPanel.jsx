import { useState, useRef, useEffect } from 'react';

export default function InterviewPanel({ history, loading, loadingText, onSubmit }) {
  const [input, setInput] = useState('');
  const endOfMessagesRef = useRef(null);

  // Auto-scroll to bottom when history changes
  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history, loading]);

  const handleSubmit = () => {
    if (!input.trim() || loading) return;
    onSubmit(input);
    setInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <>
      <div className="chat-container">
        {history.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.role === 'ai' && (
              <div className="role-label">AI INTERVIEWER</div>
            )}
            {msg.role === 'candidate' && (
              <div className="role-label">CANDIDATE</div>
            )}
            <p>{msg.text}</p>
          </div>
        ))}
        
        {loading && (
          <div className="message ai" style={{ opacity: 0.8 }}>
            <div className="role-label">AI INTERVIEWER</div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
              <span style={{ fontSize: '0.9rem', fontStyle: 'italic', color: 'var(--text-secondary)' }}>{loadingText}</span>
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>
      
      <div className="input-area">
        <div style={{ position: 'relative' }}>
          <textarea 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Formulate your response... (Enter to submit, Shift+Enter for new line)"
            disabled={loading}
            aria-label="Candidate response textarea"
            style={{ 
              width: '100%', 
              background: 'rgba(255, 255, 255, 0.02)',
              border: '1px solid var(--border-color)', 
              borderRadius: '16px',
              padding: '1.25rem 4rem 1.25rem 1.25rem',
              color: 'var(--text-primary)',
              fontSize: '1.05rem',
              resize: 'none',
              height: '120px'
            }}
          />
          <button 
            onClick={handleSubmit} 
            disabled={loading || !input.trim()}
            aria-label="Submit Answer"
            style={{ 
              position: 'absolute', 
              right: '1rem', 
              bottom: '1rem',
              width: '40px',
              height: '40px',
              borderRadius: '50%',
              background: (loading || !input.trim()) ? 'rgba(255,255,255,0.05)' : 'var(--accent-color)',
              color: (loading || !input.trim()) ? 'var(--text-muted)' : '#000',
              border: 'none',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: (loading || !input.trim()) ? 'not-allowed' : 'pointer',
              transition: 'all 0.3s ease',
              boxShadow: (loading || !input.trim()) ? 'none' : '0 0 15px var(--accent-glow)'
            }}
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
          </button>
        </div>
        <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textAlign: 'right', marginTop: '-0.5rem', marginRight: '0.5rem' }}>
          Press <kbd style={{ background: 'rgba(255,255,255,0.1)', padding: '0.1rem 0.3rem', borderRadius: '4px' }}>Enter</kbd> to submit
        </div>
      </div>
    </>
  );
}

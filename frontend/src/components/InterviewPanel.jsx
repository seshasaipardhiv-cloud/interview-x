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
            <div className="role-label">
              {msg.role === 'ai' ? (
                <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg> INTERVIEW-X</>
              ) : (
                <><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg> YOU</>
              )}
            </div>
            <p>{msg.text}</p>
          </div>
        ))}
        
        {loading && (
          <div className="message ai">
            <div className="role-label">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><path d="M12 16v-4"></path><path d="M12 8h.01"></path></svg> INTERVIEW-X
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div className="typing-indicator">
                <span></span><span></span><span></span>
              </div>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{loadingText}</span>
            </div>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>
      
      <div className="input-area">
        <div className="input-wrapper">
          <textarea 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your answer here... (Press Enter to submit, Shift+Enter for new line)"
            disabled={loading}
            aria-label="Candidate response textarea"
          />
          <button 
            className="btn" 
            onClick={handleSubmit} 
            disabled={loading || !input.trim()}
            style={{ position: 'absolute', right: '0.75rem', bottom: '0.75rem', padding: '0.5rem', borderRadius: 'var(--radius-sm)' }}
            aria-label="Submit"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
          </button>
        </div>
        <div style={{ textAlign: 'center', marginTop: '0.75rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
          Powered by Google Gemini • Press <kbd style={{ padding: '0.1rem 0.3rem', background: 'var(--bg-base)', border: '1px solid var(--border-color)', borderRadius: '3px' }}>Enter</kbd> to submit
        </div>
      </div>
    </>
  );
}

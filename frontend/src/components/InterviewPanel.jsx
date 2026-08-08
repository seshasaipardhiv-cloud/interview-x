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
            {msg.role === 'ai' && <div style={{ fontSize: '0.8rem', color: 'var(--accent-color)', marginBottom: '0.25rem', fontWeight: 'bold' }}>AI INTERVIEWER</div>}
            {msg.role === 'candidate' && <div style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.7)', marginBottom: '0.25rem', fontWeight: 'bold' }}>YOU</div>}
            <p>{msg.text}</p>
          </div>
        ))}
        
        {loading && (
          <div className="message ai pulse">
            <div style={{ fontSize: '0.8rem', color: 'var(--accent-color)', marginBottom: '0.25rem', fontWeight: 'bold' }}>AI INTERVIEWER</div>
            <p style={{ fontStyle: 'italic' }}>{loadingText}</p>
          </div>
        )}
        <div ref={endOfMessagesRef} />
      </div>
      
      <div className="input-area">
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
          style={{ alignSelf: 'flex-end' }}
        >
          Submit Answer
        </button>
      </div>
    </>
  );
}

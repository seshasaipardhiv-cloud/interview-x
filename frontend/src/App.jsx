import { useState } from 'react';
import Home from './pages/Home';
import Interview from './pages/Interview';
import FeedbackReport from './components/FeedbackReport';

export default function App() {
  const [session, setSession] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const handleStart = (newSession) => {
    setSession(newSession);
    setFeedback(null);
  };

  const handleComplete = (finalFeedback) => {
    setFeedback(finalFeedback);
  };

  const handleEnd = () => {
    setSession(null);
    setFeedback(null);
  };

  return (
    <main className="app-container">
      {!session && !feedback && <Home onStart={handleStart} />}
      {session && !feedback && (
        <Interview 
          session={session} 
          onComplete={handleComplete} 
          onAbort={handleEnd} 
        />
      )}
      {feedback && (
        <FeedbackReport feedback={feedback} onRestart={handleEnd} />
      )}
    </main>
  );
}

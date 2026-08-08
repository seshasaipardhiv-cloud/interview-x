import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import App from '../App';
import * as api from '../services/api';

// Mock the API layer entirely
vi.mock('../services/api', () => ({
  postInterview: vi.fn(),
}));

// Mock the scrollIntoView which doesn't exist in JSDOM
window.HTMLElement.prototype.scrollIntoView = vi.fn();

describe('INTERVIEW-X Frontend End-to-End Flow', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('1/2/3. Candidate selection, interview start, and displaying first question', async () => {
    api.postInterview.mockResolvedValueOnce({
      reply: 'Hello Sarah, welcome to the interview.',
      done: false,
      question_count: 1,
      curriculum_days_covered: [1],
      current_phase: 'baseline'
    });

    render(<App />);
    
    // 1. Candidate selection
    expect(screen.getByText(/Initialize Candidate Profile/i)).toBeInTheDocument();
    
    // 2. Interview start
    const startButton = screen.getByRole('button', { name: /launch session/i });
    fireEvent.click(startButton);

    // Initial loading state
    expect(screen.getByText(/Starting interview.../i)).toBeInTheDocument();

    // 3. Displaying first question
    await waitFor(() => {
      expect(screen.getByText('Hello Sarah, welcome to the interview.')).toBeInTheDocument();
    });
    
    // Progress update
    expect(screen.getByText(/Question 1 \/ 8\+/i)).toBeInTheDocument();
  });

  it('4/5/6. Submitting an answer, displaying next response, and progress updates', async () => {
    api.postInterview
      .mockResolvedValueOnce({ 
        reply: 'First question', 
        done: false,
        question_count: 1,
        curriculum_days_covered: [1],
        current_phase: 'baseline'
      })
      .mockResolvedValueOnce({ 
        reply: 'Second question', 
        done: false,
        question_count: 2,
        curriculum_days_covered: [1, 2],
        current_phase: 'core_concept'
      });

    render(<App />);
    
    // Start
    fireEvent.click(screen.getByRole('button', { name: /launch session/i }));
    
    await waitFor(() => expect(screen.getByText('First question')).toBeInTheDocument());

    // 4. Submitting an answer
    const textarea = screen.getByLabelText('Candidate response textarea');
    fireEvent.change(textarea, { target: { value: 'This is my great answer' } });
    
    const submitBtn = screen.getByRole('button', { name: /submit/i });
    fireEvent.click(submitBtn);

    // Check loading state on submit
    expect(screen.getByText(/Analyzing your response.../i)).toBeInTheDocument();
    expect(submitBtn).toBeDisabled();
    expect(textarea).toBeDisabled();

    // 5. Displaying next response
    await waitFor(() => expect(screen.getByText('Second question')).toBeInTheDocument(), { timeout: 2500 }); // Wait past setTimeout in code
    
    // 6. Progress updates
    expect(screen.getByText(/Question 2 \/ 8\+/i)).toBeInTheDocument();
    expect(screen.getByText('Core Concept').closest('.timeline-node')).toHaveClass('active');
  });

  it('7. Final feedback rendering', async () => {
    api.postInterview
      .mockResolvedValueOnce({ 
        reply: 'First question', 
        done: false,
        question_count: 1,
        curriculum_days_covered: [1],
        current_phase: 'baseline'
      })
      .mockResolvedValueOnce({
        reply: 'Interview complete',
        done: true,
        feedback: {
          summary: 'Great job!',
          strengths: ['Knowledge'],
          gaps: ['Nerves'],
          next_steps: ['Hire']
        }
      });

    render(<App />);
    
    // Start
    fireEvent.click(screen.getByRole('button', { name: /launch session/i }));
    await waitFor(() => expect(screen.getByText('First question')).toBeInTheDocument());

    // Submit answer to trigger completion
    const textarea = screen.getByLabelText('Candidate response textarea');
    fireEvent.change(textarea, { target: { value: 'Final answer' } });
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));

    // 7. Final feedback shows up after loading delay
    await waitFor(() => {
      expect(screen.getByText('Executive Summary')).toBeInTheDocument();
      expect(screen.getByText('Great job!')).toBeInTheDocument();
    }, { timeout: 2000 });
  });

  it('8. API failure displays error message without crashing', async () => {
    api.postInterview.mockRejectedValueOnce(new Error('Network error'));

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /launch session/i }));

    await waitFor(() => {
      expect(screen.getByText(/SYS_ERR:/i)).toBeInTheDocument();
      expect(screen.getByText(/Network error/i)).toBeInTheDocument();
    });
  });

  it('9. Empty answer prevention', async () => {
    api.postInterview.mockResolvedValueOnce({ 
      reply: 'First question', 
      done: false,
      question_count: 1,
      curriculum_days_covered: [1],
      current_phase: 'baseline'
    });

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /launch session/i }));
    await waitFor(() => expect(screen.getByText('First question')).toBeInTheDocument());

    const submitBtn = screen.getByRole('button', { name: /submit/i });
    const textarea = screen.getByLabelText('Candidate response textarea');
    
    // Empty value => disabled
    expect(submitBtn).toBeDisabled();

    // Just spaces => still shouldn't call API
    fireEvent.change(textarea, { target: { value: '    ' } });
    fireEvent.click(submitBtn);

    // Only called once for initialization, NOT for the submit
    expect(api.postInterview).toHaveBeenCalledTimes(1);
  });
});

/**
 * API client for INTERVIEW-X backend.
 * Full interview contract to be implemented later.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}

export async function postInterview(_payload) {
  const response = await fetch(`${API_BASE_URL}/api/interview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(_payload),
  });
  return response.json();
}

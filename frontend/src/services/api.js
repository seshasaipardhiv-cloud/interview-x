/**
 * API client for INTERVIEW-X backend.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}

export async function postInterview(payload) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/interview`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `Server Error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw new Error(error.message || "Failed to communicate with the interview server.");
  }
}

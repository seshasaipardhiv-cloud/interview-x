# Deployment Checklist

This document details the configuration and checks required to successfully deploy INTERVIEW-X to a production environment.

## 1. Environment Variables

Ensure the following environment variables are securely injected into your deployment (DO NOT commit them):

**Backend:**
- `APP_NAME`: Name of the app (default: `INTERVIEW-X`)
- `APP_VERSION`: Version (default: `0.1.0`)
- `DEBUG`: Set to `false` in production.
- `FRONTEND_URL`: The deployed URL of the frontend (e.g., `https://interview-x.mycompany.com`). This is critical for CORS security.
- `LLM_API_KEY`: Your LLM provider API Key.
- `LLM_MODEL`: The LLM model to use.
- `LLM_BASE_URL`: Base URL if using a custom endpoint.

**Frontend:**
- `VITE_API_BASE_URL`: The deployed URL of the backend (e.g., `https://api.interview-x.mycompany.com`).

## 2. Docker Deployment

Both services are fully containerized.

**Build and Run:**
```bash
docker compose build
docker compose up -d
```

**Health Check:**
Verify the backend is healthy by accessing:
```
GET /health
```
This endpoint does NOT call the LLM and is safe to use for Load Balancer pinging.

## 3. CORS Configuration

The backend dynamically configures its Allowed Origins based on the `FRONTEND_URL` environment variable.
- In production (`DEBUG=false`), **only** the `FRONTEND_URL` will be permitted.
- Wildcard `*` origins are entirely disabled in production mode.

## 4. In-Memory Session Limitations

For this hackathon/MVP deployment, INTERVIEW-X utilizes an **in-memory session store** (`backend/app/core/state.py`).

**Important Considerations:**
- Sessions **will not survive** a backend container restart.
- If multiple backend replicas are running behind a load balancer, you MUST use sticky sessions, or switch to a persistent Redis store.
- Re-accessing a completed session returns a clean `400 Bad Request` to prevent state corruption.
- Accessing an unknown session ID returns a clean `404 Not Found`.

## 5. Security & Error Handling

- **No Secrets Leaked**: All stack traces and internal unhandled exceptions are caught by a global exception handler. The client receives a generic `500 Internal Server Error`, while the full traceback is safely written to the backend's standard output/logs.
- **Structured Logging**: Key operational metrics (session started, follow-ups triggered, answer evaluations) are logged safely without exposing API keys or hidden system prompts.

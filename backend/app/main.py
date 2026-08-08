"""FastAPI application entry point."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import traceback

from app.api.interview import router as interview_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Evidence-driven, self-adaptive technical interview agent",
)

# Configure CORS
origins = [settings.frontend_url]
if settings.debug:
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_router, prefix="/api", tags=["interview"])

logger = logging.getLogger("interview")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full stack trace securely to the server
    logger.error(f"Unhandled exception: {exc}\n{traceback.format_exc()}")
    # Return a clean error to the client
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok", "service": settings.app_name}

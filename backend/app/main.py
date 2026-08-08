"""FastAPI application entry point."""

from fastapi import FastAPI

from app.api.interview import router as interview_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Evidence-driven, self-adaptive technical interview agent",
)

app.include_router(interview_router, prefix="/api", tags=["interview"])


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok", "service": settings.app_name}

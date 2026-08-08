"""Interview API routes (placeholder)."""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/interview")
async def interview_placeholder() -> JSONResponse:
    """Placeholder for POST /api/interview — full contract to be implemented later."""
    return JSONResponse(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        content={
            "detail": "Interview endpoint not implemented yet. "
            "This route will handle multi-turn adaptive interviews via sessionId."
        },
    )

"""Final feedback models (placeholder — future implementation)."""

from pydantic import BaseModel, Field


class FeedbackReport(BaseModel):
    """Evidence-backed final interview feedback."""

    summary: str = Field(..., description="Overall performance narrative")
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(
        default_factory=list,
        description="Recommended next steps aligned with curriculum",
    )
    # TODO: evidence citations, curriculum day references, confidence scores

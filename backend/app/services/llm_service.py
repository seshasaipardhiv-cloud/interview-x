"""LLM integration layer.

Future responsibility:
- Centralize LLM calls for question generation, analysis, and feedback
- Handle prompts, retries, and configuration from core.config
- Keep provider details isolated from business services
"""


class LLMService:
    """Placeholder for LLM provider integration."""

    def complete(self, prompt: str) -> None:
        """Send a completion request to the configured LLM. Not implemented."""
        raise NotImplementedError("LLMService.complete")

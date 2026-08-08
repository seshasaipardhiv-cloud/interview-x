"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the INTERVIEW-X backend."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "INTERVIEW-X"
    app_version: str = "0.1.0"
    debug: bool = False

    # LLM provider settings (placeholders — configure via .env when implemented)
    llm_api_key: str | None = None
    llm_model: str | None = None
    llm_base_url: str | None = None


settings = Settings()

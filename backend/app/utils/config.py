from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration settings.
    Fails fast if required environment variables (like GEMINI_API_KEY) are missing.
    """
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    LOG_LEVEL: str = "INFO"
    REQUEST_TIMEOUT: int = 20  # 20s page timeout + ~8s LLM = ~28s total, under Render's 30s limit
    MAX_CONCURRENT_PAGES: int = 2
    CACHE_TTL: int = 900  # 15 minutes

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """
    Dependency provider for Settings.
    Cached to prevent reading the .env file on every request.
    """
    return Settings()

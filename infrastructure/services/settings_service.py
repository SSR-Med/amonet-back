from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsService(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="api/.env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Amonet Backend documentation"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/myapp"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    JWT_SECRET: str = "supersecretkey"
    JWT_EXPIRATION_HOURS: int = 8


@lru_cache
def get_settings() -> SettingsService:
    return SettingsService()

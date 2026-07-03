from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsService(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "Amonet Backend documentation"
    DEBUG: bool = True
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/myapp"
    PORT: int = 8000
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001"
    JWT_SECRET: str = ""
    JWT_EXPIRATION_HOURS: int = 8
    S3_ENDPOINT: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_REGION: str = "us-east-1"
    S3_BUCKET: str = "amonet"
    S3_EVIDENCIA_PREFIX: str = "inventario/evidencia"
    S3_BACKUP_PREFIX: str = "backups"
    S3_BACKUP_RETENTION_DAYS: int = 5
    UPLOAD_MAX_SIZE_MB: int = 50


@lru_cache
def get_settings() -> SettingsService:
    return SettingsService()

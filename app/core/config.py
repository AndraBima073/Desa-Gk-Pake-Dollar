"""Konfigurasi global aplikasi (dibaca dari environment variables)."""
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pengaturan aplikasi. Override via file .env atau env vars."""

    APP_NAME: str = "Modular AI Backend"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Database (async). Contoh PostgreSQL:
    # postgresql+asyncpg://user:pass@localhost:5432/dbname
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"

    # AI Provider: "local" | "external"
    AI_PROVIDER: str = "local"
    AI_EXTERNAL_API_URL: str = ""
    AI_EXTERNAL_API_KEY: str = ""
    AI_MODEL_NAME: str = "demo-model-v1"
    AI_TIMEOUT_SECONDS: float = 30.0

    # CORS — sesuaikan dengan origin frontend Anda
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Singleton settings (di-cache agar tidak parse .env berulang)."""
    return Settings()

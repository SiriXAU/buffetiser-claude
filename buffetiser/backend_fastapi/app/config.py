"""
Application configuration using Pydantic Settings.
"""
from functools import lru_cache
from typing import Optional

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Buffetiser API"
    VERSION: str = "2.0.0"
    DEBUG: bool = False

    # Database Settings
    POSTGRES_USER: str = "buffetiser"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "BUFFETISER_DB"
    DATABASE_URL: Optional[str] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> str:
        """Build database URL from components."""
        if isinstance(v, str):
            return v

        values = info.data
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        ))

    # Redis Settings
    REDIS_URL: str = "redis://redis:6379"
    CACHE_TTL: int = 300  # 5 minutes

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Australian Tax Settings
    TAX_FINANCIAL_YEAR_START_MONTH: int = 7  # July
    TAX_FINANCIAL_YEAR_START_DAY: int = 1
    CGT_DISCOUNT_RATE: float = 0.5  # 50% discount for assets held > 12 months
    CGT_HOLDING_PERIOD_DAYS: int = 365  # 12 months

    # Price Update Settings
    UPDATE_TIME: str = "15:00"
    UPDATE_TIMEZONE: str = "Australia/Perth"

    # CORS Settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:81",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

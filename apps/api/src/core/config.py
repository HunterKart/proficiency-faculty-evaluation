"""Centralized configuration module for the API service."""

from __future__ import annotations

import os
from functools import lru_cache

from pydantic import BaseModel, Field


def _env(key: str, default: str) -> str:
    """Return environment variable value with a fallback."""
    value = os.getenv(key)
    return value if value else default


class Settings(BaseModel):
    """Application configuration sourced from environment variables."""

    app_name: str = "Proficiency API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = Field(default_factory=lambda: _env("DATABASE_URL", "sqlite:///./dev.db"))

    model_config = {"frozen": True}


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()

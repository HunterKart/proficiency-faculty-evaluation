"""Centralized configuration module for the API service."""

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Proficiency API"
    api_v1_prefix: str = "/api/v1"


settings = Settings()

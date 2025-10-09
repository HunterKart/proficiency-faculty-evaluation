"""Shared response models for health endpoints."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str

"""Database engine, session factory, and declarative base."""

from __future__ import annotations

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from ..core.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""


# Engine is created eagerly so Alembic and the API share configuration.
engine: Engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)

# Session factory used across the application.
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is properly closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["Base", "engine", "SessionLocal", "get_db"]

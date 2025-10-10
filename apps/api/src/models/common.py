"""Common mixins and utilities for SQLAlchemy models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Reusable mixin for timestamped models."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )


class CreatedAtMixin:
    """Mixin for models that only track creation time."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.now(),
        nullable=False,
    )


__all__ = ["TimestampMixin", "CreatedAtMixin"]


def enum_column(enum_cls: type[Enum], name: str) -> SAEnum:
    """Return a SQLAlchemy Enum column using enumeration values."""

    return SAEnum(enum_cls, name=name, values_callable=lambda obj: [member.value for member in obj])


__all__.append("enum_column")

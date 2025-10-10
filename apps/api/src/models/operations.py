"""Operational support models such as background tasks and audit logs."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .common import TimestampMixin, enum_column
from .enums import (
    BackgroundJobStatus,
    BackgroundJobType,
    NotificationStatus,
)


class BackgroundTask(TimestampMixin, Base):
    """Unified record of asynchronous jobs."""

    __tablename__ = "background_tasks"
    __table_args__ = (
        Index("idx_tasks_status", "status"),
        Index("idx_tasks_job_type", "job_type"),
        Index("idx_tasks_submitted_by", "submitted_by_user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    job_type: Mapped[BackgroundJobType] = mapped_column(
        enum_column(BackgroundJobType, "background_job_type"),
        nullable=False,
    )
    status: Mapped[BackgroundJobStatus] = mapped_column(
        enum_column(BackgroundJobStatus, "background_job_status"),
        default=BackgroundJobStatus.QUEUED,
        nullable=False,
    )
    submitted_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    job_parameters: Mapped[Optional[dict]] = mapped_column(JSON)
    progress: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    result_message: Mapped[Optional[str]] = mapped_column(Text)
    result_storage_path: Mapped[Optional[str]] = mapped_column(String(1024))
    log_output: Mapped[Optional[str]] = mapped_column(Text)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False))
    rows_total: Mapped[Optional[int]] = mapped_column(Integer)
    rows_processed: Mapped[Optional[int]] = mapped_column(Integer)
    rows_failed: Mapped[Optional[int]] = mapped_column(Integer)

    university: Mapped["University"] = relationship("University", back_populates="background_tasks")
    submitted_by: Mapped["User"] = relationship("User", back_populates="submitted_background_tasks")


class AuditLog(Base):
    """Security and operations audit trail."""

    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_audit_action", "action"),
        Index("idx_audit_target", "target_entity", "target_id"),
        Index("idx_audit_actor", "actor_user_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    university_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("universities.id", ondelete="SET NULL")
    )
    actor_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    target_entity: Mapped[Optional[str]] = mapped_column(String(100))
    target_id: Mapped[Optional[int]] = mapped_column(Integer)
    details: Mapped[Optional[dict]] = mapped_column(JSON)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )

    university: Mapped[Optional["University"]] = relationship("University", back_populates="audit_logs")
    actor: Mapped[Optional["User"]] = relationship("User", back_populates="audit_events")


class Notification(TimestampMixin, Base):
    """In-app and email notification record."""

    __tablename__ = "notifications"
    __table_args__ = (
        Index("idx_notifications_recipient", "recipient_id", "recipient_type"),
        Index("idx_notifications_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE")
    )
    recipient_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recipient_type: Mapped[str] = mapped_column(String(50), nullable=False)
    actor_id: Mapped[Optional[int]] = mapped_column(Integer)
    actor_type: Mapped[Optional[str]] = mapped_column(String(50))
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    delivery_methods: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    status: Mapped[NotificationStatus] = mapped_column(
        enum_column(NotificationStatus, "notification_status"),
        default=NotificationStatus.UNREAD,
        nullable=False,
    )
    read_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False))

    university: Mapped[Optional["University"]] = relationship(
        "University",
        back_populates="notifications",
    )


class UniversitySetting(TimestampMixin, Base):
    """Tenant-specific configuration."""

    __tablename__ = "university_settings"
    __table_args__ = (
        UniqueConstraint("university_id", "setting_name", name="uk_university_setting_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    setting_name: Mapped[str] = mapped_column(String(100), nullable=False)
    setting_value: Mapped[str] = mapped_column(String(255), nullable=False)

    university: Mapped["University"] = relationship("University", back_populates="settings")


__all__ = ["BackgroundTask", "AuditLog", "Notification", "UniversitySetting"]

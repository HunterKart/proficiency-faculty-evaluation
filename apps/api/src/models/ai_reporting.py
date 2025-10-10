"""AI assistant and reporting models."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .common import TimestampMixin, enum_column
from .enums import GeneratedReportStatus, ReportFileFormat


class AISuggestion(TimestampMixin, Base):
    """Stored AI-generated suggestion report."""

    __tablename__ = "ai_suggestions"
    __table_args__ = (
        Index("idx_ai_suggestions_for_user", "generated_for_user_id"),
        Index("idx_ai_suggestions_by_user", "generated_by_user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    generated_for_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    generated_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    context_school_term_id: Mapped[int] = mapped_column(
        ForeignKey("school_terms.id"),
        nullable=False,
    )
    context_assessment_period_id: Mapped[int] = mapped_column(
        ForeignKey("assessment_periods.id"),
        nullable=False,
    )
    suggestion_title: Mapped[str] = mapped_column(String(255), nullable=False)
    suggestion_content: Mapped[str] = mapped_column(Text, nullable=False)
    prompt_sent_to_api: Mapped[str] = mapped_column(Text, nullable=False)

    university: Mapped["University"] = relationship("University", back_populates="ai_suggestions")
    generated_for: Mapped["User"] = relationship(
        "User",
        foreign_keys=[generated_for_user_id],
        back_populates="ai_suggestion_subjects",
    )
    generated_by: Mapped["User"] = relationship(
        "User",
        foreign_keys=[generated_by_user_id],
        back_populates="generated_ai_suggestions",
    )
    context_term: Mapped["SchoolTerm"] = relationship("SchoolTerm", back_populates="ai_suggestions")
    context_assessment_period: Mapped["AssessmentPeriod"] = relationship(
        "AssessmentPeriod",
        back_populates="ai_suggestions",
    )


class GeneratedReport(TimestampMixin, Base):
    """Asynchronous generated report artifact."""

    __tablename__ = "generated_reports"
    __table_args__ = (
        Index("idx_reports_status", "status"),
        Index("idx_reports_requested_by", "requested_by_user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    requested_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    report_type: Mapped[str] = mapped_column(String(100), nullable=False)
    report_parameters: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[GeneratedReportStatus] = mapped_column(
        enum_column(GeneratedReportStatus, "generated_report_status"),
        default=GeneratedReportStatus.QUEUED,
        nullable=False,
    )
    file_format: Mapped[ReportFileFormat] = mapped_column(
        enum_column(ReportFileFormat, "generated_report_file_format"),
        nullable=False,
    )
    storage_path: Mapped[Optional[str]] = mapped_column(String(1024))
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)

    university: Mapped["University"] = relationship("University", back_populates="generated_reports")
    requested_by: Mapped["User"] = relationship("User", back_populates="requested_reports")


__all__ = ["AISuggestion", "GeneratedReport"]

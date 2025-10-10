"""Evaluation submission models storing raw responses."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .common import TimestampMixin, enum_column
from .enums import (
    AnalysisPipelineStatus,
    EvaluationSubmissionStatus,
    FlagReason,
    FlagResolution,
    FlagStatus,
    IntegrityCheckStatus,
)


class EvaluationSubmission(TimestampMixin, Base):
    """Central record for a completed evaluation submission."""

    __tablename__ = "evaluation_submissions"
    __table_args__ = (
        UniqueConstraint(
            "evaluation_period_id",
            "evaluator_id",
            "evaluatee_id",
            "subject_offering_id",
            name="uk_submission_uniqueness",
        ),
        Index("idx_submissions_status", "status"),
        Index("idx_submissions_integrity_status", "integrity_check_status"),
        Index("idx_submissions_analysis_status", "analysis_status"),
        Index("idx_evaluatee_period", "evaluatee_id", "evaluation_period_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    evaluation_period_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_periods.id"),
        nullable=False,
    )
    evaluator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    evaluatee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    subject_offering_id: Mapped[int] = mapped_column(
        ForeignKey("subject_offerings.id"),
        nullable=False,
    )
    status: Mapped[EvaluationSubmissionStatus] = mapped_column(
        enum_column(EvaluationSubmissionStatus, "evaluation_submission_status"),
        default=EvaluationSubmissionStatus.SUBMITTED,
        nullable=False,
    )
    integrity_check_status: Mapped[IntegrityCheckStatus] = mapped_column(
        enum_column(IntegrityCheckStatus, "integrity_check_status"),
        default=IntegrityCheckStatus.PENDING,
        nullable=False,
    )
    analysis_status: Mapped[AnalysisPipelineStatus] = mapped_column(
        enum_column(AnalysisPipelineStatus, "analysis_pipeline_status"),
        default=AnalysisPipelineStatus.PENDING,
        nullable=False,
    )
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
    )
    is_resubmission: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    original_submission_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("evaluation_submissions.id", ondelete="SET NULL"),
    )

    university: Mapped["University"] = relationship("University", back_populates="evaluation_submissions")
    evaluation_period: Mapped["EvaluationPeriod"] = relationship(
        "EvaluationPeriod",
        back_populates="submissions",
    )
    evaluator: Mapped["User"] = relationship(
        "User",
        foreign_keys=[evaluator_id],
        back_populates="submitted_evaluations",
    )
    evaluatee: Mapped["User"] = relationship(
        "User",
        foreign_keys=[evaluatee_id],
        back_populates="received_evaluations",
    )
    subject_offering: Mapped["SubjectOffering"] = relationship(
        "SubjectOffering",
        back_populates="evaluation_submissions",
    )
    original_submission: Mapped[Optional["EvaluationSubmission"]] = relationship(
        remote_side="EvaluationSubmission.id",
        back_populates="resubmissions",
    )
    resubmissions: Mapped[List["EvaluationSubmission"]] = relationship(
        back_populates="original_submission",
    )
    likert_answers: Mapped[List["EvaluationLikertAnswer"]] = relationship(
        "EvaluationLikertAnswer",
        back_populates="submission",
        cascade="all, delete-orphan",
    )
    open_ended_answers: Mapped[List["EvaluationOpenEndedAnswer"]] = relationship(
        "EvaluationOpenEndedAnswer",
        back_populates="submission",
        cascade="all, delete-orphan",
    )
    flag: Mapped[Optional["FlaggedEvaluation"]] = relationship(
        "FlaggedEvaluation",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan",
    )
    numerical_aggregate: Mapped[Optional["NumericalAggregate"]] = relationship(
        "NumericalAggregate",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan",
    )
    sentiment_aggregate: Mapped[Optional["SentimentAggregate"]] = relationship(
        "SentimentAggregate",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan",
    )


class EvaluationLikertAnswer(TimestampMixin, Base):
    """Likert answer for a question."""

    __tablename__ = "evaluation_likert_answers"
    __table_args__ = (
        UniqueConstraint("submission_id", "question_id", name="uk_likert_answer_uniqueness"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_submissions.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    answer_value: Mapped[int] = mapped_column(Integer, nullable=False)

    submission: Mapped["EvaluationSubmission"] = relationship(back_populates="likert_answers")
    question: Mapped["EvaluationQuestion"] = relationship(back_populates="likert_answers")


class EvaluationOpenEndedAnswer(TimestampMixin, Base):
    """Open ended response for a question."""

    __tablename__ = "evaluation_open_ended_answers"
    __table_args__ = (
        UniqueConstraint("submission_id", "question_id", name="uk_open_answer_uniqueness"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_submissions.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_questions.id", ondelete="CASCADE"),
        nullable=False,
    )
    answer_text: Mapped[str] = mapped_column(Text, nullable=False)

    submission: Mapped["EvaluationSubmission"] = relationship(back_populates="open_ended_answers")
    question: Mapped["EvaluationQuestion"] = relationship(back_populates="open_ended_answers")
    sentiment: Mapped[Optional["OpenEndedSentiment"]] = relationship(
        "OpenEndedSentiment",
        back_populates="open_ended_answer",
        uselist=False,
        cascade="all, delete-orphan",
    )
    keywords: Mapped[List["OpenEndedKeyword"]] = relationship(
        "OpenEndedKeyword",
        back_populates="open_ended_answer",
        cascade="all, delete-orphan",
    )


class FlaggedEvaluation(TimestampMixin, Base):
    """Submission flagged for review."""

    __tablename__ = "flagged_evaluations"
    __table_args__ = (
        Index("idx_flagged_status", "status"),
        Index("idx_flagged_resolution", "resolution"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_submissions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    flag_reason: Mapped[FlagReason] = mapped_column(
        enum_column(FlagReason, "flagged_evaluation_reason"),
        nullable=False,
    )
    flag_details: Mapped[Optional[dict]] = mapped_column(JSON)
    status: Mapped[FlagStatus] = mapped_column(
        enum_column(FlagStatus, "flagged_evaluation_status"),
        default=FlagStatus.PENDING,
        nullable=False,
    )
    resolution: Mapped[Optional[FlagResolution]] = mapped_column(
        enum_column(FlagResolution, "flagged_evaluation_resolution")
    )
    resolved_by_admin_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False))
    admin_notes: Mapped[Optional[str]] = mapped_column(Text)
    resubmission_grace_period_ends_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False))
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    submission: Mapped["EvaluationSubmission"] = relationship(back_populates="flag")
    resolved_by: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="resolved_flags",
    )


__all__ = [
    "EvaluationSubmission",
    "EvaluationLikertAnswer",
    "EvaluationOpenEndedAnswer",
    "FlaggedEvaluation",
]

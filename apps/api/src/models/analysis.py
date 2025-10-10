"""Processed analytics data models."""

from __future__ import annotations


from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .common import TimestampMixin, enum_column
from .enums import SentimentLabel


class NumericalAggregate(TimestampMixin, Base):
    """Quantitative aggregate scores for a submission."""

    __tablename__ = "numerical_aggregates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_submissions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    per_question_median_scores: Mapped[dict] = mapped_column(JSON, nullable=False)
    per_criterion_average_scores: Mapped[dict] = mapped_column(JSON, nullable=False)
    quant_score_raw: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    z_quant: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    final_score_60_40: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    cohort_n: Mapped[int] = mapped_column(Integer, nullable=False)
    cohort_mean: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    cohort_std_dev: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    is_final_snapshot: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    submission: Mapped["EvaluationSubmission"] = relationship(
        "EvaluationSubmission",
        back_populates="numerical_aggregate",
    )


class OpenEndedSentiment(TimestampMixin, Base):
    """Sentiment inference for an open-ended answer."""

    __tablename__ = "open_ended_sentiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    open_ended_answer_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_open_ended_answers.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    predicted_sentiment_label: Mapped[SentimentLabel] = mapped_column(
        enum_column(SentimentLabel, "sentiment_label"),
        nullable=False,
    )
    predicted_sentiment_label_score: Mapped[float] = mapped_column(Float, nullable=False)
    positive_score: Mapped[float] = mapped_column(Float, nullable=False)
    neutral_score: Mapped[float] = mapped_column(Float, nullable=False)
    negative_score: Mapped[float] = mapped_column(Float, nullable=False)
    accuracy: Mapped[float] = mapped_column(Float, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=True)

    open_ended_answer: Mapped["EvaluationOpenEndedAnswer"] = relationship(
        "EvaluationOpenEndedAnswer",
        back_populates="sentiment",
    )


class OpenEndedKeyword(TimestampMixin, Base):
    """Keywords extracted from open-ended responses."""

    __tablename__ = "open_ended_keywords"
    __table_args__ = (
        UniqueConstraint("open_ended_answer_id", "keyword", name="uk_answer_keyword"),
        Index("idx_keyword", "keyword"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    open_ended_answer_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_open_ended_answers.id", ondelete="CASCADE"),
        nullable=False,
    )
    keyword: Mapped[str] = mapped_column(String(255), nullable=False)
    relevance_score: Mapped[float] = mapped_column(Float, nullable=False)

    open_ended_answer: Mapped["EvaluationOpenEndedAnswer"] = relationship(
        "EvaluationOpenEndedAnswer",
        back_populates="keywords",
    )


class SentimentAggregate(TimestampMixin, Base):
    """Qualitative aggregated sentiment scores for a submission."""

    __tablename__ = "sentiment_aggregates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_submissions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )
    average_positive_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    average_neutral_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    average_negative_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    qual_score_raw: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    z_qual: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    is_final_snapshot: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    submission: Mapped["EvaluationSubmission"] = relationship(
        "EvaluationSubmission",
        back_populates="sentiment_aggregate",
    )


__all__ = [
    "NumericalAggregate",
    "OpenEndedSentiment",
    "OpenEndedKeyword",
    "SentimentAggregate",
]

"""Evaluation configuration models."""

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
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .common import TimestampMixin, enum_column
from .enums import EvaluationAudience, EvaluationFormStatus, EvaluationPeriodStatus, QuestionType


class LikertScaleTemplate(Base):
    """Predefined likert scale definition."""

    __tablename__ = "likert_scale_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    point_values: Mapped[dict] = mapped_column(JSON, nullable=False)
    min_value: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    max_value: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    form_templates: Mapped[List["EvaluationFormTemplate"]] = relationship(
        "EvaluationFormTemplate",
        back_populates="likert_scale_template",
    )


class EvaluationFormTemplate(TimestampMixin, Base):
    """Reusable evaluation form template."""

    __tablename__ = "evaluation_form_templates"
    __table_args__ = (
        UniqueConstraint("university_id", "name", name="uk_university_form_name"),
        Index("idx_forms_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    likert_scale_template_id: Mapped[int] = mapped_column(
        ForeignKey("likert_scale_templates.id"),
        nullable=False,
    )
    intended_for: Mapped[EvaluationAudience] = mapped_column(
        enum_column(EvaluationAudience, "evaluation_intended_for"),
        nullable=False,
    )
    status: Mapped[EvaluationFormStatus] = mapped_column(
        enum_column(EvaluationFormStatus, "evaluation_form_status"),
        default=EvaluationFormStatus.DRAFT,
        nullable=False,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    university: Mapped["University"] = relationship("University", back_populates="form_templates")
    likert_scale_template: Mapped["LikertScaleTemplate"] = relationship(back_populates="form_templates")
    criteria: Mapped[List["EvaluationCriterion"]] = relationship(
        "EvaluationCriterion",
        back_populates="form_template",
        cascade="all, delete-orphan",
    )
    questions: Mapped[List["EvaluationQuestion"]] = relationship(
        "EvaluationQuestion",
        back_populates="form_template",
        cascade="all, delete-orphan",
    )
    student_evaluation_periods: Mapped[List["EvaluationPeriod"]] = relationship(
        "EvaluationPeriod",
        foreign_keys="EvaluationPeriod.student_form_template_id",
        back_populates="student_form_template",
    )
    dept_head_evaluation_periods: Mapped[List["EvaluationPeriod"]] = relationship(
        "EvaluationPeriod",
        foreign_keys="EvaluationPeriod.dept_head_form_template_id",
        back_populates="dept_head_form_template",
    )


class EvaluationCriterion(TimestampMixin, Base):
    """Thematic section within a form."""

    __tablename__ = "evaluation_criteria"
    __table_args__ = (
        UniqueConstraint("form_template_id", "name", name="uk_form_criterion_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    form_template_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_form_templates.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    weight: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    order: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)

    form_template: Mapped["EvaluationFormTemplate"] = relationship(back_populates="criteria")
    questions: Mapped[List["EvaluationQuestion"]] = relationship(
        "EvaluationQuestion",
        back_populates="criterion",
    )


class EvaluationQuestion(TimestampMixin, Base):
    """Individual form question."""

    __tablename__ = "evaluation_questions"
    __table_args__ = (
        Index("idx_questions_form_template_id", "form_template_id"),
        Index("idx_questions_criterion_id", "criterion_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    form_template_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_form_templates.id", ondelete="CASCADE"),
        nullable=False,
    )
    criterion_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("evaluation_criteria.id", ondelete="CASCADE"),
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(
        enum_column(QuestionType, "evaluation_question_type"),
        nullable=False,
    )
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    min_word_count: Mapped[Optional[int]] = mapped_column(SmallInteger)
    max_word_count: Mapped[Optional[int]] = mapped_column(SmallInteger)
    order: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)

    form_template: Mapped["EvaluationFormTemplate"] = relationship(back_populates="questions")
    criterion: Mapped[Optional["EvaluationCriterion"]] = relationship(back_populates="questions")
    likert_answers: Mapped[List["EvaluationLikertAnswer"]] = relationship(
        "EvaluationLikertAnswer",
        back_populates="question",
    )
    open_ended_answers: Mapped[List["EvaluationOpenEndedAnswer"]] = relationship(
        "EvaluationOpenEndedAnswer",
        back_populates="question",
    )


class EvaluationPeriod(TimestampMixin, Base):
    """Defines active evaluation run for a term."""

    __tablename__ = "evaluation_periods"
    __table_args__ = (
        UniqueConstraint(
            "university_id",
            "school_term_id",
            "assessment_period_id",
            name="uk_university_term_assessment",
        ),
        Index("idx_periods_status", "status"),
        Index("idx_periods_start_time", "start_date_time"),
        Index("idx_periods_end_time", "end_date_time"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    school_term_id: Mapped[int] = mapped_column(
        ForeignKey("school_terms.id"),
        nullable=False,
    )
    assessment_period_id: Mapped[int] = mapped_column(
        ForeignKey("assessment_periods.id"),
        nullable=False,
    )
    student_form_template_id: Mapped[int] = mapped_column(
        ForeignKey("evaluation_form_templates.id"),
        nullable=False,
    )
    dept_head_form_template_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("evaluation_form_templates.id"),
    )
    start_date_time: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    end_date_time: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    status: Mapped[EvaluationPeriodStatus] = mapped_column(
        enum_column(EvaluationPeriodStatus, "evaluation_period_status"),
        nullable=False,
        default=EvaluationPeriodStatus.SCHEDULED,
    )

    university: Mapped["University"] = relationship("University", back_populates="evaluation_periods")
    school_term: Mapped["SchoolTerm"] = relationship("SchoolTerm", back_populates="evaluation_periods")
    assessment_period: Mapped["AssessmentPeriod"] = relationship(
        "AssessmentPeriod",
        back_populates="evaluation_periods",
    )
    student_form_template: Mapped["EvaluationFormTemplate"] = relationship(
        "EvaluationFormTemplate",
        foreign_keys=[student_form_template_id],
        back_populates="student_evaluation_periods",
    )
    dept_head_form_template: Mapped[Optional["EvaluationFormTemplate"]] = relationship(
        "EvaluationFormTemplate",
        foreign_keys=[dept_head_form_template_id],
        back_populates="dept_head_evaluation_periods",
    )
    submissions: Mapped[List["EvaluationSubmission"]] = relationship(
        "EvaluationSubmission",
        back_populates="evaluation_period",
        cascade="all, delete-orphan",
    )


__all__ = [
    "LikertScaleTemplate",
    "EvaluationFormTemplate",
    "EvaluationCriterion",
    "EvaluationQuestion",
    "EvaluationPeriod",
]

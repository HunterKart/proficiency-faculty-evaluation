"""Academic structure models."""

from __future__ import annotations

from typing import List, Optional

from sqlalchemy import (
    Boolean,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .common import TimestampMixin, enum_column
from .enums import AssessmentPeriodName, ModalityName, SemesterTerm


class Department(TimestampMixin, Base):
    """Organizational unit within a university."""

    __tablename__ = "departments"
    __table_args__ = (
        UniqueConstraint("university_id", "name", name="uk_university_department_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    parent_department_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("departments.id", ondelete="SET NULL")
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    short_name: Mapped[Optional[str]] = mapped_column(String(50))
    head_user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
    )

    university: Mapped["University"] = relationship("University", back_populates="departments")
    parent_department: Mapped[Optional["Department"]] = relationship(
        remote_side="Department.id",
        back_populates="child_departments",
    )
    child_departments: Mapped[List["Department"]] = relationship(
        back_populates="parent_department",
    )
    head: Mapped[Optional["User"]] = relationship("User", back_populates="headed_departments")
    programs: Mapped[List["Program"]] = relationship("Program", back_populates="department")
    subjects: Mapped[List["Subject"]] = relationship("Subject", back_populates="department")
    faculty_affiliations: Mapped[List["FacultyDepartmentAffiliation"]] = relationship(
        "FacultyDepartmentAffiliation",
        back_populates="department",
        cascade="all, delete-orphan",
    )


class Program(TimestampMixin, Base):
    """Specific academic program or degree."""

    __tablename__ = "programs"
    __table_args__ = (
        UniqueConstraint("university_id", "program_code", name="uk_university_program_code"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    program_code: Mapped[str] = mapped_column(String(50), nullable=False)

    university: Mapped["University"] = relationship("University", back_populates="programs")
    department: Mapped["Department"] = relationship(back_populates="programs")
    students: Mapped[List["User"]] = relationship("User", back_populates="program")


class Subject(TimestampMixin, Base):
    """Subject template definition."""

    __tablename__ = "subjects"
    __table_args__ = (
        UniqueConstraint("university_id", "edp_code", name="uk_university_edp_code"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
    )
    edp_code: Mapped[str] = mapped_column(String(50), nullable=False)
    subject_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    university: Mapped["University"] = relationship("University", back_populates="subjects")
    department: Mapped["Department"] = relationship(back_populates="subjects")
    offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="subject",
        cascade="all, delete-orphan",
    )


class SchoolYear(Base):
    """Academic year definition."""

    __tablename__ = "school_years"
    __table_args__ = (
        UniqueConstraint("year_start", "year_end", name="uk_school_year"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    year_start: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    year_end: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    terms: Mapped[List["SchoolTerm"]] = relationship(
        "SchoolTerm",
        back_populates="school_year",
        cascade="all, delete-orphan",
    )


class SchoolTerm(Base):
    """Specific term within a school year."""

    __tablename__ = "school_terms"
    __table_args__ = (
        UniqueConstraint("school_year_id", "semester", name="uk_school_term"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    school_year_id: Mapped[int] = mapped_column(
        ForeignKey("school_years.id", ondelete="CASCADE"),
        nullable=False,
    )
    semester: Mapped[SemesterTerm] = mapped_column(
        enum_column(SemesterTerm, "school_term_semester"),
        nullable=False,
    )

    school_year: Mapped["SchoolYear"] = relationship(back_populates="terms")
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="school_term",
    )
    faculty_affiliations: Mapped[List["FacultyDepartmentAffiliation"]] = relationship(
        "FacultyDepartmentAffiliation",
        back_populates="school_term",
    )
    evaluation_periods: Mapped[List["EvaluationPeriod"]] = relationship(
        "EvaluationPeriod",
        back_populates="school_term",
    )
    ai_suggestions: Mapped[List["AISuggestion"]] = relationship(
        "AISuggestion",
        back_populates="context_term",
    )


class AssessmentPeriod(Base):
    """Assessment slice such as Midterm or Finals."""

    __tablename__ = "assessment_periods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[AssessmentPeriodName] = mapped_column(
        enum_column(AssessmentPeriodName, "assessment_period_name"),
        nullable=False,
        unique=True,
    )

    evaluation_periods: Mapped[List["EvaluationPeriod"]] = relationship(
        "EvaluationPeriod",
        back_populates="assessment_period",
    )
    ai_suggestions: Mapped[List["AISuggestion"]] = relationship(
        "AISuggestion",
        back_populates="context_assessment_period",
    )


class Modality(Base):
    """Mode of instruction."""

    __tablename__ = "modalities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[ModalityName] = mapped_column(
        enum_column(ModalityName, "modality_name"),
        nullable=False,
        unique=True,
    )

    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="modality",
    )


class FacultyDepartmentAffiliation(TimestampMixin, Base):
    """Tracks faculty assignment per term and department."""

    __tablename__ = "faculty_department_affiliations"
    __table_args__ = (
        UniqueConstraint(
            "faculty_id",
            "department_id",
            "school_term_id",
            name="uk_faculty_department_term",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"),
        nullable=False,
    )
    school_term_id: Mapped[int] = mapped_column(
        ForeignKey("school_terms.id", ondelete="CASCADE"),
        nullable=False,
    )
    is_home_department: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    faculty: Mapped["User"] = relationship("User", back_populates="faculty_affiliations")
    department: Mapped["Department"] = relationship(back_populates="faculty_affiliations")
    school_term: Mapped["SchoolTerm"] = relationship(back_populates="faculty_affiliations")


class SubjectOffering(TimestampMixin, Base):
    """Concrete class instance for a subject."""

    __tablename__ = "subject_offerings"
    __table_args__ = (
        Index("idx_faculty_term", "faculty_id", "school_term_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
    )
    faculty_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    school_term_id: Mapped[int] = mapped_column(
        ForeignKey("school_terms.id", ondelete="CASCADE"),
        nullable=False,
    )
    modality_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("modalities.id", ondelete="SET NULL")
    )

    university: Mapped["University"] = relationship("University", back_populates="subject_offerings")
    subject: Mapped["Subject"] = relationship(back_populates="offerings")
    faculty: Mapped["User"] = relationship("User", back_populates="subject_offerings")
    school_term: Mapped["SchoolTerm"] = relationship(back_populates="subject_offerings")
    modality: Mapped[Optional["Modality"]] = relationship(back_populates="subject_offerings")
    enrollments: Mapped[List["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="subject_offering",
        cascade="all, delete-orphan",
    )
    evaluation_submissions: Mapped[List["EvaluationSubmission"]] = relationship(
        "EvaluationSubmission",
        back_populates="subject_offering",
    )


class Enrollment(TimestampMixin, Base):
    """Student enrollment within a subject offering."""

    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "subject_offering_id", name="uk_student_offering"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    subject_offering_id: Mapped[int] = mapped_column(
        ForeignKey("subject_offerings.id", ondelete="CASCADE"),
        nullable=False,
    )

    university: Mapped["University"] = relationship("University", back_populates="enrollments")
    student: Mapped["User"] = relationship("User", back_populates="enrollments")
    subject_offering: Mapped["SubjectOffering"] = relationship(back_populates="enrollments")


__all__ = [
    "Department",
    "Program",
    "Subject",
    "SchoolYear",
    "SchoolTerm",
    "AssessmentPeriod",
    "Modality",
    "FacultyDepartmentAffiliation",
    "SubjectOffering",
    "Enrollment",
]

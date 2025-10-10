"""Core identity and tenancy models."""

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
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db import Base
from .common import CreatedAtMixin, TimestampMixin, enum_column
from .enums import (
    RegistrationCodeStatus,
    SuperAdminStatus,
    UniversityRegistrationStatus,
    UniversityStatus,
    UserStatus,
)


class University(TimestampMixin, Base):
    """Tenant institution."""

    __tablename__ = "universities"
    __table_args__ = (
        Index("idx_universities_name", "name"),
        Index("idx_universities_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    street: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    country: Mapped[Optional[str]] = mapped_column(String(100))
    postal_code: Mapped[Optional[str]] = mapped_column(String(20))
    status: Mapped[UniversityStatus] = mapped_column(
        enum_column(UniversityStatus, "university_status"),
        default=UniversityStatus.PENDING,
        nullable=False,
    )

    registration_requests: Mapped[List["UniversityRegistrationRequest"]] = relationship(
        back_populates="university",
        passive_deletes=True,
    )
    registration_codes: Mapped[List["RegistrationCode"]] = relationship(
        back_populates="university",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    users: Mapped[List["User"]] = relationship(
        back_populates="university",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    departments: Mapped[List["Department"]] = relationship("Department", back_populates="university")
    programs: Mapped[List["Program"]] = relationship("Program", back_populates="university")
    subjects: Mapped[List["Subject"]] = relationship("Subject", back_populates="university")
    form_templates: Mapped[List["EvaluationFormTemplate"]] = relationship(
        "EvaluationFormTemplate",
        back_populates="university",
        cascade="all, delete-orphan",
    )
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="university",
    )
    enrollments: Mapped[List["Enrollment"]] = relationship("Enrollment", back_populates="university")
    evaluation_periods: Mapped[List["EvaluationPeriod"]] = relationship(
        "EvaluationPeriod",
        back_populates="university",
    )
    evaluation_submissions: Mapped[List["EvaluationSubmission"]] = relationship(
        "EvaluationSubmission",
        back_populates="university",
    )
    ai_suggestions: Mapped[List["AISuggestion"]] = relationship(
        "AISuggestion",
        back_populates="university",
    )
    generated_reports: Mapped[List["GeneratedReport"]] = relationship(
        "GeneratedReport",
        back_populates="university",
    )
    background_tasks: Mapped[List["BackgroundTask"]] = relationship(
        "BackgroundTask",
        back_populates="university",
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="university")
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification",
        back_populates="university",
    )
    settings: Mapped[List["UniversitySetting"]] = relationship(
        "UniversitySetting",
        back_populates="university",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class UniversityRegistrationRequest(TimestampMixin, Base):
    """Registration pipeline for onboarding universities."""

    __tablename__ = "university_registration_requests"
    __table_args__ = (
        UniqueConstraint("contact_person_email", name="uk_contact_person_email"),
        Index("idx_requests_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_person_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_person_email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[UniversityRegistrationStatus] = mapped_column(
        enum_column(UniversityRegistrationStatus, "registration_request_status"),
        default=UniversityRegistrationStatus.SUBMITTED,
        nullable=False,
    )
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text)
    details: Mapped[Optional[dict]] = mapped_column(JSON)
    university_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("universities.id", ondelete="SET NULL"),
    )

    university: Mapped[Optional["University"]] = relationship(back_populates="registration_requests")
    documents: Mapped[List["Document"]] = relationship(
        back_populates="request",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Document(CreatedAtMixin, Base):
    """Uploaded supporting document."""

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("university_registration_requests.id", ondelete="CASCADE"),
        nullable=False,
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    request: Mapped["UniversityRegistrationRequest"] = relationship(back_populates="documents")


class Role(Base):
    """Static role catalog."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    users: Mapped[List["User"]] = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles",
    )
    user_roles: Mapped[List["UserRole"]] = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan",
    )
    registration_codes: Mapped[List["RegistrationCode"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )


class SuperAdmin(TimestampMixin, Base):
    """Platform-level administrator."""

    __tablename__ = "super_admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    pin_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[SuperAdminStatus] = mapped_column(
        enum_column(SuperAdminStatus, "super_admin_status"),
        default=SuperAdminStatus.ACTIVE,
        nullable=False,
    )
    token_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


class RegistrationCode(CreatedAtMixin, Base):
    """Controlled access registration codes."""

    __tablename__ = "registration_codes"
    __table_args__ = (
        Index("idx_reg_codes_university_id", "university_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
    )
    code_value: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    max_uses: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    current_uses: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[RegistrationCodeStatus] = mapped_column(
        enum_column(RegistrationCodeStatus, "registration_code_status"),
        default=RegistrationCodeStatus.ACTIVE,
        nullable=False,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=False))

    university: Mapped["University"] = relationship(back_populates="registration_codes")
    role: Mapped["Role"] = relationship(back_populates="registration_codes")
    users: Mapped[List["User"]] = relationship(back_populates="registration_code")


class User(TimestampMixin, Base):
    """Application user tied to a university."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("university_id", "school_id", name="uk_university_school_id"),
        Index("idx_users_status", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    university_id: Mapped[int] = mapped_column(
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    school_id: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[UserStatus] = mapped_column(
        enum_column(UserStatus, "user_status"),
        default=UserStatus.UNVERIFIED,
        nullable=False,
    )
    program_id: Mapped[Optional[int]] = mapped_column(ForeignKey("programs.id", ondelete="SET NULL"))
    registration_code_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("registration_codes.id", ondelete="SET NULL"),
    )
    token_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    university: Mapped["University"] = relationship(back_populates="users")
    program: Mapped[Optional["Program"]] = relationship(
        "Program",
        back_populates="students",
    )
    registration_code: Mapped[Optional["RegistrationCode"]] = relationship(back_populates="users")
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
    )
    user_roles: Mapped[List["UserRole"]] = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    faculty_affiliations: Mapped[List["FacultyDepartmentAffiliation"]] = relationship(
        "FacultyDepartmentAffiliation",
        back_populates="faculty",
        cascade="all, delete-orphan",
    )
    subject_offerings: Mapped[List["SubjectOffering"]] = relationship(
        "SubjectOffering",
        back_populates="faculty",
    )
    headed_departments: Mapped[List["Department"]] = relationship(
        "Department",
        back_populates="head",
        foreign_keys="Department.head_user_id",
    )
    enrollments: Mapped[List["Enrollment"]] = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan",
    )
    submitted_evaluations: Mapped[List["EvaluationSubmission"]] = relationship(
        "EvaluationSubmission",
        foreign_keys="EvaluationSubmission.evaluator_id",
        back_populates="evaluator",
    )
    received_evaluations: Mapped[List["EvaluationSubmission"]] = relationship(
        "EvaluationSubmission",
        foreign_keys="EvaluationSubmission.evaluatee_id",
        back_populates="evaluatee",
    )
    resolved_flags: Mapped[List["FlaggedEvaluation"]] = relationship(
        "FlaggedEvaluation",
        foreign_keys="FlaggedEvaluation.resolved_by_admin_id",
        back_populates="resolved_by",
    )
    submitted_background_tasks: Mapped[List["BackgroundTask"]] = relationship(
        "BackgroundTask",
        back_populates="submitted_by",
    )
    generated_ai_suggestions: Mapped[List["AISuggestion"]] = relationship(
        "AISuggestion",
        foreign_keys="AISuggestion.generated_by_user_id",
        back_populates="generated_by",
    )
    ai_suggestion_subjects: Mapped[List["AISuggestion"]] = relationship(
        "AISuggestion",
        foreign_keys="AISuggestion.generated_for_user_id",
        back_populates="generated_for",
    )
    requested_reports: Mapped[List["GeneratedReport"]] = relationship(
        "GeneratedReport",
        back_populates="requested_by",
    )
    audit_events: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="actor")


class UserRole(TimestampMixin, Base):
    """Many-to-many mapping between users and roles."""

    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped["User"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship(back_populates="user_roles")


__all__ = [
    "University",
    "UniversityRegistrationRequest",
    "Document",
    "Role",
    "SuperAdmin",
    "RegistrationCode",
    "User",
    "UserRole",
]

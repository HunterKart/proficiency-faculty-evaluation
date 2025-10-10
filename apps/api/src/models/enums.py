"""Domain enumerations shared across SQLAlchemy models."""

from __future__ import annotations

from enum import StrEnum


class UniversityStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"


class UniversityRegistrationStatus(StrEnum):
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class RegistrationCodeStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class SuperAdminStatus(StrEnum):
    ACTIVE = "active"
    LOCKED = "locked"


class UserStatus(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    UNVERIFIED = "unverified"


class SemesterTerm(StrEnum):
    FIRST = "1st Semester"
    SECOND = "2nd Semester"
    SUMMER = "Summer"


class AssessmentPeriodName(StrEnum):
    MIDTERM = "Midterm"
    FINALS = "Finals"


class ModalityName(StrEnum):
    ONLINE = "Online"
    FACE_TO_FACE = "Face-to-Face"
    HYBRID = "Hybrid"
    MODULAR = "Modular"


class EvaluationAudience(StrEnum):
    STUDENTS = "Students"
    DEPARTMENT_HEADS = "Department Heads"
    BOTH = "Both"


class EvaluationFormStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    ASSIGNED = "assigned"
    ARCHIVED = "archived"


class QuestionType(StrEnum):
    LIKERT = "likert"
    OPEN_ENDED = "open_ended"


class EvaluationPeriodStatus(StrEnum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    CLOSED = "closed"
    CANCELLING = "cancelling"
    CANCELLED = "cancelled"


class EvaluationSubmissionStatus(StrEnum):
    SUBMITTED = "submitted"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ARCHIVED = "archived"
    INVALIDATED_FOR_RESUBMISSION = "invalidated_for_resubmission"
    CANCELLED = "cancelled"


class IntegrityCheckStatus(StrEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class AnalysisPipelineStatus(StrEnum):
    PENDING = "pending"
    QUANT_QUAL_COMPLETE = "quant_qual_complete"
    AGGREGATION_COMPLETE = "aggregation_complete"
    FAILED = "failed"


class FlagReason(StrEnum):
    LOW_CONFIDENCE = "Low-Confidence"
    RECYCLED_CONTENT = "Recycled Content"
    SENTIMENT_MISMATCH = "Sentiment Mismatch"


class FlagStatus(StrEnum):
    PENDING = "pending"
    RESOLVED = "resolved"


class FlagResolution(StrEnum):
    APPROVED = "approved"
    ARCHIVED = "archived"
    RESUBMISSION_REQUESTED = "resubmission_requested"


class SentimentLabel(StrEnum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class GeneratedReportStatus(StrEnum):
    QUEUED = "queued"
    GENERATING = "generating"
    READY = "ready"
    FAILED = "failed"


class ReportFileFormat(StrEnum):
    PDF = "PDF"
    CSV = "CSV"


class BackgroundJobType(StrEnum):
    ACADEMIC_STRUCTURE_IMPORT = "ACADEMIC_STRUCTURE_IMPORT"
    USER_IMPORT = "USER_IMPORT"
    HISTORICAL_USER_ENROLLMENT_IMPORT = "HISTORICAL_USER_ENROLLMENT_IMPORT"
    HISTORICAL_EVALUATION_IMPORT = "HISTORICAL_EVALUATION_IMPORT"
    PERIOD_CANCELLATION = "PERIOD_CANCELLATION"
    REPORT_GENERATION = "REPORT_GENERATION"
    RECYCLED_CONTENT_CHECK = "RECYCLED_CONTENT_CHECK"
    QUANTITATIVE_ANALYSIS = "QUANTITATIVE_ANALYSIS"
    QUALITATIVE_ANALYSIS = "QUALITATIVE_ANALYSIS"
    FINAL_AGGREGATION = "FINAL_AGGREGATION"


class BackgroundJobStatus(StrEnum):
    QUEUED = "queued"
    PROCESSING = "processing"
    CANCELLATION_REQUESTED = "cancellation_requested"
    COMPLETED_SUCCESS = "completed_success"
    COMPLETED_PARTIAL_FAILURE = "completed_partial_failure"
    FAILED = "failed"
    CANCELLED = "cancelled"


class NotificationStatus(StrEnum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"


__all__ = [
    "UniversityStatus",
    "UniversityRegistrationStatus",
    "RegistrationCodeStatus",
    "SuperAdminStatus",
    "UserStatus",
    "SemesterTerm",
    "AssessmentPeriodName",
    "ModalityName",
    "EvaluationAudience",
    "EvaluationFormStatus",
    "EvaluationPeriodStatus",
    "QuestionType",
    "EvaluationSubmissionStatus",
    "IntegrityCheckStatus",
    "AnalysisPipelineStatus",
    "FlagReason",
    "FlagStatus",
    "FlagResolution",
    "SentimentLabel",
    "GeneratedReportStatus",
    "ReportFileFormat",
    "BackgroundJobType",
    "BackgroundJobStatus",
    "NotificationStatus",
]

"""SQLAlchemy models package."""

from . import (
    academic,
    ai_reporting,
    analysis,
    evaluation_config,
    evaluation_submission,
    identity,
    operations,
)

__all__ = (
    identity.__all__
    + academic.__all__
    + evaluation_config.__all__
    + evaluation_submission.__all__
    + analysis.__all__
    + ai_reporting.__all__
    + operations.__all__
)

"""Shared platform enums."""

from enum import StrEnum


class EnvironmentCode(StrEnum):
    """Supported runtime environments."""

    LIVE = "LIVE"
    TRAINING = "TRAINING"
    TEST = "TEST"


class CommercialStatus(StrEnum):
    """Commercial module availability states."""

    AVAILABLE = "available"
    COMING_LATER = "coming_later"
    INTERNAL_ONLY = "internal_only"
    DISABLED = "disabled"

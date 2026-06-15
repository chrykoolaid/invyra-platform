"""Shared service result contract for platform service boundaries."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ServiceResult:
    """Standard response object returned by platform services."""

    success: bool
    status: str
    reason: str | None = None
    data: dict[str, Any] | None = None

    @classmethod
    def ok(cls, *, status: str = "OK", data: dict[str, Any] | None = None) -> "ServiceResult":
        """Return a successful service result."""
        return cls(success=True, status=status, reason=None, data=data)

    @classmethod
    def denied(cls, *, reason: str, data: dict[str, Any] | None = None) -> "ServiceResult":
        """Return a denied service result."""
        return cls(success=False, status="DENIED", reason=reason, data=data)

    @classmethod
    def failed(cls, *, reason: str, data: dict[str, Any] | None = None) -> "ServiceResult":
        """Return a failed service result."""
        return cls(success=False, status="FAILED", reason=reason, data=data)

    @classmethod
    def not_implemented(cls, *, data: dict[str, Any] | None = None) -> "ServiceResult":
        """Return the standard Sprint 13 skeleton result."""
        return cls(success=False, status="NOT_IMPLEMENTED", reason="SERVICE_SKELETON_ONLY", data=data)

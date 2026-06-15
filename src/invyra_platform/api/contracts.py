"""Shared API contract schemas for platform API boundaries.

These schemas define the future portal-facing response envelope without
implementing authentication, inventory runtime, or portal behavior.
"""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from invyra_platform.core.service_results import ServiceResult


class ApiStatus(StrEnum):
    """Stable API status values exposed at the API contract boundary."""

    OK = "OK"
    DENIED = "DENIED"
    FAILED = "FAILED"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"


class ApiError(BaseModel):
    """Structured API error detail."""

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    field: str | None = None


class ApiTrace(BaseModel):
    """Optional trace metadata for future request correlation."""

    trace_id: str | None = None


class ApiPagination(BaseModel):
    """Optional pagination metadata for future list endpoints."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=500)
    total_items: int | None = Field(default=None, ge=0)
    total_pages: int | None = Field(default=None, ge=0)


class ApiResponse(BaseModel):
    """Standard API response envelope for all platform API contracts."""

    model_config = ConfigDict(use_enum_values=True)

    success: bool
    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    data: dict[str, Any] | list[dict[str, Any]] | None = None
    errors: list[ApiError] = Field(default_factory=list)
    trace_id: str | None = None

    @classmethod
    def from_service_result(
        cls,
        result: ServiceResult,
        *,
        message: str = "Service result mapped to API response.",
        trace_id: str | None = None,
    ) -> "ApiResponse":
        """Map a ServiceResult into the shared API envelope.

        This is a contract-only mapper. It does not execute service behavior,
        issue tokens, validate credentials, or call inventory runtime logic.
        """
        errors: list[ApiError] = []
        if not result.success:
            errors.append(
                ApiError(
                    code=result.reason or result.status,
                    message=result.reason or result.status,
                )
            )

        return cls(
            success=result.success,
            code=result.status,
            message=message,
            data=result.data,
            errors=errors,
            trace_id=trace_id,
        )

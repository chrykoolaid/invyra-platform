"""API adapter helpers for service result mapping."""

from invyra_platform.api.contracts import ApiResponse
from invyra_platform.core.service_results import ServiceResult


def map_service_result_to_api_response(
    result: ServiceResult,
    *,
    message: str,
    trace_id: str | None = None,
) -> ApiResponse:
    """Map a service result into the standard API response envelope."""
    return ApiResponse.from_service_result(result, message=message, trace_id=trace_id)

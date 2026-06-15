"""Shared API contract schema tests."""

import pytest
from pydantic import ValidationError

from invyra_platform.api.contracts import ApiError, ApiPagination, ApiResponse, ApiStatus, ApiTrace
from invyra_platform.core.service_results import ServiceResult


def test_api_response_envelope_shape() -> None:
    response = ApiResponse(
        success=True,
        code=ApiStatus.OK,
        message="OK",
        data={"service": "platform"},
        trace_id="trace-001",
    )

    assert response.model_dump() == {
        "success": True,
        "code": "OK",
        "message": "OK",
        "data": {"service": "platform"},
        "errors": [],
        "trace_id": "trace-001",
    }


def test_api_error_requires_code_and_message() -> None:
    with pytest.raises(ValidationError):
        ApiError(code="", message="Missing code")

    with pytest.raises(ValidationError):
        ApiError(code="VALIDATION_ERROR", message="")


def test_api_trace_defaults_to_no_trace_id() -> None:
    trace = ApiTrace()

    assert trace.trace_id is None


def test_api_pagination_defaults_and_limits() -> None:
    pagination = ApiPagination()

    assert pagination.page == 1
    assert pagination.page_size == 50
    assert pagination.total_items is None
    assert pagination.total_pages is None

    with pytest.raises(ValidationError):
        ApiPagination(page=0)

    with pytest.raises(ValidationError):
        ApiPagination(page_size=501)


def test_api_response_maps_successful_service_result() -> None:
    result = ServiceResult.ok(data={"key": "value"})

    response = ApiResponse.from_service_result(result, message="Mapped", trace_id="trace-002")

    assert response.success is True
    assert response.code == "OK"
    assert response.message == "Mapped"
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.trace_id == "trace-002"


def test_api_response_maps_denied_service_result_to_error() -> None:
    result = ServiceResult.denied(reason="PERMISSION_DENIED")

    response = ApiResponse.from_service_result(result)

    assert response.success is False
    assert response.code == "DENIED"
    assert response.data is None
    assert len(response.errors) == 1
    assert response.errors[0].code == "PERMISSION_DENIED"
    assert response.errors[0].message == "PERMISSION_DENIED"


def test_api_response_maps_skeleton_service_result_to_error() -> None:
    result = ServiceResult.not_implemented(data={"service": "InventoryLaunchService"})

    response = ApiResponse.from_service_result(result)

    assert response.success is False
    assert response.code == "NOT_IMPLEMENTED"
    assert response.data == {"service": "InventoryLaunchService"}
    assert len(response.errors) == 1
    assert response.errors[0].code == "SERVICE_SKELETON_ONLY"

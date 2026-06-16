"""API adapter mapping tests."""

from invyra_platform.api.adapters import map_service_result_to_api_response
from invyra_platform.api.contracts import ApiResponse
from invyra_platform.core.service_results import ServiceResult


def test_adapter_maps_successful_service_result() -> None:
    result = ServiceResult.ok(data={"key": "value"})

    response = map_service_result_to_api_response(result, message="Mapped.", trace_id="trace-001")

    assert isinstance(response, ApiResponse)
    assert response.success is True
    assert response.code == "OK"
    assert response.message == "Mapped."
    assert response.data == {"key": "value"}
    assert response.errors == []
    assert response.trace_id == "trace-001"


def test_adapter_maps_skeleton_service_result() -> None:
    result = ServiceResult.not_implemented(data={"service": "ExampleService", "method": "example"})

    response = map_service_result_to_api_response(result, message="Skeleton only.")

    assert response.success is False
    assert response.code == "NOT_IMPLEMENTED"
    assert response.message == "Skeleton only."
    assert response.data == {"service": "ExampleService", "method": "example"}
    assert len(response.errors) == 1
    assert response.errors[0].code == "SERVICE_SKELETON_ONLY"
    assert response.trace_id is None


def test_adapter_maps_denied_service_result() -> None:
    result = ServiceResult.denied(reason="PERMISSION_DENIED")

    response = map_service_result_to_api_response(result, message="Denied.")

    assert response.success is False
    assert response.code == "DENIED"
    assert response.errors[0].code == "PERMISSION_DENIED"

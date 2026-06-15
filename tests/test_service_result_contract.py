"""Service result contract tests."""

from invyra_platform.core.service_results import ServiceResult


def test_service_result_ok() -> None:
    result = ServiceResult.ok(data={"key": "value"})

    assert result.success is True
    assert result.status == "OK"
    assert result.reason is None
    assert result.data == {"key": "value"}


def test_service_result_denied() -> None:
    result = ServiceResult.denied(reason="PERMISSION_DENIED")

    assert result.success is False
    assert result.status == "DENIED"
    assert result.reason == "PERMISSION_DENIED"
    assert result.data is None


def test_service_result_failed() -> None:
    result = ServiceResult.failed(reason="UNKNOWN_ERROR")

    assert result.success is False
    assert result.status == "FAILED"
    assert result.reason == "UNKNOWN_ERROR"
    assert result.data is None


def test_service_result_not_implemented() -> None:
    result = ServiceResult.not_implemented(data={"service": "ExampleService", "method": "example"})

    assert result.success is False
    assert result.status == "NOT_IMPLEMENTED"
    assert result.reason == "SERVICE_SKELETON_ONLY"
    assert result.data == {"service": "ExampleService", "method": "example"}

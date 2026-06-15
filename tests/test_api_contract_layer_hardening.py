"""Stable API contract layer hardening tests."""

from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.v1.auth_contracts import LoginRequest
from invyra_platform.api.v1.inventory_access_contracts import InventoryAccessEvaluationRequest
from invyra_platform.api.v1.inventory_launch_contracts import InventoryLaunchAttemptRequest
from invyra_platform.core.service_results import ServiceResult


def test_shared_api_response_contract_keys_are_stable() -> None:
    response = ApiResponse.from_service_result(
        ServiceResult.not_implemented(data={"service": "ContractLayer", "method": "test"}),
        message="Skeleton only.",
        trace_id="trace-001",
    )

    assert set(response.model_dump().keys()) == {
        "success",
        "code",
        "message",
        "data",
        "errors",
        "trace_id",
    }
    assert response.success is False
    assert response.code == "NOT_IMPLEMENTED"
    assert response.errors[0].code == "SERVICE_SKELETON_ONLY"
    assert response.trace_id == "trace-001"


def test_environment_values_are_consistent_across_contracts() -> None:
    auth = LoginRequest(email="operator@example.com", password="password123", environment="LIVE")
    access = InventoryAccessEvaluationRequest(user_id="user-001", organisation_id="org-001", environment="TRAINING")
    launch = InventoryLaunchAttemptRequest(user_id="user-001", organisation_id="org-001", environment="TEST")

    assert auth.environment == "LIVE"
    assert access.environment == "TRAINING"
    assert launch.environment == "TEST"

"""API contract layer hardening tests."""

from fastapi.testclient import TestClient

from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.v1.auth_contracts import LoginRequest
from invyra_platform.api.v1.inventory_access_contracts import InventoryAccessEvaluationRequest
from invyra_platform.api.v1.inventory_launch_contracts import InventoryLaunchAttemptRequest
from invyra_platform.app import create_app
from invyra_platform.core.service_results import ServiceResult


EXPECTED_CONTRACT_ROUTES = {
    "/api/v1/auth/login",
    "/api/v1/auth/logout",
    "/api/v1/auth/refresh",
    "/api/v1/auth/password-reset/request",
    "/api/v1/auth/password-reset/confirm",
    "/api/v1/auth/session",
    "/api/v1/inventory/access/evaluate",
    "/api/v1/inventory/access/status",
    "/api/v1/inventory/access/events",
    "/api/v1/inventory/launch/attempt",
    "/api/v1/inventory/launch/token",
    "/api/v1/inventory/launch/session",
    "/api/v1/inventory/launch/session/{session_id}",
    "/api/v1/inventory/launch/events",
}


def test_all_sprint_14_contract_routes_are_registered() -> None:
    route_paths = {route.path for route in create_app().routes}

    assert EXPECTED_CONTRACT_ROUTES.issubset(route_paths)


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


def test_core_contract_endpoints_return_standard_skeleton_envelope() -> None:
    client = TestClient(create_app())

    responses = [
        client.post("/api/v1/auth/login", json={"email": "operator@example.com", "password": "password123"}),
        client.post(
            "/api/v1/inventory/access/evaluate",
            json={"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
        ),
        client.post(
            "/api/v1/inventory/launch/attempt",
            json={"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
        ),
    ]

    for response in responses:
        assert response.status_code == 200
        body = response.json()
        assert set(body.keys()) == {"success", "code", "message", "data", "errors", "trace_id"}
        assert body["success"] is False
        assert body["code"] == "NOT_IMPLEMENTED"
        assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"

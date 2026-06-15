"""Inventory access API contract tests."""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from invyra_platform.api.v1.inventory_access_contracts import (
    InventoryAccessEvaluationRequest,
    InventoryAccessEvaluationResponse,
    InventoryAccessEventResponse,
    InventoryAccessStatusResponse,
)
from invyra_platform.app import create_app


def test_inventory_access_evaluation_request_validates_required_fields() -> None:
    request = InventoryAccessEvaluationRequest(
        user_id="user-001",
        organisation_id="org-001",
        license_id="license-001",
        entitlement_id="entitlement-001",
        device_id="device-001",
        environment="LIVE",
    )

    assert request.user_id == "user-001"
    assert request.organisation_id == "org-001"
    assert request.environment == "LIVE"

    with pytest.raises(ValidationError):
        InventoryAccessEvaluationRequest(user_id="", organisation_id="org-001", environment="LIVE")

    with pytest.raises(ValidationError):
        InventoryAccessEvaluationRequest(user_id="user-001", organisation_id="", environment="LIVE")

    with pytest.raises(ValidationError):
        InventoryAccessEvaluationRequest(user_id="user-001", organisation_id="org-001", environment="DEV")


def test_inventory_access_response_contracts_validate_environment() -> None:
    evaluation = InventoryAccessEvaluationResponse(environment="TRAINING")
    status = InventoryAccessStatusResponse(environment="TEST")
    event = InventoryAccessEventResponse(environment="LIVE")

    assert evaluation.allowed is False
    assert evaluation.reasons == []
    assert status.available is False
    assert event.environment == "LIVE"

    with pytest.raises(ValidationError):
        InventoryAccessEvaluationResponse(environment="DEV")

    with pytest.raises(ValidationError):
        InventoryAccessStatusResponse(environment="DEV")

    with pytest.raises(ValidationError):
        InventoryAccessEventResponse(environment="DEV")


def test_inventory_access_routes_return_skeleton_api_response() -> None:
    client = TestClient(create_app())

    routes = [
        (
            "post",
            "/api/v1/inventory/access/evaluate",
            {"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
        ),
        ("get", "/api/v1/inventory/access/status", None),
        ("get", "/api/v1/inventory/access/events", None),
    ]

    for method, path, payload in routes:
        if method == "post":
            response = client.post(path, json=payload)
        else:
            response = client.get(path)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is False
        assert body["code"] == "NOT_IMPLEMENTED"
        assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"
        assert body["data"]["service"] == "InventoryAccessGatewayService"

"""Inventory launch API smoke tests."""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from invyra_platform.api.v1.inventory_launch_contracts import InventoryLaunchAttemptRequest
from invyra_platform.app import create_app


def test_launch_attempt_request_contract() -> None:
    request = InventoryLaunchAttemptRequest(
        user_id="user-001",
        organisation_id="org-001",
        environment="LIVE",
    )

    assert request.user_id == "user-001"
    assert request.organisation_id == "org-001"
    assert request.environment == "LIVE"

    with pytest.raises(ValidationError):
        InventoryLaunchAttemptRequest(user_id="", organisation_id="org-001", environment="LIVE")

    with pytest.raises(ValidationError):
        InventoryLaunchAttemptRequest(user_id="user-001", organisation_id="org-001", environment="DEV")


def test_launch_attempt_route_returns_skeleton_response() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/inventory/launch/attempt",
        json={"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"
    assert body["data"]["service"] == "InventoryLaunchService"

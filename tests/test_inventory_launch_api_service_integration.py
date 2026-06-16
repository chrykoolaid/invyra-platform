"""Inventory launch API service integration tests."""

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def test_inventory_launch_attempt_route_uses_service_integration_path() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/inventory/launch/attempt",
        json={"user_id": "user-001", "organisation_id": "org-001", "environment": "LIVE"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Inventory launch attempt skeleton only."
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"
    assert body["data"] == {"service": "InventoryLaunchService", "method": "create_launch_attempt"}


def test_inventory_launch_events_route_preserves_skeleton_envelope() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/inventory/launch/events")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Inventory launch events skeleton only."
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"
    assert body["data"] == {"service": "InventoryLaunchService", "method": "record_launch_event"}

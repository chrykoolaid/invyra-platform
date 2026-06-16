"""Portal Inventory entry API contract exposure tests."""

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def test_portal_inventory_entry_route_returns_disabled_skeleton_response() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/inventory-entry",
        json={
            "user_id": "user-001",
            "organisation_id": "org-001",
            "session_id": "portal-session-001",
            "device_id": "device-001",
            "environment": "LIVE",
            "trace_id": "trace-001",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Portal Inventory entry boundary skeleton only."
    assert body["trace_id"] == "trace-001"
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"

    data = body["data"]
    assert data["environment"] == "LIVE"
    assert data["message"] == "Portal Inventory entry boundary skeleton only."

    entry = data["entry"]
    assert entry["module_code"] == "INVENTORY"
    assert entry["display_name"] == "Invyra Inventory"
    assert entry["commercial_status"] == "AVAILABLE"
    assert entry["environment"] == "LIVE"
    assert entry["visible"] is False
    assert entry["enabled"] is False
    assert entry["entry_allowed"] is False
    assert entry["availability"]["allowed"] is False
    assert entry["reason"] == "Portal Inventory entry skeleton only."


def test_portal_inventory_entry_route_does_not_launch_inventory_or_runtime_access() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/inventory-entry",
        json={
            "user_id": "user-001",
            "organisation_id": "org-001",
            "environment": "TRAINING",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"

    entry = body["data"]["entry"]
    assert entry["environment"] == "TRAINING"
    assert entry["enabled"] is False
    assert entry["entry_allowed"] is False
    assert entry["availability"]["allowed"] is False
    assert entry["availability"]["target_key"] is None
    assert entry["availability"]["evaluation_id"] is None


def test_portal_inventory_entry_route_rejects_invalid_contract_payload() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/inventory-entry",
        json={
            "user_id": "",
            "organisation_id": "org-001",
            "environment": "DEV",
            "trace_id": "",
        },
    )

    assert response.status_code == 422

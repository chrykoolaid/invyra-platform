"""Portal entitlement API contract exposure tests."""

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def test_portal_entitlements_route_returns_empty_skeleton_response() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/entitlements",
        json={
            "user_id": "user-001",
            "organisation_id": "org-001",
            "session_id": "portal-session-001",
            "environment": "TEST",
            "include_future_modules": True,
            "trace_id": "trace-001",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Portal entitlement boundary skeleton only."
    assert body["trace_id"] == "trace-001"
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"

    data = body["data"]
    assert data["environment"] == "TEST"
    assert data["groups"] == []
    assert data["message"] == "Portal entitlement boundary skeleton only."


def test_portal_entitlements_route_does_not_evaluate_licenses_or_unlock_modules() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/entitlements",
        json={
            "user_id": "user-001",
            "organisation_id": "org-001",
            "environment": "LIVE",
            "include_future_modules": False,
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["data"]["environment"] == "LIVE"
    assert body["data"]["groups"] == []


def test_portal_entitlements_route_rejects_invalid_contract_payload() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/entitlements",
        json={
            "user_id": "",
            "organisation_id": "org-001",
            "environment": "DEV",
            "trace_id": "",
        },
    )

    assert response.status_code == 422

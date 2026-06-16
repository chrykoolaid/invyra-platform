"""Portal session API contract exposure tests."""

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def test_portal_session_route_returns_unauthenticated_skeleton_response() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/session",
        json={
            "session_id": "portal-session-001",
            "auth_session_id": "auth-session-001",
            "user_id": "user-001",
            "organisation_id": "org-001",
            "device_id": "device-001",
            "environment": "LIVE",
            "trace_id": "trace-001",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Portal session boundary skeleton only."
    assert body["trace_id"] == "trace-001"
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"

    data = body["data"]
    assert data["authenticated"] is False
    assert data["session"] is None
    assert data["context"] is None
    assert data["message"] == "Portal session boundary skeleton only."


def test_portal_session_route_does_not_execute_runtime_session_behavior() -> None:
    client = TestClient(create_app())

    response = client.post("/api/v1/portal/session", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["data"]["authenticated"] is False
    assert body["data"]["session"] is None
    assert body["data"]["context"] is None


def test_portal_session_route_rejects_invalid_contract_payload() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/session",
        json={
            "environment": "DEV",
            "trace_id": "",
        },
    )

    assert response.status_code == 422

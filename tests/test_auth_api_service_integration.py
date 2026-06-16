"""Auth API service integration tests."""

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def test_auth_login_route_uses_service_integration_path() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "operator@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Auth login skeleton only."
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"
    assert body["data"] == {"service": "AuthRuntimeService", "method": "login"}


def test_auth_session_route_preserves_skeleton_envelope() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/auth/session")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Auth session skeleton only."
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"
    assert body["data"] == {"service": "AuthRuntimeService", "method": "record_auth_security_event"}

"""Portal navigation API contract exposure tests."""

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def test_portal_navigation_route_returns_empty_skeleton_response() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/navigation",
        json={
            "user_id": "user-001",
            "organisation_id": "org-001",
            "session_id": "portal-session-001",
            "environment": "TRAINING",
            "include_hidden": True,
            "trace_id": "trace-001",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Portal navigation boundary skeleton only."
    assert body["trace_id"] == "trace-001"
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"

    data = body["data"]
    assert data["environment"] == "TRAINING"
    assert data["sections"] == []
    assert data["message"] == "Portal navigation boundary skeleton only."


def test_portal_navigation_route_does_not_generate_sidebar_or_runtime_items() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/navigation",
        json={
            "user_id": "user-001",
            "organisation_id": "org-001",
            "environment": "LIVE",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["data"]["environment"] == "LIVE"
    assert body["data"]["sections"] == []


def test_portal_navigation_route_rejects_invalid_contract_payload() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/v1/portal/navigation",
        json={
            "user_id": "",
            "organisation_id": "org-001",
            "environment": "DEV",
            "trace_id": "",
        },
    )

    assert response.status_code == 422

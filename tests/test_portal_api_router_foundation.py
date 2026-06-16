"""Portal API router foundation tests."""

from fastapi.testclient import TestClient

from invyra_platform.app import create_app


def test_portal_status_route_is_exposed_under_api_v1_prefix() -> None:
    client = TestClient(create_app())

    response = client.get("/api/v1/portal/status")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is False
    assert body["code"] == "NOT_IMPLEMENTED"
    assert body["message"] == "Portal API boundary skeleton only."
    assert body["errors"][0]["code"] == "SERVICE_SKELETON_ONLY"
    assert body["data"]["boundary"] == "portal-api"
    assert body["data"]["runtime"] == "not-implemented"
    assert body["data"]["routes"] == []


def test_portal_router_is_not_exposed_outside_api_v1_prefix() -> None:
    client = TestClient(create_app())

    response = client.get("/portal/status")

    assert response.status_code == 404

"""Health endpoint tests."""

from fastapi.testclient import TestClient


def test_root_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "invyra-platform"}


def test_api_v1_health_endpoint(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "api": "v1", "service": "invyra-platform"}

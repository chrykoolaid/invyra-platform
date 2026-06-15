"""Authentication API contract tests."""

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from invyra_platform.api.v1.auth_contracts import (
    LoginRequest,
    PasswordResetConfirmRequest,
    RefreshRequest,
    SessionResponse,
)
from invyra_platform.app import create_app


def test_login_request_validates_email_password_and_environment() -> None:
    request = LoginRequest(
        email="operator@example.com",
        password="password123",
        device_id="device-001",
        environment="LIVE",
    )

    assert request.email == "operator@example.com"
    assert request.environment == "LIVE"

    with pytest.raises(ValidationError):
        LoginRequest(email="not-an-email", password="password123")

    with pytest.raises(ValidationError):
        LoginRequest(email="operator@example.com", password="short")

    with pytest.raises(ValidationError):
        LoginRequest(email="operator@example.com", password="password123", environment="DEV")


def test_refresh_request_requires_token() -> None:
    request = RefreshRequest(refresh_token="refresh-token")

    assert request.refresh_token == "refresh-token"

    with pytest.raises(ValidationError):
        RefreshRequest(refresh_token="")


def test_password_reset_confirm_request_requires_token_and_password() -> None:
    request = PasswordResetConfirmRequest(reset_token="reset-token", new_password="new-password")

    assert request.reset_token == "reset-token"
    assert request.new_password == "new-password"

    with pytest.raises(ValidationError):
        PasswordResetConfirmRequest(reset_token="", new_password="new-password")

    with pytest.raises(ValidationError):
        PasswordResetConfirmRequest(reset_token="reset-token", new_password="short")


def test_session_response_environment_contract() -> None:
    response = SessionResponse(environment="TRAINING")

    assert response.authenticated is False
    assert response.environment == "TRAINING"

    with pytest.raises(ValidationError):
        SessionResponse(environment="DEV")


def test_auth_routes_return_skeleton_api_response() -> None:
    client = TestClient(create_app())

    routes = [
        ("post", "/api/v1/auth/login", {"email": "operator@example.com", "password": "password123"}),
        ("post", "/api/v1/auth/logout", {"session_id": "session-001"}),
        ("post", "/api/v1/auth/refresh", {"refresh_token": "refresh-token"}),
        ("post", "/api/v1/auth/password-reset/request", {"email": "operator@example.com"}),
        (
            "post",
            "/api/v1/auth/password-reset/confirm",
            {"reset_token": "reset-token", "new_password": "new-password"},
        ),
        ("get", "/api/v1/auth/session", None),
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

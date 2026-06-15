"""Authentication runtime foundation tests."""

from invyra_platform.auth.models import (
    AuthRefreshToken,
    AuthSecurityEvent,
    AuthSession,
    LoginAttempt,
    PasswordResetToken,
)
from invyra_platform.db.base import Base


def test_auth_runtime_tables_registered_in_metadata() -> None:
    expected_tables = {
        "auth_sessions",
        "auth_refresh_tokens",
        "password_reset_tokens",
        "login_attempts",
        "auth_security_events",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_auth_session_runtime_fields_exist() -> None:
    columns = AuthSession.__table__.columns
    assert columns["user_id"].nullable is False
    assert columns["session_token_hash"].nullable is False
    assert columns["expires_at"].nullable is False
    assert "environment" in columns
    assert "status" in columns
    assert "revoked_at" in columns
    assert "revoked_reason" in columns


def test_auth_refresh_token_stores_hash_only() -> None:
    columns = AuthRefreshToken.__table__.columns
    assert columns["session_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["token_hash"].nullable is False
    assert columns["expires_at"].nullable is False
    assert "raw_refresh_token" not in columns
    assert "refresh_token" not in columns


def test_password_reset_token_stores_hash_only() -> None:
    columns = PasswordResetToken.__table__.columns
    assert columns["user_id"].nullable is False
    assert columns["token_hash"].nullable is False
    assert columns["expires_at"].nullable is False
    assert "raw_reset_token" not in columns
    assert "plain_password" not in columns
    assert "revoked_at" in columns


def test_login_attempt_can_record_failure_context() -> None:
    columns = LoginAttempt.__table__.columns
    assert columns["email"].nullable is False
    assert columns["success"].nullable is False
    assert "failure_reason" in columns
    assert "organisation_id" in columns
    assert "environment" in columns


def test_auth_security_event_links_to_session_and_login_attempt() -> None:
    columns = AuthSecurityEvent.__table__.columns
    assert columns["event_type"].nullable is False
    assert columns["result"].nullable is False
    assert columns["session_id"].nullable is True
    assert columns["login_attempt_id"].nullable is True
    assert "message" in columns

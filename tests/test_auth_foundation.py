"""Authentication data foundation tests."""

from invyra_platform.auth.models import AuthIdentity, AuthSession, LoginAttempt, PasswordResetToken
from invyra_platform.db.base import Base


def test_auth_tables_registered_in_metadata() -> None:
    expected_tables = {
        "auth_identities",
        "auth_sessions",
        "password_reset_tokens",
        "login_attempts",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_auth_identity_uses_password_hash_not_plain_password() -> None:
    columns = AuthIdentity.__table__.columns
    assert "password_hash" in columns
    assert "password" not in columns
    assert columns["password_hash"].nullable is False
    assert columns["password_hash_algorithm"].nullable is False


def test_session_stores_token_hash_not_raw_token() -> None:
    columns = AuthSession.__table__.columns
    assert "session_token_hash" in columns
    assert "session_token" not in columns
    assert columns["session_token_hash"].nullable is False


def test_reset_token_stores_hash_not_raw_token() -> None:
    columns = PasswordResetToken.__table__.columns
    assert "token_hash" in columns
    assert "token" not in columns
    assert columns["token_hash"].nullable is False


def test_login_attempt_tracks_email_without_requiring_user() -> None:
    columns = LoginAttempt.__table__.columns
    assert columns["email"].nullable is False
    assert columns["user_id"].nullable is True


def test_auth_session_can_hold_tenant_and_device_context() -> None:
    columns = AuthSession.__table__.columns
    assert "organisation_id" in columns
    assert "device_id" in columns
    assert columns["organisation_id"].nullable is True
    assert columns["device_id"].nullable is True

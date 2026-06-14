"""Configuration tests."""

import pytest

from invyra_platform.core.config import Settings


def test_default_settings_load() -> None:
    settings = Settings()

    assert settings.app_name == "Invyra Platform"
    assert settings.app_env == "local"
    assert settings.debug is False
    assert settings.password_hash_algorithm == "argon2id"
    assert settings.default_timezone == "Asia/Manila"


def test_future_modules_disabled_by_default() -> None:
    settings = Settings()

    assert settings.allow_crm is False
    assert settings.allow_pos is False
    assert settings.allow_payroll is False
    assert settings.allow_workforce_management is False
    assert settings.allow_forecasting is False
    assert settings.allow_purchasing_extensions is False


def test_production_rejects_placeholder_secrets() -> None:
    settings = Settings(app_env="production", session_cookie_secure=True)

    with pytest.raises(ValueError, match="Production secrets"):
        settings.validate_production_safety()


def test_production_requires_secure_cookies() -> None:
    settings = Settings(
        app_env="production",
        secret_key="production-secret-key",
        jwt_secret_key="production-jwt-secret-key",
        session_cookie_secure=False,
    )

    with pytest.raises(ValueError, match="Secure session cookies"):
        settings.validate_production_safety()

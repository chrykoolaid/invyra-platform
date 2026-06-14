"""Application settings for Invyra Platform."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

EnvironmentName = Literal["local", "test", "ci", "staging", "production"]
SameSitePolicy = Literal["lax", "strict", "none"]


class Settings(BaseSettings):
    """Environment-driven application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Invyra Platform"
    app_env: EnvironmentName = "local"
    debug: bool = False

    database_url: str = "postgresql+psycopg://invyra:invyra@localhost:5432/invyra_platform"
    test_database_url: str = (
        "postgresql+psycopg://invyra:invyra@localhost:5433/invyra_platform_test"
    )

    secret_key: str = Field(default="change-me", min_length=8)
    jwt_secret_key: str = Field(default="change-me", min_length=8)
    session_cookie_name: str = "invyra_session"

    session_cookie_secure: bool = False
    session_cookie_httponly: bool = True
    session_cookie_samesite: SameSitePolicy = "lax"

    password_hash_algorithm: str = "argon2id"
    default_timezone: str = "Asia/Manila"

    enable_dev_seed: bool = False
    enable_test_seed: bool = False
    audit_logging_enabled: bool = True
    log_level: str = "INFO"

    allow_crm: bool = False
    allow_pos: bool = False
    allow_payroll: bool = False
    allow_workforce_management: bool = False
    allow_forecasting: bool = False
    allow_purchasing_extensions: bool = False

    def validate_production_safety(self) -> None:
        """Raise when unsafe local defaults are used in production."""
        if self.app_env == "production":
            if self.debug:
                raise ValueError("DEBUG must be false in production")
            if not self.session_cookie_secure:
                raise ValueError("Secure session cookies are required in production")
            if self.enable_dev_seed or self.enable_test_seed:
                raise ValueError("Seed data must be disabled in production")
            if self.secret_key == "change-me" or self.jwt_secret_key == "change-me":
                raise ValueError("Production secrets must not use placeholder values")


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    settings = Settings()
    settings.validate_production_safety()
    return settings

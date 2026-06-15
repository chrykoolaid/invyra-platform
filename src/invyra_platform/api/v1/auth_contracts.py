"""Authentication API contract models.

These models define the future portal-facing authentication boundary only.
They do not implement login, token issuance, password verification, email
sending, or session persistence.
"""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """Future login request contract."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=256)
    device_id: str | None = Field(default=None, min_length=1, max_length=128)
    environment: str | None = Field(default=None, pattern="^(LIVE|TRAINING|TEST)$")


class LoginResponse(BaseModel):
    """Future login response data contract."""

    user_id: str | None = None
    organisation_id: str | None = None
    session_id: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None


class LogoutRequest(BaseModel):
    """Future logout request contract."""

    session_id: str = Field(min_length=1, max_length=128)


class LogoutResponse(BaseModel):
    """Future logout response data contract."""

    session_closed: bool = False


class RefreshRequest(BaseModel):
    """Future session refresh request contract."""

    refresh_token: str = Field(min_length=1, max_length=512)
    device_id: str | None = Field(default=None, min_length=1, max_length=128)


class RefreshResponse(BaseModel):
    """Future session refresh response data contract."""

    access_token: str | None = None
    refresh_token: str | None = None
    session_id: str | None = None


class PasswordResetRequest(BaseModel):
    """Future password reset request contract."""

    email: EmailStr


class PasswordResetResponse(BaseModel):
    """Future password reset response data contract."""

    request_accepted: bool = False


class PasswordResetConfirmRequest(BaseModel):
    """Future password reset confirmation request contract."""

    reset_token: str = Field(min_length=1, max_length=512)
    new_password: str = Field(min_length=8, max_length=256)


class PasswordResetConfirmResponse(BaseModel):
    """Future password reset confirmation response data contract."""

    password_reset: bool = False


class SessionResponse(BaseModel):
    """Future current-session response data contract."""

    authenticated: bool = False
    user_id: str | None = None
    organisation_id: str | None = None
    session_id: str | None = None
    environment: str | None = Field(default=None, pattern="^(LIVE|TRAINING|TEST)$")

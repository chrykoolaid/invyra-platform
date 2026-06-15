"""Inventory launch API contract models."""

from pydantic import BaseModel, Field


class InventoryLaunchAttemptRequest(BaseModel):
    """Future Inventory launch attempt request contract."""

    user_id: str = Field(min_length=1, max_length=128)
    organisation_id: str = Field(min_length=1, max_length=128)
    device_id: str | None = Field(default=None, min_length=1, max_length=128)
    environment: str = Field(pattern="^(LIVE|TRAINING|TEST)$")


class InventoryLaunchAttemptResponse(BaseModel):
    """Future Inventory launch attempt response data contract."""

    attempt_id: str | None = None
    accepted: bool = False
    environment: str | None = Field(default=None, pattern="^(LIVE|TRAINING|TEST)$")


class InventoryLaunchTokenRequest(BaseModel):
    """Future Inventory launch token request contract."""

    attempt_id: str = Field(min_length=1, max_length=128)
    user_id: str = Field(min_length=1, max_length=128)
    organisation_id: str = Field(min_length=1, max_length=128)
    environment: str = Field(pattern="^(LIVE|TRAINING|TEST)$")


class InventoryLaunchTokenResponse(BaseModel):
    """Future Inventory launch token response data contract."""

    token_id: str | None = None
    launch_token: str | None = None
    expires_at: str | None = None


class InventoryLaunchSessionRequest(BaseModel):
    """Future Inventory launch session request contract."""

    launch_token: str = Field(min_length=1, max_length=512)
    device_id: str | None = Field(default=None, min_length=1, max_length=128)


class InventoryLaunchSessionResponse(BaseModel):
    """Future Inventory launch session response data contract."""

    session_id: str | None = None
    active: bool = False
    environment: str | None = Field(default=None, pattern="^(LIVE|TRAINING|TEST)$")
    launch_url: str | None = None


class InventoryLaunchEventResponse(BaseModel):
    """Future Inventory launch event response data contract."""

    event_id: str | None = None
    attempt_id: str | None = None
    session_id: str | None = None
    event_type: str | None = None
    environment: str | None = Field(default=None, pattern="^(LIVE|TRAINING|TEST)$")

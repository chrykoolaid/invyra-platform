"""Inventory access API contract models.

These models define the future portal-facing Inventory access boundary only.
They do not implement inventory runtime, stock reads, orders, receiving,
transfers, stocktakes, wastage, or reports.
"""

from pydantic import BaseModel, Field


class InventoryAccessEvaluationRequest(BaseModel):
    """Future Inventory access evaluation request contract."""

    user_id: str = Field(min_length=1, max_length=128)
    organisation_id: str = Field(min_length=1, max_length=128)
    license_id: str | None = Field(default=None, min_length=1, max_length=128)
    entitlement_id: str | None = Field(default=None, min_length=1, max_length=128)
    device_id: str | None = Field(default=None, min_length=1, max_length=128)
    environment: str = Field(pattern="^(LIVE|TRAINING|TEST)$")


class InventoryAccessEvaluationResponse(BaseModel):
    """Future Inventory access evaluation response data contract."""

    allowed: bool = False
    evaluation_id: str | None = None
    user_id: str | None = None
    organisation_id: str | None = None
    environment: str | None = Field(default=None, pattern="^(LIVE|TRAINING|TEST)$")
    reasons: list[str] = Field(default_factory=list)


class InventoryAccessStatusResponse(BaseModel):
    """Future Inventory access status response data contract."""

    available: bool = False
    user_id: str | None = None
    organisation_id: str | None = None
    environment: str | None = Field(default=None, pattern="^(LIVE|TRAINING|TEST)$")
    status: str | None = None


class InventoryAccessEventResponse(BaseModel):
    """Future Inventory access event response data contract."""

    event_id: str | None = None
    evaluation_id: str | None = None
    event_type: str | None = None
    user_id: str | None = None
    organisation_id: str | None = None
    environment: str | None = Field(default=None, pattern="^(LIVE|TRAINING|TEST)$")

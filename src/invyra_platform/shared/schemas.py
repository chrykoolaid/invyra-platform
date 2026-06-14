"""Shared API schemas."""

from pydantic import BaseModel, ConfigDict


class ApiStatusResponse(BaseModel):
    """Generic API status response."""

    model_config = ConfigDict(from_attributes=True)

    status: str
    service: str

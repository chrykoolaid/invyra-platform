"""Portal Inventory entry boundary contract models."""

from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from invyra_platform.portal.contracts import (
    PortalCommercialStatus,
    PortalContractDTO,
    PortalEnvironment,
    PortalModuleCode,
)


class PortalInventoryEntryStatus(StrEnum):
    """Stable Inventory entry states visible at the portal boundary."""

    AVAILABLE = "AVAILABLE"
    DISABLED = "DISABLED"
    DENIED = "DENIED"
    NOT_LICENSED = "NOT_LICENSED"
    ENVIRONMENT_BLOCKED = "ENVIRONMENT_BLOCKED"
    UNAVAILABLE = "UNAVAILABLE"


class PortalInventoryLaunchAvailabilityDTO(PortalContractDTO):
    """Portal-safe Inventory launch availability summary."""

    allowed: bool = False
    status: PortalInventoryEntryStatus = PortalInventoryEntryStatus.DISABLED
    action_label: str | None = Field(default=None, min_length=1, max_length=80)
    target_key: str | None = Field(default=None, min_length=1, max_length=160)
    evaluation_id: str | None = Field(default=None, min_length=1, max_length=128)
    reasons: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def enforce_launch_availability_consistency(self) -> Self:
        """Keep launch availability flags internally consistent."""

        if self.allowed and self.status != PortalInventoryEntryStatus.AVAILABLE:
            raise ValueError("Inventory launch availability requires available status.")

        if self.allowed and self.target_key is None:
            raise ValueError("Inventory launch availability requires a target key.")

        if self.allowed and self.action_label is None:
            raise ValueError("Inventory launch availability requires an action label.")

        return self


class PortalInventoryEntryRequest(PortalContractDTO):
    """Future portal Inventory entry request contract."""

    user_id: str = Field(min_length=1, max_length=128)
    organisation_id: str = Field(min_length=1, max_length=128)
    session_id: str | None = Field(default=None, min_length=1, max_length=128)
    device_id: str | None = Field(default=None, min_length=1, max_length=128)
    environment: PortalEnvironment = PortalEnvironment.LIVE
    trace_id: str | None = Field(default=None, min_length=1, max_length=128)


class PortalInventoryEntryDTO(PortalContractDTO):
    """Portal-safe Inventory entry description.

    This contract describes Inventory visibility and entry eligibility only. It
    does not expose stock, orders, receiving, transfers, stocktake, wastage,
    markdowns, reports, or Inventory runtime data.
    """

    module_code: PortalModuleCode = PortalModuleCode.INVENTORY
    display_name: str = Field(default="Invyra Inventory", min_length=1, max_length=160)
    commercial_status: PortalCommercialStatus = PortalCommercialStatus.AVAILABLE
    status: PortalInventoryEntryStatus = PortalInventoryEntryStatus.DISABLED
    visible: bool = False
    enabled: bool = False
    entry_allowed: bool = False
    environment: PortalEnvironment
    required_permissions: list[str] = Field(default_factory=list)
    availability: PortalInventoryLaunchAvailabilityDTO = Field(default_factory=PortalInventoryLaunchAvailabilityDTO)
    reason: str | None = Field(default=None, min_length=1, max_length=255)

    @model_validator(mode="after")
    def enforce_inventory_entry_consistency(self) -> Self:
        """Keep Inventory entry state aligned with commercial and access status."""

        if self.module_code != PortalModuleCode.INVENTORY:
            raise ValueError("Portal Inventory entry must use the Inventory module code.")

        if self.enabled and not self.visible:
            raise ValueError("Enabled Inventory entry must be visible.")

        if self.entry_allowed and not self.enabled:
            raise ValueError("Inventory entry requires enabled state.")

        if self.entry_allowed and self.status != PortalInventoryEntryStatus.AVAILABLE:
            raise ValueError("Inventory entry requires available status.")

        if self.entry_allowed and self.commercial_status != PortalCommercialStatus.AVAILABLE:
            raise ValueError("Inventory entry requires commercial availability.")

        if self.availability.allowed and not self.entry_allowed:
            raise ValueError("Inventory launch availability requires entry to be allowed.")

        return self


class PortalInventoryEntryResponse(PortalContractDTO):
    """Portal Inventory entry response data contract."""

    environment: PortalEnvironment
    entry: PortalInventoryEntryDTO | None = None
    message: str = Field(default="Portal Inventory entry boundary response.", min_length=1, max_length=255)

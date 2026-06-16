"""Portal navigation boundary contract models."""

from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from invyra_platform.portal.contracts import (
    FUTURE_MODULE_CODES,
    PortalCommercialStatus,
    PortalContractDTO,
    PortalEnvironment,
    PortalModuleCode,
)


class PortalNavigationSectionCode(StrEnum):
    """Stable portal navigation section codes."""

    PRIMARY = "PRIMARY"
    OPERATIONS = "OPERATIONS"
    INTELLIGENCE = "INTELLIGENCE"
    ADMIN = "ADMIN"
    TRAINING = "TRAINING"
    SUPPORT = "SUPPORT"


class PortalNavigationItemType(StrEnum):
    """Stable portal navigation item types."""

    MODULE = "MODULE"
    PAGE = "PAGE"
    ACTION = "ACTION"


class PortalNavigationItemStatus(StrEnum):
    """Stable portal navigation item states."""

    AVAILABLE = "AVAILABLE"
    DISABLED = "DISABLED"
    HIDDEN = "HIDDEN"
    LOCKED = "LOCKED"
    FUTURE = "FUTURE"


class PortalNavigationRequest(PortalContractDTO):
    """Future portal navigation request contract."""

    user_id: str = Field(min_length=1, max_length=128)
    organisation_id: str = Field(min_length=1, max_length=128)
    session_id: str | None = Field(default=None, min_length=1, max_length=128)
    environment: PortalEnvironment = PortalEnvironment.LIVE
    include_hidden: bool = False
    trace_id: str | None = Field(default=None, min_length=1, max_length=128)


class PortalNavigationItemDTO(PortalContractDTO):
    """Portal-safe navigation item description."""

    item_id: str = Field(min_length=1, max_length=128)
    label: str = Field(min_length=1, max_length=160)
    item_type: PortalNavigationItemType = PortalNavigationItemType.PAGE
    status: PortalNavigationItemStatus = PortalNavigationItemStatus.DISABLED
    visible: bool = False
    enabled: bool = False
    module_code: PortalModuleCode | None = None
    commercial_status: PortalCommercialStatus | None = None
    target_key: str | None = Field(default=None, min_length=1, max_length=160)
    required_permissions: list[str] = Field(default_factory=list)
    reason: str | None = Field(default=None, min_length=1, max_length=255)
    sort_order: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def enforce_navigation_item_consistency(self) -> Self:
        """Keep item flags internally consistent."""

        if self.status == PortalNavigationItemStatus.HIDDEN and self.visible:
            raise ValueError("Hidden items cannot be visible.")

        if self.enabled and not self.visible:
            raise ValueError("Enabled items must be visible.")

        if self.enabled and self.status != PortalNavigationItemStatus.AVAILABLE:
            raise ValueError("Only available items can be enabled.")

        if self.enabled and self.target_key is None:
            raise ValueError("Enabled items require a target key.")

        is_future_module = self.module_code is not None and self.module_code in FUTURE_MODULE_CODES
        if is_future_module and self.enabled:
            raise ValueError("Future module items cannot be enabled.")

        blocked_status = self.commercial_status not in {None, PortalCommercialStatus.AVAILABLE}
        if blocked_status and self.enabled:
            raise ValueError("Unavailable module items cannot be enabled.")

        return self


class PortalNavigationSectionDTO(PortalContractDTO):
    """Portal-safe navigation section description."""

    section_id: str = Field(min_length=1, max_length=128)
    code: PortalNavigationSectionCode
    label: str = Field(min_length=1, max_length=160)
    visible: bool = True
    collapsed_by_default: bool = False
    items: list[PortalNavigationItemDTO] = Field(default_factory=list)
    sort_order: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def enforce_section_visibility_consistency(self) -> Self:
        """Hidden sections cannot contain visible items."""

        if not self.visible and any(item.visible for item in self.items):
            raise ValueError("Hidden sections cannot contain visible items.")

        return self


class PortalNavigationResponse(PortalContractDTO):
    """Portal navigation response data contract."""

    environment: PortalEnvironment
    sections: list[PortalNavigationSectionDTO] = Field(default_factory=list)
    message: str = Field(default="Portal navigation boundary response.", min_length=1, max_length=255)

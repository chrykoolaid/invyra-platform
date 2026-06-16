"""Shared portal boundary contract DTOs.

These contracts define portal-safe data shapes for the future Portal ↔ API
boundary. They do not implement portal UI, runtime execution, authentication,
inventory operations, launch execution, CRM, POS, forecasting, or purchasing
behavior.
"""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class PortalEnvironment(StrEnum):
    """Stable portal environment codes."""

    LIVE = "LIVE"
    TRAINING = "TRAINING"
    TEST = "TEST"


class PortalModuleCode(StrEnum):
    """Stable portal module codes exposed at the portal boundary."""

    INVENTORY = "INVENTORY"
    CRM = "CRM"
    POS = "POS"
    PAYROLL = "PAYROLL"
    WORKFORCE_MANAGEMENT = "WORKFORCE_MANAGEMENT"
    FORECASTING = "FORECASTING"
    PURCHASING_EXTENSIONS = "PURCHASING_EXTENSIONS"


class PortalCommercialStatus(StrEnum):
    """Commercial availability states exposed to the future portal."""

    AVAILABLE = "AVAILABLE"
    LOCKED = "LOCKED"
    FUTURE = "FUTURE"
    UNAVAILABLE = "UNAVAILABLE"
    NOT_COMMERCIALLY_AVAILABLE = "NOT_COMMERCIALLY_AVAILABLE"


class PortalPermissionScope(StrEnum):
    """Permission scope categories visible to portal contracts."""

    PLATFORM = "PLATFORM"
    ORGANISATION = "ORGANISATION"
    INVENTORY = "INVENTORY"
    BILLING = "BILLING"
    SUPPORT = "SUPPORT"


class PortalContractDTO(BaseModel):
    """Base class for portal DTO contract models."""

    model_config = ConfigDict(extra="forbid")


class PortalUserDTO(PortalContractDTO):
    """Portal-safe user summary."""

    user_id: str = Field(min_length=1, max_length=128)
    email: EmailStr | None = None
    display_name: str | None = Field(default=None, min_length=1, max_length=255)
    roles: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)


class PortalOrganisationDTO(PortalContractDTO):
    """Portal-safe organisation summary."""

    organisation_id: str = Field(min_length=1, max_length=128)
    name: str = Field(min_length=1, max_length=255)
    slug: str | None = Field(default=None, min_length=1, max_length=120)
    membership_role: str | None = Field(default=None, min_length=1, max_length=120)


class PortalEnvironmentDTO(PortalContractDTO):
    """Portal-safe environment summary."""

    environment: PortalEnvironment
    environment_id: str | None = Field(default=None, min_length=1, max_length=128)
    display_name: str | None = Field(default=None, min_length=1, max_length=120)
    is_active: bool = True
    is_selected: bool = False


class PortalDeviceDTO(PortalContractDTO):
    """Portal-safe device summary."""

    device_id: str | None = Field(default=None, min_length=1, max_length=128)
    display_name: str | None = Field(default=None, min_length=1, max_length=120)
    trusted: bool = False
    registered: bool = False


class PortalPermissionDTO(PortalContractDTO):
    """Portal-safe permission summary."""

    permission_code: str = Field(min_length=1, max_length=160)
    display_name: str | None = Field(default=None, min_length=1, max_length=160)
    scope: PortalPermissionScope = PortalPermissionScope.PLATFORM
    granted: bool = False


FUTURE_MODULE_CODES: frozenset[PortalModuleCode] = frozenset(
    {
        PortalModuleCode.CRM,
        PortalModuleCode.POS,
        PortalModuleCode.PAYROLL,
        PortalModuleCode.WORKFORCE_MANAGEMENT,
        PortalModuleCode.FORECASTING,
        PortalModuleCode.PURCHASING_EXTENSIONS,
    }
)


class PortalModuleDTO(PortalContractDTO):
    """Portal-safe module summary.

    This DTO describes module visibility only. It does not execute module launch
    behavior or expose runtime module data.
    """

    module_code: PortalModuleCode
    display_name: str = Field(min_length=1, max_length=160)
    commercial_status: PortalCommercialStatus
    visible: bool = False
    available: bool = False
    launch_allowed: bool = False
    route_key: str | None = Field(default=None, min_length=1, max_length=160)
    status_reason: str | None = Field(default=None, min_length=1, max_length=255)

    @model_validator(mode="after")
    def prevent_locked_modules_from_becoming_available(self) -> Self:
        """Prevent future or locked modules from being marked available."""

        non_available_status = self.commercial_status != PortalCommercialStatus.AVAILABLE
        requested_runtime_access = self.available or self.launch_allowed

        if non_available_status and requested_runtime_access:
            raise ValueError("Only commercially available modules can be available or launch allowed.")

        if self.module_code in FUTURE_MODULE_CODES and requested_runtime_access:
            raise ValueError("Future modules cannot be marked available or launch allowed.")

        return self

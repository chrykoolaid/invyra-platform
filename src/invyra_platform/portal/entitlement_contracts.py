"""Portal entitlement boundary contract models."""

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


class PortalEntitlementStatus(StrEnum):
    """Stable entitlement states visible at the portal boundary."""

    ENTITLED = "ENTITLED"
    NOT_ENTITLED = "NOT_ENTITLED"
    LOCKED = "LOCKED"
    FUTURE = "FUTURE"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"


class PortalEntitlementRequest(PortalContractDTO):
    """Future portal entitlement request contract."""

    user_id: str = Field(min_length=1, max_length=128)
    organisation_id: str = Field(min_length=1, max_length=128)
    session_id: str | None = Field(default=None, min_length=1, max_length=128)
    environment: PortalEnvironment = PortalEnvironment.LIVE
    include_future_modules: bool = True
    trace_id: str | None = Field(default=None, min_length=1, max_length=128)


class PortalEntitlementDTO(PortalContractDTO):
    """Portal-safe module entitlement summary."""

    module_code: PortalModuleCode
    display_name: str = Field(min_length=1, max_length=160)
    commercial_status: PortalCommercialStatus
    status: PortalEntitlementStatus = PortalEntitlementStatus.UNKNOWN
    visible: bool = False
    entitled: bool = False
    available: bool = False
    launch_allowed: bool = False
    license_id: str | None = Field(default=None, min_length=1, max_length=128)
    entitlement_id: str | None = Field(default=None, min_length=1, max_length=128)
    required_permissions: list[str] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
    sort_order: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def enforce_entitlement_consistency(self) -> Self:
        """Keep portal entitlement state aligned with commercial availability."""

        is_future_module = self.module_code in FUTURE_MODULE_CODES
        runtime_enabled = self.available or self.launch_allowed

        if self.launch_allowed and not self.available:
            raise ValueError("Launch allowed requires available entitlement.")

        if runtime_enabled and not self.entitled:
            raise ValueError("Available entitlements require entitled state.")

        if self.entitled and self.status != PortalEntitlementStatus.ENTITLED:
            raise ValueError("Entitled modules require ENTITLED status.")

        if runtime_enabled and self.commercial_status != PortalCommercialStatus.AVAILABLE:
            raise ValueError("Runtime-enabled entitlements require commercial availability.")

        if is_future_module and runtime_enabled:
            raise ValueError("Future modules cannot be available or launch allowed.")

        if is_future_module and self.entitled:
            raise ValueError("Future modules cannot be marked entitled.")

        return self


class PortalEntitlementGroupDTO(PortalContractDTO):
    """Portal-safe entitlement group summary."""

    group_id: str = Field(min_length=1, max_length=128)
    label: str = Field(min_length=1, max_length=160)
    entitlements: list[PortalEntitlementDTO] = Field(default_factory=list)
    sort_order: int = Field(default=0, ge=0)


class PortalEntitlementResponse(PortalContractDTO):
    """Portal entitlement response data contract."""

    environment: PortalEnvironment
    groups: list[PortalEntitlementGroupDTO] = Field(default_factory=list)
    message: str = Field(default="Portal entitlement boundary response.", min_length=1, max_length=255)

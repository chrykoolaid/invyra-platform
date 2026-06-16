"""Portal session boundary contract models.

These contracts describe future portal-visible session state after platform
authentication exists. They do not implement login, logout, token issuance,
session persistence, portal runtime execution, inventory launch execution, or UI.
"""

from datetime import datetime
from enum import StrEnum
from typing import Self

from pydantic import Field, model_validator

from invyra_platform.portal.contracts import (
    PortalContractDTO,
    PortalDeviceDTO,
    PortalEnvironment,
    PortalEnvironmentDTO,
    PortalOrganisationDTO,
    PortalUserDTO,
)


class PortalSessionStatus(StrEnum):
    """Stable portal session states visible at the portal boundary."""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    UNAUTHENTICATED = "UNAUTHENTICATED"
    UNKNOWN = "UNKNOWN"


class PortalSessionRequest(PortalContractDTO):
    """Future portal current-session request contract."""

    session_id: str | None = Field(default=None, min_length=1, max_length=128)
    auth_session_id: str | None = Field(default=None, min_length=1, max_length=128)
    user_id: str | None = Field(default=None, min_length=1, max_length=128)
    organisation_id: str | None = Field(default=None, min_length=1, max_length=128)
    device_id: str | None = Field(default=None, min_length=1, max_length=128)
    environment: PortalEnvironment | None = None
    trace_id: str | None = Field(default=None, min_length=1, max_length=128)


class PortalSessionContextDTO(PortalContractDTO):
    """Portal-safe context attached to a future portal session."""

    user: PortalUserDTO | None = None
    organisation: PortalOrganisationDTO | None = None
    environment: PortalEnvironmentDTO | None = None
    device: PortalDeviceDTO | None = None


class PortalSessionDTO(PortalContractDTO):
    """Portal-safe session summary.

    This DTO describes session visibility only. It does not create, refresh,
    revoke, validate, persist, or execute a session.
    """

    session_id: str | None = Field(default=None, min_length=1, max_length=128)
    auth_session_id: str | None = Field(default=None, min_length=1, max_length=128)
    status: PortalSessionStatus = PortalSessionStatus.UNKNOWN
    authenticated: bool = False
    user_id: str | None = Field(default=None, min_length=1, max_length=128)
    organisation_id: str | None = Field(default=None, min_length=1, max_length=128)
    environment: PortalEnvironment | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None

    @model_validator(mode="after")
    def enforce_session_state_consistency(self) -> Self:
        """Keep portal session status and identity fields internally consistent."""

        if self.status == PortalSessionStatus.ACTIVE:
            missing_active_fields = not all(
                [self.authenticated, self.session_id, self.user_id, self.organisation_id, self.environment]
            )
            if missing_active_fields:
                raise ValueError("Active portal sessions require authentication, session, user, organisation, and environment.")

        inactive_status = self.status in {
            PortalSessionStatus.EXPIRED,
            PortalSessionStatus.REVOKED,
            PortalSessionStatus.UNAUTHENTICATED,
        }
        if inactive_status and self.authenticated:
            raise ValueError("Inactive portal sessions cannot be marked authenticated.")

        if self.status == PortalSessionStatus.REVOKED and self.revoked_at is None:
            raise ValueError("Revoked portal sessions require revoked_at.")

        return self


class PortalSessionResponse(PortalContractDTO):
    """Portal current-session response data contract."""

    authenticated: bool = False
    session: PortalSessionDTO | None = None
    context: PortalSessionContextDTO | None = None
    message: str = Field(default="Portal session boundary response.", min_length=1, max_length=255)

    @model_validator(mode="after")
    def enforce_response_consistency(self) -> Self:
        """Ensure authenticated responses include an active session and context."""

        if self.authenticated:
            if self.session is None or self.session.status != PortalSessionStatus.ACTIVE:
                raise ValueError("Authenticated portal responses require an active session.")
            if self.context is None or self.context.user is None or self.context.organisation is None:
                raise ValueError("Authenticated portal responses require user and organisation context.")

        return self

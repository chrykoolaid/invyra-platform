"""Portal API adapter skeleton builders.

These helpers prepare portal contract DTO payloads for the API route layer.
They do not execute portal runtime behavior, authenticate users, evaluate
entitlements, launch Inventory, read Inventory data, or access persistence.
"""

from invyra_platform.core.service_results import ServiceResult
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest, PortalEntitlementResponse
from invyra_platform.portal.inventory_entry_contracts import (
    PortalInventoryEntryDTO,
    PortalInventoryEntryRequest,
    PortalInventoryEntryResponse,
)
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest, PortalNavigationResponse
from invyra_platform.portal.session_contracts import PortalSessionRequest, PortalSessionResponse


def build_portal_status_result() -> ServiceResult:
    """Build the Portal API boundary status skeleton result."""
    return ServiceResult.not_implemented(
        data={
            "boundary": "portal-api",
            "runtime": "not-implemented",
            "routes": [],
        }
    )


def build_portal_session_result(_: PortalSessionRequest) -> ServiceResult:
    """Build the Portal current-session skeleton result."""
    response = PortalSessionResponse(
        authenticated=False,
        session=None,
        context=None,
        message="Portal session boundary skeleton only.",
    )
    return ServiceResult.not_implemented(data=response.model_dump(mode="json"))


def build_portal_navigation_result(request: PortalNavigationRequest) -> ServiceResult:
    """Build the Portal navigation skeleton result."""
    response = PortalNavigationResponse(
        environment=request.environment,
        sections=[],
        message="Portal navigation boundary skeleton only.",
    )
    return ServiceResult.not_implemented(data=response.model_dump(mode="json"))


def build_portal_entitlement_result(request: PortalEntitlementRequest) -> ServiceResult:
    """Build the Portal entitlement skeleton result."""
    response = PortalEntitlementResponse(
        environment=request.environment,
        groups=[],
        message="Portal entitlement boundary skeleton only.",
    )
    return ServiceResult.not_implemented(data=response.model_dump(mode="json"))


def build_portal_inventory_entry_result(request: PortalInventoryEntryRequest) -> ServiceResult:
    """Build the Portal Inventory entry skeleton result."""
    response = PortalInventoryEntryResponse(
        environment=request.environment,
        entry=PortalInventoryEntryDTO(
            environment=request.environment,
            visible=False,
            enabled=False,
            entry_allowed=False,
            reason="Portal Inventory entry skeleton only.",
        ),
        message="Portal Inventory entry boundary skeleton only.",
    )
    return ServiceResult.not_implemented(data=response.model_dump(mode="json"))

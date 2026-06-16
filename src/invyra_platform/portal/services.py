"""Portal service boundary skeletons.

These services reserve the future Portal service layer without executing
runtime behavior. They do not authenticate users, create sessions, evaluate
entitlements, check licenses, launch Inventory, read Inventory data, or access
persistence.
"""

from invyra_platform.core.service_results import ServiceResult
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest
from invyra_platform.portal.inventory_entry_contracts import PortalInventoryEntryRequest
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest
from invyra_platform.portal.session_contracts import PortalSessionRequest


class PortalStatusService:
    """Future Portal status service boundary."""

    def get_status(self) -> ServiceResult:
        """Return the Portal status service skeleton result."""
        return ServiceResult.not_implemented(
            data={
                "boundary": "portal-service-status",
                "runtime": "not-implemented",
                "message": "Portal status service boundary skeleton only.",
            }
        )


class PortalSessionService:
    """Future Portal session service boundary."""

    def get_session(self, _request: PortalSessionRequest) -> ServiceResult:
        """Return the Portal session service skeleton result."""
        return ServiceResult.not_implemented(
            data={
                "boundary": "portal-service-session",
                "runtime": "not-implemented",
                "message": "Portal session service boundary skeleton only.",
            }
        )


class PortalNavigationService:
    """Future Portal navigation service boundary."""

    def get_navigation(self, _request: PortalNavigationRequest) -> ServiceResult:
        """Return the Portal navigation service skeleton result."""
        return ServiceResult.not_implemented(
            data={
                "boundary": "portal-service-navigation",
                "runtime": "not-implemented",
                "message": "Portal navigation service boundary skeleton only.",
            }
        )


class PortalEntitlementService:
    """Future Portal entitlement service boundary."""

    def get_entitlements(self, _request: PortalEntitlementRequest) -> ServiceResult:
        """Return the Portal entitlement service skeleton result."""
        return ServiceResult.not_implemented(
            data={
                "boundary": "portal-service-entitlement",
                "runtime": "not-implemented",
                "message": "Portal entitlement service boundary skeleton only.",
            }
        )


class PortalInventoryEntryService:
    """Future Portal Inventory entry service boundary."""

    def get_inventory_entry(self, _request: PortalInventoryEntryRequest) -> ServiceResult:
        """Return the Portal Inventory entry service skeleton result."""
        return ServiceResult.not_implemented(
            data={
                "boundary": "portal-service-inventory-entry",
                "runtime": "not-implemented",
                "message": "Portal Inventory entry service boundary skeleton only.",
            }
        )

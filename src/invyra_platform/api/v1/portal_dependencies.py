"""Portal dependency provider skeletons.

These helpers expose safe provider boundaries for the Portal API layer.
They return portal adapter callable references only. They do not execute
portal runtime behavior, authenticate users, evaluate entitlements, launch
Inventory, read Inventory data, or access persistence.
"""

from collections.abc import Callable

from invyra_platform.api.v1.portal_adapters import (
    build_portal_entitlement_result,
    build_portal_inventory_entry_result,
    build_portal_navigation_result,
    build_portal_session_result,
    build_portal_status_result,
)
from invyra_platform.core.service_results import ServiceResult
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest
from invyra_platform.portal.inventory_entry_contracts import PortalInventoryEntryRequest
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest
from invyra_platform.portal.session_contracts import PortalSessionRequest

PortalStatusAdapter = Callable[[], ServiceResult]
PortalSessionAdapter = Callable[[PortalSessionRequest], ServiceResult]
PortalNavigationAdapter = Callable[[PortalNavigationRequest], ServiceResult]
PortalEntitlementAdapter = Callable[[PortalEntitlementRequest], ServiceResult]
PortalInventoryEntryAdapter = Callable[[PortalInventoryEntryRequest], ServiceResult]


def get_portal_status_adapter() -> PortalStatusAdapter:
    """Return the Portal status adapter skeleton boundary."""
    return build_portal_status_result


def get_portal_session_adapter() -> PortalSessionAdapter:
    """Return the Portal session adapter skeleton boundary."""
    return build_portal_session_result


def get_portal_navigation_adapter() -> PortalNavigationAdapter:
    """Return the Portal navigation adapter skeleton boundary."""
    return build_portal_navigation_result


def get_portal_entitlement_adapter() -> PortalEntitlementAdapter:
    """Return the Portal entitlement adapter skeleton boundary."""
    return build_portal_entitlement_result


def get_portal_inventory_entry_adapter() -> PortalInventoryEntryAdapter:
    """Return the Portal Inventory entry adapter skeleton boundary."""
    return build_portal_inventory_entry_result

"""Portal API route skeletons."""

from fastapi import APIRouter

from invyra_platform.api.adapters import map_service_result_to_api_response
from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.v1.portal_adapters import (
    build_portal_entitlement_result,
    build_portal_inventory_entry_result,
    build_portal_navigation_result,
    build_portal_session_result,
    build_portal_status_result,
)
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest
from invyra_platform.portal.inventory_entry_contracts import PortalInventoryEntryRequest
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest
from invyra_platform.portal.session_contracts import PortalSessionRequest

router = APIRouter(prefix="/portal", tags=["portal"])


@router.get("/status", response_model=ApiResponse)
def portal_status() -> ApiResponse:
    """Future Portal API boundary status."""
    return map_service_result_to_api_response(
        build_portal_status_result(),
        message="Portal API boundary skeleton only.",
    )


@router.post("/session", response_model=ApiResponse)
def portal_session(request: PortalSessionRequest) -> ApiResponse:
    """Future Portal current-session boundary."""
    return map_service_result_to_api_response(
        build_portal_session_result(request),
        message="Portal session boundary skeleton only.",
        trace_id=request.trace_id,
    )


@router.post("/navigation", response_model=ApiResponse)
def portal_navigation(request: PortalNavigationRequest) -> ApiResponse:
    """Future Portal navigation boundary."""
    return map_service_result_to_api_response(
        build_portal_navigation_result(request),
        message="Portal navigation boundary skeleton only.",
        trace_id=request.trace_id,
    )


@router.post("/entitlements", response_model=ApiResponse)
def portal_entitlements(request: PortalEntitlementRequest) -> ApiResponse:
    """Future Portal entitlement boundary."""
    return map_service_result_to_api_response(
        build_portal_entitlement_result(request),
        message="Portal entitlement boundary skeleton only.",
        trace_id=request.trace_id,
    )


@router.post("/inventory-entry", response_model=ApiResponse)
def portal_inventory_entry(request: PortalInventoryEntryRequest) -> ApiResponse:
    """Future Portal Inventory entry boundary."""
    return map_service_result_to_api_response(
        build_portal_inventory_entry_result(request),
        message="Portal Inventory entry boundary skeleton only.",
        trace_id=request.trace_id,
    )

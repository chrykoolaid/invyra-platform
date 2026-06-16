"""Portal API route skeletons."""

from fastapi import APIRouter

from invyra_platform.api.adapters import map_service_result_to_api_response
from invyra_platform.api.contracts import ApiResponse
from invyra_platform.core.service_results import ServiceResult
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest, PortalEntitlementResponse
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest, PortalNavigationResponse
from invyra_platform.portal.session_contracts import PortalSessionRequest, PortalSessionResponse

router = APIRouter(prefix="/portal", tags=["portal"])


@router.get("/status", response_model=ApiResponse)
def portal_status() -> ApiResponse:
    """Future Portal API boundary status."""
    return map_service_result_to_api_response(
        ServiceResult.not_implemented(
            data={
                "boundary": "portal-api",
                "runtime": "not-implemented",
                "routes": [],
            }
        ),
        message="Portal API boundary skeleton only.",
    )


@router.post("/session", response_model=ApiResponse)
def portal_session(request: PortalSessionRequest) -> ApiResponse:
    """Future Portal current-session boundary."""
    response = PortalSessionResponse(
        authenticated=False,
        session=None,
        context=None,
        message="Portal session boundary skeleton only.",
    )

    return map_service_result_to_api_response(
        ServiceResult.not_implemented(data=response.model_dump(mode="json")),
        message="Portal session boundary skeleton only.",
        trace_id=request.trace_id,
    )


@router.post("/navigation", response_model=ApiResponse)
def portal_navigation(request: PortalNavigationRequest) -> ApiResponse:
    """Future Portal navigation boundary."""
    response = PortalNavigationResponse(
        environment=request.environment,
        sections=[],
        message="Portal navigation boundary skeleton only.",
    )

    return map_service_result_to_api_response(
        ServiceResult.not_implemented(data=response.model_dump(mode="json")),
        message="Portal navigation boundary skeleton only.",
        trace_id=request.trace_id,
    )


@router.post("/entitlements", response_model=ApiResponse)
def portal_entitlements(request: PortalEntitlementRequest) -> ApiResponse:
    """Future Portal entitlement boundary."""
    response = PortalEntitlementResponse(
        environment=request.environment,
        groups=[],
        message="Portal entitlement boundary skeleton only.",
    )

    return map_service_result_to_api_response(
        ServiceResult.not_implemented(data=response.model_dump(mode="json")),
        message="Portal entitlement boundary skeleton only.",
        trace_id=request.trace_id,
    )

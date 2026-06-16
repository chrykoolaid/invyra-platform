"""Portal API route skeletons."""

from fastapi import APIRouter

from invyra_platform.api.adapters import map_service_result_to_api_response
from invyra_platform.api.contracts import ApiResponse
from invyra_platform.core.service_results import ServiceResult

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

"""Inventory launch API route skeletons."""

from fastapi import APIRouter

from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.v1.inventory_launch_contracts import (
    InventoryLaunchAttemptRequest,
    InventoryLaunchSessionRequest,
    InventoryLaunchTokenRequest,
)
from invyra_platform.inventory_launch.service import InventoryLaunchService

router = APIRouter(prefix="/inventory/launch", tags=["inventory-launch"])


def _service() -> InventoryLaunchService:
    return InventoryLaunchService()


@router.post("/attempt", response_model=ApiResponse)
def create_launch_attempt(_: InventoryLaunchAttemptRequest) -> ApiResponse:
    """Future Inventory launch attempt boundary."""
    return ApiResponse.from_service_result(
        _service().create_launch_attempt(),
        message="Inventory launch attempt skeleton only.",
    )


@router.post("/token", response_model=ApiResponse)
def create_launch_token(_: InventoryLaunchTokenRequest) -> ApiResponse:
    """Future Inventory launch token boundary."""
    return ApiResponse.from_service_result(
        _service().create_launch_token(),
        message="Inventory launch token skeleton only.",
    )


@router.post("/session", response_model=ApiResponse)
def create_launch_session(_: InventoryLaunchSessionRequest) -> ApiResponse:
    """Future Inventory launch session boundary."""
    return ApiResponse.from_service_result(
        _service().create_launch_session(),
        message="Inventory launch session skeleton only.",
    )


@router.get("/session/{session_id}", response_model=ApiResponse)
def get_launch_session(session_id: str) -> ApiResponse:
    """Future Inventory launch session lookup boundary."""
    _ = session_id
    return ApiResponse.from_service_result(
        _service().expire_launch_session(),
        message="Inventory launch session lookup skeleton only.",
    )


@router.get("/events", response_model=ApiResponse)
def inventory_launch_events() -> ApiResponse:
    """Future Inventory launch events boundary."""
    return ApiResponse.from_service_result(
        _service().record_launch_event(),
        message="Inventory launch events skeleton only.",
    )

"""Inventory launch API route skeletons."""

from typing import Annotated

from fastapi import APIRouter, Depends

from invyra_platform.api.adapters import map_service_result_to_api_response
from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.dependencies import get_inventory_launch_service
from invyra_platform.api.v1.inventory_launch_contracts import (
    InventoryLaunchAttemptRequest,
    InventoryLaunchSessionRequest,
    InventoryLaunchTokenRequest,
)
from invyra_platform.inventory_launch.service import InventoryLaunchService

router = APIRouter(prefix="/inventory/launch", tags=["inventory-launch"])
InventoryLaunchServiceDependency = Annotated[
    InventoryLaunchService,
    Depends(get_inventory_launch_service),
]


@router.post("/attempt", response_model=ApiResponse)
def create_launch_attempt(
    _: InventoryLaunchAttemptRequest,
    service: InventoryLaunchServiceDependency,
) -> ApiResponse:
    """Future Inventory launch attempt boundary."""
    return map_service_result_to_api_response(
        service.create_launch_attempt(),
        message="Inventory launch attempt skeleton only.",
    )


@router.post("/token", response_model=ApiResponse)
def create_launch_token(
    _: InventoryLaunchTokenRequest,
    service: InventoryLaunchServiceDependency,
) -> ApiResponse:
    """Future Inventory launch token boundary."""
    return map_service_result_to_api_response(
        service.create_launch_token(),
        message="Inventory launch token skeleton only.",
    )


@router.post("/session", response_model=ApiResponse)
def create_launch_session(
    _: InventoryLaunchSessionRequest,
    service: InventoryLaunchServiceDependency,
) -> ApiResponse:
    """Future Inventory launch session boundary."""
    return map_service_result_to_api_response(
        service.create_launch_session(),
        message="Inventory launch session skeleton only.",
    )


@router.get("/session/{session_id}", response_model=ApiResponse)
def get_launch_session(session_id: str, service: InventoryLaunchServiceDependency) -> ApiResponse:
    """Future Inventory launch session lookup boundary."""
    _ = session_id
    return map_service_result_to_api_response(
        service.expire_launch_session(),
        message="Inventory launch session lookup skeleton only.",
    )


@router.get("/events", response_model=ApiResponse)
def inventory_launch_events(service: InventoryLaunchServiceDependency) -> ApiResponse:
    """Future Inventory launch events boundary."""
    return map_service_result_to_api_response(
        service.record_launch_event(),
        message="Inventory launch events skeleton only.",
    )

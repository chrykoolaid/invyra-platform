"""Inventory access API route skeletons."""

from typing import Annotated

from fastapi import APIRouter, Depends

from invyra_platform.api.adapters import map_service_result_to_api_response
from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.dependencies import get_inventory_access_gateway_service
from invyra_platform.api.v1.inventory_access_contracts import InventoryAccessEvaluationRequest
from invyra_platform.inventory_access.service import InventoryAccessGatewayService

router = APIRouter(prefix="/inventory/access", tags=["inventory-access"])
InventoryAccessServiceDependency = Annotated[
    InventoryAccessGatewayService,
    Depends(get_inventory_access_gateway_service),
]


@router.post("/evaluate", response_model=ApiResponse)
def evaluate_inventory_access(
    _: InventoryAccessEvaluationRequest,
    service: InventoryAccessServiceDependency,
) -> ApiResponse:
    """Future Inventory access evaluation boundary."""
    return map_service_result_to_api_response(
        service.evaluate_inventory_access(),
        message="Inventory access evaluation skeleton only.",
    )


@router.get("/status", response_model=ApiResponse)
def inventory_access_status(service: InventoryAccessServiceDependency) -> ApiResponse:
    """Future Inventory access status boundary."""
    return map_service_result_to_api_response(
        service.validate_environment_access(),
        message="Inventory access status skeleton only.",
    )


@router.get("/events", response_model=ApiResponse)
def inventory_access_events(service: InventoryAccessServiceDependency) -> ApiResponse:
    """Future Inventory access events boundary."""
    return map_service_result_to_api_response(
        service.record_access_event(),
        message="Inventory access events skeleton only.",
    )

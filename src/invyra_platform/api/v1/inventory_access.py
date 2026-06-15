"""Inventory access API route skeletons."""

from fastapi import APIRouter

from invyra_platform.api.contracts import ApiResponse
from invyra_platform.api.v1.inventory_access_contracts import InventoryAccessEvaluationRequest
from invyra_platform.inventory_access.service import InventoryAccessGatewayService

router = APIRouter(prefix="/inventory/access", tags=["inventory-access"])


def _service() -> InventoryAccessGatewayService:
    return InventoryAccessGatewayService()


@router.post("/evaluate", response_model=ApiResponse)
def evaluate_inventory_access(_: InventoryAccessEvaluationRequest) -> ApiResponse:
    """Future Inventory access evaluation boundary."""
    return ApiResponse.from_service_result(
        _service().evaluate_inventory_access(),
        message="Inventory access evaluation skeleton only.",
    )


@router.get("/status", response_model=ApiResponse)
def inventory_access_status() -> ApiResponse:
    """Future Inventory access status boundary."""
    return ApiResponse.from_service_result(
        _service().validate_environment_access(),
        message="Inventory access status skeleton only.",
    )


@router.get("/events", response_model=ApiResponse)
def inventory_access_events() -> ApiResponse:
    """Future Inventory access events boundary."""
    return ApiResponse.from_service_result(
        _service().record_access_event(),
        message="Inventory access events skeleton only.",
    )

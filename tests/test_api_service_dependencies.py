"""API service dependency provider tests."""

from invyra_platform.api.dependencies import (
    get_auth_runtime_service,
    get_inventory_access_gateway_service,
    get_inventory_launch_service,
)
from invyra_platform.auth.service import AuthRuntimeService
from invyra_platform.inventory_access.service import InventoryAccessGatewayService
from invyra_platform.inventory_launch.service import InventoryLaunchService


def test_auth_runtime_service_provider_returns_service_boundary() -> None:
    service = get_auth_runtime_service()

    assert isinstance(service, AuthRuntimeService)
    result = service.login()
    assert result.status == "NOT_IMPLEMENTED"
    assert result.reason == "SERVICE_SKELETON_ONLY"


def test_inventory_access_gateway_service_provider_returns_service_boundary() -> None:
    service = get_inventory_access_gateway_service()

    assert isinstance(service, InventoryAccessGatewayService)
    result = service.evaluate_inventory_access()
    assert result.status == "NOT_IMPLEMENTED"
    assert result.reason == "SERVICE_SKELETON_ONLY"


def test_inventory_launch_service_provider_returns_service_boundary() -> None:
    service = get_inventory_launch_service()

    assert isinstance(service, InventoryLaunchService)
    result = service.create_launch_attempt()
    assert result.status == "NOT_IMPLEMENTED"
    assert result.reason == "SERVICE_SKELETON_ONLY"

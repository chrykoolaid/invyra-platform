"""API dependency providers for platform services."""

from invyra_platform.auth.service import AuthRuntimeService
from invyra_platform.inventory_access.service import InventoryAccessGatewayService
from invyra_platform.inventory_launch.service import InventoryLaunchService


def get_auth_runtime_service() -> AuthRuntimeService:
    """Provide the authentication runtime service boundary."""
    return AuthRuntimeService()


def get_inventory_access_gateway_service() -> InventoryAccessGatewayService:
    """Provide the Inventory access gateway service boundary."""
    return InventoryAccessGatewayService()


def get_inventory_launch_service() -> InventoryLaunchService:
    """Provide the Inventory launch service boundary."""
    return InventoryLaunchService()

"""Inventory launch service skeleton tests."""

from invyra_platform.inventory_launch.service import InventoryLaunchService


LAUNCH_METHODS = [
    "create_launch_attempt",
    "create_launch_token",
    "consume_launch_token",
    "create_launch_session",
    "expire_launch_session",
    "revoke_launch_session",
    "record_launch_event",
]


def test_inventory_launch_service_methods_return_skeleton_result() -> None:
    service = InventoryLaunchService()

    for method_name in LAUNCH_METHODS:
        method = getattr(service, method_name)
        result = method()

        assert result.success is False
        assert result.status == "NOT_IMPLEMENTED"
        assert result.reason == "SERVICE_SKELETON_ONLY"
        assert result.data == {"service": "InventoryLaunchService", "method": method_name}

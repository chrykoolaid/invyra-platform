"""Inventory launch API smoke tests."""

import pytest
from pydantic import ValidationError

from invyra_platform.api.v1.inventory_launch_contracts import InventoryLaunchAttemptRequest
from invyra_platform.app import create_app


def test_launch_attempt_request_contract() -> None:
    request = InventoryLaunchAttemptRequest(
        user_id="user-001",
        organisation_id="org-001",
        environment="LIVE",
    )

    assert request.user_id == "user-001"
    assert request.organisation_id == "org-001"
    assert request.environment == "LIVE"

    with pytest.raises(ValidationError):
        InventoryLaunchAttemptRequest(user_id="", organisation_id="org-001", environment="LIVE")

    with pytest.raises(ValidationError):
        InventoryLaunchAttemptRequest(user_id="user-001", organisation_id="org-001", environment="DEV")


def test_app_includes_launch_routes() -> None:
    route_paths = {route.path for route in create_app().routes}

    assert "/api/v1/inventory/launch/attempt" in route_paths
    assert "/api/v1/inventory/launch/session/{session_id}" in route_paths
    assert "/api/v1/inventory/launch/events" in route_paths

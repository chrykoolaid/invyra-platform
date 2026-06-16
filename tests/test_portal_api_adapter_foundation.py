"""Portal API adapter foundation tests."""

from pathlib import Path

from invyra_platform.api.v1.portal_adapters import (
    build_portal_entitlement_result,
    build_portal_inventory_entry_result,
    build_portal_navigation_result,
    build_portal_session_result,
    build_portal_status_result,
)
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest
from invyra_platform.portal.inventory_entry_contracts import PortalInventoryEntryRequest
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest
from invyra_platform.portal.session_contracts import PortalSessionRequest


def test_portal_status_adapter_returns_skeleton_result() -> None:
    result = build_portal_status_result()

    assert result.success is False
    assert result.status == "NOT_IMPLEMENTED"
    assert result.reason == "SERVICE_SKELETON_ONLY"
    assert result.data == {
        "boundary": "portal-api",
        "runtime": "not-implemented",
        "routes": [],
    }


def test_portal_session_adapter_returns_unauthenticated_skeleton_result() -> None:
    result = build_portal_session_result(PortalSessionRequest(trace_id="trace-001"))

    assert result.success is False
    assert result.status == "NOT_IMPLEMENTED"
    assert result.data is not None
    assert result.data["authenticated"] is False
    assert result.data["session"] is None
    assert result.data["context"] is None


def test_portal_navigation_adapter_returns_empty_sections() -> None:
    result = build_portal_navigation_result(
        PortalNavigationRequest(
            user_id="user-001",
            organisation_id="org-001",
            environment="TRAINING",
        )
    )

    assert result.success is False
    assert result.status == "NOT_IMPLEMENTED"
    assert result.data is not None
    assert result.data["environment"] == "TRAINING"
    assert result.data["sections"] == []


def test_portal_entitlement_adapter_returns_empty_groups() -> None:
    result = build_portal_entitlement_result(
        PortalEntitlementRequest(
            user_id="user-001",
            organisation_id="org-001",
            environment="TEST",
        )
    )

    assert result.success is False
    assert result.status == "NOT_IMPLEMENTED"
    assert result.data is not None
    assert result.data["environment"] == "TEST"
    assert result.data["groups"] == []


def test_portal_inventory_entry_adapter_returns_disabled_entry() -> None:
    result = build_portal_inventory_entry_result(
        PortalInventoryEntryRequest(
            user_id="user-001",
            organisation_id="org-001",
            environment="LIVE",
        )
    )

    assert result.success is False
    assert result.status == "NOT_IMPLEMENTED"
    assert result.data is not None
    assert result.data["environment"] == "LIVE"

    entry = result.data["entry"]
    assert entry["module_code"] == "INVENTORY"
    assert entry["visible"] is False
    assert entry["enabled"] is False
    assert entry["entry_allowed"] is False
    assert entry["availability"]["allowed"] is False


def test_portal_adapter_module_has_no_runtime_dependencies() -> None:
    adapter_source = Path("src/invyra_platform/api/v1/portal_adapters.py").read_text(encoding="utf-8")

    assert "Depends(" not in adapter_source
    assert "from sqlalchemy" not in adapter_source
    assert "import sqlalchemy" not in adapter_source
    assert "from invyra_platform.models" not in adapter_source
    assert "get_auth_runtime_service" not in adapter_source
    assert "get_inventory_access_gateway_service" not in adapter_source
    assert "get_inventory_launch_service" not in adapter_source

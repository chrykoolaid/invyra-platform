"""Portal adapter boundary hardening tests."""

from pathlib import Path
from typing import Any

from invyra_platform.api.v1 import portal_adapters
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest
from invyra_platform.portal.inventory_entry_contracts import PortalInventoryEntryRequest
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest
from invyra_platform.portal.session_contracts import PortalSessionRequest

RUNTIME_DATA_KEYS = {
    "stock",
    "stock_on_hand",
    "orders",
    "purchase_orders",
    "receiving",
    "transfers",
    "stocktake",
    "wastage",
    "markdowns",
    "reports",
    "inventory_items",
    "item_id",
    "sku",
    "quantity",
}

FORBIDDEN_ADAPTER_FRAGMENTS = {
    "Depends(",
    "from sqlalchemy",
    "import sqlalchemy",
    "from invyra_platform.models",
    "from invyra_platform.db",
    "from invyra_platform.database",
    "from invyra_platform.api.dependencies",
    "get_auth_runtime_service",
    "get_inventory_access_gateway_service",
    "get_inventory_launch_service",
    "AuthRuntimeService",
    "InventoryAccessGatewayService",
    "InventoryLaunchService",
    "commit(",
    "execute(",
    "query(",
}

LOCKED_EXISTING_PORTAL_MIGRATIONS = {"008_portal_runtime_foundation.py"}


def _iter_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        keys = set(value.keys())
        for nested in value.values():
            keys.update(_iter_keys(nested))
        return keys
    if isinstance(value, list):
        keys: set[str] = set()
        for item in value:
            keys.update(_iter_keys(item))
        return keys
    return set()


def test_portal_adapters_do_not_leak_inventory_runtime_data() -> None:
    results = [
        portal_adapters.build_portal_status_result(),
        portal_adapters.build_portal_session_result(PortalSessionRequest()),
        portal_adapters.build_portal_navigation_result(
            PortalNavigationRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
        ),
        portal_adapters.build_portal_entitlement_result(
            PortalEntitlementRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
        ),
        portal_adapters.build_portal_inventory_entry_result(
            PortalInventoryEntryRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
        ),
    ]

    for result in results:
        assert result.data is not None
        assert _iter_keys(result.data).isdisjoint(RUNTIME_DATA_KEYS)


def test_portal_adapters_do_not_create_runtime_session_or_launch_payloads() -> None:
    session_result = portal_adapters.build_portal_session_result(PortalSessionRequest())
    inventory_result = portal_adapters.build_portal_inventory_entry_result(
        PortalInventoryEntryRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
    )

    assert session_result.data is not None
    assert session_result.data["authenticated"] is False
    assert session_result.data["session"] is None
    assert session_result.data["context"] is None

    assert inventory_result.data is not None
    entry = inventory_result.data["entry"]
    assert entry["visible"] is False
    assert entry["enabled"] is False
    assert entry["entry_allowed"] is False
    assert entry["availability"]["allowed"] is False
    assert entry["availability"]["target_key"] is None
    assert entry["availability"]["evaluation_id"] is None


def test_portal_adapters_keep_future_module_unlocks_impossible() -> None:
    result = portal_adapters.build_portal_entitlement_result(
        PortalEntitlementRequest(
            user_id="user-001",
            organisation_id="org-001",
            environment="LIVE",
            include_future_modules=True,
        )
    )

    assert result.data is not None
    assert result.success is False
    assert result.status == "NOT_IMPLEMENTED"
    assert result.data["groups"] == []


def test_portal_adapter_module_has_no_runtime_service_or_persistence_dependencies() -> None:
    adapter_source = Path("src/invyra_platform/api/v1/portal_adapters.py").read_text(encoding="utf-8")

    for fragment in FORBIDDEN_ADAPTER_FRAGMENTS:
        assert fragment not in adapter_source


def test_portal_adapter_sprint_does_not_introduce_new_portal_migrations() -> None:
    migration_versions_path = Path("migrations/versions")

    if not migration_versions_path.exists():
        return

    portal_migration_files = {
        path.name for path in migration_versions_path.glob("*.py") if "portal" in path.name.lower()
    }
    unexpected_portal_migrations = portal_migration_files - LOCKED_EXISTING_PORTAL_MIGRATIONS

    assert unexpected_portal_migrations == set()

"""Portal service boundary hardening tests."""

from pathlib import Path
from typing import Any

from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest
from invyra_platform.portal.inventory_entry_contracts import PortalInventoryEntryRequest
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest
from invyra_platform.portal.services import (
    PortalEntitlementService,
    PortalInventoryEntryService,
    PortalNavigationService,
    PortalSessionService,
    PortalStatusService,
)
from invyra_platform.portal.session_contracts import PortalSessionRequest

FORBIDDEN_SERVICE_FRAGMENTS = {
    "Depends(",
    "from fastapi",
    "from sqlalchemy",
    "import sqlalchemy",
    "from invyra_platform.models",
    "from invyra_platform.db",
    "from invyra_platform.database",
    "from invyra_platform.api.dependencies",
    "from invyra_platform.api.v1.portal_dependencies",
    "from invyra_platform.api.v1.portal_adapters",
    "get_auth_runtime_service",
    "get_inventory_access_gateway_service",
    "get_inventory_launch_service",
    "AuthRuntimeService",
    "InventoryAccessGatewayService",
    "InventoryLaunchService",
    "ServiceResult.ok(",
    "ServiceResult.denied(",
    "ServiceResult.failed(",
    "commit(",
    "execute(",
    "query(",
    "add(",
    "delete(",
    "flush(",
}

FORBIDDEN_ROUTE_OR_PROVIDER_SERVICE_WIRING = {
    "PortalStatusService",
    "PortalSessionService",
    "PortalNavigationService",
    "PortalEntitlementService",
    "PortalInventoryEntryService",
    "portal.services",
}

RUNTIME_DATA_KEYS = {
    "authenticated",
    "session",
    "context",
    "token",
    "refresh_token",
    "access_token",
    "license",
    "entitlements",
    "groups",
    "entry_allowed",
    "launch_token",
    "launch_session",
    "stock",
    "stock_on_hand",
    "orders",
    "purchase_orders",
    "receiving",
    "transfers",
    "stocktake",
    "wastage",
    "markdowns",
    "sku",
    "quantity",
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


def _service_payloads() -> list[dict[str, Any]]:
    results = [
        PortalStatusService().get_status(),
        PortalSessionService().get_session(PortalSessionRequest()),
        PortalNavigationService().get_navigation(
            PortalNavigationRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
        ),
        PortalEntitlementService().get_entitlements(
            PortalEntitlementRequest(user_id="user-001", organisation_id="org-001", environment="TRAINING")
        ),
        PortalInventoryEntryService().get_inventory_entry(
            PortalInventoryEntryRequest(user_id="user-001", organisation_id="org-001", environment="TEST")
        ),
    ]

    payloads: list[dict[str, Any]] = []
    for result in results:
        assert result.data is not None
        payloads.append(result.data)
    return payloads


def test_portal_service_boundary_has_no_runtime_or_persistence_wiring() -> None:
    service_source = Path("src/invyra_platform/portal/services.py").read_text(encoding="utf-8")

    for fragment in FORBIDDEN_SERVICE_FRAGMENTS:
        assert fragment not in service_source


def test_portal_service_boundary_returns_not_implemented_only() -> None:
    service_source = Path("src/invyra_platform/portal/services.py").read_text(encoding="utf-8")

    assert "ServiceResult.not_implemented(" in service_source
    assert "ServiceResult.ok(" not in service_source
    assert "ServiceResult.denied(" not in service_source
    assert "ServiceResult.failed(" not in service_source


def test_portal_service_payloads_do_not_expose_runtime_data() -> None:
    for payload in _service_payloads():
        assert _iter_keys(payload).isdisjoint(RUNTIME_DATA_KEYS)
        assert payload["runtime"] == "not-implemented"


def test_portal_routes_are_not_wired_to_portal_services_in_sprint_20() -> None:
    route_source = Path("src/invyra_platform/api/v1/portal.py").read_text(encoding="utf-8")

    for fragment in FORBIDDEN_ROUTE_OR_PROVIDER_SERVICE_WIRING:
        assert fragment not in route_source


def test_portal_dependency_providers_are_not_wired_to_portal_services_in_sprint_20() -> None:
    provider_source = Path("src/invyra_platform/api/v1/portal_dependencies.py").read_text(encoding="utf-8")

    for fragment in FORBIDDEN_ROUTE_OR_PROVIDER_SERVICE_WIRING:
        assert fragment not in provider_source


def test_portal_service_boundary_sprint_does_not_introduce_new_portal_migrations() -> None:
    migration_versions_path = Path("migrations/versions")

    if not migration_versions_path.exists():
        return

    portal_migration_files = {
        path.name for path in migration_versions_path.glob("*.py") if "portal" in path.name.lower()
    }
    unexpected_portal_migrations = portal_migration_files - LOCKED_EXISTING_PORTAL_MIGRATIONS

    assert unexpected_portal_migrations == set()

"""Portal dependency provider boundary hardening tests."""

from pathlib import Path

from invyra_platform.api.v1 import portal_adapters, portal_dependencies

FORBIDDEN_PROVIDER_FRAGMENTS = {
    "Depends(",
    "from fastapi import Depends",
    "from sqlalchemy",
    "import sqlalchemy",
    "from invyra_platform.models",
    "from invyra_platform.db",
    "from invyra_platform.database",
    "from invyra_platform.api.dependencies",
    "from invyra_platform.services",
    "from invyra_platform.inventory",
    "from invyra_platform.inventory_launch",
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

FORBIDDEN_ROUTE_DEPENDENCY_FRAGMENTS = {
    "Depends(",
    "from fastapi import Depends",
    "portal_dependencies",
    "get_portal_status_adapter",
    "get_portal_session_adapter",
    "get_portal_navigation_adapter",
    "get_portal_entitlement_adapter",
    "get_portal_inventory_entry_adapter",
}

LOCKED_EXISTING_PORTAL_MIGRATIONS = {"008_portal_runtime_foundation.py"}


def test_portal_dependency_provider_module_has_no_runtime_or_persistence_wiring() -> None:
    provider_source = Path("src/invyra_platform/api/v1/portal_dependencies.py").read_text(encoding="utf-8")

    for fragment in FORBIDDEN_PROVIDER_FRAGMENTS:
        assert fragment not in provider_source


def test_portal_dependency_providers_return_adapter_references_without_invocation() -> None:
    provider_source = Path("src/invyra_platform/api/v1/portal_dependencies.py").read_text(encoding="utf-8")

    expected_reference_returns = {
        "return build_portal_status_result",
        "return build_portal_session_result",
        "return build_portal_navigation_result",
        "return build_portal_entitlement_result",
        "return build_portal_inventory_entry_result",
    }
    forbidden_invoked_returns = {
        "return build_portal_status_result(",
        "return build_portal_session_result(",
        "return build_portal_navigation_result(",
        "return build_portal_entitlement_result(",
        "return build_portal_inventory_entry_result(",
    }

    for expected_return in expected_reference_returns:
        assert expected_return in provider_source

    for forbidden_return in forbidden_invoked_returns:
        assert forbidden_return not in provider_source


def test_portal_dependency_providers_do_not_create_new_runtime_boundaries() -> None:
    assert portal_dependencies.get_portal_status_adapter() is portal_adapters.build_portal_status_result
    assert portal_dependencies.get_portal_session_adapter() is portal_adapters.build_portal_session_result
    assert portal_dependencies.get_portal_navigation_adapter() is portal_adapters.build_portal_navigation_result
    assert portal_dependencies.get_portal_entitlement_adapter() is portal_adapters.build_portal_entitlement_result
    assert portal_dependencies.get_portal_inventory_entry_adapter() is portal_adapters.build_portal_inventory_entry_result


def test_portal_routes_remain_direct_adapter_calls_for_sprint_19() -> None:
    route_source = Path("src/invyra_platform/api/v1/portal.py").read_text(encoding="utf-8")

    for fragment in FORBIDDEN_ROUTE_DEPENDENCY_FRAGMENTS:
        assert fragment not in route_source

    assert "build_portal_status_result()" in route_source
    assert "build_portal_session_result(request)" in route_source
    assert "build_portal_navigation_result(request)" in route_source
    assert "build_portal_entitlement_result(request)" in route_source
    assert "build_portal_inventory_entry_result(request)" in route_source


def test_portal_dependency_sprint_does_not_introduce_new_portal_migrations() -> None:
    migration_versions_path = Path("migrations/versions")

    if not migration_versions_path.exists():
        return

    portal_migration_files = {
        path.name for path in migration_versions_path.glob("*.py") if "portal" in path.name.lower()
    }
    unexpected_portal_migrations = portal_migration_files - LOCKED_EXISTING_PORTAL_MIGRATIONS

    assert unexpected_portal_migrations == set()

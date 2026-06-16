"""Portal dependency provider contract tests."""

from pathlib import Path

from invyra_platform.api.v1 import portal_adapters, portal_dependencies
from invyra_platform.core.service_results import ServiceResult
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest
from invyra_platform.portal.inventory_entry_contracts import PortalInventoryEntryRequest
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest
from invyra_platform.portal.session_contracts import PortalSessionRequest

EXPECTED_PROVIDER_NAMES = {
    "get_portal_status_adapter",
    "get_portal_session_adapter",
    "get_portal_navigation_adapter",
    "get_portal_entitlement_adapter",
    "get_portal_inventory_entry_adapter",
}

FORBIDDEN_PROVIDER_FRAGMENTS = {
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


def test_portal_dependency_provider_module_exists() -> None:
    provider_path = Path("src/invyra_platform/api/v1/portal_dependencies.py")

    assert provider_path.exists()


def test_all_expected_portal_dependency_providers_exist() -> None:
    for provider_name in EXPECTED_PROVIDER_NAMES:
        provider = getattr(portal_dependencies, provider_name)

        assert callable(provider)


def test_portal_dependency_providers_return_callable_adapter_boundaries() -> None:
    for provider_name in EXPECTED_PROVIDER_NAMES:
        provider = getattr(portal_dependencies, provider_name)
        adapter = provider()

        assert callable(adapter)


def test_portal_dependency_providers_return_existing_adapter_references() -> None:
    assert portal_dependencies.get_portal_status_adapter() is portal_adapters.build_portal_status_result
    assert portal_dependencies.get_portal_session_adapter() is portal_adapters.build_portal_session_result
    assert portal_dependencies.get_portal_navigation_adapter() is portal_adapters.build_portal_navigation_result
    assert portal_dependencies.get_portal_entitlement_adapter() is portal_adapters.build_portal_entitlement_result
    assert portal_dependencies.get_portal_inventory_entry_adapter() is portal_adapters.build_portal_inventory_entry_result


def test_portal_dependency_returned_adapters_preserve_service_result_contract() -> None:
    results = [
        portal_dependencies.get_portal_status_adapter()(),
        portal_dependencies.get_portal_session_adapter()(PortalSessionRequest()),
        portal_dependencies.get_portal_navigation_adapter()(
            PortalNavigationRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
        ),
        portal_dependencies.get_portal_entitlement_adapter()(
            PortalEntitlementRequest(user_id="user-001", organisation_id="org-001", environment="TRAINING")
        ),
        portal_dependencies.get_portal_inventory_entry_adapter()(
            PortalInventoryEntryRequest(user_id="user-001", organisation_id="org-001", environment="TEST")
        ),
    ]

    for result in results:
        assert isinstance(result, ServiceResult)
        assert result.success is False
        assert result.status == "NOT_IMPLEMENTED"
        assert result.reason == "SERVICE_SKELETON_ONLY"
        assert result.data is not None


def test_portal_dependency_provider_lookup_does_not_execute_adapter_results() -> None:
    status_adapter = portal_dependencies.get_portal_status_adapter()
    session_adapter = portal_dependencies.get_portal_session_adapter()
    navigation_adapter = portal_dependencies.get_portal_navigation_adapter()
    entitlement_adapter = portal_dependencies.get_portal_entitlement_adapter()
    inventory_entry_adapter = portal_dependencies.get_portal_inventory_entry_adapter()

    assert status_adapter is portal_adapters.build_portal_status_result
    assert session_adapter is portal_adapters.build_portal_session_result
    assert navigation_adapter is portal_adapters.build_portal_navigation_result
    assert entitlement_adapter is portal_adapters.build_portal_entitlement_result
    assert inventory_entry_adapter is portal_adapters.build_portal_inventory_entry_result


def test_portal_dependency_provider_module_has_no_runtime_service_or_persistence_dependencies() -> None:
    provider_source = Path("src/invyra_platform/api/v1/portal_dependencies.py").read_text(encoding="utf-8")

    for fragment in FORBIDDEN_PROVIDER_FRAGMENTS:
        assert fragment not in provider_source

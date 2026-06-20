"""Portal service boundary contract tests."""

from pathlib import Path

from invyra_platform.core.service_results import ServiceResult
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

EXPECTED_SERVICE_CLASSES = {
    "PortalStatusService",
    "PortalSessionService",
    "PortalNavigationService",
    "PortalEntitlementService",
    "PortalInventoryEntryService",
}

FORBIDDEN_SERVICE_FRAGMENTS = {
    "Depends(",
    "from fastapi",
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
    "ServiceResult.ok(",
    "ServiceResult.denied(",
    "ServiceResult.failed(",
    "commit(",
    "execute(",
    "query(",
}


def _service_results() -> list[ServiceResult]:
    return [
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


def test_portal_service_boundary_module_exists() -> None:
    service_path = Path("src/invyra_platform/portal/services.py")

    assert service_path.exists()


def test_all_expected_portal_service_classes_exist() -> None:
    import invyra_platform.portal.services as portal_services

    for service_class_name in EXPECTED_SERVICE_CLASSES:
        service_class = getattr(portal_services, service_class_name)

        assert isinstance(service_class(), service_class)


def test_portal_service_methods_exist() -> None:
    assert callable(PortalStatusService().get_status)
    assert callable(PortalSessionService().get_session)
    assert callable(PortalNavigationService().get_navigation)
    assert callable(PortalEntitlementService().get_entitlements)
    assert callable(PortalInventoryEntryService().get_inventory_entry)


def test_portal_service_methods_return_service_results() -> None:
    for result in _service_results():
        assert isinstance(result, ServiceResult)
        assert result.data is not None


def test_portal_service_methods_return_locked_skeleton_contract() -> None:
    for result in _service_results():
        assert result.success is False
        assert result.status == "NOT_IMPLEMENTED"
        assert result.reason == "SERVICE_SKELETON_ONLY"


def test_portal_service_methods_expose_boundary_skeleton_payloads_only() -> None:
    for result in _service_results():
        assert result.data is not None
        assert result.data["runtime"] == "not-implemented"
        assert "boundary" in result.data
        assert result.data["message"].endswith("service boundary skeleton only.")


def test_portal_service_boundary_has_no_runtime_success_path() -> None:
    service_source = Path("src/invyra_platform/portal/services.py").read_text(encoding="utf-8")

    for fragment in FORBIDDEN_SERVICE_FRAGMENTS:
        assert fragment not in service_source

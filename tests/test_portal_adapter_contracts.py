"""Portal adapter contract tests."""

from pathlib import Path

from invyra_platform.api.v1 import portal_adapters
from invyra_platform.core.service_results import ServiceResult
from invyra_platform.portal.entitlement_contracts import PortalEntitlementRequest
from invyra_platform.portal.inventory_entry_contracts import PortalInventoryEntryRequest
from invyra_platform.portal.navigation_contracts import PortalNavigationRequest
from invyra_platform.portal.session_contracts import PortalSessionRequest


def test_all_portal_adapter_builders_return_service_results() -> None:
    results = [
        portal_adapters.build_portal_status_result(),
        portal_adapters.build_portal_session_result(PortalSessionRequest()),
        portal_adapters.build_portal_navigation_result(
            PortalNavigationRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
        ),
        portal_adapters.build_portal_entitlement_result(
            PortalEntitlementRequest(user_id="user-001", organisation_id="org-001", environment="TRAINING")
        ),
        portal_adapters.build_portal_inventory_entry_result(
            PortalInventoryEntryRequest(user_id="user-001", organisation_id="org-001", environment="TEST")
        ),
    ]

    for result in results:
        assert isinstance(result, ServiceResult)
        assert result.success is False
        assert result.status == "NOT_IMPLEMENTED"
        assert result.reason == "SERVICE_SKELETON_ONLY"
        assert result.data is not None


def test_portal_adapters_preserve_environment_contracts() -> None:
    navigation = portal_adapters.build_portal_navigation_result(
        PortalNavigationRequest(user_id="user-001", organisation_id="org-001", environment="TRAINING")
    )
    entitlement = portal_adapters.build_portal_entitlement_result(
        PortalEntitlementRequest(user_id="user-001", organisation_id="org-001", environment="TEST")
    )
    inventory_entry = portal_adapters.build_portal_inventory_entry_result(
        PortalInventoryEntryRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
    )

    assert navigation.data is not None
    assert entitlement.data is not None
    assert inventory_entry.data is not None
    assert navigation.data["environment"] == "TRAINING"
    assert entitlement.data["environment"] == "TEST"
    assert inventory_entry.data["environment"] == "LIVE"
    assert inventory_entry.data["entry"]["environment"] == "LIVE"


def test_portal_session_adapter_remains_unauthenticated() -> None:
    result = portal_adapters.build_portal_session_result(PortalSessionRequest())

    assert result.data is not None
    assert result.data["authenticated"] is False
    assert result.data["session"] is None
    assert result.data["context"] is None
    assert result.data["message"] == "Portal session boundary skeleton only."


def test_portal_navigation_adapter_remains_empty() -> None:
    result = portal_adapters.build_portal_navigation_result(
        PortalNavigationRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
    )

    assert result.data is not None
    assert result.data["sections"] == []
    assert result.data["message"] == "Portal navigation boundary skeleton only."


def test_portal_entitlement_adapter_remains_empty() -> None:
    result = portal_adapters.build_portal_entitlement_result(
        PortalEntitlementRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
    )

    assert result.data is not None
    assert result.data["groups"] == []
    assert result.data["message"] == "Portal entitlement boundary skeleton only."


def test_portal_inventory_entry_adapter_remains_disabled() -> None:
    result = portal_adapters.build_portal_inventory_entry_result(
        PortalInventoryEntryRequest(user_id="user-001", organisation_id="org-001", environment="LIVE")
    )

    assert result.data is not None
    entry = result.data["entry"]
    assert entry["visible"] is False
    assert entry["enabled"] is False
    assert entry["entry_allowed"] is False
    assert entry["availability"]["allowed"] is False
    assert entry["availability"]["target_key"] is None
    assert entry["availability"]["evaluation_id"] is None


def test_portal_adapter_module_remains_implementation_free() -> None:
    adapter_source = Path("src/invyra_platform/api/v1/portal_adapters.py").read_text(encoding="utf-8")

    forbidden_fragments = [
        "Depends(",
        "from sqlalchemy",
        "import sqlalchemy",
        "from invyra_platform.models",
        "from invyra_platform.db",
        "from invyra_platform.database",
        "get_auth_runtime_service",
        "get_inventory_access_gateway_service",
        "get_inventory_launch_service",
        "create_",
        "commit(",
        "execute(",
        "query(",
    ]

    for fragment in forbidden_fragments:
        assert fragment not in adapter_source

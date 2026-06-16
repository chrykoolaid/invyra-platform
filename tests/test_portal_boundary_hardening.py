"""Portal boundary hardening tests for the full Sprint 16 contract line."""

from importlib import import_module
from types import ModuleType

import pytest
from pydantic import ValidationError

from invyra_platform.portal.contracts import (
    PortalCommercialStatus,
    PortalEnvironment,
    PortalEnvironmentDTO,
    PortalModuleCode,
    PortalModuleDTO,
    PortalOrganisationDTO,
    PortalUserDTO,
)
from invyra_platform.portal.entitlement_contracts import (
    PortalEntitlementDTO,
    PortalEntitlementStatus,
)
from invyra_platform.portal.inventory_entry_contracts import (
    PortalInventoryEntryDTO,
    PortalInventoryEntryStatus,
    PortalInventoryLaunchAvailabilityDTO,
)
from invyra_platform.portal.navigation_contracts import (
    PortalNavigationItemDTO,
    PortalNavigationItemStatus,
    PortalNavigationItemType,
)
from invyra_platform.portal.session_contracts import (
    PortalSessionContextDTO,
    PortalSessionDTO,
    PortalSessionResponse,
    PortalSessionStatus,
)

PORTAL_CONTRACT_MODULES = (
    "invyra_platform.portal.contracts",
    "invyra_platform.portal.session_contracts",
    "invyra_platform.portal.navigation_contracts",
    "invyra_platform.portal.inventory_entry_contracts",
    "invyra_platform.portal.entitlement_contracts",
)

FORBIDDEN_CONTRACT_SOURCE_FRAGMENTS = (
    "fastapi",
    "sqlalchemy",
    "invyra_platform.db",
    "invyra_platform.auth.service",
    "invyra_platform.inventory_access.service",
    "invyra_platform.inventory_launch.service",
    "APIRouter",
    "Depends(",
    "mapped_column",
)


def test_all_portal_contract_modules_import_cleanly() -> None:
    imported_modules = [import_module(module_name) for module_name in PORTAL_CONTRACT_MODULES]

    assert all(isinstance(module, ModuleType) for module in imported_modules)


def test_portal_contract_modules_do_not_depend_on_runtime_layers() -> None:
    for module_name in PORTAL_CONTRACT_MODULES:
        module = import_module(module_name)
        module_file = getattr(module, "__file__", None)
        assert module_file is not None
        source = open(module_file, encoding="utf-8").read()

        for forbidden_fragment in FORBIDDEN_CONTRACT_SOURCE_FRAGMENTS:
            assert forbidden_fragment not in source


def test_inventory_first_portal_contracts_compose_consistently() -> None:
    user = PortalUserDTO(user_id="user-001", email="operator@example.com")
    organisation = PortalOrganisationDTO(organisation_id="org-001", name="Invyra Demo")
    environment = PortalEnvironmentDTO(environment=PortalEnvironment.LIVE, is_selected=True)
    session = PortalSessionDTO(
        session_id="portal-session-001",
        status=PortalSessionStatus.ACTIVE,
        authenticated=True,
        user_id=user.user_id,
        organisation_id=organisation.organisation_id,
        environment=PortalEnvironment.LIVE,
    )
    session_response = PortalSessionResponse(
        authenticated=True,
        session=session,
        context=PortalSessionContextDTO(user=user, organisation=organisation, environment=environment),
    )
    entitlement = PortalEntitlementDTO(
        module_code=PortalModuleCode.INVENTORY,
        display_name="Invyra Inventory",
        commercial_status=PortalCommercialStatus.AVAILABLE,
        status=PortalEntitlementStatus.ENTITLED,
        visible=True,
        entitled=True,
        available=True,
        launch_allowed=True,
    )
    navigation_item = PortalNavigationItemDTO(
        item_id="nav-inventory",
        label="Inventory",
        item_type=PortalNavigationItemType.MODULE,
        status=PortalNavigationItemStatus.AVAILABLE,
        visible=True,
        enabled=True,
        module_code=PortalModuleCode.INVENTORY,
        commercial_status=PortalCommercialStatus.AVAILABLE,
        target_key="inventory",
    )
    launch_availability = PortalInventoryLaunchAvailabilityDTO(
        allowed=True,
        status=PortalInventoryEntryStatus.AVAILABLE,
        action_label="Open Inventory",
        target_key="inventory",
    )
    inventory_entry = PortalInventoryEntryDTO(
        status=PortalInventoryEntryStatus.AVAILABLE,
        visible=True,
        enabled=True,
        entry_allowed=True,
        environment=PortalEnvironment.LIVE,
        availability=launch_availability,
    )

    assert session_response.authenticated is True
    assert entitlement.launch_allowed is True
    assert navigation_item.enabled is True
    assert inventory_entry.entry_allowed is True
    assert inventory_entry.availability.allowed is True


def test_future_modules_remain_locked_across_portal_contracts() -> None:
    with pytest.raises(ValidationError):
        PortalModuleDTO(
            module_code=PortalModuleCode.CRM,
            display_name="CRM",
            commercial_status=PortalCommercialStatus.FUTURE,
            visible=True,
            available=True,
        )

    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.POS,
            display_name="POS",
            commercial_status=PortalCommercialStatus.FUTURE,
            status=PortalEntitlementStatus.ENTITLED,
            visible=True,
            entitled=True,
        )

    with pytest.raises(ValidationError):
        PortalNavigationItemDTO(
            item_id="nav-forecasting",
            label="Forecasting",
            item_type=PortalNavigationItemType.MODULE,
            status=PortalNavigationItemStatus.AVAILABLE,
            visible=True,
            enabled=True,
            module_code=PortalModuleCode.FORECASTING,
            commercial_status=PortalCommercialStatus.FUTURE,
            target_key="forecasting",
        )


def test_portal_boundary_rejects_inventory_runtime_payload_fields() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryEntryDTO(
            status=PortalInventoryEntryStatus.DISABLED,
            environment=PortalEnvironment.LIVE,
            inventory_items=[],
        )


def test_portal_boundary_rejects_ui_payload_fields() -> None:
    with pytest.raises(ValidationError):
        PortalNavigationItemDTO(
            item_id="nav-ui",
            label="UI",
            item_type=PortalNavigationItemType.PAGE,
            component="SidebarItem",
        )

"""Portal navigation contract tests."""

import pytest
from pydantic import ValidationError

from invyra_platform.portal.contracts import PortalCommercialStatus, PortalEnvironment, PortalModuleCode
from invyra_platform.portal.navigation_contracts import (
    PortalNavigationItemDTO,
    PortalNavigationItemStatus,
    PortalNavigationItemType,
    PortalNavigationRequest,
    PortalNavigationResponse,
    PortalNavigationSectionCode,
    PortalNavigationSectionDTO,
)


def test_navigation_request_accepts_context() -> None:
    request = PortalNavigationRequest(
        user_id="user-001",
        organisation_id="org-001",
        session_id="portal-session-001",
        environment=PortalEnvironment.LIVE,
        include_hidden=False,
        trace_id="trace-001",
    )

    assert request.user_id == "user-001"
    assert request.organisation_id == "org-001"
    assert request.environment == PortalEnvironment.LIVE


def test_navigation_request_restricts_environment_codes() -> None:
    with pytest.raises(ValidationError):
        PortalNavigationRequest(user_id="user-001", organisation_id="org-001", environment="DEMO")


def test_inventory_navigation_item_can_be_enabled() -> None:
    item = PortalNavigationItemDTO(
        item_id="nav-inventory",
        label="Inventory",
        item_type=PortalNavigationItemType.MODULE,
        status=PortalNavigationItemStatus.AVAILABLE,
        visible=True,
        enabled=True,
        module_code=PortalModuleCode.INVENTORY,
        commercial_status=PortalCommercialStatus.AVAILABLE,
        target_key="inventory",
        required_permissions=["inventory.launch"],
        sort_order=1,
    )

    assert item.enabled is True
    assert item.visible is True
    assert item.module_code == PortalModuleCode.INVENTORY


def test_enabled_navigation_item_must_be_visible() -> None:
    with pytest.raises(ValidationError):
        PortalNavigationItemDTO(
            item_id="nav-inventory",
            label="Inventory",
            status=PortalNavigationItemStatus.AVAILABLE,
            enabled=True,
            target_key="inventory",
        )


def test_enabled_navigation_item_requires_available_status() -> None:
    with pytest.raises(ValidationError):
        PortalNavigationItemDTO(
            item_id="nav-admin",
            label="Admin",
            status=PortalNavigationItemStatus.DISABLED,
            visible=True,
            enabled=True,
            target_key="admin",
        )


def test_enabled_navigation_item_requires_target_key() -> None:
    with pytest.raises(ValidationError):
        PortalNavigationItemDTO(
            item_id="nav-inventory",
            label="Inventory",
            status=PortalNavigationItemStatus.AVAILABLE,
            visible=True,
            enabled=True,
        )


def test_future_module_navigation_item_cannot_be_enabled() -> None:
    with pytest.raises(ValidationError):
        PortalNavigationItemDTO(
            item_id="nav-crm",
            label="CRM",
            item_type=PortalNavigationItemType.MODULE,
            status=PortalNavigationItemStatus.AVAILABLE,
            visible=True,
            enabled=True,
            module_code=PortalModuleCode.CRM,
            commercial_status=PortalCommercialStatus.FUTURE,
            target_key="crm",
        )


def test_locked_module_navigation_item_can_be_visible_but_disabled() -> None:
    item = PortalNavigationItemDTO(
        item_id="nav-pos",
        label="POS",
        item_type=PortalNavigationItemType.MODULE,
        status=PortalNavigationItemStatus.FUTURE,
        visible=True,
        enabled=False,
        module_code=PortalModuleCode.POS,
        commercial_status=PortalCommercialStatus.NOT_COMMERCIALLY_AVAILABLE,
        reason="Future module.",
        sort_order=2,
    )

    assert item.visible is True
    assert item.enabled is False
    assert item.status == PortalNavigationItemStatus.FUTURE


def test_hidden_navigation_item_cannot_be_visible() -> None:
    with pytest.raises(ValidationError):
        PortalNavigationItemDTO(
            item_id="nav-hidden",
            label="Hidden",
            status=PortalNavigationItemStatus.HIDDEN,
            visible=True,
        )


def test_navigation_section_accepts_items() -> None:
    item = PortalNavigationItemDTO(
        item_id="nav-inventory",
        label="Inventory",
        status=PortalNavigationItemStatus.AVAILABLE,
        visible=True,
        enabled=True,
        module_code=PortalModuleCode.INVENTORY,
        commercial_status=PortalCommercialStatus.AVAILABLE,
        target_key="inventory",
    )
    section = PortalNavigationSectionDTO(
        section_id="section-operations",
        code=PortalNavigationSectionCode.OPERATIONS,
        label="Operations",
        visible=True,
        items=[item],
        sort_order=1,
    )

    assert section.items == [item]
    assert section.code == PortalNavigationSectionCode.OPERATIONS


def test_hidden_navigation_section_cannot_contain_visible_items() -> None:
    item = PortalNavigationItemDTO(
        item_id="nav-inventory",
        label="Inventory",
        status=PortalNavigationItemStatus.AVAILABLE,
        visible=True,
        enabled=True,
        module_code=PortalModuleCode.INVENTORY,
        commercial_status=PortalCommercialStatus.AVAILABLE,
        target_key="inventory",
    )

    with pytest.raises(ValidationError):
        PortalNavigationSectionDTO(
            section_id="section-hidden",
            code=PortalNavigationSectionCode.PRIMARY,
            label="Hidden Section",
            visible=False,
            items=[item],
        )


def test_navigation_response_accepts_sections() -> None:
    section = PortalNavigationSectionDTO(
        section_id="section-support",
        code=PortalNavigationSectionCode.SUPPORT,
        label="Support",
    )
    response = PortalNavigationResponse(environment=PortalEnvironment.TRAINING, sections=[section])

    assert response.environment == PortalEnvironment.TRAINING
    assert response.sections == [section]


def test_navigation_contracts_forbid_ui_fields() -> None:
    with pytest.raises(ValidationError):
        PortalNavigationItemDTO(item_id="nav-ui", label="UI", component_name="SidebarItem")

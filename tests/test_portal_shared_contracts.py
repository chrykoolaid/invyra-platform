"""Shared portal contract DTO tests."""

import pytest
from pydantic import ValidationError

from invyra_platform.portal.contracts import (
    PortalCommercialStatus,
    PortalDeviceDTO,
    PortalEnvironment,
    PortalEnvironmentDTO,
    PortalModuleCode,
    PortalModuleDTO,
    PortalOrganisationDTO,
    PortalPermissionDTO,
    PortalPermissionScope,
    PortalUserDTO,
)


def test_portal_user_dto_accepts_safe_identity_summary() -> None:
    user = PortalUserDTO(
        user_id="user-001",
        email="operator@example.com",
        display_name="Operator",
        roles=["manager"],
        permissions=["inventory.launch"],
    )

    assert user.user_id == "user-001"
    assert user.email == "operator@example.com"
    assert user.roles == ["manager"]
    assert user.permissions == ["inventory.launch"]


def test_portal_organisation_dto_requires_identity_and_name() -> None:
    organisation = PortalOrganisationDTO(
        organisation_id="org-001",
        name="Invyra Demo",
        slug="invyra-demo",
        membership_role="owner",
    )

    assert organisation.organisation_id == "org-001"
    assert organisation.name == "Invyra Demo"

    with pytest.raises(ValidationError):
        PortalOrganisationDTO(organisation_id="", name="Invyra Demo")


def test_portal_environment_dto_restricts_environment_codes() -> None:
    environment = PortalEnvironmentDTO(environment=PortalEnvironment.LIVE, is_selected=True)

    assert environment.environment == PortalEnvironment.LIVE
    assert environment.is_selected is True

    with pytest.raises(ValidationError):
        PortalEnvironmentDTO(environment="DEMO")


def test_portal_device_dto_defaults_to_untrusted_unregistered() -> None:
    device = PortalDeviceDTO(device_id="device-001")

    assert device.device_id == "device-001"
    assert device.trusted is False
    assert device.registered is False


def test_portal_permission_dto_defaults_to_not_granted() -> None:
    permission = PortalPermissionDTO(permission_code="inventory.launch", scope=PortalPermissionScope.INVENTORY)

    assert permission.scope == PortalPermissionScope.INVENTORY
    assert permission.granted is False


def test_inventory_module_can_be_available_for_portal_boundary() -> None:
    module = PortalModuleDTO(
        module_code=PortalModuleCode.INVENTORY,
        display_name="Invyra Inventory",
        commercial_status=PortalCommercialStatus.AVAILABLE,
        visible=True,
        available=True,
        launch_allowed=True,
        route_key="inventory",
    )

    assert module.module_code == PortalModuleCode.INVENTORY
    assert module.available is True
    assert module.launch_allowed is True


def test_future_module_cannot_be_marked_available() -> None:
    with pytest.raises(ValidationError):
        PortalModuleDTO(
            module_code=PortalModuleCode.CRM,
            display_name="CRM",
            commercial_status=PortalCommercialStatus.FUTURE,
            visible=True,
            available=True,
        )


def test_future_module_cannot_be_launch_allowed() -> None:
    with pytest.raises(ValidationError):
        PortalModuleDTO(
            module_code=PortalModuleCode.POS,
            display_name="POS",
            commercial_status=PortalCommercialStatus.NOT_COMMERCIALLY_AVAILABLE,
            visible=True,
            launch_allowed=True,
        )


def test_portal_contracts_forbid_extra_fields() -> None:
    with pytest.raises(ValidationError):
        PortalEnvironmentDTO(environment=PortalEnvironment.TEST, ui_component="dashboard")

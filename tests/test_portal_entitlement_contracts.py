"""Portal entitlement contract tests."""

import pytest
from pydantic import ValidationError

from invyra_platform.portal.contracts import PortalCommercialStatus, PortalEnvironment, PortalModuleCode
from invyra_platform.portal.entitlement_contracts import (
    PortalEntitlementDTO,
    PortalEntitlementGroupDTO,
    PortalEntitlementRequest,
    PortalEntitlementResponse,
    PortalEntitlementStatus,
)


def test_entitlement_request_accepts_context() -> None:
    request = PortalEntitlementRequest(
        user_id="user-001",
        organisation_id="org-001",
        session_id="portal-session-001",
        environment=PortalEnvironment.LIVE,
        include_future_modules=True,
        trace_id="trace-001",
    )

    assert request.user_id == "user-001"
    assert request.organisation_id == "org-001"
    assert request.environment == PortalEnvironment.LIVE


def test_entitlement_request_restricts_environment_codes() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementRequest(user_id="user-001", organisation_id="org-001", environment="DEMO")


def test_inventory_entitlement_can_be_available_and_launch_allowed() -> None:
    entitlement = PortalEntitlementDTO(
        module_code=PortalModuleCode.INVENTORY,
        display_name="Invyra Inventory",
        commercial_status=PortalCommercialStatus.AVAILABLE,
        status=PortalEntitlementStatus.ENTITLED,
        visible=True,
        entitled=True,
        available=True,
        launch_allowed=True,
        license_id="license-001",
        entitlement_id="entitlement-001",
        required_permissions=["inventory.launch"],
        sort_order=1,
    )

    assert entitlement.module_code == PortalModuleCode.INVENTORY
    assert entitlement.entitled is True
    assert entitlement.available is True
    assert entitlement.launch_allowed is True


def test_launch_allowed_requires_available_entitlement() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.INVENTORY,
            display_name="Invyra Inventory",
            commercial_status=PortalCommercialStatus.AVAILABLE,
            status=PortalEntitlementStatus.ENTITLED,
            visible=True,
            entitled=True,
            available=False,
            launch_allowed=True,
        )


def test_available_entitlement_requires_entitled_state() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.INVENTORY,
            display_name="Invyra Inventory",
            commercial_status=PortalCommercialStatus.AVAILABLE,
            status=PortalEntitlementStatus.NOT_ENTITLED,
            visible=True,
            entitled=False,
            available=True,
        )


def test_entitled_module_requires_entitled_status() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.INVENTORY,
            display_name="Invyra Inventory",
            commercial_status=PortalCommercialStatus.AVAILABLE,
            status=PortalEntitlementStatus.UNKNOWN,
            visible=True,
            entitled=True,
        )


def test_runtime_enabled_entitlement_requires_commercial_availability() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.INVENTORY,
            display_name="Invyra Inventory",
            commercial_status=PortalCommercialStatus.NOT_COMMERCIALLY_AVAILABLE,
            status=PortalEntitlementStatus.ENTITLED,
            visible=True,
            entitled=True,
            available=True,
        )


def test_future_module_cannot_be_available() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.CRM,
            display_name="CRM",
            commercial_status=PortalCommercialStatus.FUTURE,
            status=PortalEntitlementStatus.ENTITLED,
            visible=True,
            entitled=True,
            available=True,
        )


def test_future_module_cannot_be_launch_allowed() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.POS,
            display_name="POS",
            commercial_status=PortalCommercialStatus.NOT_COMMERCIALLY_AVAILABLE,
            status=PortalEntitlementStatus.ENTITLED,
            visible=True,
            entitled=True,
            available=True,
            launch_allowed=True,
        )


def test_future_module_cannot_be_marked_entitled() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.FORECASTING,
            display_name="Forecasting",
            commercial_status=PortalCommercialStatus.FUTURE,
            status=PortalEntitlementStatus.ENTITLED,
            visible=True,
            entitled=True,
        )


def test_future_module_can_be_visible_but_locked() -> None:
    entitlement = PortalEntitlementDTO(
        module_code=PortalModuleCode.PURCHASING_EXTENSIONS,
        display_name="Purchasing Extensions",
        commercial_status=PortalCommercialStatus.FUTURE,
        status=PortalEntitlementStatus.FUTURE,
        visible=True,
        entitled=False,
        available=False,
        launch_allowed=False,
        reasons=["Future module."],
        sort_order=4,
    )

    assert entitlement.visible is True
    assert entitlement.entitled is False
    assert entitlement.available is False
    assert entitlement.launch_allowed is False


def test_entitlement_group_accepts_entitlements() -> None:
    entitlement = PortalEntitlementDTO(
        module_code=PortalModuleCode.INVENTORY,
        display_name="Invyra Inventory",
        commercial_status=PortalCommercialStatus.AVAILABLE,
        status=PortalEntitlementStatus.ENTITLED,
        visible=True,
        entitled=True,
        available=True,
    )
    group = PortalEntitlementGroupDTO(group_id="group-products", label="Products", entitlements=[entitlement])

    assert group.entitlements == [entitlement]
    assert group.label == "Products"


def test_entitlement_response_accepts_groups() -> None:
    group = PortalEntitlementGroupDTO(group_id="group-products", label="Products")
    response = PortalEntitlementResponse(environment=PortalEnvironment.TRAINING, groups=[group])

    assert response.environment == PortalEnvironment.TRAINING
    assert response.groups == [group]


def test_entitlement_contracts_forbid_billing_execution_fields() -> None:
    with pytest.raises(ValidationError):
        PortalEntitlementDTO(
            module_code=PortalModuleCode.INVENTORY,
            display_name="Invyra Inventory",
            commercial_status=PortalCommercialStatus.AVAILABLE,
            status=PortalEntitlementStatus.UNKNOWN,
            invoice_total=100,
        )

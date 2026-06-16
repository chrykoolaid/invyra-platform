"""Portal Inventory entry contract tests."""

import pytest
from pydantic import ValidationError

from invyra_platform.portal.contracts import PortalCommercialStatus, PortalEnvironment, PortalModuleCode
from invyra_platform.portal.inventory_entry_contracts import (
    PortalInventoryEntryDTO,
    PortalInventoryEntryRequest,
    PortalInventoryEntryResponse,
    PortalInventoryEntryStatus,
    PortalInventoryLaunchAvailabilityDTO,
)


def test_inventory_entry_request_accepts_context() -> None:
    request = PortalInventoryEntryRequest(
        user_id="user-001",
        organisation_id="org-001",
        session_id="portal-session-001",
        device_id="device-001",
        environment=PortalEnvironment.LIVE,
        trace_id="trace-001",
    )

    assert request.user_id == "user-001"
    assert request.organisation_id == "org-001"
    assert request.environment == PortalEnvironment.LIVE


def test_inventory_entry_request_restricts_environment_codes() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryEntryRequest(user_id="user-001", organisation_id="org-001", environment="DEMO")


def test_launch_availability_accepts_allowed_shape() -> None:
    availability = PortalInventoryLaunchAvailabilityDTO(
        allowed=True,
        status=PortalInventoryEntryStatus.AVAILABLE,
        action_label="Open Inventory",
        target_key="inventory",
        evaluation_id="eval-001",
    )

    assert availability.allowed is True
    assert availability.status == PortalInventoryEntryStatus.AVAILABLE
    assert availability.target_key == "inventory"


def test_launch_availability_requires_available_status_when_allowed() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryLaunchAvailabilityDTO(
            allowed=True,
            status=PortalInventoryEntryStatus.DENIED,
            action_label="Open Inventory",
            target_key="inventory",
        )


def test_launch_availability_requires_target_key_when_allowed() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryLaunchAvailabilityDTO(
            allowed=True,
            status=PortalInventoryEntryStatus.AVAILABLE,
            action_label="Open Inventory",
        )


def test_launch_availability_requires_action_label_when_allowed() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryLaunchAvailabilityDTO(
            allowed=True,
            status=PortalInventoryEntryStatus.AVAILABLE,
            target_key="inventory",
        )


def test_inventory_entry_accepts_available_entry_shape() -> None:
    availability = PortalInventoryLaunchAvailabilityDTO(
        allowed=True,
        status=PortalInventoryEntryStatus.AVAILABLE,
        action_label="Open Inventory",
        target_key="inventory",
        evaluation_id="eval-001",
    )
    entry = PortalInventoryEntryDTO(
        status=PortalInventoryEntryStatus.AVAILABLE,
        visible=True,
        enabled=True,
        entry_allowed=True,
        environment=PortalEnvironment.TRAINING,
        required_permissions=["inventory.launch"],
        availability=availability,
    )

    assert entry.module_code == PortalModuleCode.INVENTORY
    assert entry.commercial_status == PortalCommercialStatus.AVAILABLE
    assert entry.entry_allowed is True
    assert entry.availability.allowed is True


def test_inventory_entry_rejects_non_inventory_module_code() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryEntryDTO(
            module_code=PortalModuleCode.CRM,
            status=PortalInventoryEntryStatus.DISABLED,
            environment=PortalEnvironment.LIVE,
        )


def test_enabled_inventory_entry_must_be_visible() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryEntryDTO(
            status=PortalInventoryEntryStatus.AVAILABLE,
            enabled=True,
            environment=PortalEnvironment.LIVE,
        )


def test_entry_allowed_requires_enabled_state() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryEntryDTO(
            status=PortalInventoryEntryStatus.AVAILABLE,
            visible=True,
            entry_allowed=True,
            environment=PortalEnvironment.LIVE,
        )


def test_entry_allowed_requires_available_status() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryEntryDTO(
            status=PortalInventoryEntryStatus.DENIED,
            visible=True,
            enabled=True,
            entry_allowed=True,
            environment=PortalEnvironment.LIVE,
        )


def test_entry_allowed_requires_commercial_availability() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryEntryDTO(
            commercial_status=PortalCommercialStatus.NOT_COMMERCIALLY_AVAILABLE,
            status=PortalInventoryEntryStatus.AVAILABLE,
            visible=True,
            enabled=True,
            entry_allowed=True,
            environment=PortalEnvironment.LIVE,
        )


def test_launch_availability_requires_entry_allowed() -> None:
    availability = PortalInventoryLaunchAvailabilityDTO(
        allowed=True,
        status=PortalInventoryEntryStatus.AVAILABLE,
        action_label="Open Inventory",
        target_key="inventory",
    )

    with pytest.raises(ValidationError):
        PortalInventoryEntryDTO(
            status=PortalInventoryEntryStatus.AVAILABLE,
            visible=True,
            enabled=True,
            entry_allowed=False,
            environment=PortalEnvironment.LIVE,
            availability=availability,
        )


def test_inventory_entry_response_accepts_entry() -> None:
    entry = PortalInventoryEntryDTO(
        status=PortalInventoryEntryStatus.DISABLED,
        visible=True,
        enabled=False,
        entry_allowed=False,
        environment=PortalEnvironment.TEST,
        reason="Access evaluation pending.",
    )
    response = PortalInventoryEntryResponse(environment=PortalEnvironment.TEST, entry=entry)

    assert response.environment == PortalEnvironment.TEST
    assert response.entry is entry


def test_inventory_entry_contracts_forbid_runtime_data_fields() -> None:
    with pytest.raises(ValidationError):
        PortalInventoryEntryDTO(
            status=PortalInventoryEntryStatus.DISABLED,
            environment=PortalEnvironment.LIVE,
            stock_on_hand=100,
        )

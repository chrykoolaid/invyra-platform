"""Devices foundation tests."""

from invyra_platform.db.base import Base
from invyra_platform.devices.models import Device, DeviceAssignment, DeviceEvent, DeviceSession


def test_device_tables_registered_in_metadata() -> None:
    expected_tables = {
        "devices",
        "device_assignments",
        "device_sessions",
        "device_events",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_device_is_tenant_scoped() -> None:
    columns = Device.__table__.columns
    assert columns["organisation_id"].nullable is False


def test_device_stores_fingerprint_hash_not_raw_fingerprint() -> None:
    columns = Device.__table__.columns
    assert "device_fingerprint_hash" in columns
    assert "device_fingerprint" not in columns
    assert columns["device_fingerprint_hash"].nullable is False


def test_device_fingerprint_hash_unique_constraint_exists() -> None:
    constraints = {constraint.name for constraint in Device.__table__.constraints}
    assert "uq_devices_device_fingerprint_hash" in constraints


def test_device_assignment_is_tenant_and_device_scoped() -> None:
    columns = DeviceAssignment.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["device_id"].nullable is False


def test_device_session_is_tenant_and_device_scoped() -> None:
    columns = DeviceSession.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["device_id"].nullable is False


def test_device_event_is_tenant_and_device_scoped() -> None:
    columns = DeviceEvent.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["device_id"].nullable is False

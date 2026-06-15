"""Inventory launch foundation tests."""

from invyra_platform.db.base import Base
from invyra_platform.inventory_launch.models import (
    InventoryLaunchAttempt,
    InventoryLaunchEvent,
    InventoryLaunchSession,
    InventoryLaunchToken,
)


def test_inventory_launch_tables_registered_in_metadata() -> None:
    expected_tables = {
        "inventory_launch_attempts",
        "inventory_launch_tokens",
        "inventory_launch_sessions",
        "inventory_launch_events",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_inventory_launch_attempt_is_tenant_user_environment_scoped() -> None:
    columns = InventoryLaunchAttempt.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["environment"].nullable is False
    assert columns["requested_product"].default.arg == "inventory"


def test_inventory_launch_token_stores_hash_only() -> None:
    columns = InventoryLaunchToken.__table__.columns
    assert "token_hash" in columns
    assert "raw_token" not in columns
    assert columns["token_hash"].nullable is False
    assert columns["expires_at"].nullable is False
    assert columns["attempt_id"].nullable is False


def test_inventory_launch_session_requires_attempt_token_and_expiry() -> None:
    columns = InventoryLaunchSession.__table__.columns
    assert columns["attempt_id"].nullable is False
    assert columns["token_id"].nullable is False
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["environment"].nullable is False
    assert columns["expires_at"].nullable is False


def test_inventory_launch_events_attach_to_lifecycle() -> None:
    columns = InventoryLaunchEvent.__table__.columns
    assert columns["attempt_id"].nullable is False
    assert columns["token_id"].nullable is True
    assert columns["session_id"].nullable is True
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["environment"].nullable is False
    assert columns["event_type"].nullable is False
    assert columns["event_status"].nullable is False

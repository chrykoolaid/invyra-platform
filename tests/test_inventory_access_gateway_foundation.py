"""Inventory access gateway foundation tests."""

from invyra_platform.db.base import Base
from invyra_platform.inventory_access.models import InventoryAccessEvaluation, InventoryAccessEvent


def test_inventory_access_tables_registered_in_metadata() -> None:
    expected_tables = {
        "inventory_access_evaluations",
        "inventory_access_events",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_inventory_access_evaluation_required_scope() -> None:
    columns = InventoryAccessEvaluation.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["environment"].nullable is False
    assert columns["product_code"].nullable is False
    assert columns["result"].nullable is False


def test_inventory_access_evaluation_nullable_resolution_boundary() -> None:
    columns = InventoryAccessEvaluation.__table__.columns
    assert columns["failure_reason"].nullable is True
    assert columns["license_id"].nullable is True
    assert columns["entitlement_id"].nullable is True
    assert columns["auth_session_id"].nullable is True


def test_inventory_access_event_required_scope() -> None:
    columns = InventoryAccessEvent.__table__.columns
    assert columns["evaluation_id"].nullable is False
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["environment"].nullable is False
    assert columns["event_type"].nullable is False
    assert columns["event_status"].nullable is False


def test_inventory_access_event_nullable_metadata_boundary() -> None:
    columns = InventoryAccessEvent.__table__.columns
    assert columns["message"].nullable is True
    assert columns["metadata_json"].nullable is True


def test_inventory_access_relationships_exist() -> None:
    assert hasattr(InventoryAccessEvaluation, "events")
    assert hasattr(InventoryAccessEvent, "evaluation")


def test_inventory_access_gateway_is_product_and_environment_scoped() -> None:
    columns = InventoryAccessEvaluation.__table__.columns
    assert "product_code" in columns
    assert "environment" in columns
    assert columns["environment"].default is None


def test_inventory_access_gateway_does_not_add_inventory_operational_tables() -> None:
    forbidden_tables = {
        "inventory_items",
        "stock",
        "receiving",
        "transfers",
        "stocktakes",
        "wastage",
        "reports",
        "forecasting",
        "crm",
        "pos",
    }

    assert forbidden_tables.isdisjoint(Base.metadata.tables.keys())

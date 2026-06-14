"""Licensing foundation tests."""

from invyra_platform.core.constants import AVAILABLE_COMMERCIAL_PRODUCT, FUTURE_MODULE_CODES
from invyra_platform.db.base import Base
from invyra_platform.licensing.models import (
    License,
    LicenseEntitlement,
    LicenseEvent,
    LicenseProduct,
    LicenseSeat,
)


def test_licensing_tables_registered_in_metadata() -> None:
    expected_tables = {
        "license_products",
        "licenses",
        "license_entitlements",
        "license_seats",
        "license_events",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_inventory_is_only_available_commercial_product_constant() -> None:
    assert AVAILABLE_COMMERCIAL_PRODUCT == "inventory"
    assert "inventory" not in FUTURE_MODULE_CODES
    assert "crm" in FUTURE_MODULE_CODES
    assert "pos" in FUTURE_MODULE_CODES


def test_license_product_code_is_unique() -> None:
    constraints = {constraint.name for constraint in LicenseProduct.__table__.constraints}
    assert "uq_license_products_product_code" in constraints


def test_license_is_tenant_scoped() -> None:
    columns = License.__table__.columns
    assert columns["organisation_id"].nullable is False


def test_license_entitlement_is_tenant_and_license_scoped() -> None:
    columns = LicenseEntitlement.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["license_id"].nullable is False
    assert columns["product_id"].nullable is False


def test_license_seat_is_tenant_scoped() -> None:
    columns = LicenseSeat.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["license_id"].nullable is False


def test_license_event_is_tenant_scoped() -> None:
    columns = LicenseEvent.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["license_id"].nullable is False

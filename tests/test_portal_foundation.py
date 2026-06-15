"""Portal runtime foundation tests."""

from invyra_platform.core.constants import AVAILABLE_COMMERCIAL_PRODUCT, FUTURE_MODULE_CODES
from invyra_platform.db.base import Base
from invyra_platform.portal.models import (
    PortalAccessEvent,
    PortalModuleRegistry,
    PortalSession,
    PortalUserPreference,
)


def test_portal_tables_registered_in_metadata() -> None:
    expected_tables = {
        "portal_sessions",
        "portal_module_registry",
        "portal_user_preferences",
        "portal_access_events",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_portal_session_is_tenant_user_and_auth_scoped() -> None:
    columns = PortalSession.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["auth_session_id"].nullable is False


def test_portal_module_registry_has_unique_module_code() -> None:
    constraints = {constraint.name for constraint in PortalModuleRegistry.__table__.constraints}
    assert "uq_portal_module_registry_module_code" in constraints


def test_portal_user_preference_is_tenant_user_scoped() -> None:
    columns = PortalUserPreference.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False


def test_portal_access_event_is_tenant_scoped() -> None:
    columns = PortalAccessEvent.__table__.columns
    assert columns["organisation_id"].nullable is False


def test_inventory_first_constants_remain_locked() -> None:
    assert AVAILABLE_COMMERCIAL_PRODUCT == "inventory"
    assert "inventory" not in FUTURE_MODULE_CODES
    assert "crm" in FUTURE_MODULE_CODES
    assert "pos" in FUTURE_MODULE_CODES

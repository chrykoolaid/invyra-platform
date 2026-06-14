"""Tenant and event foundation tests."""

from invyra_platform.audit.models import AuditEvent
from invyra_platform.db.base import Base
from invyra_platform.organisations.models import Organisation, OrganisationSettings


def test_tenant_tables_registered_in_metadata() -> None:
    assert "organisations" in Base.metadata.tables
    assert "organisation_settings" in Base.metadata.tables


def test_event_table_registered_in_metadata() -> None:
    assert "audit_events" in Base.metadata.tables


def test_tenant_settings_requires_tenant_id() -> None:
    columns = OrganisationSettings.__table__.columns
    assert "organisation_id" in columns
    assert columns["organisation_id"].nullable is False


def test_event_record_allows_platform_level_entries() -> None:
    columns = AuditEvent.__table__.columns
    assert "organisation_id" in columns
    assert columns["organisation_id"].nullable is True


def test_tenant_slug_unique_constraint_exists() -> None:
    constraints = {constraint.name for constraint in Organisation.__table__.constraints}
    assert "uq_organisations_slug" in constraints

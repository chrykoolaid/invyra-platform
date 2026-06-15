"""Environment foundation tests."""

from invyra_platform.db.base import Base
from invyra_platform.environments.models import (
    EnvironmentAccessRule,
    EnvironmentSwitchEvent,
    OrganisationEnvironment,
)
from invyra_platform.shared.enums import EnvironmentCode


def test_environment_tables_registered_in_metadata() -> None:
    expected_tables = {
        "organisation_environments",
        "environment_access_rules",
        "environment_switch_events",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_environment_codes_are_locked() -> None:
    assert {EnvironmentCode.LIVE, EnvironmentCode.TRAINING, EnvironmentCode.TEST} == {
        "LIVE",
        "TRAINING",
        "TEST",
    }


def test_organisation_environment_is_tenant_scoped() -> None:
    columns = OrganisationEnvironment.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["environment_code"].nullable is False


def test_organisation_environment_unique_constraint_exists() -> None:
    constraints = {constraint.name for constraint in OrganisationEnvironment.__table__.constraints}
    assert "uq_organisation_environment_code" in constraints


def test_environment_access_rule_is_role_and_tenant_scoped() -> None:
    columns = EnvironmentAccessRule.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["environment_id"].nullable is False
    assert columns["role_id"].nullable is False


def test_environment_switch_event_is_tenant_scoped() -> None:
    columns = EnvironmentSwitchEvent.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["to_environment_id"].nullable is True

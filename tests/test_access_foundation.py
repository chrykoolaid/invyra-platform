"""Access foundation tests."""

from invyra_platform.db.base import Base
from invyra_platform.users.models import (
    OrganisationMembership,
    Permission,
    Role,
    RolePermission,
    User,
    UserRoleAssignment,
)


def test_access_tables_registered_in_metadata() -> None:
    expected_tables = {
        "users",
        "organisation_memberships",
        "roles",
        "permissions",
        "role_permissions",
        "user_role_assignments",
    }

    assert expected_tables.issubset(Base.metadata.tables.keys())


def test_user_email_unique_constraint_exists() -> None:
    constraints = {constraint.name for constraint in User.__table__.constraints}
    assert "uq_users_email" in constraints


def test_membership_requires_tenant_and_user() -> None:
    columns = OrganisationMembership.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False


def test_role_can_be_system_or_tenant_scoped() -> None:
    columns = Role.__table__.columns
    assert columns["organisation_id"].nullable is True
    assert columns["is_system_role"].nullable is False


def test_permission_code_is_unique() -> None:
    constraints = {constraint.name for constraint in Permission.__table__.constraints}
    assert "uq_permissions_code" in constraints


def test_role_permission_unique_mapping_exists() -> None:
    constraints = {constraint.name for constraint in RolePermission.__table__.constraints}
    assert "uq_role_permission" in constraints


def test_role_assignment_requires_tenant_user_and_role() -> None:
    columns = UserRoleAssignment.__table__.columns
    assert columns["organisation_id"].nullable is False
    assert columns["user_id"].nullable is False
    assert columns["role_id"].nullable is False

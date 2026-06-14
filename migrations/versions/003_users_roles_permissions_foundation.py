"""Users, memberships, roles, and permissions foundation.

Revision ID: 003_users_roles_permissions_foundation
Revises: 002_organisations_audit_foundation
Create Date: 2026-06-14
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "003_users_roles_permissions_foundation"
down_revision: str | None = "002_organisations_audit_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_status", "users", ["status"])

    op.create_table(
        "permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=160), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("code", name="uq_permissions_code"),
    )
    op.create_index("ix_permissions_code", "permissions", ["code"])

    op.create_table(
        "organisation_memberships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("membership_status", sa.String(length=40), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("removed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_organisation_memberships_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_organisation_memberships_user_id_users", ondelete="CASCADE"),
        sa.UniqueConstraint("organisation_id", "user_id", name="uq_membership_organisation_user"),
    )
    op.create_index("ix_organisation_memberships_organisation_id", "organisation_memberships", ["organisation_id"])
    op.create_index("ix_organisation_memberships_user_id", "organisation_memberships", ["user_id"])
    op.create_index("ix_organisation_memberships_membership_status", "organisation_memberships", ["membership_status"])

    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("role_type", sa.String(length=40), nullable=False),
        sa.Column("is_system_role", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_roles_organisation_id_organisations", ondelete="CASCADE"),
        sa.UniqueConstraint("organisation_id", "name", name="uq_roles_organisation_name"),
    )
    op.create_index("ix_roles_organisation_id", "roles", ["organisation_id"])
    op.create_index("ix_roles_role_type", "roles", ["role_type"])

    op.create_table(
        "role_permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("permission_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_role_permissions_role_id_roles", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], name="fk_role_permissions_permission_id_permissions", ondelete="CASCADE"),
        sa.UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )
    op.create_index("ix_role_permissions_role_id", "role_permissions", ["role_id"])
    op.create_index("ix_role_permissions_permission_id", "role_permissions", ["permission_id"])

    op.create_table(
        "user_role_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("assigned_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_user_role_assignments_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_user_role_assignments_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_user_role_assignments_role_id_roles", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["assigned_by_user_id"], ["users.id"], name="fk_user_role_assignments_assigned_by_user_id_users", ondelete="SET NULL"),
        sa.UniqueConstraint("organisation_id", "user_id", "role_id", name="uq_user_role_assignment"),
    )
    op.create_index("ix_user_role_assignments_organisation_id", "user_role_assignments", ["organisation_id"])
    op.create_index("ix_user_role_assignments_user_id", "user_role_assignments", ["user_id"])
    op.create_index("ix_user_role_assignments_role_id", "user_role_assignments", ["role_id"])


def downgrade() -> None:
    """Rollback migration."""
    op.drop_index("ix_user_role_assignments_role_id", table_name="user_role_assignments")
    op.drop_index("ix_user_role_assignments_user_id", table_name="user_role_assignments")
    op.drop_index("ix_user_role_assignments_organisation_id", table_name="user_role_assignments")
    op.drop_table("user_role_assignments")

    op.drop_index("ix_role_permissions_permission_id", table_name="role_permissions")
    op.drop_index("ix_role_permissions_role_id", table_name="role_permissions")
    op.drop_table("role_permissions")

    op.drop_index("ix_roles_role_type", table_name="roles")
    op.drop_index("ix_roles_organisation_id", table_name="roles")
    op.drop_table("roles")

    op.drop_index("ix_organisation_memberships_membership_status", table_name="organisation_memberships")
    op.drop_index("ix_organisation_memberships_user_id", table_name="organisation_memberships")
    op.drop_index("ix_organisation_memberships_organisation_id", table_name="organisation_memberships")
    op.drop_table("organisation_memberships")

    op.drop_index("ix_permissions_code", table_name="permissions")
    op.drop_table("permissions")

    op.drop_index("ix_users_status", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

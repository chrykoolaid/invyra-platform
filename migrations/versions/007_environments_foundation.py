"""Environment separation foundation.

Revision ID: 007_environments_foundation
Revises: 006_devices_foundation
Create Date: 2026-06-15
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "007_environments_foundation"
down_revision: str | None = "006_devices_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "organisation_environments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment_code", sa.String(length=20), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_organisation_environments_organisation_id_organisations", ondelete="CASCADE"),
        sa.UniqueConstraint("organisation_id", "environment_code", name="uq_organisation_environment_code"),
    )
    op.create_index("ix_organisation_environments_organisation_id", "organisation_environments", ["organisation_id"])
    op.create_index("ix_organisation_environments_environment_code", "organisation_environments", ["environment_code"])
    op.create_index("ix_organisation_environments_status", "organisation_environments", ["status"])

    op.create_table(
        "environment_access_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("can_access", sa.Boolean(), nullable=False),
        sa.Column("can_switch_to", sa.Boolean(), nullable=False),
        sa.Column("requires_admin_pin", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_environment_access_rules_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["environment_id"], ["organisation_environments.id"], name="fk_environment_access_rules_environment_id_organisation_environments", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name="fk_environment_access_rules_role_id_roles", ondelete="CASCADE"),
        sa.UniqueConstraint("organisation_id", "environment_id", "role_id", name="uq_environment_access_rule"),
    )
    op.create_index("ix_environment_access_rules_organisation_id", "environment_access_rules", ["organisation_id"])
    op.create_index("ix_environment_access_rules_environment_id", "environment_access_rules", ["environment_id"])
    op.create_index("ix_environment_access_rules_role_id", "environment_access_rules", ["role_id"])

    op.create_table(
        "environment_switch_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("from_environment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("to_environment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("result", sa.String(length=80), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_environment_switch_events_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_environment_switch_events_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["from_environment_id"], ["organisation_environments.id"], name="fk_environment_switch_events_from_environment_id_organisation_environments", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["to_environment_id"], ["organisation_environments.id"], name="fk_environment_switch_events_to_environment_id_organisation_environments", ondelete="SET NULL"),
    )
    op.create_index("ix_environment_switch_events_organisation_id", "environment_switch_events", ["organisation_id"])
    op.create_index("ix_environment_switch_events_user_id", "environment_switch_events", ["user_id"])
    op.create_index("ix_environment_switch_events_to_environment_id", "environment_switch_events", ["to_environment_id"])
    op.create_index("ix_environment_switch_events_result", "environment_switch_events", ["result"])


def downgrade() -> None:
    """Rollback migration."""
    op.drop_index("ix_environment_switch_events_result", table_name="environment_switch_events")
    op.drop_index("ix_environment_switch_events_to_environment_id", table_name="environment_switch_events")
    op.drop_index("ix_environment_switch_events_user_id", table_name="environment_switch_events")
    op.drop_index("ix_environment_switch_events_organisation_id", table_name="environment_switch_events")
    op.drop_table("environment_switch_events")

    op.drop_index("ix_environment_access_rules_role_id", table_name="environment_access_rules")
    op.drop_index("ix_environment_access_rules_environment_id", table_name="environment_access_rules")
    op.drop_index("ix_environment_access_rules_organisation_id", table_name="environment_access_rules")
    op.drop_table("environment_access_rules")

    op.drop_index("ix_organisation_environments_status", table_name="organisation_environments")
    op.drop_index("ix_organisation_environments_environment_code", table_name="organisation_environments")
    op.drop_index("ix_organisation_environments_organisation_id", table_name="organisation_environments")
    op.drop_table("organisation_environments")

"""Portal runtime foundation.

Revision ID: 008_portal_runtime_foundation
Revises: 007_environments_foundation
Create Date: 2026-06-15
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "008_portal_runtime_foundation"
down_revision: str | None = "007_environments_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "portal_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("auth_session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("active_environment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_portal_sessions_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_portal_sessions_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["auth_session_id"], ["auth_sessions.id"], name="fk_portal_sessions_auth_session_id_auth_sessions", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["active_environment_id"], ["organisation_environments.id"], name="fk_portal_sessions_active_environment_id_organisation_environments", ondelete="SET NULL"),
    )
    op.create_index("ix_portal_sessions_organisation_id", "portal_sessions", ["organisation_id"])
    op.create_index("ix_portal_sessions_user_id", "portal_sessions", ["user_id"])
    op.create_index("ix_portal_sessions_auth_session_id", "portal_sessions", ["auth_session_id"])
    op.create_index("ix_portal_sessions_active_environment_id", "portal_sessions", ["active_environment_id"])
    op.create_index("ix_portal_sessions_expires_at", "portal_sessions", ["expires_at"])
    op.create_index("ix_portal_sessions_revoked_at", "portal_sessions", ["revoked_at"])

    op.create_table(
        "portal_module_registry",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("module_code", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("commercial_status", sa.String(length=40), nullable=False),
        sa.Column("is_visible", sa.String(length=10), nullable=False),
        sa.Column("launch_route", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("module_code", name="uq_portal_module_registry_module_code"),
    )
    op.create_index("ix_portal_module_registry_module_code", "portal_module_registry", ["module_code"])
    op.create_index("ix_portal_module_registry_commercial_status", "portal_module_registry", ["commercial_status"])

    op.create_table(
        "portal_user_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("default_environment_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_portal_user_preferences_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_portal_user_preferences_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["default_environment_id"], ["organisation_environments.id"], name="fk_portal_user_preferences_default_environment_id_organisation_environments", ondelete="SET NULL"),
        sa.UniqueConstraint("organisation_id", "user_id", name="uq_portal_user_preference"),
    )
    op.create_index("ix_portal_user_preferences_organisation_id", "portal_user_preferences", ["organisation_id"])
    op.create_index("ix_portal_user_preferences_user_id", "portal_user_preferences", ["user_id"])

    op.create_table(
        "portal_access_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("portal_session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("result", sa.String(length=80), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_portal_access_events_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_portal_access_events_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["portal_session_id"], ["portal_sessions.id"], name="fk_portal_access_events_portal_session_id_portal_sessions", ondelete="SET NULL"),
    )
    op.create_index("ix_portal_access_events_organisation_id", "portal_access_events", ["organisation_id"])
    op.create_index("ix_portal_access_events_user_id", "portal_access_events", ["user_id"])
    op.create_index("ix_portal_access_events_portal_session_id", "portal_access_events", ["portal_session_id"])
    op.create_index("ix_portal_access_events_event_type", "portal_access_events", ["event_type"])
    op.create_index("ix_portal_access_events_result", "portal_access_events", ["result"])


def downgrade() -> None:
    """Rollback migration."""
    op.drop_index("ix_portal_access_events_result", table_name="portal_access_events")
    op.drop_index("ix_portal_access_events_event_type", table_name="portal_access_events")
    op.drop_index("ix_portal_access_events_portal_session_id", table_name="portal_access_events")
    op.drop_index("ix_portal_access_events_user_id", table_name="portal_access_events")
    op.drop_index("ix_portal_access_events_organisation_id", table_name="portal_access_events")
    op.drop_table("portal_access_events")

    op.drop_index("ix_portal_user_preferences_user_id", table_name="portal_user_preferences")
    op.drop_index("ix_portal_user_preferences_organisation_id", table_name="portal_user_preferences")
    op.drop_table("portal_user_preferences")

    op.drop_index("ix_portal_module_registry_commercial_status", table_name="portal_module_registry")
    op.drop_index("ix_portal_module_registry_module_code", table_name="portal_module_registry")
    op.drop_table("portal_module_registry")

    op.drop_index("ix_portal_sessions_revoked_at", table_name="portal_sessions")
    op.drop_index("ix_portal_sessions_expires_at", table_name="portal_sessions")
    op.drop_index("ix_portal_sessions_active_environment_id", table_name="portal_sessions")
    op.drop_index("ix_portal_sessions_auth_session_id", table_name="portal_sessions")
    op.drop_index("ix_portal_sessions_user_id", table_name="portal_sessions")
    op.drop_index("ix_portal_sessions_organisation_id", table_name="portal_sessions")
    op.drop_table("portal_sessions")

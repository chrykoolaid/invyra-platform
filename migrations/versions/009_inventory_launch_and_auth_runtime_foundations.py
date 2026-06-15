"""Inventory launch and auth runtime foundations.

Revision ID: 009_inventory_launch_auth_runtime
Revises: 008_portal_runtime_foundation
Create Date: 2026-06-15
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "009_inventory_launch_auth_runtime"
down_revision: str | None = "008_portal_runtime_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration."""
    op.add_column("auth_sessions", sa.Column("environment", sa.String(length=20), nullable=True))
    op.add_column("auth_sessions", sa.Column("status", sa.String(length=40), nullable=False, server_default="active"))
    op.add_column("auth_sessions", sa.Column("revoked_reason", sa.String(length=160), nullable=True))
    op.create_index("ix_auth_sessions_environment", "auth_sessions", ["environment"])
    op.create_index("ix_auth_sessions_status", "auth_sessions", ["status"])

    op.add_column("login_attempts", sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("login_attempts", sa.Column("environment", sa.String(length=20), nullable=True))
    op.create_foreign_key(
        "fk_login_attempts_organisation_id_organisations",
        "login_attempts",
        "organisations",
        ["organisation_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_login_attempts_organisation_id", "login_attempts", ["organisation_id"])
    op.create_index("ix_login_attempts_environment", "login_attempts", ["environment"])

    op.add_column("password_reset_tokens", sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("password_reset_tokens", sa.Column("revoked_reason", sa.String(length=160), nullable=True))
    op.create_index("ix_password_reset_tokens_revoked_at", "password_reset_tokens", ["revoked_at"])

    op.create_table(
        "auth_refresh_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("environment", sa.String(length=20), nullable=True),
        sa.Column("token_hash", sa.String(length=500), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="active"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_reason", sa.String(length=160), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["auth_sessions.id"], name="fk_auth_refresh_tokens_session_id_auth_sessions", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_auth_refresh_tokens_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_auth_refresh_tokens_organisation_id_organisations", ondelete="SET NULL"),
        sa.UniqueConstraint("token_hash", name="uq_auth_refresh_tokens_token_hash"),
    )
    op.create_index("ix_auth_refresh_tokens_session_id", "auth_refresh_tokens", ["session_id"])
    op.create_index("ix_auth_refresh_tokens_user_id", "auth_refresh_tokens", ["user_id"])
    op.create_index("ix_auth_refresh_tokens_organisation_id", "auth_refresh_tokens", ["organisation_id"])
    op.create_index("ix_auth_refresh_tokens_environment", "auth_refresh_tokens", ["environment"])
    op.create_index("ix_auth_refresh_tokens_status", "auth_refresh_tokens", ["status"])
    op.create_index("ix_auth_refresh_tokens_expires_at", "auth_refresh_tokens", ["expires_at"])
    op.create_index("ix_auth_refresh_tokens_revoked_at", "auth_refresh_tokens", ["revoked_at"])

    op.create_table(
        "auth_security_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("environment", sa.String(length=20), nullable=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("login_attempt_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("result", sa.String(length=80), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(length=80), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_auth_security_events_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_auth_security_events_organisation_id_organisations", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["session_id"], ["auth_sessions.id"], name="fk_auth_security_events_session_id_auth_sessions", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["login_attempt_id"], ["login_attempts.id"], name="fk_auth_security_events_login_attempt_id_login_attempts", ondelete="SET NULL"),
    )
    op.create_index("ix_auth_security_events_user_id", "auth_security_events", ["user_id"])
    op.create_index("ix_auth_security_events_organisation_id", "auth_security_events", ["organisation_id"])
    op.create_index("ix_auth_security_events_environment", "auth_security_events", ["environment"])
    op.create_index("ix_auth_security_events_session_id", "auth_security_events", ["session_id"])
    op.create_index("ix_auth_security_events_login_attempt_id", "auth_security_events", ["login_attempt_id"])
    op.create_index("ix_auth_security_events_event_type", "auth_security_events", ["event_type"])
    op.create_index("ix_auth_security_events_result", "auth_security_events", ["result"])

    op.create_table(
        "inventory_launch_attempts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment", sa.String(length=20), nullable=False),
        sa.Column("requested_product", sa.String(length=80), nullable=False, server_default="inventory"),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="requested"),
        sa.Column("failure_reason", sa.String(length=160), nullable=True),
        sa.Column("license_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("entitlement_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("platform_session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("ip_address", sa.String(length=80), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_inventory_launch_attempts_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_inventory_launch_attempts_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["license_id"], ["licenses.id"], name="fk_inventory_launch_attempts_license_id_licenses", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["entitlement_id"], ["license_entitlements.id"], name="fk_inventory_launch_attempts_entitlement_id_license_entitlements", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["platform_session_id"], ["auth_sessions.id"], name="fk_inventory_launch_attempts_platform_session_id_auth_sessions", ondelete="SET NULL"),
    )
    for column in ["organisation_id", "user_id", "environment", "requested_product", "status", "license_id", "entitlement_id", "platform_session_id"]:
        op.create_index(f"ix_inventory_launch_attempts_{column}", "inventory_launch_attempts", [column])

    op.create_table(
        "inventory_launch_tokens",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment", sa.String(length=20), nullable=False),
        sa.Column("token_hash", sa.String(length=500), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("consumed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("revocation_reason", sa.String(length=160), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["attempt_id"], ["inventory_launch_attempts.id"], name="fk_inventory_launch_tokens_attempt_id_inventory_launch_attempts", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_inventory_launch_tokens_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_inventory_launch_tokens_user_id_users", ondelete="CASCADE"),
        sa.UniqueConstraint("token_hash", name="uq_inventory_launch_tokens_token_hash"),
    )
    for column in ["attempt_id", "organisation_id", "user_id", "environment", "expires_at", "consumed_at", "revoked_at"]:
        op.create_index(f"ix_inventory_launch_tokens_{column}", "inventory_launch_tokens", [column])

    op.create_table(
        "inventory_launch_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False, server_default="active"),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["attempt_id"], ["inventory_launch_attempts.id"], name="fk_inventory_launch_sessions_attempt_id_inventory_launch_attempts", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["token_id"], ["inventory_launch_tokens.id"], name="fk_inventory_launch_sessions_token_id_inventory_launch_tokens", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_inventory_launch_sessions_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_inventory_launch_sessions_user_id_users", ondelete="CASCADE"),
    )
    for column in ["attempt_id", "token_id", "organisation_id", "user_id", "environment", "status", "started_at", "ended_at", "expires_at", "revoked_at"]:
        op.create_index(f"ix_inventory_launch_sessions_{column}", "inventory_launch_sessions", [column])

    op.create_table(
        "inventory_launch_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("attempt_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment", sa.String(length=20), nullable=False),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("event_status", sa.String(length=80), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["attempt_id"], ["inventory_launch_attempts.id"], name="fk_inventory_launch_events_attempt_id_inventory_launch_attempts", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["token_id"], ["inventory_launch_tokens.id"], name="fk_inventory_launch_events_token_id_inventory_launch_tokens", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["session_id"], ["inventory_launch_sessions.id"], name="fk_inventory_launch_events_session_id_inventory_launch_sessions", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_inventory_launch_events_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_inventory_launch_events_user_id_users", ondelete="CASCADE"),
    )
    for column in ["attempt_id", "token_id", "session_id", "organisation_id", "user_id", "environment", "event_type", "event_status"]:
        op.create_index(f"ix_inventory_launch_events_{column}", "inventory_launch_events", [column])


def downgrade() -> None:
    """Rollback migration."""
    for column in ["event_status", "event_type", "environment", "user_id", "organisation_id", "session_id", "token_id", "attempt_id"]:
        op.drop_index(f"ix_inventory_launch_events_{column}", table_name="inventory_launch_events")
    op.drop_table("inventory_launch_events")

    for column in ["revoked_at", "expires_at", "ended_at", "started_at", "status", "environment", "user_id", "organisation_id", "token_id", "attempt_id"]:
        op.drop_index(f"ix_inventory_launch_sessions_{column}", table_name="inventory_launch_sessions")
    op.drop_table("inventory_launch_sessions")

    for column in ["revoked_at", "consumed_at", "expires_at", "environment", "user_id", "organisation_id", "attempt_id"]:
        op.drop_index(f"ix_inventory_launch_tokens_{column}", table_name="inventory_launch_tokens")
    op.drop_table("inventory_launch_tokens")

    for column in ["platform_session_id", "entitlement_id", "license_id", "status", "requested_product", "environment", "user_id", "organisation_id"]:
        op.drop_index(f"ix_inventory_launch_attempts_{column}", table_name="inventory_launch_attempts")
    op.drop_table("inventory_launch_attempts")

    op.drop_index("ix_auth_security_events_result", table_name="auth_security_events")
    op.drop_index("ix_auth_security_events_event_type", table_name="auth_security_events")
    op.drop_index("ix_auth_security_events_login_attempt_id", table_name="auth_security_events")
    op.drop_index("ix_auth_security_events_session_id", table_name="auth_security_events")
    op.drop_index("ix_auth_security_events_environment", table_name="auth_security_events")
    op.drop_index("ix_auth_security_events_organisation_id", table_name="auth_security_events")
    op.drop_index("ix_auth_security_events_user_id", table_name="auth_security_events")
    op.drop_table("auth_security_events")

    op.drop_index("ix_auth_refresh_tokens_revoked_at", table_name="auth_refresh_tokens")
    op.drop_index("ix_auth_refresh_tokens_expires_at", table_name="auth_refresh_tokens")
    op.drop_index("ix_auth_refresh_tokens_status", table_name="auth_refresh_tokens")
    op.drop_index("ix_auth_refresh_tokens_environment", table_name="auth_refresh_tokens")
    op.drop_index("ix_auth_refresh_tokens_organisation_id", table_name="auth_refresh_tokens")
    op.drop_index("ix_auth_refresh_tokens_user_id", table_name="auth_refresh_tokens")
    op.drop_index("ix_auth_refresh_tokens_session_id", table_name="auth_refresh_tokens")
    op.drop_table("auth_refresh_tokens")

    op.drop_index("ix_password_reset_tokens_revoked_at", table_name="password_reset_tokens")
    op.drop_column("password_reset_tokens", "revoked_reason")
    op.drop_column("password_reset_tokens", "revoked_at")

    op.drop_index("ix_login_attempts_environment", table_name="login_attempts")
    op.drop_index("ix_login_attempts_organisation_id", table_name="login_attempts")
    op.drop_constraint("fk_login_attempts_organisation_id_organisations", "login_attempts", type_="foreignkey")
    op.drop_column("login_attempts", "environment")
    op.drop_column("login_attempts", "organisation_id")

    op.drop_index("ix_auth_sessions_status", table_name="auth_sessions")
    op.drop_index("ix_auth_sessions_environment", table_name="auth_sessions")
    op.drop_column("auth_sessions", "revoked_reason")
    op.drop_column("auth_sessions", "status")
    op.drop_column("auth_sessions", "environment")

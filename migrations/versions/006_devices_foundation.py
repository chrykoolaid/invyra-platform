"""Devices foundation.

Revision ID: 006_devices_foundation
Revises: 005_licensing_entitlements_foundation
Create Date: 2026-06-15
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "006_devices_foundation"
down_revision: str | None = "005_licensing_entitlements_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "devices",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("device_name", sa.String(length=255), nullable=False),
        sa.Column("device_type", sa.String(length=80), nullable=False),
        sa.Column("device_fingerprint_hash", sa.String(length=500), nullable=False),
        sa.Column("trust_status", sa.String(length=40), nullable=False),
        sa.Column("registered_by_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_devices_organisation_id_organisations", ondelete="CASCADE"),
        sa.UniqueConstraint("device_fingerprint_hash", name="uq_devices_device_fingerprint_hash"),
    )
    op.create_index("ix_devices_organisation_id", "devices", ["organisation_id"])
    op.create_index("ix_devices_device_type", "devices", ["device_type"])
    op.create_index("ix_devices_trust_status", "devices", ["trust_status"])

    op.create_table(
        "device_assignments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("device_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("assigned_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("environment_code", sa.String(length=20), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_device_assignments_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], name="fk_device_assignments_device_id_devices", ondelete="CASCADE"),
    )
    op.create_index("ix_device_assignments_organisation_id", "device_assignments", ["organisation_id"])
    op.create_index("ix_device_assignments_device_id", "device_assignments", ["device_id"])
    op.create_index("ix_device_assignments_environment_code", "device_assignments", ["environment_code"])
    op.create_index("ix_device_assignments_status", "device_assignments", ["status"])

    op.create_table(
        "device_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("device_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("auth_session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_device_sessions_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], name="fk_device_sessions_device_id_devices", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_device_sessions_user_id_users", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["auth_session_id"], ["auth_sessions.id"], name="fk_device_sessions_auth_session_id_auth_sessions", ondelete="SET NULL"),
    )
    op.create_index("ix_device_sessions_organisation_id", "device_sessions", ["organisation_id"])
    op.create_index("ix_device_sessions_device_id", "device_sessions", ["device_id"])
    op.create_index("ix_device_sessions_user_id", "device_sessions", ["user_id"])
    op.create_index("ix_device_sessions_auth_session_id", "device_sessions", ["auth_session_id"])
    op.create_index("ix_device_sessions_status", "device_sessions", ["status"])

    op.create_table(
        "device_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("device_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("result", sa.String(length=80), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_device_events_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["device_id"], ["devices.id"], name="fk_device_events_device_id_devices", ondelete="CASCADE"),
    )
    op.create_index("ix_device_events_organisation_id", "device_events", ["organisation_id"])
    op.create_index("ix_device_events_device_id", "device_events", ["device_id"])
    op.create_index("ix_device_events_event_type", "device_events", ["event_type"])
    op.create_index("ix_device_events_result", "device_events", ["result"])


def downgrade() -> None:
    """Rollback migration."""
    op.drop_index("ix_device_events_result", table_name="device_events")
    op.drop_index("ix_device_events_event_type", table_name="device_events")
    op.drop_index("ix_device_events_device_id", table_name="device_events")
    op.drop_index("ix_device_events_organisation_id", table_name="device_events")
    op.drop_table("device_events")

    op.drop_index("ix_device_sessions_status", table_name="device_sessions")
    op.drop_index("ix_device_sessions_auth_session_id", table_name="device_sessions")
    op.drop_index("ix_device_sessions_user_id", table_name="device_sessions")
    op.drop_index("ix_device_sessions_device_id", table_name="device_sessions")
    op.drop_index("ix_device_sessions_organisation_id", table_name="device_sessions")
    op.drop_table("device_sessions")

    op.drop_index("ix_device_assignments_status", table_name="device_assignments")
    op.drop_index("ix_device_assignments_environment_code", table_name="device_assignments")
    op.drop_index("ix_device_assignments_device_id", table_name="device_assignments")
    op.drop_index("ix_device_assignments_organisation_id", table_name="device_assignments")
    op.drop_table("device_assignments")

    op.drop_index("ix_devices_trust_status", table_name="devices")
    op.drop_index("ix_devices_device_type", table_name="devices")
    op.drop_index("ix_devices_organisation_id", table_name="devices")
    op.drop_table("devices")

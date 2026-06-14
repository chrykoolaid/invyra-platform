"""Organisations and platform event foundation.

Revision ID: 002_organisations_audit_foundation
Revises: 001_platform_base
Create Date: 2026-06-14
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "002_organisations_audit_foundation"
down_revision: str | None = "001_platform_base"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "organisations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("slug", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("owner_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("slug", name="uq_organisations_slug"),
    )
    op.create_index("ix_organisations_slug", "organisations", ["slug"])
    op.create_index("ix_organisations_status", "organisations", ["status"])

    op.create_table(
        "organisation_settings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("default_timezone", sa.String(length=80), nullable=False),
        sa.Column("default_environment_code", sa.String(length=20), nullable=False),
        sa.Column("support_access_allowed", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_id"],
            ["organisations.id"],
            name="fk_organisation_settings_organisation_id_organisations",
            ondelete="CASCADE",
        ),
        sa.UniqueConstraint("organisation_id", name="uq_organisation_settings_organisation_id"),
    )
    op.create_index(
        "ix_organisation_settings_organisation_id",
        "organisation_settings",
        ["organisation_id"],
    )

    op.create_table(
        "audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("actor_device_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("environment_code", sa.String(length=20), nullable=True),
        sa.Column("event_category", sa.String(length=80), nullable=False),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("result", sa.String(length=80), nullable=False),
        sa.Column("resource_type", sa.String(length=120), nullable=True),
        sa.Column("resource_id", sa.String(length=120), nullable=True),
        sa.Column("ip_address", sa.String(length=80), nullable=True),
        sa.Column("user_agent", sa.Text(), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_id"],
            ["organisations.id"],
            name="fk_audit_events_organisation_id_organisations",
            ondelete="SET NULL",
        ),
    )
    op.create_index("ix_audit_events_organisation_id", "audit_events", ["organisation_id"])
    op.create_index("ix_audit_events_environment_code", "audit_events", ["environment_code"])
    op.create_index("ix_audit_events_event_category", "audit_events", ["event_category"])
    op.create_index("ix_audit_events_event_type", "audit_events", ["event_type"])
    op.create_index("ix_audit_events_result", "audit_events", ["result"])
    op.create_index(
        "ix_audit_events_org_category_created",
        "audit_events",
        ["organisation_id", "event_category", "created_at"],
    )


def downgrade() -> None:
    """Rollback migration."""
    op.drop_index("ix_audit_events_org_category_created", table_name="audit_events")
    op.drop_index("ix_audit_events_result", table_name="audit_events")
    op.drop_index("ix_audit_events_event_type", table_name="audit_events")
    op.drop_index("ix_audit_events_event_category", table_name="audit_events")
    op.drop_index("ix_audit_events_environment_code", table_name="audit_events")
    op.drop_index("ix_audit_events_organisation_id", table_name="audit_events")
    op.drop_table("audit_events")

    op.drop_index("ix_organisation_settings_organisation_id", table_name="organisation_settings")
    op.drop_table("organisation_settings")

    op.drop_index("ix_organisations_status", table_name="organisations")
    op.drop_index("ix_organisations_slug", table_name="organisations")
    op.drop_table("organisations")

"""Inventory access gateway foundation.

Revision ID: 010_inventory_access_gateway
Revises: 009_inventory_launch_auth_runtime
Create Date: 2026-06-16
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "010_inventory_access_gateway"
down_revision: str | None = "009_inventory_launch_auth_runtime"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "inventory_access_evaluations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment", sa.String(length=20), nullable=False),
        sa.Column("product_code", sa.String(length=80), nullable=False),
        sa.Column("result", sa.String(length=40), nullable=False),
        sa.Column("failure_reason", sa.String(length=160), nullable=True),
        sa.Column("license_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("entitlement_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("auth_session_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_inventory_access_evaluations_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_inventory_access_evaluations_user_id_users", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["license_id"], ["licenses.id"], name="fk_inventory_access_evaluations_license_id_licenses", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["entitlement_id"], ["license_entitlements.id"], name="fk_inventory_access_evaluations_entitlement_id_license_entitlements", ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["auth_session_id"], ["auth_sessions.id"], name="fk_inventory_access_evaluations_auth_session_id_auth_sessions", ondelete="SET NULL"),
    )
    for column in [
        "organisation_id",
        "user_id",
        "environment",
        "product_code",
        "result",
        "failure_reason",
        "license_id",
        "entitlement_id",
        "auth_session_id",
        "created_at",
    ]:
        op.create_index(f"ix_inventory_access_evaluations_{column}", "inventory_access_evaluations", [column])

    op.create_table(
        "inventory_access_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("evaluation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment", sa.String(length=20), nullable=False),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("event_status", sa.String(length=80), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["evaluation_id"], ["inventory_access_evaluations.id"], name="fk_inventory_access_events_evaluation_id_inventory_access_evaluations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_inventory_access_events_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name="fk_inventory_access_events_user_id_users", ondelete="CASCADE"),
    )
    for column in [
        "evaluation_id",
        "organisation_id",
        "user_id",
        "environment",
        "event_type",
        "event_status",
        "created_at",
    ]:
        op.create_index(f"ix_inventory_access_events_{column}", "inventory_access_events", [column])


def downgrade() -> None:
    """Rollback migration."""
    for column in [
        "created_at",
        "event_status",
        "event_type",
        "environment",
        "user_id",
        "organisation_id",
        "evaluation_id",
    ]:
        op.drop_index(f"ix_inventory_access_events_{column}", table_name="inventory_access_events")
    op.drop_table("inventory_access_events")

    for column in [
        "created_at",
        "auth_session_id",
        "entitlement_id",
        "license_id",
        "failure_reason",
        "result",
        "product_code",
        "environment",
        "user_id",
        "organisation_id",
    ]:
        op.drop_index(f"ix_inventory_access_evaluations_{column}", table_name="inventory_access_evaluations")
    op.drop_table("inventory_access_evaluations")

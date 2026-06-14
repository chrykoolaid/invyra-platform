"""Licensing and entitlements foundation.

Revision ID: 005_licensing_entitlements_foundation
Revises: 004_auth_credentials_sessions_foundation
Create Date: 2026-06-14
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "005_licensing_entitlements_foundation"
down_revision: str | None = "004_auth_credentials_sessions_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Apply migration."""
    op.create_table(
        "license_products",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("product_code", sa.String(length=120), nullable=False),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("commercial_status", sa.String(length=40), nullable=False),
        sa.Column("launch_enabled", sa.String(length=10), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("product_code", name="uq_license_products_product_code"),
    )
    op.create_index("ix_license_products_product_code", "license_products", ["product_code"])
    op.create_index("ix_license_products_commercial_status", "license_products", ["commercial_status"])

    op.create_table(
        "licenses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("license_status", sa.String(length=40), nullable=False),
        sa.Column("plan_name", sa.String(length=160), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("suspended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_licenses_organisation_id_organisations", ondelete="CASCADE"),
    )
    op.create_index("ix_licenses_organisation_id", "licenses", ["organisation_id"])
    op.create_index("ix_licenses_license_status", "licenses", ["license_status"])
    op.create_index("ix_licenses_expires_at", "licenses", ["expires_at"])

    op.create_table(
        "license_entitlements",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("license_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("entitlement_code", sa.String(length=160), nullable=False),
        sa.Column("entitlement_status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_license_entitlements_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["license_id"], ["licenses.id"], name="fk_license_entitlements_license_id_licenses", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["product_id"], ["license_products.id"], name="fk_license_entitlements_product_id_license_products", ondelete="CASCADE"),
        sa.UniqueConstraint("license_id", "entitlement_code", name="uq_license_entitlement_code"),
    )
    op.create_index("ix_license_entitlements_organisation_id", "license_entitlements", ["organisation_id"])
    op.create_index("ix_license_entitlements_license_id", "license_entitlements", ["license_id"])
    op.create_index("ix_license_entitlements_product_id", "license_entitlements", ["product_id"])
    op.create_index("ix_license_entitlements_entitlement_code", "license_entitlements", ["entitlement_code"])
    op.create_index("ix_license_entitlements_entitlement_status", "license_entitlements", ["entitlement_status"])

    op.create_table(
        "license_seats",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("license_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("max_users", sa.Integer(), nullable=False),
        sa.Column("active_users_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_license_seats_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["license_id"], ["licenses.id"], name="fk_license_seats_license_id_licenses", ondelete="CASCADE"),
    )
    op.create_index("ix_license_seats_organisation_id", "license_seats", ["organisation_id"])
    op.create_index("ix_license_seats_license_id", "license_seats", ["license_id"])

    op.create_table(
        "license_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("organisation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("license_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actor_user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("result", sa.String(length=80), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["organisation_id"], ["organisations.id"], name="fk_license_events_organisation_id_organisations", ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["license_id"], ["licenses.id"], name="fk_license_events_license_id_licenses", ondelete="CASCADE"),
    )
    op.create_index("ix_license_events_organisation_id", "license_events", ["organisation_id"])
    op.create_index("ix_license_events_license_id", "license_events", ["license_id"])
    op.create_index("ix_license_events_event_type", "license_events", ["event_type"])
    op.create_index("ix_license_events_result", "license_events", ["result"])


def downgrade() -> None:
    """Rollback migration."""
    op.drop_index("ix_license_events_result", table_name="license_events")
    op.drop_index("ix_license_events_event_type", table_name="license_events")
    op.drop_index("ix_license_events_license_id", table_name="license_events")
    op.drop_index("ix_license_events_organisation_id", table_name="license_events")
    op.drop_table("license_events")

    op.drop_index("ix_license_seats_license_id", table_name="license_seats")
    op.drop_index("ix_license_seats_organisation_id", table_name="license_seats")
    op.drop_table("license_seats")

    op.drop_index("ix_license_entitlements_entitlement_status", table_name="license_entitlements")
    op.drop_index("ix_license_entitlements_entitlement_code", table_name="license_entitlements")
    op.drop_index("ix_license_entitlements_product_id", table_name="license_entitlements")
    op.drop_index("ix_license_entitlements_license_id", table_name="license_entitlements")
    op.drop_index("ix_license_entitlements_organisation_id", table_name="license_entitlements")
    op.drop_table("license_entitlements")

    op.drop_index("ix_licenses_expires_at", table_name="licenses")
    op.drop_index("ix_licenses_license_status", table_name="licenses")
    op.drop_index("ix_licenses_organisation_id", table_name="licenses")
    op.drop_table("licenses")

    op.drop_index("ix_license_products_commercial_status", table_name="license_products")
    op.drop_index("ix_license_products_product_code", table_name="license_products")
    op.drop_table("license_products")

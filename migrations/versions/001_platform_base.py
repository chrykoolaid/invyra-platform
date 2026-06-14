"""Initial platform base.

Revision ID: 001_platform_base
Revises: None
Create Date: 2026-06-14
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "001_platform_base"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


environment_code_enum = sa.Enum(
    "LIVE",
    "TRAINING",
    "TEST",
    name="environment_code",
)

commercial_status_enum = sa.Enum(
    "available",
    "coming_later",
    "internal_only",
    "disabled",
    name="commercial_status",
)

platform_record_status_enum = sa.Enum(
    "active",
    "inactive",
    "suspended",
    "archived",
    name="platform_record_status",
)


def upgrade() -> None:
    """Apply migration."""
    bind = op.get_bind()
    environment_code_enum.create(bind, checkfirst=True)
    commercial_status_enum.create(bind, checkfirst=True)
    platform_record_status_enum.create(bind, checkfirst=True)


def downgrade() -> None:
    """Rollback migration."""
    bind = op.get_bind()
    platform_record_status_enum.drop(bind, checkfirst=True)
    commercial_status_enum.drop(bind, checkfirst=True)
    environment_code_enum.drop(bind, checkfirst=True)

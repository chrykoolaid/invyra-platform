"""Environment SQLAlchemy models."""

from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column

from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class OrganisationEnvironment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Represents LIVE, TRAINING, or TEST for an organisation."""

    __tablename__ = "organisation_environments"
    __table_args__ = (
        UniqueConstraint("organisation_id", "environment_code", name="uq_organisation_environment_code"),
    )

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    environment_code: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)


class EnvironmentAccessRule(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Role-based access rule for an organisation environment."""

    __tablename__ = "environment_access_rules"
    __table_args__ = (
        UniqueConstraint("organisation_id", "environment_id", "role_id", name="uq_environment_access_rule"),
    )

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    environment_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisation_environments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    can_access: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    can_switch_to: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    requires_admin_pin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class EnvironmentSwitchEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Environment switch attempt or outcome."""

    __tablename__ = "environment_switch_events"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    from_environment_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisation_environments.id", ondelete="SET NULL"),
        nullable=True,
    )
    to_environment_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisation_environments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    result: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

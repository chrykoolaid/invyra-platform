"""Portal runtime SQLAlchemy models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column

from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class PortalSession(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Runtime portal context after authentication."""

    __tablename__ = "portal_sessions"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    auth_session_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("auth_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    active_environment_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisation_environments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)


class PortalModuleRegistry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Module registry visible to portal runtime."""

    __tablename__ = "portal_module_registry"

    module_code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    commercial_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    is_visible: Mapped[str] = mapped_column(String(10), nullable=False, default="false")
    launch_route: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class PortalUserPreference(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """User-level portal preference within an organisation."""

    __tablename__ = "portal_user_preferences"
    __table_args__ = (
        UniqueConstraint("organisation_id", "user_id", name="uq_portal_user_preference"),
    )

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    default_environment_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisation_environments.id", ondelete="SET NULL"),
        nullable=True,
    )


class PortalAccessEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Portal access event record."""

    __tablename__ = "portal_access_events"

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
    portal_session_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("portal_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

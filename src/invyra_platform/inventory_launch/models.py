"""Inventory launch SQLAlchemy models.

These models belong to the platform control layer only. They track launch attempts,
short-lived launch tokens, bridge sessions, and lifecycle events for the future
handoff from invyra-platform to invyra-inventory.
"""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from invyra_platform.licensing.models import License, LicenseEntitlement
from invyra_platform.users.models import User


class InventoryLaunchAttempt(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Initial platform-side request to launch Invyra Inventory."""

    __tablename__ = "inventory_launch_attempts"

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
    environment: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    requested_product: Mapped[str] = mapped_column(String(80), nullable=False, default="inventory", index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="requested", index=True)
    failure_reason: Mapped[str | None] = mapped_column(String(160), nullable=True)
    license_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("licenses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    entitlement_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("license_entitlements.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    platform_session_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("auth_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    ip_address: Mapped[str | None] = mapped_column(String(80), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User] = relationship()
    license: Mapped[License | None] = relationship()
    entitlement: Mapped[LicenseEntitlement | None] = relationship()
    tokens: Mapped[list["InventoryLaunchToken"]] = relationship(back_populates="attempt")
    sessions: Mapped[list["InventoryLaunchSession"]] = relationship(back_populates="attempt")
    events: Mapped[list["InventoryLaunchEvent"]] = relationship(back_populates="attempt")


class InventoryLaunchToken(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Short-lived hashed launch token for controlled Inventory handoff."""

    __tablename__ = "inventory_launch_tokens"

    attempt_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_launch_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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
    environment: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    consumed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    revocation_reason: Mapped[str | None] = mapped_column(String(160), nullable=True)

    attempt: Mapped[InventoryLaunchAttempt] = relationship(back_populates="tokens")
    user: Mapped[User] = relationship()
    session: Mapped["InventoryLaunchSession | None"] = relationship(back_populates="token")
    events: Mapped[list["InventoryLaunchEvent"]] = relationship(back_populates="token")


class InventoryLaunchSession(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Platform-visible bridge session created from an Inventory launch token."""

    __tablename__ = "inventory_launch_sessions"

    attempt_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_launch_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_launch_tokens.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
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
    environment: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    attempt: Mapped[InventoryLaunchAttempt] = relationship(back_populates="sessions")
    token: Mapped[InventoryLaunchToken] = relationship(back_populates="session")
    user: Mapped[User] = relationship()
    events: Mapped[list["InventoryLaunchEvent"]] = relationship(back_populates="session")


class InventoryLaunchEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Detailed event trail for Inventory launch lifecycle transitions."""

    __tablename__ = "inventory_launch_events"

    attempt_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_launch_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_launch_tokens.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    session_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_launch_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
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
    environment: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    event_status: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    attempt: Mapped[InventoryLaunchAttempt] = relationship(back_populates="events")
    token: Mapped[InventoryLaunchToken | None] = relationship(back_populates="events")
    session: Mapped[InventoryLaunchSession | None] = relationship(back_populates="events")
    user: Mapped[User] = relationship()

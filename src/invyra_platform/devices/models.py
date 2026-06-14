"""Device SQLAlchemy models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Device(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Registered device identity."""

    __tablename__ = "devices"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_name: Mapped[str] = mapped_column(String(255), nullable=False)
    device_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    device_fingerprint_hash: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    trust_status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending", index=True)
    registered_by_user_id: Mapped[UUID | None] = mapped_column(PostgresUUID(as_uuid=True), nullable=True)

    assignments: Mapped[list["DeviceAssignment"]] = relationship(back_populates="device")
    sessions: Mapped[list["DeviceSession"]] = relationship(back_populates="device")
    events: Mapped[list["DeviceEvent"]] = relationship(back_populates="device")


class DeviceAssignment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Assignment of a device to a tenant/user/environment context."""

    __tablename__ = "device_assignments"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assigned_user_id: Mapped[UUID | None] = mapped_column(PostgresUUID(as_uuid=True), nullable=True)
    environment_code: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    device: Mapped[Device] = relationship(back_populates="assignments")


class DeviceSession(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Device usage session record."""

    __tablename__ = "device_sessions"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    auth_session_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("auth_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)

    device: Mapped[Device] = relationship(back_populates="sessions")


class DeviceEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Device lifecycle or validation event."""

    __tablename__ = "device_events"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    device_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("devices.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    actor_user_id: Mapped[UUID | None] = mapped_column(PostgresUUID(as_uuid=True), nullable=True)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    device: Mapped[Device] = relationship(back_populates="events")

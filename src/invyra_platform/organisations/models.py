"""Organisation SQLAlchemy models."""

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from invyra_platform.audit.models import AuditEvent


class Organisation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tenant anchor for platform records."""

    __tablename__ = "organisations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)
    owner_user_id: Mapped[UUID | None] = mapped_column(PostgresUUID(as_uuid=True), nullable=True)

    settings: Mapped["OrganisationSettings"] = relationship(
        back_populates="organisation",
        cascade="all, delete-orphan",
        uselist=False,
    )
    audit_events: Mapped[list["AuditEvent"]] = relationship(back_populates="organisation")


class OrganisationSettings(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Tenant-level platform settings."""

    __tablename__ = "organisation_settings"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    default_timezone: Mapped[str] = mapped_column(String(80), nullable=False, default="Asia/Manila")
    default_environment_code: Mapped[str] = mapped_column(String(20), nullable=False, default="LIVE")
    support_access_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    organisation: Mapped[Organisation] = relationship(back_populates="settings")

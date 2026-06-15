"""Inventory access gateway SQLAlchemy models.

These models belong to the platform authorization layer only. They record whether
an authenticated user is allowed to access Invyra Inventory for a specific
organisation, product, and environment.
"""

from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from invyra_platform.auth.models import AuthSession
from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from invyra_platform.licensing.models import License, LicenseEntitlement
from invyra_platform.users.models import User


class InventoryAccessEvaluation(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """One platform-side authorization decision for Inventory access."""

    __tablename__ = "inventory_access_evaluations"

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
    product_code: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    failure_reason: Mapped[str | None] = mapped_column(String(160), nullable=True, index=True)
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
    auth_session_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("auth_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    user: Mapped[User] = relationship()
    license: Mapped[License | None] = relationship()
    entitlement: Mapped[LicenseEntitlement | None] = relationship()
    auth_session: Mapped[AuthSession | None] = relationship()
    events: Mapped[list["InventoryAccessEvent"]] = relationship(back_populates="evaluation")


class InventoryAccessEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Lifecycle event for an Inventory access gateway evaluation."""

    __tablename__ = "inventory_access_events"

    evaluation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_access_evaluations.id", ondelete="CASCADE"),
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
    event_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    event_status: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    evaluation: Mapped[InventoryAccessEvaluation] = relationship(back_populates="events")
    user: Mapped[User] = relationship()

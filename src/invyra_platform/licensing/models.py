"""Licensing SQLAlchemy models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class LicenseProduct(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Commercial product or future module known to the platform."""

    __tablename__ = "license_products"
    __table_args__ = (UniqueConstraint("product_code", name="uq_license_products_product_code"),)

    product_code: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    commercial_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    launch_enabled: Mapped[str] = mapped_column(String(10), nullable=False, default="false")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    entitlements: Mapped[list["LicenseEntitlement"]] = relationship(back_populates="product")


class License(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Commercial access agreement for an organisation."""

    __tablename__ = "licenses"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    license_status: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    plan_name: Mapped[str] = mapped_column(String(160), nullable=False)
    starts_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    suspended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    entitlements: Mapped[list["LicenseEntitlement"]] = relationship(back_populates="license")
    seats: Mapped[list["LicenseSeat"]] = relationship(back_populates="license")
    events: Mapped[list["LicenseEvent"]] = relationship(back_populates="license")


class LicenseEntitlement(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Specific entitlement granted under a license."""

    __tablename__ = "license_entitlements"
    __table_args__ = (
        UniqueConstraint("license_id", "entitlement_code", name="uq_license_entitlement_code"),
    )

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    license_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("licenses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("license_products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    entitlement_code: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    entitlement_status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)

    license: Mapped[License] = relationship(back_populates="entitlements")
    product: Mapped[LicenseProduct] = relationship(back_populates="entitlements")


class LicenseSeat(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Seat limits for an organisation license."""

    __tablename__ = "license_seats"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    license_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("licenses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    max_users: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    active_users_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    license: Mapped[License] = relationship(back_populates="seats")


class LicenseEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """License lifecycle event."""

    __tablename__ = "license_events"

    organisation_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    license_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("licenses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    actor_user_id: Mapped[UUID | None] = mapped_column(PostgresUUID(as_uuid=True), nullable=True)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    license: Mapped[License] = relationship(back_populates="events")

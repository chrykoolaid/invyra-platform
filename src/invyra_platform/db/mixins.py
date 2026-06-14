"""Shared SQLAlchemy model mixins."""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class UUIDPrimaryKeyMixin:
    """Mixin that adds a UUID primary key column."""

    id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )


class TimestampMixin:
    """Mixin that adds created and updated timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class OrganisationScopedMixin:
    """Mixin for tenant-scoped records.

    Concrete tenant-owned models should inherit this mixin and define the foreign key target
    when the organisations module is introduced.
    """

    @declared_attr.directive
    def __mapper_args__(cls) -> dict[str, Any]:
        return {"eager_defaults": True}

"""User, membership, role, and permission SQLAlchemy models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Global user identity record."""

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)

    memberships: Mapped[list["OrganisationMembership"]] = relationship(back_populates="user")
    role_assignments: Mapped[list["UserRoleAssignment"]] = relationship(
        back_populates="user",
        foreign_keys="UserRoleAssignment.user_id",
    )


class OrganisationMembership(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Connects a user to an organisation."""

    __tablename__ = "organisation_memberships"
    __table_args__ = (
        UniqueConstraint("organisation_id", "user_id", name="uq_membership_organisation_user"),
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
    membership_status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)
    joined_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    removed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="memberships")


class Role(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Role definition, optionally scoped to an organisation."""

    __tablename__ = "roles"
    __table_args__ = (
        UniqueConstraint("organisation_id", "name", name="uq_roles_organisation_name"),
    )

    organisation_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    role_type: Mapped[str] = mapped_column(String(40), nullable=False, default="tenant", index=True)
    is_system_role: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    permissions: Mapped[list["RolePermission"]] = relationship(back_populates="role")
    assignments: Mapped[list["UserRoleAssignment"]] = relationship(back_populates="role")


class Permission(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Atomic permission definition."""

    __tablename__ = "permissions"

    code: Mapped[str] = mapped_column(String(160), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)

    roles: Mapped[list["RolePermission"]] = relationship(back_populates="permission")


class RolePermission(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Maps a role to a permission."""

    __tablename__ = "role_permissions"
    __table_args__ = (UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),)

    role_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    permission_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[Role] = relationship(back_populates="permissions")
    permission: Mapped[Permission] = relationship(back_populates="roles")


class UserRoleAssignment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Assigns a role to a user inside an organisation."""

    __tablename__ = "user_role_assignments"
    __table_args__ = (
        UniqueConstraint("organisation_id", "user_id", "role_id", name="uq_user_role_assignment"),
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
    role_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assigned_by_user_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped[User] = relationship(back_populates="role_assignments", foreign_keys=[user_id])
    role: Mapped[Role] = relationship(back_populates="assignments")

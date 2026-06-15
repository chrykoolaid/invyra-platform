"""Authentication SQLAlchemy models."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from invyra_platform.db.base import Base
from invyra_platform.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin
from invyra_platform.users.models import User


class AuthIdentity(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Authentication credential identity for a user."""

    __tablename__ = "auth_identities"

    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(500), nullable=False)
    password_hash_algorithm: Mapped[str] = mapped_column(String(80), nullable=False, default="argon2id")
    password_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    mfa_enabled: Mapped[str] = mapped_column(String(10), nullable=False, default="false")
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)

    user: Mapped[User] = relationship()


class AuthSession(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Server-side authentication session."""

    __tablename__ = "auth_sessions"

    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organisation_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    environment: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    device_id: Mapped[UUID | None] = mapped_column(PostgresUUID(as_uuid=True), nullable=True, index=True)
    session_token_hash: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)
    ip_address: Mapped[str | None] = mapped_column(String(80), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    revoked_reason: Mapped[str | None] = mapped_column(String(160), nullable=True)

    user: Mapped[User] = relationship()
    refresh_tokens: Mapped[list["AuthRefreshToken"]] = relationship(back_populates="session")
    security_events: Mapped[list["AuthSecurityEvent"]] = relationship(back_populates="session")


class AuthRefreshToken(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Hashed refresh token record for an authenticated session."""

    __tablename__ = "auth_refresh_tokens"

    session_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("auth_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organisation_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    environment: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    token_hash: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active", index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    revoked_reason: Mapped[str | None] = mapped_column(String(160), nullable=True)

    session: Mapped[AuthSession] = relationship(back_populates="refresh_tokens")
    user: Mapped[User] = relationship()


class PasswordResetToken(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Single-use password reset token record."""

    __tablename__ = "password_reset_tokens"

    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_hash: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    revoked_reason: Mapped[str | None] = mapped_column(String(160), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(80), nullable=True)

    user: Mapped[User] = relationship()


class LoginAttempt(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Login attempt record for monitoring and lockout rules."""

    __tablename__ = "login_attempts"

    email: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    user_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    organisation_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    environment: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    success: Mapped[str] = mapped_column(String(10), nullable=False, default="false", index=True)
    failure_reason: Mapped[str | None] = mapped_column(String(160), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(80), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User | None] = relationship()
    security_events: Mapped[list["AuthSecurityEvent"]] = relationship(back_populates="login_attempt")


class AuthSecurityEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    """Security event emitted by authentication runtime lifecycle changes."""

    __tablename__ = "auth_security_events"

    user_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    organisation_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("organisations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    environment: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    session_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("auth_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    login_attempt_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("login_attempts.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    result: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(80), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped[User | None] = relationship()
    session: Mapped[AuthSession | None] = relationship(back_populates="security_events")
    login_attempt: Mapped[LoginAttempt | None] = relationship(back_populates="security_events")

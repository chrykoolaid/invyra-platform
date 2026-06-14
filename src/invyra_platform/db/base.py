"""SQLAlchemy declarative base."""

from sqlalchemy.orm import DeclarativeBase

from invyra_platform.db.metadata import metadata


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    metadata = metadata

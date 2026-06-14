"""Identifier helpers."""

from uuid import UUID, uuid4


def new_uuid() -> UUID:
    """Return a new UUID4 identifier."""
    return uuid4()

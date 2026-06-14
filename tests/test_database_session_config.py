"""Database foundation tests."""

from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker

from invyra_platform.db.base import Base
from invyra_platform.db.metadata import NAMING_CONVENTION
from invyra_platform.db.session import SessionLocal


def test_base_metadata_uses_naming_convention() -> None:
    assert isinstance(Base.metadata, MetaData)
    assert Base.metadata.naming_convention == NAMING_CONVENTION


def test_session_local_is_sessionmaker() -> None:
    assert isinstance(SessionLocal, sessionmaker)

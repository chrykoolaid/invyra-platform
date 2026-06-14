"""Pytest fixtures for Invyra Platform."""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from invyra_platform.app import create_app
from invyra_platform.core.config import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Generator[None, None, None]:
    """Clear cached settings before and after each test."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def client() -> TestClient:
    """Return a FastAPI test client."""
    app = create_app()
    return TestClient(app)

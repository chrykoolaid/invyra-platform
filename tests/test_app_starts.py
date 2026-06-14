"""Application factory tests."""

from fastapi import FastAPI

from invyra_platform.app import create_app


def test_create_app_returns_fastapi_instance() -> None:
    app = create_app()

    assert isinstance(app, FastAPI)
    assert app.title == "Invyra Platform"

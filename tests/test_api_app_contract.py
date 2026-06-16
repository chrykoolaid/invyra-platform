"""API app contract tests."""

from invyra_platform.app import create_app


def test_api_app_builds() -> None:
    app = create_app()

    assert app is not None
    assert len(app.routes) > 0

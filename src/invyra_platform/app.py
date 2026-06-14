"""FastAPI application factory."""

from fastapi import FastAPI

from invyra_platform.api.router import api_router
from invyra_platform.core.config import get_settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        version="0.1.0",
        docs_url="/docs" if settings.app_env != "production" else None,
        redoc_url="/redoc" if settings.app_env != "production" else None,
    )

    @app.get("/health", tags=["health"])
    def root_health() -> dict[str, str]:
        return {"status": "ok", "service": "invyra-platform"}

    app.include_router(api_router)
    return app

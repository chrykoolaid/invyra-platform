"""Health endpoints for API v1."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def api_health() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok", "api": "v1", "service": "invyra-platform"}

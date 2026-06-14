"""API v1 router."""

from fastapi import APIRouter

from invyra_platform.api.v1.health import router as health_router

router = APIRouter()
router.include_router(health_router, tags=["health"])

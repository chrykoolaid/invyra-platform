"""API v1 router."""

from fastapi import APIRouter

from invyra_platform.api.v1.auth import router as auth_router
from invyra_platform.api.v1.health import router as health_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(auth_router)

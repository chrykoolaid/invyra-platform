"""API v1 router."""

from fastapi import APIRouter

from invyra_platform.api.v1.auth import router as auth_router
from invyra_platform.api.v1.health import router as health_router
from invyra_platform.api.v1.inventory_access import router as inventory_access_router
from invyra_platform.api.v1.inventory_launch import router as launch_router
from invyra_platform.api.v1.portal import router as portal_router

router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(auth_router)
router.include_router(inventory_access_router)
router.include_router(launch_router)
router.include_router(portal_router)

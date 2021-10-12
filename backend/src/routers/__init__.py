from fastapi import APIRouter

from src.routers import movement

router = APIRouter()
router.include_router(movement.router, tags=["movement"])
# router.include_router(movement.router, tags=["movement"])
# router.include_router(movement.router, tags=["movement"])
# router.include_router(movement.router, tags=["movement"])

from fastapi import APIRouter

from src.routers import movement, home, mongo

router = APIRouter()
router.include_router(movement.router, tags=["Movement"])
router.include_router(home.router, tags=["Home"])
router.include_router(mongo.router, tags=["MongoDB"])
# router.include_router(movement.router, tags=["movement"])
# router.include_router(movement.router, tags=["movement"])

from fastapi import APIRouter

from src.applications.routers import applications, home, mongo

router = APIRouter()
router.include_router(applications.router)
router.include_router(home.router)
router.include_router(mongo.router, tags=["MongoDB"])
# router.include_router(movement.router, tags=["movement"])
# router.include_router(movement.router, tags=["movement"])

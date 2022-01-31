from fastapi import APIRouter

from src.applications import routers as application_routers
from src.routers import home
from src.routers import mongo

router = APIRouter()
router.include_router(application_routers.router)
router.include_router(home.router)
router.include_router(mongo.router, tags=["MongoDB"])

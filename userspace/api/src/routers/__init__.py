from fastapi import APIRouter
#from src.applications import routers as application_routers
#from src.routers import home, mongo

from applications import routers as application_routers
from routers import home, mongo


router = APIRouter()
router.include_router(application_routers.router)
router.include_router(home.router)
router.include_router(mongo.router, tags=["MongoDB"])

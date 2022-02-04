from fastapi import APIRouter, HTTPException, status
from src.applications.routers import bltouch
from src.applications.routers import camera
from src.utils.apps import NoAppRunningException, ctx_manager

router = APIRouter(prefix="/applications", tags=["Applications"])
router.include_router(camera.router)
router.include_router(bltouch.router)



@router.get("/")
async def read_movements():
    """Get all possible applications."""

    return ["Open Webcam"]


@router.post("/stop")
async def stop_running_app():
    """Stop the running app."""

    try:
        ctx_manager.stop_app()
    except NoAppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "App stopped."}

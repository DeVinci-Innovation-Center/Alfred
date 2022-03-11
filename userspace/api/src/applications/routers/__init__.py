from fastapi import APIRouter, HTTPException, status
from src.applications.routers import aruco, bltouch, camera, grasping
from src.utils.apps import NoAppRunningException, ctx_manager
from src.utils.state import alfred_state

router = APIRouter(prefix="/applications", tags=["Applications"])
router.include_router(camera.router)
router.include_router(bltouch.router)
router.include_router(grasping.router)
router.include_router(aruco.router)


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

    alfred_state.mode = None

    return {"message": "App stopped."}

"""Router for the Camera module."""

from fastapi import APIRouter, HTTPException, status

from src.applications.modules.camera import camera
from src.utils.apps import App, AppRunningException, ctx_manager

router = APIRouter(prefix="/camera", tags=["Applications"])


@router.post("/show-camera")
async def show_camera():
    """Simple show camera function."""

    try:
        app = App(
            target=camera.show_camera,
            f_args=("device-data-realsense",),
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Camera running."}


@router.post("/show-depth")
async def show_depth():
    """Simple show camera function."""

    try:
        app = App(
            target=camera.show_camera,
            f_args=("device-data-realsense-depth",),
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Depth running."}

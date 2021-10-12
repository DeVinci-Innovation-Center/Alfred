from fastapi import APIRouter
from fastapi import HTTPException

from src.modules import utils
from src.utils import NoAppRunningException, ctx_manager, AppRunningException

router = APIRouter()


@router.get("/movement/", tags=["movement"])
async def read_movements():
    """Returns all possible movements."""

    return [{"username": "Rick"}, {"username": "Morty"}]

@router.get("/movement/stop", tags=["movement"])
async def stop_running_app():
    """Stop the running app."""

    try:
        ctx_manager.stop_app()
    except NoAppRunningException as e:
        raise HTTPException(status_code=400, detail=e.message) from None

    return {"message": "App stopped."}

@router.get("/movement/open_webcam", tags=["movement"])
async def open_webcam():
    """Simple open webcam function."""

    try:
        ctx_manager.run_app(utils.open_webcam, video_path="/dev/video0")
    except AppRunningException as e:
        raise HTTPException(status_code=400, detail=e.message) from None

    return {"message": "Camera running."}

from fastapi import APIRouter, HTTPException

from src.modules import utils
from src.utils import App, AppRunningException, NoAppRunningException, ctx_manager
from src.socketio_server import sio as backend_sio_server

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
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=utils.open_webcam,
            f_args=("/dev/video0",)
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(status_code=400, detail=e.message) from None

    return {"message": "Camera running."}

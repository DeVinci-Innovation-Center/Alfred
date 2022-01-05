from fastapi import APIRouter, HTTPException
from src.modules.camera import camera

# from src.modules.hand_control.hand_control import start_hand_control
from src.modules import basic_commands
from src.utils.apps import (
    App,
    AppRunningException,
    NoAppRunningException,
    ctx_manager,
)
from src.utils.global_instances import sio as backend_sio_server

router = APIRouter(prefix="/applications", tags=["Applications"])


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
        raise HTTPException(status_code=400, detail=e.message) from None

    return {"message": "App stopped."}


@router.post("/show-camera")
async def show_camera():
    """Simple show camera function."""

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=camera.show_camera,
            f_args=("device-data-realsense",),
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(status_code=400, detail=e.message) from None

    return {"message": "Camera running."}


# @router.post("/movement/hand_control")
# def hand_control():
#     """xArm hand control."""

#     try:
#         app = App(target=start_hand_control)
#         ctx_manager.run_app(app)
#     except AppRunningException as e:
#         raise HTTPException(status_code=400, detail=e.message) from None

#     return {"message": "Hand control running."}


@router.get("/movement/random")
async def random_move():
    """Make robot move to random location."""

    try:
        app = App(use_sockets=False, socket=None, target=basic_commands.move_random)
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(status_code=400, detail=e.message) from None

    return {"message": "moving randomly."}

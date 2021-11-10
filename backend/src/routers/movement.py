from fastapi import APIRouter, HTTPException
from src.utils.global_instances import sio as backend_sio_server
# from src.modules import basic_commands, utils
from src.modules import utils
from src.utils.apps import (App, AppRunningException, NoAppRunningException,
                       ctx_manager)
from src.modules.hand_control.hand_control import start_hand_control

router = APIRouter()


@router.get("/movement/")
async def read_movements():
    """Returns all possible movements."""

    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/movement/stop")
async def stop_running_app():
    """Stop the running app."""

    try:
        ctx_manager.stop_app()
    except NoAppRunningException as e:
        raise HTTPException(status_code=400, detail=e.message) from None

    return {"message": "App stopped."}


@router.get("/movement/open_webcam")
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

@router.get("/movement/hand_control")
def hand_control():
    """xArm hand control."""

    try:
        app = App(
            target=start_hand_control,
            f_args=("/dev/video0",)
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(status_code=400, detail=e.message) from None

    return {"message": "Hand control running."}


# @router.get("/movement/random")
# async def random_move():
#     """Make robot move to random location."""

#     try:
#         app = App(
#             use_sockets=False,
#             socket=None,
#             target=basic_commands.move_random
#         )
#         ctx_manager.run_app(app)
#     except AppRunningException as e:
#         raise HTTPException(status_code=400, detail=e.message) from None

#     return {"message": "moving randomly."}

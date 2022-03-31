from fastapi import APIRouter, HTTPException, status
from src.applications.modules.aruco import aruco, calibration_cam
from src.utils.apps import App, AppRunningException, ctx_manager
from src.utils.global_instances import sio as backend_sio_server

router = APIRouter(prefix="/aruco", tags=["Applications"])


@router.post("/take-picture")
async def take_picture():
    """Simple show camera function."""

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=calibration_cam.take_picture,
            f_args=("device-data-realsense",),
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Take a picture."}


@router.get("/track/{id_aruco}")
async def robot_scan(id_aruco: int):
    """Move to the initial scanning pose."""

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=aruco.scanning,
            f_args=(id_aruco,),
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "arm moves."}

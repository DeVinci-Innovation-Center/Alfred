from fastapi import APIRouter, HTTPException, status
from src.applications.modules.bltouch import bltouch
from src.utils.apps import App, AppRunningException, ctx_manager
from src.utils.global_instances import sio as backend_sio_server

router = APIRouter(prefix="/bltouch", tags=["Applications"])


@router.post("/calibration")
async def bltouch_calibration():
    """BLTouch calibration."""

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=bltouch.main,
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Calibration running."}

@router.post("/receive")
async def bltouch_receive():
    """BLTouch signal received"""
    try:
        app=App(
            use_sockets=False,
            socket=backend_sio_server,
            target=bltouch.receive_data,
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None
    return {"message": "Receiving signal."}


@router.post("/send")
async def bltouch_calibration():
    """BLTouch activate."""

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=bltouch.send_command,
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Activation running."}
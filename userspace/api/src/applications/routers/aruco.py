from fastapi import APIRouter, HTTPException, status
from applications.modules.aruco import aruco
from utils.apps import App, AppRunningException, ctx_manager
from utils.global_instances import sio as backend_sio_server

router = APIRouter(prefix="/aruco", tags=["Applications"])

@router.post("/detect")
async def stream_aruco():
    """Stream and detect aruco marker."""

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=aruco.stream_aruco,
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Streaming camera with detection of aruco marker."}


@router.get("/track/{id_aruco}")
async def robot_scan(id_aruco: int):
    """Scan the environment to track the aruco."""

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=aruco.scanning,
            f_args=([id_aruco],),
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "arm moves."}

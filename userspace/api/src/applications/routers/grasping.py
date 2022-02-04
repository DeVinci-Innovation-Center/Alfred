from fastapi import APIRouter, HTTPException, status
from src.applications.modules.grasping import main as grasping
from src.utils.apps import App, AppRunningException, ctx_manager
from src.utils.global_instances import sio as backend_sio_server

router = APIRouter(prefix="/grasping", tags=["Applications"])


@router.post("/start-grasping")
async def show_camera():
    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=grasping.main,
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Grasping running."}

from typing import Optional

import requests
from fastapi import APIRouter, Form, HTTPException, status
from applications.modules.grasping import main as grasping
from utils.apps import App, AppRunningException, ctx_manager
from utils.global_instances import sio as backend_sio_server
from utils.state import alfred_state

router = APIRouter(prefix="/grasping", tags=["Applications"])


@router.post("/start-grasping")
async def start_grasping(grasping_target: Optional[str] = Form(None)):
    to_grab = "" if grasping_target is None else grasping_target

    try:
        app = App(
            use_pipe=True,
            target=grasping.main,
            f_args=(to_grab,),
        )
        ctx_manager.run_app(app)
        alfred_state.mode = "grasping"
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Grasping running."}


@router.post("/change_target")
async def change_grasping_target(grasping_target: str = Form(None)):
    if not alfred_state.mode == "grasping":
        return HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Grasping is not running"
        )

    ctx_manager.current_app.parent_conn.send(["flag:update", grasping_target])

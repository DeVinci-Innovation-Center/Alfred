from typing import Optional

import requests
from fastapi import APIRouter, Form, HTTPException, status
from src.applications.modules.grasping import main as grasping
from src.utils.apps import App, AppRunningException, ctx_manager
from src.utils.global_instances import sio as backend_sio_server
from src.utils.state import alfred_state

router = APIRouter(prefix="/grasping", tags=["Applications"])


@router.post("/grasp")
async def grasp(grasping_target: Optional[str] = Form(None)):
    if alfred_state.mode == "grasping":
        pass
    else:
        requests.post(
            "/applications/grasping/start-grasping",
            data={"grasping_target": grasping_target},
        )


@router.post("/start-grasping")
async def start_grasping(grasping_target: Optional[str] = Form(None)):
    to_grab = "" if grasping_target is None else grasping_target

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
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

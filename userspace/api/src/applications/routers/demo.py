from fastapi import APIRouter, HTTPException, status
from src.applications.modules.gripper import gripper
from src.utils.apps import App, AppRunningException, ctx_manager
from src.utils.global_instances import sio as backend_sio_server

router = APIRouter(prefix="/demo", tags=["Applications"])


@router.post("/gripper")
async def demo_gripper():
    """Simple show camera function."""

    try:
        app = App(
            use_sockets=False,
            socket=backend_sio_server,
            target=gripper.grip_demo,
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "Grip an object."}

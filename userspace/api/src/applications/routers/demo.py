import ast
import time


from libalfred import AlfredAPI
from fastapi import APIRouter, HTTPException, status

from applications.modules.gripper import gripper
from applications.modules.handwriting import writing, plot
from utils.apps import App, AppRunningException, ctx_manager
from utils.global_instances import sio as backend_sio_server

from pydantic import BaseModel
from typing import List, Union


class Drawing(BaseModel):
    name: str
    draw_list: Union[List[float], None] = None


router = APIRouter(prefix="/demo", tags=["Applications"])


@router.post("/gripper")
async def demo_gripper():
    """Demo of grasping an object."""

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


@router.post("/write/{word}")
async def write(word: str):
    """Demo writing"""
    try:
        app = App(
            target=writing.write_demo_from_file,
            f_args=(word,),
        )
        ctx_manager.run_app(app)
    except AppRunningException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
        ) from None

    return {"message": "arm moves."}


@router.post("/drawing/")
async def get_draw(draw: Drawing):
    if draw.name != "" or draw.name is not None:
        try:
            app = App(
                target=writing.write_demo_from_ui,
                f_args=(draw.draw_list,),
            )
            ctx_manager.run_app(app)
        except AppRunningException as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=e.message
            ) from None

        return {"msg": "received"}
    else:
        return {"msg": "Fail"}

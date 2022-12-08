import ast
import asyncio
import time

from fastapi import APIRouter, WebSocket
from starlette.responses import RedirectResponse
from src.utils.global_instances import rc
from libalfred import AlfredAPI

router = APIRouter(tags=["Home"])


@router.get("/")
async def redirect():
    response = RedirectResponse(url="/docs")
    return response

@router.websocket("/angle")
async def websocket_angle(websocket: WebSocket):
    """Send the arm angles every 100ms"""
    await websocket.accept()
    arm = AlfredAPI()
    while True:
        await asyncio.sleep(0.1)
        p = arm.get_servo_angle()
        pos = ast.literal_eval(p)
        if pos[0]==0:
            servo_angle = [round(a,2) for a in pos[1][:-1]]
            await websocket.send_json(servo_angle)

#TO DO - not working
@router.websocket("/video")
async def websocket_video(websocket:WebSocket):
    await websocket.accept()
    p = rc.redis_instance.pubsub(ignore_subscribe_messages=True)
    p.subscribe("device-data-realsense")
    t0 = time.time()
    while time.time()-t0<20:
        message = p.get_message()
        if not message:
            time.sleep(0.001)
            continue
        await asyncio.sleep(0.1)
        data = message["data"]
        print(data)
        await websocket.send_bytes(data)

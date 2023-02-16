"""Entrypoint for the ALFRED API."""

import socketio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

import routers, socketio_events
from utils.global_instances import sio

from socketio_events.emits import background_thread_arm_pose

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio_asgi_app = socketio.ASGIApp(socketio_server=sio, socketio_path="socket.io")
app.mount("/ws", sio_asgi_app)
app.include_router(routers.router)

socketio_events.register_routes()
sio.start_background_task(background_thread_arm_pose)

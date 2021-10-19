import src.prelaunch  # pylint: disable=unused-import

src.prelaunch.prelaunch()

from typing import Optional  # pylint: disable=wrong-import-order

import socketio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src import routers
from src.global_instances import sio, rc

DUMMY_VAR: Optional[str]

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio_asgi_app = socketio.ASGIApp(sio, app, socketio_path="/socket.io/")

app.mount("/socket.io/", sio_asgi_app)

app.include_router(routers.router)
app.include_router(routers.router)


@sio.on("disconnect")
def test_disconnect(*_):
    print("Client disconnected")


@sio.on("connect")
def test_connect(*_):
    print("Client connected")


@sio.on("connect_error")
def print_err(*args):
    print(args)


@sio.on("app_watcher")
def get_app_event(*args):
    print(args)

from typing import Optional
import socketio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src import routers
from src.socketio_server import sio
import src.env_getset

DUMMY_VAR: Optional[str]

src.env_getset.set_envs()

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


@app.get("/")
async def read_index():
    return {"message": "Welcome to ALFRED's dashboard."}


@app.get("/hello")
async def hello_world():
    return {"message": "Hello World"}

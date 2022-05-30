import logging

import socketio
from fastapi import FastAPI
from src import routers, socketio_events
from src.utils.global_instances import sio
from starlette.middleware.cors import CORSMiddleware

logger = logging.getLogger("uvicorn.error")


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

socketio_events.register_routes()

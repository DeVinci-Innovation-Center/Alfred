import os

import socketio

from src import global_instances
from src.redis_client import RedisClient

REDIS_HOST = os.getenv("REDIS_HOST", "")
try:
    REDIS_PORT = int(os.getenv("REDIS_PORT", ""))
except ValueError:
    REDIS_PORT = 6379
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


global_instances.rc = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)


global_instances.sio = socketio.Server(cors_allowed_origins="*")
# global_instances.sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


def prelaunch():
    """Dummy function."""

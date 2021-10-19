import os

import socketio
import pymongo

from src import global_instances
from src.redis_client import RedisClient

REDIS_HOST = os.getenv("REDIS_HOST", "")
try:
    REDIS_PORT = int(os.getenv("REDIS_PORT", ""))
except ValueError:
    REDIS_PORT = 6379
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

global_instances.rc = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)


MONGODB_HOST = os.getenv("MONGODB_HOST")
try:
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", "27017"))
except ValueError:
    MONGODB_PORT = 27017
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

if MONGODB_USERNAME is None or MONGODB_PASSWORD is None:
    credentials = ""
else:
    credentials = f"{MONGODB_USERNAME}:{MONGODB_PASSWORD}@"
conn_string = f"mongodb://{credentials}{MONGODB_HOST}:{MONGODB_PORT}"
print(f"{MONGODB_DATABASE=}")

global_instances.mc = pymongo.MongoClient(conn_string)
global_instances.md = global_instances.mc[MONGODB_DATABASE]


global_instances.sio = socketio.Server(cors_allowed_origins="*")
# global_instances.sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


def prelaunch():
    """Dummy function."""

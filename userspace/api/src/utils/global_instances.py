"""Instances to be shared accross the API."""

import logging

import pymongo
import socketio

from libalfred.utils import config_logger
from src.utils import config as cfg
from src.utils.redis_client import RedisClient

config_logger("api", propagate=False)
logger = logging.getLogger("api")

rc = RedisClient(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

sio = socketio.Server(cors_allowed_origins="*")
# sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

mc = pymongo.MongoClient(cfg.MONGO_CONN_STRING)
md: pymongo.database.Database = mc[cfg.MONGODB_DATABASE]

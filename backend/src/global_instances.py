import pymongo
from pymongo.mongo_client import MongoClient
import socketio

from src.redis_client import RedisClient


rc: RedisClient
sio: socketio.Server
mc: pymongo.MongoClient
md: pymongo.database.Database

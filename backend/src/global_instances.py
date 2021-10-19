import socketio

from src.redis_client import RedisClient


rc: RedisClient
sio: socketio.Server

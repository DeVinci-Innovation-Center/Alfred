import socketio

sio = socketio.Server(cors_allowed_origins="*")
# sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

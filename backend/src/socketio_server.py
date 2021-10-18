import socketio

# sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio = socketio.Server(cors_allowed_origins="*")
sio_asgi_app = socketio.ASGIApp(sio, socketio_path="/socket.io")

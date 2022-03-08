import json

import redis
import socketio

from client import config as cfg


def treat_input_cb(sio: socketio.Server):
    def treat_input_cb_inner(message: dict):
        """Treat an input message coming from Redis"""

        data_str = message["data"].decode("utf-8")
        try:
            data = json.loads(f"{data_str}")
        except json.decoder.JSONDecodeError:
            data = {"message": data_str}

        to_rasa = {"sender": cfg.RASA_SENDER_NAME, "message": data["message"]}

        print(f"to send: {to_rasa}")

        # asyncio.run(sio.emit(cfg.RASA_USER_MSG_EVT, to_rasa))
        sio.emit(cfg.RASA_USER_MSG_EVT, to_rasa)

    return treat_input_cb_inner


def register_sio_routes(sio):
    @sio.on(cfg.RASA_BOT_MSG_EVT)
    def receive_rasa_response(response):
        print(response)

    @sio.event
    def connect():
        print("I'm connected!")

    @sio.event
    def connect_error(data):
        print("The connection failed!")
        print(data)

    @sio.event
    def disconnect():
        print("I'm disconnected!")


def main():
    sio = socketio.Client()
    register_sio_routes(sio)

    # setup redis
    rc = redis.Redis(
        cfg.REDIS_HOST, cfg.REDIS_PORT, password=cfg.REDIS_PASSWORD
    )
    rps = rc.pubsub()
    rps.subscribe(**{cfg.RASA_REDIS_INPUT_CHANNEL: treat_input_cb(sio)})

    # listen to messages in thread
    rps_thread = rps.run_in_thread(sleep_time=0.001)

    sio.connect(cfg.RASA_SIO_SERVER_ADDR)

    # program exits with error code 1 by default
    code = 1
    try:
        sio.wait()
    except KeyboardInterrupt:
        # set exit code to 0 if keyboard interrupt
        code = 0
    finally:
        rps_thread.stop()
        exit(code)

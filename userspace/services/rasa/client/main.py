import json
import logging
import time

import redis
import requests
import socketio
from client import config as cfg
from client import utils

utils.config_logger("rasa")
logger = logging.getLogger("rasa")


def treat_input_cb(sio: socketio.Server):
    def treat_input_cb_inner(message: dict):
        """Treat an input message coming from Redis"""

        data_str = message["data"].decode("utf-8")
        try:
            data = json.loads(f"{data_str}")
        except json.decoder.JSONDecodeError:
            data = {"message": data_str}

        to_rasa = {"sender": cfg.RASA_SENDER_NAME, "message": data["message"]}

        logger.debug("to send: %s", to_rasa)

        # asyncio.run(sio.emit(cfg.RASA_USER_MSG_EVT, to_rasa))
        sio.emit(cfg.RASA_USER_MSG_EVT, to_rasa)

    return treat_input_cb_inner


def register_sio_routes(sio, rc: redis.Redis):
    @sio.on(cfg.RASA_BOT_MSG_EVT)
    def receive_rasa_response(response):
        logger.debug("from rasa: %s", response)
        rc.publish(cfg.RASA_REDIS_OUTPUT_CHANNEL, json.dumps(response))

    @sio.event
    def connect():
        logger.info("Connected to socketio server.")

    @sio.event
    def connect_error(data):
        logger.error("Socketio connection failed. Data:\n%s", data)

    @sio.event
    def disconnect():
        logger.info("Disconnected from socketio server.")


def main():
    # wait for rasa server to be running
    logger.info("Waiting for RASA server to be up.")
    code = 0
    while code != 200:
        try:
            r = requests.get(cfg.RASA_SIO_SERVER_ADDR)
            code = r.status_code
        except requests.exceptions.RequestException:
            time.sleep(1)
    logger.info("RASA server running.")

    # setup redis
    rc = redis.Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, password=cfg.REDIS_PASSWORD)
    rps = rc.pubsub()

    sio = socketio.Client()

    register_sio_routes(sio, rc)
    logger.info("Registered socketio routes.")

    rps.subscribe(**{cfg.RASA_REDIS_INPUT_CHANNEL: treat_input_cb(sio)})
    # listen to messages in thread
    rps_thread = rps.run_in_thread(sleep_time=0.001)
    logger.info("Listening to messages from Redis.")

    sio.connect(cfg.RASA_SIO_SERVER_ADDR)

    # program exits with error code 1 by default
    code = 1
    try:
        logger.info("Running indefinitely.")
        sio.wait()
    except KeyboardInterrupt:
        logger.error("KeyboardInterrupt received. Exiting.")
        # set exit code to 0 if keyboard interrupt
        code = 0
    except Exception:
        logger.error("Exception encountered.", exc_info=1)
    finally:
        rps_thread.stop()
        exit(code)

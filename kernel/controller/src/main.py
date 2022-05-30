import json
import logging
import time
import traceback

import redis
from config import cfg
from controller.controller import Controller
from real.robot_real import RobotReal

from libalfred import utils

PROP_PUBSUB_CHANNEL = "robot-props"
FUNC_PUBSUB_CHANNEL = "robot-funcs"


def main():
    utils.config_logger("controller")
    logger = logging.getLogger("controller")

    if cfg.MOVE_ARM:
        logger.info("MOVE_ARM was set to True. Connecting to real arm.")
        robot_real = RobotReal(cfg.ARM_IP)
        robot_real.connect_loop()
        logger.info("Connected to real arm.")
    else:
        logger.info("MOVE_ARM was set to False. Not connecting to real arm.")
        robot_real = None

    rc = redis.Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    controller = Controller(rc, robot_real)

    logger.info("Setting up PubSub.")

    rp = rc.pubsub(ignore_subscribe_messages=True)
    rp.subscribe(cfg.REDIS_CHANNEL)

    rp.subscribe(**{PROP_PUBSUB_CHANNEL: controller.prop_message_handler})
    rp.subscribe(**{FUNC_PUBSUB_CHANNEL: controller.func_message_handler})

    logger.info("Subscribed to channels: %s", list(rp.channels.keys()))
    logger.info("Starting get_message loop.")

    while True:
        message = rp.get_message()
        if message:
            try:
                decoded_msg = message["data"].decode("utf-8")
                json_msg = json.loads(decoded_msg)
                command = utils.Command.from_string(json_msg["command"])
                controller.treat_command(command)
            except Exception:  # pylint: disable = broad-except
                print(traceback.format_exc())

        time.sleep(0.001)


if __name__ == "__main__":
    main()

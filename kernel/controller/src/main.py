import json
import pathlib
import time
import traceback

import redis
from libalfred import utils

from src.config import cfg
from src.controller.controller import Controller
from src.real.robot_real import RobotReal


def main():
    utils.config_logger("controller")

    if cfg.MOVE_ARM:
        robot_real = RobotReal(cfg.ARM_IP)
        robot_real.connect_loop()
    else:
        robot_real = None

    rc = redis.Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    controller = Controller(rc, robot_real)

    rp = rc.pubsub(ignore_subscribe_messages=True)
    rp.subscribe(cfg.REDIS_CHANNEL)

    rp.subscribe({"robot-props": controller.prop_message_handler})

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

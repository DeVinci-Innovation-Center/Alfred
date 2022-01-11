import json
import time
import traceback

import redis
from libalfred import utils

from src.config import cfg
from src.controller.controller import Controller
from src.real.robot_real import RobotReal
from src.sim.robot_sim import RobotSim


def main():
    utils.config_logger("controller")

    if cfg.MOVE_ARM:
        robot_real = RobotReal(cfg.ARM_IP)
        robot_real.connect_loop()
    else:
        robot_real = None

    robot_sim = RobotSim(cfg.END_EFFECTOR_INDEX, cfg.ROBOT_DOFS)

    controller = Controller(robot_real=robot_real, robot_sim=robot_sim)

    rc = redis.Redis(cfg.REDIS_HOST, cfg.REDIS_PORT, cfg.REDIS_PASSWORD)

    rp = rc.pubsub(ignore_subscribe_messages=True)
    rp.subscribe(cfg.REDIS_CHANNEL)

    while True:
        message = rp.get_message()
        if message:
            try:
                decoded_msg = message["data"].decode("utf-8")
                json_msg = json.loads(decoded_msg)
                command = utils.Command.from_string(json_msg["command"])
                controller.decompose_command(command)
            except Exception:
                print(traceback.format_exc())

        time.sleep(0.001)


if __name__ == "__main__":
    main()

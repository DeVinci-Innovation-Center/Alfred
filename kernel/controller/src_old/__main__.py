import json
import os
import time
import traceback

from redis.exceptions import ConnectionError as RedisConnectionError

import src_old.sim.robot_sim as xarm_sim
from src_old.controller import Controller  # type: ignore
from src_old.real.robot_real import XArmReal
from src_old.redis_client import RedisClient
from src_old.command import Command

REDIS_HOST = os.getenv("REDIS_HOST", "0.0.0.0")
REDIS_PORT = os.getenv("REDIS_PORT")
try:
    REDIS_PORT = int(REDIS_PORT)  # type: ignore
except (ValueError, TypeError):
    REDIS_PORT = 6379  # type: ignore
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
REDIS_CHANNELS = os.getenv("REDIS_CHANNELS", "")  # comma separated, no spaces

MOVE_ARM = os.getenv("MOVE_ARM") == True  # pylint: disable=singleton-comparison
ARM_IP = os.getenv("ARM_IP")


def main():
    """Example: move xArm with hand."""

    if MOVE_ARM:
        xarm_real = XArmReal(ARM_IP)
        xarm_real.connect_loop()
    else:
        xarm_real = None

    controller = Controller(move_real=MOVE_ARM, arm_real=xarm_real)
    robot_sim = xarm_sim.XArmSim(controller)
    robot_sim.start()

    try:
        rc = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)
    except RedisConnectionError:
        print(traceback.format_exc())
        return

    channels = REDIS_CHANNELS.split(",")
    rp = rc.redis_instance.pubsub()
    rp.subscribe(*channels)

    while True:
        message = rp.get_message(ignore_subscribe_messages=True)
        if message:
            try:
                decoded_msg = message["data"].decode("utf-8")
                json_msg = json.loads(decoded_msg)
                command = Command.from_string(json_msg["command"])
                # print(f"{command=}")
                controller.decompose_command(command)

            except Exception:
                print(traceback.format_exc())
            # do something with the message
        time.sleep(0.001)  # be nice to the system :)

if __name__ == "__main__":
    main()

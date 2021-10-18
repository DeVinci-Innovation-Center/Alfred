import os
import time
import traceback

from redis.exceptions import ConnectionError as RedisConnectionError

import src.sim.robot_sim as xarm_sim
from src.controller import Controller  # type: ignore
from src.real.robot_real import XArmReal
from src.redis_client import RedisClient

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

    for channel in REDIS_CHANNELS.split(","):
        rc.add_subscriber({channel: RedisClient.print_message})

    while True:
        time.sleep(10)


if __name__ == "__main__":
    main()

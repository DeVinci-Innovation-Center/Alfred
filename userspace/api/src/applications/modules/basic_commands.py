import json
import numpy as np

from libalfred.utils import Command
from utils.global_instances import rc


def move_random():
    """Sends random command to robot."""

    rng = np.random.default_rng()
    random_pos = (rng.random((6,)) - 0.5) / 2.0
    command = Command(
        x=random_pos[0],
        y=random_pos[0],
        z=random_pos[0],
        roll=random_pos[0],
        pitch=random_pos[0],
        yaw=random_pos[0],
        speed=500,
        acc=500,
        is_radian=True,
        is_relative=False,
    )
    redis_command = {"function": "move_line", "command": repr(command)}
    print(redis_command)

    res = rc.redis_instance.publish("commands", json.dumps(redis_command))
    print(res)

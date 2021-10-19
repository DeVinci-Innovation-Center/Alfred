import json
import os

import numpy as np

from src.redis_client import RedisClient
from src.modules.command import Command

REDIS_HOST = os.getenv("REDIS_HOST", "")
try:
    REDIS_PORT = int(os.getenv("REDIS_PORT", ""))
except ValueError:
    REDIS_PORT = 6379
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

rc = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)

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

import json
import os
from typing import Any

import cv2
import numpy as np
import xarm_hand_control.processing.process as xhcpp
from src.modules.command import Command
from src.redis_client import RedisClient

REDIS_HOST = os.getenv("REDIS_HOST", "")
try:
    REDIS_PORT = int(os.getenv("REDIS_PORT", ""))
except ValueError:
    REDIS_PORT = 6379
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")


rc = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD)

def send_command(command: Command):
    redis_command = {"function": "move_line", "command": repr(command)}
    # print(redis_command)

    res = rc.redis_instance.publish("commands", json.dumps(redis_command))
    # print(res)

def coords_extracter():
    """Exctract coords to send command to robot.
    To be executed inside of xarm_hand_control module."""

    SKIPPED_COMMANDS = 5
    COEFF = 22

    current = [0]

    def coords_to_command(data: Any):
        current[0] += 1
        if current[0] < SKIPPED_COMMANDS:
            return

        current[0] = 0

        if np.linalg.norm(data[0:2], 2) < 0.05:
            return

        x = data[0] * COEFF / 1000
        z = data[1] * COEFF / 1000

        # speed = np.linalg.norm(data, ord=2) * COEFF * 50
        # speed = int(speed)
        # # speed = np.log(speed) * COEFF
        # mvacc = speed * 10
        speed = 500
        mvacc = speed * 10

        command = Command(
            x=x,
            y=0.0,
            z=z,
            speed=speed,
            acc=mvacc,
            is_radian=True,
            is_cartesian=True,
            is_relative=True,
        )

        # print(command)

        send_command(command)

    return coords_to_command

def start_hand_control(video_path):
    cap = cv2.VideoCapture(video_path)  # pylint: disable=no-member

    send_command(
        Command(
            0.207,
            0.0,
            0.112,
            180,
            0,
            0,
            speed=10,
            is_radian=False,
            is_cartesian=True,
            is_relative=False,
        )
    )

    send_command(
        Command(
            0.207,
            0.0,
            0.510,
            180,
            0,
            0,
            speed=10,
            is_radian=False,
            is_cartesian=True,
            is_relative=False,
        )
    )

    send_command(
        Command(
            0,
            -0.2278,
            0.6439,
            0,
            -90,
            90,
            speed=10,
            is_radian=False,
            is_cartesian=True,
            is_relative=False,
        )
    )

    xhcpp.loop(cap, coords_extracter_func=coords_extracter())

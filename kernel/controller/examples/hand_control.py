import os
import sys
import threading
from typing import Any

import cv2
import numpy as np
import xarm_hand_control.processing.process as xhcpp

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import src.sim.robot_sim as xarm_sim
from src.command import Command
from src.controller import Controller
from src.real.robot_real import XArmReal
from src.event import post_event

VIDEO_PATH = "/dev/video0"
MOVE_ARM = True
ARM_IP = "172.21.72.200"

lock = threading.Lock()


def send_command(command: Command) -> None:
    """Send extracted command to robot."""

    with lock:
        post_event("new_command", command)


def coords_extracter(controller: Controller):
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

        curr_pos = controller.future_cartesian_pos
        # print(f"{curr_pos=}")

        command = Command(
            x=curr_pos.x + x,
            y=curr_pos.y,
            z=curr_pos.z + z,
            roll=curr_pos.roll,
            pitch=curr_pos.pitch,
            yaw=curr_pos.yaw,
            speed=speed,
            acc=mvacc,
            is_radian=curr_pos.is_radian,
            is_cartesian=True,
            is_relative=False,
        )

        # print(command)

        send_command(command)

    return coords_to_command


def main():
    """Example: move xArm with hand."""

    cap = cv2.VideoCapture(VIDEO_PATH)  # pylint: disable=no-member

    if MOVE_ARM:
        xarm_real = XArmReal(ARM_IP)
        xarm_real.connect_loop()
    else:
        xarm_real = None

    controller = Controller(move_real=MOVE_ARM, arm_real=xarm_real)
    robot_sim = xarm_sim.XArmSim(controller)
    robot_sim.start()

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

    hand_control_thread = threading.Thread(
        target=xhcpp.loop,
        args=[
            cap,
        ],
        kwargs={"coords_extracter_func": coords_extracter(controller)},
        daemon=True,
    )
    hand_control_thread.start()

    hand_control_thread.join()


if __name__ == "__main__":
    main()

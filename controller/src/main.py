import os
import sys
import threading
from typing import Any

import cv2
import numpy as np
import xarm_hand_control.processing.process as xhcpp

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import src.sim.robot_sim as xarm_sim
from src.controller import Controller
from src.real.robot_real import XArmReal

MOVE_ARM = True
ARM_IP = "172.21.72.200"


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


if __name__ == "__main__":
    main()

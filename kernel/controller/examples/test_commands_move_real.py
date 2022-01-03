import asyncio
import math
import os
import sys
import threading
import time
from typing import Any

import pybullet as p
import pybullet_data as pd
from xarm.wrapper import XArmAPI

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import src.sim.robot_sim as xarm_sim
from src.command import Command


ARM_IP = "172.21.72.200"


def send_command(command: list) -> None:
    xarm_sim.command_queue.put(command)


def worker(robot: Any, timeStep: float) -> None:
    # create asyncio event loop to fire and forget command decomposition
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while 1:
        robot.step()
        p.stepSimulation()
        time.sleep(timeStep)


def setup_pybullet(time_step: float) -> None:
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pd.getDataPath())


def setup_arm():
    arm = "dummy"

    connected = False
    while not connected:
        try:
            arm = XArmAPI(ARM_IP, do_not_open=True)
            arm.connect()
            connected = True
        except:
            print("arm is not online. trying again in 3 seconds...")
            time.sleep(3)

    arm.motion_enable(enable=True)
    arm.set_mode(mode=0)
    arm.set_state(state=0)
    time.sleep(1)

    arm.move_gohome(speed=50, mvacc=500)

    time.sleep(1)
    arm.set_mode(mode=1)
    arm.set_state(state=0)
    time.sleep(1)

    return arm


def main():
    arm = setup_arm()
    # time_step = 20.0 / 60.0
    time_step = 1.0 / 60.0
    setup_pybullet(time_step=time_step)
    robot = xarm_sim.XArm6Sim(p, move_real=True, arm=arm)
    worker_thread = threading.Thread(
        target=worker, args=[robot, time_step], daemon=True
    )
    worker_thread.start()

    for x in range(3):
        print(x)
        time.sleep(1)

    send_command(
        Command(
            0.3,
            0.3,
            0.3,
            math.pi,
            0.0,
            0.0,
            is_radian=True,
            is_cartesian=True,
            speed=10,
        )
    )
    time.sleep(1)
    send_command(
        Command(
            0.5,
            0.0,
            0.2,
            180.0,
            0.0,
            0.0,
            is_radian=False,
            is_cartesian=True,
            speed=10,
        )
    )
    time.sleep(1)
    send_command(
        Command(
            0.3,
            -0.3,
            0.3,
            math.pi,
            0.0,
            0.0,
            is_radian=True,
            is_cartesian=True,
            speed=10,
        )
    )
    time.sleep(1)
    send_command(
        Command(
            0.3,
            0.3,
            0.3,
            math.pi,
            0.0,
            0.0,
            is_radian=True,
            is_cartesian=True,
            speed=10,
        )
    )

    worker_thread.join()


if __name__ == "__main__":
    main()

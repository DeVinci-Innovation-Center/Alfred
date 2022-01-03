import math
import os
import sys
import threading
import time
from typing import Any

import pybullet as p
import pybullet_data as pd

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import src.sim.robot_sim as xarm_sim
from src.command import Command
from src.controller import Controller


def send_command(controller: Controller, command: Command) -> None:
    controller.command_queue.put(command)


def worker(robot: Any, time_step: float) -> None:
    # create asyncio event loop to fire and forget command decomposition
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)

    while 1:
        robot.step()
        p.stepSimulation()
        time.sleep(time_step)


def setup_pybullet(time_step: float) -> None:
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pd.getDataPath())


def main():
    # time_step = 20.0 / 60.0
    time_step = 1.0 / 60.0
    setup_pybullet(time_step=time_step)

    controller = Controller()
    xarm = xarm_sim.XArm6Sim(p, controller)

    for x in range(3):
        print(x)
        time.sleep(1)

    worker_thread = threading.Thread(
        target=worker, args=[xarm, time_step], daemon=True
    )
    worker_thread.start()

    send_command(
        controller,
        Command(
            0.3, 0.3, 0.3, math.pi, 0.0, 0.0, is_radian=True, is_cartesian=True, speed=10
        )
    )
    time.sleep(1)
    send_command(
        controller,
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
        controller,
        Command(
            0.3, -0.3, 0.3, math.pi, 0.0, 0.0, is_radian=True, is_cartesian=True, speed=10
        )
    )
    time.sleep(1)
    send_command(
        controller,
        Command(
            0.3, 0.3, 0.3, math.pi, 0.0, 0.0, is_radian=True, is_cartesian=True, speed=10
        )
    )

    worker_thread.join()


if __name__ == "__main__":
    main()

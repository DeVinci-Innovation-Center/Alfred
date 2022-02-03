import time
from typing import Optional

import redis
from libalfred.utils import Command
from src.real.robot_real import RobotReal


class Controller:
    """Controller class for ALFRED. Handles treating commands, moving the arm,
    and using environment data to influence robot paths."""

    PROP_PUBSUB_CHANNEL = "robot-props"
    FUNC_PUBSUB_CHANNEL = "robot-funcs"

    rc: redis.Redis
    robot_real: Optional[RobotReal]

    def __init__(
        self, rc: redis.Redis, robot_real: Optional[RobotReal] = None,
    ):
        self.rc = rc
        self.robot_real = robot_real

    def loop(self, time_step: float = 1 / 60):
        """Actions that should execute in a loop
        (by default, 60 times per second)"""
        while True:
            if self.robot_real is not None:
                arm_pos_cartesian = self.robot_real.position
                arm_pos_angles = self.robot_real.position_aa

                print(arm_pos_angles, arm_pos_cartesian)

            time.sleep(time_step)

    def treat_command(self, command: Command):
        """Interpret and execute command."""

        command = self.check_command(command)

        if self.robot_real is not None:
            try:
                self.treat_command_real(command)
            except Exception:  # pylint: disable = broad-except
                pass

        # if self.show_sim:
        #     try:
        #         self.treat_command_sim(command)
        #     except Exception:  # pylint: disable = broad-except
        #         pass

    def check_command(self, command: Command):
        """Analyze and modify command if needed.
        Check collisions, path, etc..."""

        return command

    def treat_command_real(self, command: Command):
        """Interpret and execute command for the real robot."""

    def treat_command_sim(self, command: Command):
        """Interpret and execute command for the simulated robot."""

    def prop_message_handler(self, message):
        data = message["data"]

        kw, value = data.split(":")

        if kw == "ret":
            return

        if kw == "get":
            try:
                to_send = self.robot_real.__getattr__(value)
            except Exception:
                print("exception occured")
                to_send = "i'm sending something"

            self.rc.publish(self.PROP_PUBSUB_CHANNEL, f"ret:{to_send}")

        if kw == "set":
            prop_name, prop_val = value.split("=")

import json
import logging
import time
from typing import Optional
import traceback

import redis
from libalfred.utils import Command
from real.robot_real import RobotReal


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

        self.logger = logging.getLogger("controller.controller")

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
        data = message["data"].decode("utf-8")

        self.logger.debug("Got property message: %s", data)

        kw, value = data.split(":", 1)

        if kw == "ret":
            return

        if kw == "get":
            prop_name = value

            try:
                to_send = getattr(self.robot_real, prop_name)
            except AttributeError:
                self.logger.error(
                    "User tried to access attribute %s but it doesn't exist.",
                    prop_name,
                )
                to_send = "AttributeError"
                error = traceback.format_exc()
                print(error)

            self.rc.publish(
                self.PROP_PUBSUB_CHANNEL, f"ret:{prop_name}={to_send}"
            )

            return

        # if kw == "set":
        #     prop_name, prop_val = value.split("=")

    def func_message_handler(self, message):
        data = message["data"].decode("utf-8")

        self.logger.debug("Got function message: %s", data)

        kw, value = data.split(":", 1)

        if kw == "ret":
            return

        if kw == "exec":
            func_dict = json.loads(value)
            try:
                to_call_name = func_dict["name"]
                to_call_args = func_dict["args"]
                to_call_kwargs = func_dict["kwargs"]
                to_call = getattr(self.robot_real, to_call_name)
                print(f"{to_call=}")
                print(f"{to_call_args=}")
                print(f"{to_call_kwargs=}")
                ret = to_call(*to_call_args, **to_call_kwargs)
                # ret = to_call(**to_call_kwargs)
            except AttributeError:
                self.logger.error(
                    (
                        "User tried to call function %s with args %s and "
                        "kwargs %s but it doesn't exist."
                    ),
                    func_dict["name"],
                    func_dict["args"],
                    func_dict["kwargs"],
                )
                ret = "AttributeError"
                error = traceback.format_exc()
                print(error)

            self.rc.publish(self.FUNC_PUBSUB_CHANNEL, f"ret:{ret}")

            return

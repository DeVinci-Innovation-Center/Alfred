import logging
import queue
import threading
from functools import singledispatchmethod
from operator import add
import time
from typing import List, Optional

import numpy as np
from libalfred.utils import Command, Position
from src.config import cfg
from src.controller.trajectory import compute_trajectory
from src.real.robot_real import RobotReal
from src.sim.robot_sim import RobotSim

logger = logging.getLogger("controller.controller")


class Controller:
    """Robot controller class. Holds global variables used when
    controlling the robot."""

    dofs: int
    end_effector_index: int
    max_speed: int
    move_real: bool

    robot_sim: RobotSim
    robot_real: Optional[RobotReal]

    use_null_space: bool
    use_dynamics: bool

    cartesian_pos: Position
    future_cartesian_pos: Position
    joint_positions: List[int]

    decomposed_command_queue: queue.Queue

    sim_thread: threading.Thread

    def __init__(
        self,
        robot_sim: RobotSim,
        robot_real: Optional[RobotReal] = None,
        use_null_space: bool = False,
        use_dynamics: bool = True,
    ):
        self.dofs = cfg.ROBOT_DOFS
        self.end_effector_index = cfg.END_EFFECTOR_INDEX
        self.max_speed = cfg.MAX_SPEED
        self.move_real = cfg.MOVE_ARM

        self.robot_sim = robot_sim
        self.robot_real = robot_real
        self.use_null_space = use_null_space
        self.use_dynamics = use_dynamics

        self.cartesian_pos = Position()
        self.future_cartesian_pos = Position()

        if not self.move_real:
            self.joint_positions = [0] * self.dofs

        elif self.move_real and self.robot_real is not None:
            if self.robot_real.default_is_radian:
                self.joint_positions = self.robot_real.angles
            else:
                self.joint_positions = list(np.deg2rad(self.robot_real.angles))

        elif self.move_real and self.robot_real is None:
            raise Exception("move_real is True but robot_real is None")

        self.decomposed_command_queue = queue.Queue()

        logger.info("Initialized controller.")
        logger.info("Starting sim thread.")

        self.cartesian_pos = self.robot_sim.set_base_pose(self.joint_positions)
        self.future_cartesian_pos = self.cartesian_pos

        self.start_sim_thread()

        logger.info("Sim thread started.")

    def start_sim_thread(self):
        self.sim_thread = threading.Thread(target=self.robot_sim.run)
        self.sim_thread.daemon = True
        self.sim_thread.start()

    @singledispatchmethod
    def decompose_command(self, command: Command):
        """Create intermediate points from a Command to generate a path."""

        logger.debug("Received command: %s", repr(command))

        if command.is_relative:
            non_relative_xyzrpy = list(
                map(add, self.future_cartesian_pos.xyzrpy, command.xyzrpy)
            )
            goal_xyzrpy = Position(*non_relative_xyzrpy)
        else:
            goal_xyzrpy = Position(*command.xyzrpy)

        logger.debug("Goal xyzpry: %s", repr(goal_xyzrpy))

        if command.is_cartesian:
            traj_type = "lspb"
        else:
            traj_type = "tpoly"

        if command.speed > self.max_speed:
            steps = 1
        else:
            steps = self.max_speed // command.speed

        goal_traj = compute_trajectory(
            traj_type, self.future_cartesian_pos, goal_xyzrpy, steps
        )

        points = goal_traj.q

        for point in points:
            self.decomposed_command_queue.put(point)

        self.future_cartesian_pos = goal_xyzrpy

    @decompose_command.register
    def _(self, command: str):
        """Create intermediate points from a string representing a Command to
        generate a path."""

        new_command = Command.from_string(command)
        self.decompose_command(new_command)

    def run(self):
        while 1:
            self.step()
            self.robot_sim.stepSimulation()
            time.sleep(self.robot_sim.time_step)

    def run_ik(self, xyzrpy: list):
        xyz = xyzrpy[:3]
        rpy = xyzrpy[3:]

        rpy_quaternion = self.robot_sim.get_quaternion_from_euler(rpy)

        target_joint_positions = self.robot_sim.calculateInverseKinematics(
            xyz, rpy_quaternion,
        )

        return target_joint_positions

    def move(self, target_joint_positions: list):
        self.robot_sim.move()

        if cfg.MOVE_ARM:
            self.robot_real.set_servo_angle_j(  # type: ignore
                target_joint_positions, is_radian=True,
            )

    def reset(self):
        pass

    def step(self):
        try:
            target_position = self.decomposed_command_queue.get(block=False)

            self.decomposed_command_queue.task_done()
        except queue.Empty:
            return

        target_joint_positions = self.run_ik(target_position)

        self.move(target_joint_positions)

        self.joint_positions = target_joint_positions
        self.cartesian_pos = self.robot_sim.get_cartesian_pos(compute=True)

        RobotSim.add_user_debug_line(
            self.cartesian_pos[:3], target_position[:3],
        )

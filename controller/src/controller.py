import queue
from typing import List, Optional

import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox.tools.trajectory import Trajectory

from .real.robot_real import XArmReal
from .command import Position, Command
from .event import subscribe, post_event

# * -----------------------------------------------------------------
# * GLOBAL VARIABLES
# * -----------------------------------------------------------------
ROBOT_DOFS = 6
END_EFFECTOR_INDEX = 6
MAX_SPEED = 1000
# * -----------------------------------------------------------------

# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-locals


class Controller:
    """Robot controller class. Holds global variables used when controlling the robot."""

    DOFs: int
    end_effector_index: int
    max_speed: int

    move_real: bool
    arm_real: Optional[XArmReal]
    use_null_space: bool
    use_dynamics: bool

    cartesian_pos: Position
    future_cartesian_pos: Position
    joint_positions: List[int]

    decomposed_command_queue: queue.Queue

    def __init__(
        self,
        move_real: bool = False,
        arm_real: Optional[XArmReal] = None,
        use_null_space: bool = False,
        use_dynamics: bool = True,
    ):
        if move_real and arm_real is None:
            raise Exception("arm must not be None if move_real is True")

        self.DOFs = ROBOT_DOFS
        self.end_effector_index = END_EFFECTOR_INDEX
        self.max_speed = MAX_SPEED
        # self.ll = ll
        # self.ul = ul
        # self.jr = jr
        # sefl.rp = rp

        self.move_real = move_real
        self.arm_real = arm_real
        self.use_null_space = use_null_space
        self.use_dynamics = use_dynamics

        self.cartesian_pos = Position()
        self.future_cartesian_pos = Position()
        if move_real and self.arm_real.connected:  # type: ignore
            if self.arm_real.default_is_radian:  # type: ignore
                self.joint_positions = self.arm_real.angles  # type: ignore
            else:
                self.joint_positions = list(np.deg2rad(self.arm_real.angles))  # type: ignore
        else:
            self.joint_positions = [0] * self.DOFs

        self.decomposed_command_queue = queue.Queue()

        subscribe("new_command_str", decompose_commands)
        subscribe("new_command", self.decompose_command)

    def decompose_command(self, command: Command):
        """Create intermediate points from a Command to generate a path."""
        # print(command)

        goal_xyzrpy = Position(*command.xyzrpy)
        # goal_xyzrpy = list(map(lambda x: round(x, 4), goal_xyzrpy))
        # print(goal_xyzrpy)

        if command.is_cartesian:
            traj_type = "lspb"
        else:
            traj_type = "tpoly"

        # print(command.speed, self.max_speed, self.max_speed // command.speed)

        if command.speed > self.max_speed:
            steps = 1
        else:
            steps = self.max_speed // command.speed

        goal_traj = compute_trajectory(
            traj_type, self.future_cartesian_pos, goal_xyzrpy, steps
        )

        points = goal_traj.q
        # print(f"{points=}")

        for point in points:
            self.decomposed_command_queue.put(point)

        self.future_cartesian_pos = command


def decompose_commands(command_str: str):
    """Loop for getting commands and decomposing them."""

    new_command = Command.from_string(command_str)

    post_event("decompose_new_command", new_command)


def compute_trajectory(
    traj_type: str,
    origin: Position,
    goal: Position,
    step: int,
    origin_qd: float = 0.002,
    goal_qd: float = 0.002,
) -> rtb.tools.trajectory.Trajectory:
    """Compute a roboticstoolbox Trajectory from origin and goal positions."""
    # print(f"{origin=}\n{goal=}\n")

    trajs = []
    for origin_q, goal_q in zip(origin.xyzrpy, goal.xyzrpy):

        if traj_type == "lspb":
            traj_func = rtb.tools.trajectory.lspb
            args = [origin_q, goal_q, step]
        elif traj_type == "tpoly":
            traj_func = rtb.tools.trajectory.tpoly
            args = [origin_q, goal_q, step, origin_qd, goal_qd]

        if origin_q == goal_q:
            trajs.append(
                Trajectory(
                    traj_type,
                    step,
                    [origin_q] * step,
                    [0] * step,
                    [0] * step,
                    istime=False,
                )
            )
        else:
            trajs.append(traj_func(*args))

    x = trajs[0].t
    y = np.array([tg.s for tg in trajs]).T
    yd = np.array([tg.sd for tg in trajs]).T
    ydd = np.array([tg.sdd for tg in trajs]).T

    istime = trajs[0].istime

    return Trajectory("mtraj", x, y, yd, ydd, istime)

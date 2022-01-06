import numpy as np
import roboticstoolbox as rtb
from libalfred.utils import Position
from roboticstoolbox.tools.trajectory import Trajectory


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

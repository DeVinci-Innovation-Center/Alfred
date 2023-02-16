import ast
import numpy as np

from libalfred import AlfredAPI
from utils.global_instances import rc


def research_linear(
    arm: AlfredAPI,
    precisionStep: float = 0.5,
    speed: float = 50.0,
    mvacc: float = 100.0,
):
    data = None
    p = rc.redis_instance.pubsub()
    p.subscribe("device-data-imu")
    while data is None:  # move z position until bltouch detects the table
        arm.set_position(
            z=-precisionStep, speed=speed, mvacc=mvacc, relative=True, wait=True
        )
    p = arm.get_position()  # return string "[0,[x,y,z,r,y,p]]"
    try:
        pos = ast.literal_eval(p)[1]
    except:
        pos = p[1]
    return [round(coord, 1) for coord in pos[:3]]  # only XYZ coord


def get_pen_height(
    arm: AlfredAPI, position: np.ndarray, cartesian_equation: np.ndarray
) -> float:
    arm.set_position(*position, speed=50, mvacc=100)
    x, y = position[:2]
    z = 151.6
    a, b, c, d = cartesian_equation
    # x, y, z = research_linear(arm)
    z_cartesian = -1 / c * (a * x + b * y + d)
    return round(z - z_cartesian, 2)

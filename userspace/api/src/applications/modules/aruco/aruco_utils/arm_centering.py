import numpy as np

from typing import Tuple

from libalfred import AlfredAPI

def get_xy_diff(corner: np.array, x_center: float = 320., y_center: float = 240., tolerance_diff: float = 10.) -> Tuple[float, float]:
    """Set the angle for the robot

    :param corner: top-left corner of the ArUco marker
    :type corner: np.array
    :return: angles for x,y to move
    :rtype: Tuple[float,float]
    """
    angle = 2.
    x, y = corner[0][0]
    x_angle, y_angle = 0, 0
    x_center, y_center = 320, 240
    tolerance_diff = 10  # tolerance for the centering

    x_is_centered = (-tolerance_diff < x-x_center < +tolerance_diff)
    y_is_centered = (-tolerance_diff < y - y_center < +tolerance_diff)
    if not (x_is_centered & y_is_centered):
        if not x_is_centered:
            x_angle = angle if x < x_center else -angle
        if not y_is_centered:
            y_angle = angle if y > y_center else -angle
        return x_angle, y_angle
    else:
        return None


def center_camera(arm: AlfredAPI, xy_diff: np.array = np.array([0, 0]), precision: int = 1):
    """Center the camera depending on xy_diff

    :param arm: xArm
    :type arm: AlfredAPI
    :param xy_diff: angles given to the servo 1 & 5
    :type xy_diff: np.array
    :param precision: _description_, defaults to 1
    :type precision: int, optional
    """
    j1 = xy_diff[0] / precision
    j5 = xy_diff[1] / precision

    try:
        ret = arm.set_servo_angle(servo_id=1, angle=j1, relative=True)
        ret = arm.set_servo_angle(servo_id=5, angle=j5, relative=True)
    except Exception as e:
        print(e)

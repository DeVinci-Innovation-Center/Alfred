import math
from typing import List, Union

from torch._C import Value


def get_xyxy_center_point(xyxy: list) -> list:
    center_x = (xyxy[0] + xyxy[2]) / 2.0
    center_y = (xyxy[1] + xyxy[3]) / 2.0

    return [center_x, center_y]


def xy_diff(xy1: list, xy2: list) -> list:
    if not len(xy1) == len(xy2):
        raise ValueError("xy1 and xy2 must be of same length.")

    return [xy1[i] - xy2[i] for i in range(len(xy1))]


def xy_softequals(xy1: list, xy2: list, abs_tol: Union[float, List[float]]) -> bool:
    """Returns True if xy1 is almost equal to xy2."""

    if isinstance(abs_tol, float):
        abs_tol = [abs_tol, abs_tol]

    softequals = [math.isclose(xy1[i], xy2[i], abs_tol=abs_tol[i]) for i in range(2)]
    return all(softequals)

import numpy as np
import svgpathtools
import time
import os

from libalfred import AlfredAPI
from .trajectory_path import TrajectoryPath, TrajectoryPaths
from .pen_height import get_pen_height
from typing import Any, List


def write_letter(
    arm: AlfredAPI, path: TrajectoryPath, init_pos: np.ndarray, z_offset: float
) -> None:
    coords = path.get_points()
    first = True
    for coord in coords:
        if coord[-1] == "M":
            if not first:
                arm.set_position(
                    z=z_offset, wait=False, speed=50, relative=True
                )  # move up
            else:
                first = False
            arm.set_position(x=coord[0], y=coord[1], wait=False, speed=100)
            arm.set_position(z=coord[2], speed=30, wait=False)
            continue
        arm.set_position(
            x=coord[0],
            y=coord[1],
            z=coord[2],
            wait=False,
            speed=30,
        )
    arm.set_position(z=z_offset, wait=False, speed=50, relative=True)  # move up


def write_from_file(
    arm: AlfredAPI,
    filename: str,
    init_pos: np.ndarray,
    pen_tip_height: float,
    cartesian_equation: np.ndarray,
    z_offset: float,
) -> None:
    paths = TrajectoryPaths(
        filename, cartesian_equation, pen_tip_height, xy_start=init_pos[:2]
    )
    for path in paths.list_path:
        write_letter(arm, path, init_pos, z_offset)
    arm.set_position(*init_pos, wait=False, speed=50)
    time.sleep(1)
    p = arm.get_is_moving()
    move = eval(p)
    while move:
        time.sleep(0.3)
        p = arm.get_is_moving()
        move = eval(p)


def write_demo_from_file(word: str) -> None:
    arm = AlfredAPI()
    init_pos = np.array([35, 210, 180, 180, -54.1, 77.6])
    dir = "applications/modules/handwriting/svg/"
    filename = word[0].lower() + ".svg"
    if filename not in os.listdir(dir):
        exit(1)
    path = dir + filename
    z_offset = 10
    cartesian_equation = [2, -8, -320, 62240]
    pen_tip_height = get_pen_height(arm, init_pos, cartesian_equation)
    arm.set_position(*init_pos, wait=False, speed=50, mvacc=10)
    write_from_file(arm, path, init_pos, pen_tip_height, cartesian_equation, z_offset)


def _to_svgpath(tab: List[float]) -> svgpathtools.path.Path:
    path = ""
    start = True
    x_old, y_old = None, None
    for i in range(0, len(tab) - 3, 3):
        x, y, t = tab[i : i + 3]
        if x == 0 or y == 0:
            break
        if x == x_old and y == y_old:
            continue
        if x == -1 or y == -1:
            start = True
            continue
        if start:
            path += "M "
            start = False
        else:
            path += "L "
        path += f"{str(int(x))},{str(int(y))} "
        x_old, y_old = x, y
    return svgpathtools.parse_path(path)


def list_to_svgpath(
    path: List[float], svg_scale: float = 1.0, svg_width: int = 2560
) -> svgpathtools.path.Path:
    svg_path = _to_svgpath(path)
    svg_translate = svg_scale * svg_width
    svg_path = svg_path.scaled(-svg_scale, svg_scale)
    svg_path = svg_path.translated(svg_translate)
    return svg_path


def write_from_ui(
    arm: AlfredAPI,
    draw_list: List[float],
    init_pos: np.ndarray,
    pen_tip_height: float,
    cartesian_equation: np.ndarray,
    z_offset: float,
) -> None:
    svg_path = list_to_svgpath(draw_list, svg_scale=0.05)
    path = TrajectoryPath(
        svg_path, cartesian_equation, pen_tip_height, xy_start=init_pos[:2]
    )
    write_letter(arm, path, init_pos, z_offset)
    arm.set_position(*init_pos, speed=50)
    time.sleep(1)
    p = arm.get_is_moving()
    move = eval(p)
    while move:
        time.sleep(0.3)
        p = arm.get_is_moving()
        move = eval(p)


def write_demo_from_ui(draw_list: List[float]) -> None:
    arm = AlfredAPI()
    init_pos = np.array([35, 210, 180, 180, -54.1, 77.6])
    z_offset = 10
    cartesian_equation = [2, -8, -320, 62240]
    pen_tip_height = get_pen_height(arm, init_pos, cartesian_equation)
    arm.set_position(*init_pos, wait=False, speed=50, mvacc=10)
    write_from_ui(
        arm, draw_list, init_pos, pen_tip_height, cartesian_equation, z_offset
    )

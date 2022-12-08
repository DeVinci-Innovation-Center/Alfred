import numpy as np
import os

from libalfred import AlfredAPI
from .trajectory_path import TrajectoryPath, TrajectoryPaths
from typing import Any, List


def write_letter(
    arm: AlfredAPI, path: TrajectoryPath, init_pos: np.ndarray, z_offset: float
) -> None:
    coords = path.get_points()
    for coord in coords:
        if coord[-1] == "M":
            arm.set_position(z=z_offset, wait=True, speed=50, relative=True)  # move up
            arm.set_position(
                x=init_pos[0] + coord[0], y=init_pos[1] + coord[1], wait=True, speed=100
            )
            arm.set_position(z=coord[2], speed=30, wait=True)
            continue
        arm.set_position(
            x=init_pos[0] + coord[0],
            y=init_pos[1] + coord[1],
            z=coord[2],
            wait=False,
            speed=30,
        )
    arm.set_position(z=z_offset, wait=True, speed=50, relative=True)  # move up


def write_from_file(
    arm: AlfredAPI,
    filename: str,
    init_pos: np.ndarray,
    pen_tip_height: float,
    cartesian_equation: np.ndarray,
    z_offset: float,
) -> None:
    paths = TrajectoryPaths(filename, cartesian_equation, pen_tip_height)
    for path in paths.list_path:
        write_letter(arm, path, init_pos, z_offset)
    arm.set_position(*init_pos, wait=True, speed=100)


def write_demo(word: str)->None:
    arm = AlfredAPI()
    init_pos = np.array([35, 200, 170, 180, -54.1, 77.6])
    dir = "src/applications/modules/handwriting/svg/"
    filename = word[0].lower() + ".svg"
    if filename not in os.listdir(dir):
        exit(1)
    path = dir + filename
    z_offset = 10
    pen_tip_height = -46
    pen_tip_height = 40
    cartesian_equation = [20, -77, -2800, 546940]
    arm.set_position(*init_pos, wait=True, speed=50, mvacc=10)
    write_from_file(arm, path, init_pos, pen_tip_height, cartesian_equation, z_offset)

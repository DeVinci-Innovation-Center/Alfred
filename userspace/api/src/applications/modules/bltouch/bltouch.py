import json
import libalfred
import numpy as np
import time

from redis.client import PubSub
from src.utils.global_instances import rc
from typing import List

def mouvement_coordinates(precision: str = "default") -> List[List[float]]:
    """Get all the coordinates for the robot

    :param precision: precision, defaults to "default"
    :type precision: str, optional
    :return: matrix of coordinates
    :rtype: List[List[float]]
    """

    pos = [215, -215, -134, 180, 0, -50]
    #pos = [215, -215, -34, 180, 0, -50]
    times = 5
    start_x, stop_x = pos[0], pos[0] + 200  # 350
    start_y, stop_y = pos[1] - 200, pos[1] + 10
    data = []
    if precision == "high":
        times = 10
    elif precision == "low":
        times = 2
    coor = []
    col = []
    step_x = np.linspace(start_x, stop_x, num=times).tolist()
    step_y = np.flip(np.linspace(start_y, stop_y, num=times)).tolist()
    for i in range(times):
        for j in range(times):
            l = [step_x[i], step_y[j]] + pos[2:]
            col.append(l)
        data.append(col)
        col = []
    return data


def send_command(command: str = "activate") -> None:
    """Send a command to "device-command-bltouch"

    :param command: command, defaults to "activate"
    :type command: str, optional
    """
    redis_command = {"function": "activate-bltouch", "data": repr(command)}
    # print(redis_command)

    res = rc.redis_instance.publish(
        "device-command-bltouch", json.dumps(redis_command))
    # print(res)


def receive_data() -> str:
    """Receive the data from "device-data-bltouch" Redis channel,
    data = None if nothing is received

    :return: data
    :rtype: str
    """
    data = None
    p = rc.redis_instance.pubsub()
    p.subscribe("device-data-bltouch")
    msg = p.get_message(ignore_subscribe_messages=True)
    if msg:
        data = msg["data"].decode("utf-8")
    return data


def research_surface(research: str = "linear") -> float:
    """Make the research at one specific point

    :param research: type of research (linear,logarithm,minmax), defaults to "linear"
    :type research: str, optional
    :raises ValueError: _description_
    :return: value of 
    :rtype: float
    """
    if research == "linear":
        research_linear()
    elif research == "logarithmic":
        research_logarithmic()
    elif research == "minmax":
        research_minmax()
    else:
        raise ValueError("Invalid research mode.")
    return 1.  # arm.get_position()[1][2]


def research_linear(precisionMove: float = 0.1) -> None:
    data = None
    send_command()
    time.sleep(0.5)  # wait push-pin DOWN
    while data:  # move z position until bltouch detects the table
        # arm.set_position(
        #    z=-precisionMove, speed=speed, mvacc=mvacc, relative=True, wait=False
        # )
        data = receive_data()


def research_logarithmic(precisionRate: float = 0.5, maxMove: float = 4.) -> None:
    while maxMove > precisionRate:
        data = None
        send_command()
        time.sleep(0.5)  # wait push-pin DOWN
        while data:
            # arm.set_position(
            #    z=-maxMove, speed=speed, mvacc=mvacc, relative=True, wait=True
            # )
            data = receive_data()
        # arm.set_position(
        #    z=+maxMove, speed=speed, mvacc=mvacc, relative=True, wait=True
        # )  # allow to set the robot at the last position
        maxMove = round(maxMove/2, 1)


def research_minmax(minMove: float = 0.1, maxMove: float = 4.) -> None:
    data = None
    send_command()
    time.sleep(0.5)  # wait push-pin DOWN
    while data:
        # arm.set_position(z=-maxMove, speed=speed, mvacc=mvacc,
        #                 relative=True, wait=True)
        data = receive_data()
    print("Sucess 1")
    data = None
    send_command()
    time.sleep(0.5)  # wait push-pin DOWN
    # arm.set_position(z=+maxMove, speed=speed, mvacc=mvacc,
    #                 relative=True, wait=True)
    while data:
        # arm.set_position(z=-minMove, speed=speed, mvacc=mvacc,
        #                 relative=True, wait=False)
        data = receive_data()
    print("Sucess 2")


def main():
    coordinates = mouvement_coordinates(precision="low")
    len_col, len_row = len(coordinates[0]), len(coordinates[1])
    x_values = np.zeros(len_row)
    y_values = np.zeros(len_col)
    z_values = np.zeros((len_col, len_row))
    for i in range(len_col):
        for j in range(len_row):
            # arm.set_position(*coordinates[i][j],
            #                 speed=speed, mvacc=mvacc, wait=True)

            z_values[i][j] = research_surface(research="minmax")
            if i == 0:
                x_values[j] = coordinates[j][0][0]
            if j == 0:
                y_values[i] = coordinates[0][i][1]
            # arm.set_position(*coordinates[i][j],
            #                 speed=speed, mvacc=mvacc, wait=True)
    #arm.set_position(*init_pos, speed=speed, mvacc=mvacc, wait=False)

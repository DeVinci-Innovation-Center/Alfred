import ast
import json
import numpy as np
import time

from libalfred import AlfredAPI
from multiprocessing.sharedctypes import SynchronizedBase
from redis.client import PubSub
from src.utils.global_instances import rc
from typing import List,Tuple,Union

speed = 50
mvacc = 1000

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


def receive_data(p: PubSub, data_value: SynchronizedBase=None) -> str:
    """Receive the data from "device-data-bltouch" Redis channel,
    data = None if nothing is received

    :return: data
    :rtype: str
    """
    data = None
    msg = p.get_message(ignore_subscribe_messages=True)
    if msg:
        data = msg["data"].decode("utf-8")
    if data_value is not None:
        data_value.value=data
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


def research_linear(arm:AlfredAPI, precisionStep: float = 0.5) -> Tuple[float,float,float]:
    """Return XYZ arm coordinates at one point

    :param arm: arm
    :type arm: AlfredAPI
    :param precisionMove: Z-step, defaults to 0.5mm
    :type precisionMove: float, optional
    :return: XYZ coord
    :rtype: Tuple
    """
    data = None
    p = rc.redis_instance.pubsub()
    p.subscribe("device-data-bltouch")
    send_command()
    time.sleep(0.5)  # wait push-pin DOWN
    while data is None:  # move z position until bltouch detects the table
        arm.set_position(
           z=-precisionStep, speed=speed, mvacc=mvacc, relative=True, wait=True
        )
        data = receive_data(p)
    p=arm.get_position() #return string "[0,[x,y,z,r,y,p]]"
    try:
        pos=ast.literal_eval(p)[1]
    except:
        pos=p[1]
    return [round(coord,1) for coord in pos[:3]] #only XYZ coord



def research_logarithmic(precisionRate: float = 0.5, maxMove: float = 4.) -> None:
    while maxMove > precisionRate:
        data = None
        p = rc.redis_instance.pubsub()
        p.subscribe("device-data-bltouch")
        send_command()
        time.sleep(0.5)  # wait push-pin DOWN
        while data:
            # arm.set_position(
            #    z=-maxMove, speed=speed, mvacc=mvacc, relative=True, wait=True
            # )
            data = receive_data(p)
        # arm.set_position(
        #    z=+maxMove, speed=speed, mvacc=mvacc, relative=True, wait=True
        # )  # allow to set the robot at the last position
        maxMove = round(maxMove/2, 1)


def research_minmax(minMove: float = 0.1, maxMove: float = 4.) -> None:
    data = None
    p = rc.redis_instance.pubsub()
    p.subscribe("device-data-bltouch")
    send_command()
    time.sleep(0.5)  # wait push-pin DOWN
    while data:
        # arm.set_position(z=-maxMove, speed=speed, mvacc=mvacc,
        #                 relative=True, wait=True)
        data = receive_data(p)
    print("Sucess 1")
    data = None
    send_command()
    time.sleep(0.5)  # wait push-pin DOWN
    # arm.set_position(z=+maxMove, speed=speed, mvacc=mvacc,
    #                 relative=True, wait=True)
    while data:
        # arm.set_position(z=-minMove, speed=speed, mvacc=mvacc,
        #                 relative=True, wait=False)
        data = receive_data(p)
    print("Sucess 2")

def compare_list(n1:np.ndarray,n2:np.ndarray)->bool:
    if len(n1)!=len(n2):
        return False
    comp = n1==n2
    for b in comp:
        if not b:
            return False
    return True

def recolt_data_table(arm: AlfredAPI,init_pos: np.ndarray, path: np.ndarray, relative: bool=False, speed: float = 50, mvacc: float=1000,height:float=30.)->List[List[float]]:
    positions=[]
    # compare if there is the same start btw init_pos and path
    if not ((compare_list(path[0],init_pos[:3]) and not relative) or (compare_list(path[0],np.array([0]*3)) and relative)):
        return None
    init_pos[2]+=height
    arm.set_position(*init_pos,speed=speed*1.5,mvacc=mvacc,wait=True,is_radian=False, relative = False)
    for p in path:
        arm.set_position(*p, speed=speed*1.5,mvacc=mvacc,wait=True,is_radian=False, relative = relative)
        pos = research_linear(arm)
        positions.append(pos[:3])
        arm.set_position(*p, speed=speed*1.5,mvacc=mvacc,wait=True,is_radian=False, relative = relative)
    arm.set_position(*init_pos,speed=speed*1.5,mvacc=mvacc,wait=True,is_radian=False, relative = False)
    return positions

def to_normal_vector(positions: Union[np.ndarray,List[Tuple]])->np.ndarray:
    pos = np.array(positions[:3])
    v1, v2 = pos[1]-pos[0], pos[2]-pos[0]
    return np.cross(v1,v2)

def cartesian_equation(positions: Union[np.ndarray,List[Tuple]])->np.ndarray:
    normal_vect = to_normal_vector(positions)
    d = -np.dot(normal_vect,positions[0])
    return np.append(normal_vect,[d])



def main():
    arm = AlfredAPI()
    init_pos = np.array([70, 320, 195.0, 180, 0.0, 90.])
    path = np.array([[70, 320, 195.0],[70,520,195],[210,520,195],[210,320,195]])
    #z=50
    #init_pos[2]+=z
    #for Z in path:
    #   Z[2]+=z
    relative = False
    positions = recolt_data_table(arm,init_pos,path,relative,speed,mvacc)
    abcd = cartesian_equation(positions)
    for i,p in enumerate(positions):
        print(f"p{i}: {p}")
    print(f"fct: {abcd[0]}x+{abcd[1]}y+{abcd[2]}z+{abcd[3]}=0")

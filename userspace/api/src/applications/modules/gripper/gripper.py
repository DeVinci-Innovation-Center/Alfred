import json
import time

from multiprocessing.sharedctypes import SynchronizedBase
from typing import Any

from libalfred import AlfredAPI
from utils.global_instances import rc


def receive_data(p: Any) -> str:
    """Receive the data from "device-data-gripper" Redis channel,
    data = None if nothing is received

    :return: data
    :rtype: str
    """
    msg = None
    while msg is None:
        msg = p.get_message()
        time.sleep(0.001)
    return msg["data"].decode("utf-8")


def send_command(command: str = "activate") -> None:
    """Send a command to "device-command-gripper"

    :param command: command, defaults to "activate"
    :type command: str, optional
    """
    redis_command = {"function": "activate-fsr", "data": repr(command)}
    # print(redis_command)

    res = rc.redis_instance.publish("device-command-gripper", json.dumps(redis_command))
    # print(res)


def grip(
    arm: AlfredAPI = None, init_pos: float = 750.0, limits: float = 15.0, step: int = 10
) -> None:
    """Grasp with a certain threshold

    :param arm: xArm, defaults to None
    :type arm: AlfredAPI, optional
    :param init_pos: initial position (0 to 800), defaults to 750.
    :type init_pos: float, optional
    :param limits: threshold, defaults to 15.
    :type limits: float, optional
    :param step: incrementation gripper pose, defaults to 10
    :type step: int, optional
    """
    arm.set_gripper_enable(True)
    arm.set_gripper_speed(20000)
    arm.set_gripper_position(init_pos, wait=True)
    pos = init_pos

    # Subscribe to redis publisher
    p = rc.redis_instance.pubsub(ignore_subscribe_messages=True)
    p.subscribe("device-data-gripper")

    while True:
        send_command()  # send command to read value from the fsr sensor
        data = receive_data(p)
        force = int(data[:-2])
        pos = pos - step
        start = time.time()
        arm.set_gripper_position(pos, wait=True, timeout=0.05)
        diff = time.time() - start
        if force > limits:
            break
        time.sleep(0.05)


def grip_demo():
    """Demo of the gripper"""
    arm = AlfredAPI()
    grip(arm)
    arm.stop()


def grip_test_time(
    arm: AlfredAPI = None, init_pos: float = 750.0, step: int = 1
) -> None:
    """Testing the execution time

    :param arm: xArm, defaults to None
    :type arm: AlfredAPI, optional
    :param init_pos: initial position, defaults to 750.
    :type init_pos: float, optional
    :param step: incrementation of the gripper, defaults to 1
    :type step: int, optional
    """
    arm.set_gripper_enable(True)
    arm.set_gripper_speed(20000)
    arm.set_gripper_position(init_pos, wait=True)
    pos = init_pos

    # Subscribe to redis publisher
    p = rc.redis_instance.pubsub(ignore_subscribe_messages=True)
    p.subscribe("device-data-gripper")

    # for i in range(10):
    #     start=time.time()
    #     send_command()
    #     data= receive_data(p)
    #     arm.set_gripper_position(pos, wait=True, timeout=0.05)
    #     diff=time.time()-start
    #     print(f"{i}: {diff} time")
    #     pos=pos-i

    start = time.time()
    times = 100
    for i in range(times):
        send_command()
        data = receive_data(p)
        arm.set_gripper_position(pos, wait=False, timeout=0.05)
        pos = pos - step
        # time.sleep(0.05)
    arm.set_gripper_position(pos, wait=True, timeout=0.05)
    diff = time.time() - start
    print(f"{times}: {diff} time")


def return_value(return_val: SynchronizedBase = None) -> str:
    # Subscribe to redis publisher
    p = rc.redis_instance.pubsub(ignore_subscribe_messages=True)
    p.subscribe("device-data-gripper")

    send_command()  # send command to read value from the fsr sensor
    data = receive_data(p)
    print(f"value: {data[:-1]}")

    if return_val is not None:
        return_val.value = data
        print("is not None")
    print(f"stored: {return_val.value}")
    return data

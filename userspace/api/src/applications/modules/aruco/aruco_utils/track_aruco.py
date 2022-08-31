import cv2
import cv2.aruco as aruco
import numpy as np
import threading
import time
import json


from typing import Any, Dict, List, Tuple

from libalfred import AlfredAPI
from libalfred.utils.camera_stream import StreamCamThread

from .detection import DetectFlag
from .scanner import ScannerThread
from .show_cam import ShowThread
from src.utils.global_instances import rc
from src.applications.modules.aruco import calibration_cam
from src.applications.modules.gripper import gripper

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

DEBUG = True
DIRPATH = "/alfred/api/src/applications/modules/aruco/images"
CAM = "device-data-realsense"

start_pose_degrees = [0.0, -42.3, -71.5, 0.0, 91.0, 0.0]


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


def aruco_detect(frame: np.array, aruco_dict, parameters, mtx: Any, dist: Any, aruco_detect: DetectFlag = None) -> Tuple[Any, Any, np.array, np.array]:
    """Detect the aruco markers and set a specific aruco id marker

    :return: _description_
    :rtype: Tuple[Any, Any, np.array, np.array]
    """
    rvec, tvec = None, None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Change to grayscale
    corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict,
                                                            parameters=parameters,
                                                            cameraMatrix=mtx,
                                                            distCoeff=dist)
    if np.all(ids is not None):  # If there are markers found by detector
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec
            rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(
                corners[i], 0.02, mtx, dist)
            (rvec - tvec).any()  # get rid of that nasty numpy value array error
            if aruco_detect is not None:
                if ids[i] == aruco_detect.target_id:
                    aruco_detect.update(corners[i])
                    aruco_detect.set()
    else:
        if aruco_detect is not None:
            aruco_detect.unset()
    return rvec, tvec, corners, ids


def stream_aruco(aruco_dict_type: aruco = aruco.DICT_6X6_250) -> None:
    """Stream and track the ArUco markers

    :param aruco_dict_type: type of the aruco dictionnary, defaults to aruco.DICT_6X6_250
    :type aruco_dict_type: aruco, optional
    """
    # Init aruco tracking
    aruco_dict = aruco.Dictionary_get(aruco_dict_type)
    parameters = aruco.DetectorParameters_create()
    mtx, dist = calibration_cam.get_calibration_coef()

    # Init stream thread
    stream_thread = StreamCamThread()
    stream_thread.start()

    # Init show thread
    show_cam_thread = ShowThread(is_aruco=True, mtx=mtx, dist=dist)
    show_cam_thread.start()

    while True:
        frame = stream_thread.get_frame()
        if frame is None:
            time.sleep(0.001)
            continue
        if show_cam_thread._stop.is_set():
            break

        rvec, tvec, corners, ids = aruco_detect(
            frame, aruco_dict, parameters, mtx, dist)

        show_cam_thread.update(frame, rvec, tvec, corners, ids)
        time.sleep(0.03)

    stream_thread.stop()


def track_aruco(aruco_dict_type: aruco = aruco.DICT_6X6_250, id_aruco: int = 3, min_angle: float = -100., max_angle: float = 100.) -> None:
    """Track a specific ArUco and center the camera"""
    # Init aruco tracking
    aruco_dict = aruco.Dictionary_get(aruco_dict_type)
    parameters = aruco.DetectorParameters_create()
    mtx, dist = calibration_cam.get_calibration_coef()
    detect_aruco = DetectFlag(target_id=id_aruco)

    # Init stream thread
    stream_thread = StreamCamThread()
    stream_thread.start()

    # Init scanner thread
    arm = AlfredAPI()
    arm.set_servo_angle(
        angle=start_pose_degrees, is_radian=False, wait=True)
    scanner_thread = ScannerThread(
        arm, min_angle, max_angle, daemon=True)
    scanner_thread.start()

    # Init show thread
    show_cam_thread = ShowThread(is_aruco=True, mtx=mtx, dist=dist)
    show_cam_thread.start()

    # Track specific aruco marker
    count = 0
    flag_is_centered = False
    while True:
        frame = stream_thread.get_frame()
        if frame is None:
            time.sleep(0.001)
            continue
        if show_cam_thread._stop.is_set():
            break

        rvec, tvec, corners, ids = aruco_detect(
            frame, aruco_dict, parameters, mtx, dist, detect_aruco)

        show_cam_thread.update(frame, rvec, tvec, corners, ids)
        if detect_aruco:
            scanner_thread.set()
            count += 1
            xy_diff = get_xy_diff(detect_aruco.corner)
            if xy_diff is not None:
                if count > 10:
                    center_camera(arm, xy_diff)
                    count = 0
            else:  # if centered
                flag_is_centered = True
                time.sleep(2)
                show_cam_thread.stop()
                cv2.destroyAllWindows()
                break
                get_angle = arm.get_servo_angle(servo_id=1, is_radian=False)
                # rget_servo_angle returns a string, ex. "(0,-47.7)" -> not a tuple!
                angle = float(get_angle[3:-2])
                # from 3 to -2 because it is a string, we extract only the angle and convert it in a float
                move_to_arm(arm, angle)
                break
        elif not flag_is_centered:
            # show_cam_thread.start()
            scanner_thread.unset()
        time.sleep(0.03)

    # gripper.grip(arm)
    # move_object_forward(arm)



    scanner_thread.set()
    scanner_thread.stop()
    show_cam_thread.stop()
    stream_thread.stop()

    # return to initial position
    arm.set_servo_angle(
        angle=start_pose_degrees, is_radian=False, wait=True)
    arm.stop()


def move_object_to_hand(arm: AlfredAPI, z: float = 200.):
    """Move the grasped object to the desk

    :param arm: xArm
    :type arm: AlfredAPI
    :param z: move upwards, defaults to 200.
    :type z: float, optional
    """
    pos_angle = [-75.4, 22.5, -52, -4.5, -58.2, -0.2]  # position of the desk
    arm.set_position(z=z, relative=True, wait=False)
    arm.set_servo_angle(
        angle=pos_angle, is_radian=False, wait=True)
    time.sleep(0.5)
    arm.set_gripper_position(750, speed=500, wait=True)
    time.sleep(1)


def move_object_forward(arm: AlfredAPI, z: float = 100.):
    """Move the grasped object forward

    :param arm: xArm
    :type arm: AlfredAPI
    :param z: move "z-axis tool coordinates" forward, defaults to 100
    :type z: float, optional
    """
    arm.set_position(z=z, relative=True, wait=False)
    arm.set_position_aa(axis_angle_pose=[
                        0, 0, z, 0, 0, 0], is_tool_coord=True, relative=True, wait=True)
    arm.set_position(z=-z+2, relative=True, wait=True)
    arm.set_gripper_position(750, speed=500, wait=True)
    arm.set_position(z=z+40, relative=True, wait=False)


def move_to_arm(arm: AlfredAPI = None, angle: float = .0) -> None:
    """Move the arm to the right position depending on the given angle

    :param arm: xArm, defaults to None
    :type arm: AlfredAPI, optional
    :param angle: _description_, defaults to .0
    :type angle: float, optional
    """
    j1 = [47.1, 21.9, -4.4, -47.1]
    j_pos1 = [28.8, -31.7, -4.6, -82.1, -2]
    j_pos2 = [51.4, -45, -4.3, -94, -2.9]
    # get the index of the closest float of j1 depending on angle
    index = min(enumerate(j1), key=lambda x: abs(x[1]-angle))[0]
    # add j1[index] angle to j_pos1 and j_pos2
    pos1, pos2 = get_pos(j1, j_pos1, j_pos2, index)
    arm.set_servo_angle(angle=pos1, is_radian=False, wait=False)
    arm.set_servo_angle(angle=pos2, is_radian=False, wait=False)
    # Move forward -> to the object
    z = 100
    arm.set_position_aa(axis_angle_pose=[
                        0, 0, z, 0, 0, 0], is_tool_coord=True, relative=True, wait=True)


def get_pos(j1: Any, j_pos1: Any, j_pos2: Any, index: int = 0) -> Any:
    """Add j1[index] angle to j_pos1 and j_pos2
        :return complet pos1 and pos2"""
    pos1 = j_pos1.copy()
    pos1.insert(0, j1[index])

    pos2 = j_pos2.copy()
    pos2.insert(0, j1[index])
    return pos1, pos2

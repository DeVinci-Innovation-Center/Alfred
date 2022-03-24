import cv2
import cv2.aruco as aruco
import numpy as np
import threading
import time


from typing import Any, Dict, List, Tuple

from libalfred import AlfredAPI
from libalfred.wrapper.utils.camera_stream import StreamCamThread

from .detection import DetectFlag
from .scanner import ScannerThread
from .show_cam import ShowThread
from src.utils.global_instances import rc
from src.applications.modules.aruco import calibration_cam

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

DEBUG = True
DIRPATH = "/alfred/api/src/applications/modules/aruco/images"
CAM = "device-data-realsense"


def get_xy_diff(corner: np.array, x_center: float = 320., y_center: float = 240., tolerance_diff: float = 10.) -> Tuple[float, float]:
    """Set the angle for the robot

    :param corner: top-left corner of the ArUco marker
    :type corner: np.array
    :return: angles for x,y to move
    :rtype: Tuple[float,float]
    """
    angle = 1.
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


def track_aruco(aruco_dict_type: aruco = aruco.DICT_6X6_250, id_aruco: int = 3, min_angle: float = -130., max_angle: float = 100.) -> None:
    """Track a specific ArUco and center the camera"""
    # Init aruco tracking
    aruco_dict = aruco.Dictionary_get(aruco_dict_type)
    parameters = aruco.DetectorParameters_create()
    mtx, dist = calibration_cam.get_calibration_coef()
    detect_aruco = DetectFlag(target_id=id_aruco)

    # Init stream thread
    stream_thread = StreamCamThread()
    stream_thread.start()

    # Init show thread
    show_cam_thread = ShowThread(is_aruco=True, mtx=mtx, dist=dist)
    show_cam_thread.start()

    # Init scanner thread
    arm = AlfredAPI()
    scanner_thread = ScannerThread(
        arm, min_angle, max_angle, daemon=True)
    scanner_thread.start()

    # Track specific aruco marker
    count = 0
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
        else:
            scanner_thread.unset()
        time.sleep(0.03)

    scanner_thread.stop()
    show_cam_thread.stop()
    stream_thread.stop()
    # while scanner_thread.flag.is_set():
    #     continue
    arm.stop()

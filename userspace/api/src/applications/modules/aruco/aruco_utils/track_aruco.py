import cv2
import cv2.aruco as aruco
import numpy as np
import time


from typing import Any, List, Tuple

from libalfred import AlfredAPI
from libalfred.utils.camera_stream import StreamCamThread
from libalfred.utils.show_frame_stream import ShowThread

from .arm_centering import center_camera, get_xy_diff
from .detection import DetectFlag
from .scanner import ScannerThread
from src.utils.global_instances import rc
from src.applications.modules.aruco import calibration_cam

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

DEBUG = True
DIRPATH = "/alfred/api/src/applications/modules/aruco/images"
CAM = "device-data-realsense"

start_pose_degrees = [0.0, -42.3, -71.5, 0.0, 91.0, 0.0]


def aruco_detect(frame: np.array, aruco_dict, parameters, mtx: Any, dist: Any, aruco_detect: DetectFlag = None) -> Tuple[Any, Any, np.array, np.array, DetectFlag]:
    """Detect the aruco markers and set a specific aruco id marker

    :return: _description_
    :rtype: Tuple[Any, Any, np.array, np.array, DetectFlag]
    """
    rvec, tvec = None, None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Change to grayscale
    corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict,
                                                            parameters=parameters,
                                                            cameraMatrix=mtx,
                                                            distCoeff=dist)
    nb_aruco_detected=0
    if np.all(ids is not None):  # If there are markers found by detector
        for i in range(0, len(ids)):
            # Estimate pose of each marker and return the values rvec and tvec
            rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(
                corners[i], 0.02, mtx, dist)
            (rvec - tvec).any()  # get rid of that nasty numpy value array error
            if aruco_detect is not None:
                if aruco_detect.target_exist(ids[i][0]):
                    aruco_detect.update(ids[i][0],corners[i])
                    nb_aruco_detected+=1
        if aruco_detect is not None:
            if nb_aruco_detected==len(aruco_detect.target_dict):
                aruco_detect.set()
    else:
        if aruco_detect is not None:
            aruco_detect.unset()
    return rvec, tvec, corners, ids, aruco_detect


def track_aruco(aruco_dict_type: aruco = aruco.DICT_6X6_250, ids_aruco: List[int] = [3], min_angle: float = -100., max_angle: float = 100.) -> None:
    """Track a specific ArUco and center the camera"""
    # Init aruco tracking
    aruco_dict = aruco.Dictionary_get(aruco_dict_type)
    parameters = aruco.DetectorParameters_create()
    mtx, dist = calibration_cam.get_calibration_coef()
    detect_aruco = DetectFlag(ids_aruco=ids_aruco)

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
    while True:
        frame = stream_thread.get_frame()
        if frame is None:
            time.sleep(0.001)
            continue
        if show_cam_thread._stop.is_set():
            break

        rvec, tvec, corners, ids, detect_aruco = aruco_detect(
            frame, aruco_dict, parameters, mtx, dist, detect_aruco)

        show_cam_thread.update(frame, rvec, tvec, corners, ids)
        if detect_aruco:
            scanner_thread.set()
            count += 1
            xy_diff = get_xy_diff(detect_aruco.target_dict.get(ids_aruco[0]))
            if xy_diff is not None: #if not centered
                if count > 10: #every 10 times, arm moves
                    center_camera(arm, xy_diff)
                    count = 0
            else:  # if centered
                flag_is_centered = True
        else:
            scanner_thread.unset()
        time.sleep(0.03)

    scanner_thread.set()
    scanner_thread.stop()
    show_cam_thread.stop()
    stream_thread.stop()
    cv2.destroyAllWindows()

    # return to initial position
    arm.set_servo_angle(
        angle=start_pose_degrees, is_radian=False, wait=True)
    arm.stop()

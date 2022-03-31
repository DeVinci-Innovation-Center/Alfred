import cv2
import cv2.aruco as aruco
import numpy as np
import threading
import time
import src.applications.modules.aruco.aruco_utils.track_aruco as track_aruco


from libalfred import AlfredAPI
from libalfred.utils.camera_stream import StreamCamThread
from .aruco_utils.show_cam import ShowThread
from src.applications.modules.aruco import calibration_cam

from typing import Any


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

DEBUG = False
DIRPATH = "/alfred/api/src/applications/modules/aruco/images"
CAM = "device-data-realsense"


def scanning(id: int = 3):
    track_aruco.track_aruco(id_aruco=id)


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

        rvec, tvec, corners, ids = track_aruco.aruco_detect(
            frame, aruco_dict, parameters, mtx, dist)

        show_cam_thread.update(frame, rvec, tvec, corners, ids)
        time.sleep(0.03)

    stream_thread.stop()

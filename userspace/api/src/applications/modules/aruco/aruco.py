import cv2
import numpy as np
import threading
import time
import src.applications.modules.aruco.aruco_utils.track_aruco as track_aruco


from libalfred import AlfredAPI
from libalfred.wrapper.utils.camera_stream import StreamCamThread
# from src.utils.global_instances import rc
from .aruco_utils.detection import DetectFlag

# from src.applications.modules.aruco.aruco_utils.scanner import ScannerThread
from typing import Any


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

DEBUG = False
DIRPATH = "/alfred/api/src/applications/modules/aruco/images"
CAM = "device-data-realsense"


def scanning():
    track_aruco.track_aruco()


def testing():
    track_aruco.stream_aruco()

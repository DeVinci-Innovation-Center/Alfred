import cv2
import glob
import numpy as np
import shutil

from src.applications.modules.aruco import aruco
from src.utils.global_instances import rc
from typing import Any

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

DEBUG = False
DIRPATH = "/alfred/api/src/applications/modules/aruco/images"
CAM = "device-data-realsense"


def calibrate(dirpath: str = DIRPATH, square_size: float = 0.025, width: int = 9, height: int = 6) -> Any:
    """Apply camera calibration operation for images in the given directory path

    :param dirpath: directory of the taken pictures
    :type dirpath: str
    :param square_size: edge size of one square
    :type square_size: float
    :param width: number of intersection points of squares in the long side of the calibration board, defaults to 9
    :type width: int, optional
    :param height: umber of intersection points of squares in the short side of the calibration board, defaults to 6
    :type height: int, optional
    :return: calibration parameters
    :rtype: Any
    """
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    objp = np.zeros((height*width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob(dirpath+"/image*.png")

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(
                img, (width, height), corners2, ret)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None)

    return [ret, mtx, dist, rvecs, tvecs]


def get_calibration_coef(dirpath: str = DIRPATH, taking_picture: bool = False) -> Any:
    """Get the camera matrix and the distortion coefficient

    :param dirpath: path of the directory, defaults to DIRPATH
    :type dirpath: str, optional
    :return: [mtx, dist]
    :rtype: Any
    """
    square_size = 0.025
    if taking_picture:
        aruco.take_pictures(dirpath, 20)
    ret, mtx, dist, rvecs, tvecs = calibrate(dirpath, square_size)

    try:
        shutil.rmtree(dirpath)
    except OSError as e:
        print("Error: %s : %s" % (dirpath, e.strerror))

    return mtx, dist
